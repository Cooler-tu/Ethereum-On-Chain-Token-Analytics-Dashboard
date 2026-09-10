#!/usr/bin/env python3
"""Build the frozen TURBO LP event, link, and campaign fact tables."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eth_abi import decode
import pandas as pd
import requests
from web3 import Web3
from web3.logs import DISCARD

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in os.sys.path:
    os.sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv

    # For reproducible project runs, an explicitly supplied --rpc-url still
    # wins; otherwise use this repository's own configuration.
    load_dotenv(PROJECT_ROOT / ".env", override=True)
except ImportError:  # pragma: no cover
    pass

from src.analysis.lp_event_ledger import build_campaign_ledger, build_event_readd_links
from src.client import get_contract, get_web3


TURBO = "0xA35923162C49cF95e6BF26623385eb431ad920D3"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
POSITION_MANAGER = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
COHORT_FROM_BLOCK = 25_241_305
COHORT_TO_BLOCK = 25_886_879
DEFAULT_FOLLOWUP_TO_BLOCK = 25_944_714
MAIN_CACHE = PROJECT_ROOT / "output-turbo-lp-whale-90d" / "notebook_cache"
POOL_EVENT_SIGNATURES = {
    "Mint": "Mint(address,address,int24,int24,uint128,uint256,uint256)",
    "Burn": "Burn(address,int24,int24,uint128,uint256,uint256)",
}


def _hex(value: Any) -> str:
    if isinstance(value, str):
        return value if value.startswith("0x") else f"0x{value}"
    text = value.hex()
    return text if text.startswith("0x") else f"0x{text}"


def _int(value: Any) -> int:
    return int(value, 16) if isinstance(value, str) else int(value)


def _topic_int24(value: Any) -> int:
    number = int(_hex(value), 16)
    return number - 2**256 if number >= 2**255 else number


def _topic_address(value: Any) -> str:
    return Web3.to_checksum_address("0x" + _hex(value)[-40:])


def _rpc_logs(rpc_url: str, pool: str, event_type: str, start: int, end: int) -> list[dict]:
    topic = "0x" + Web3.keccak(text=POOL_EVENT_SIGNATURES[event_type]).hex().removeprefix("0x")
    params = {
        "address": Web3.to_checksum_address(pool),
        "fromBlock": hex(start),
        "toBlock": hex(end),
        "topics": [topic],
    }
    def fetch(left: int, right: int) -> list[dict]:
        params["fromBlock"], params["toBlock"] = hex(left), hex(right)
        response = requests.post(
            rpc_url,
            json={"jsonrpc": "2.0", "id": 1, "method": "eth_getLogs", "params": [params]},
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        if "error" in payload:
            raise RuntimeError(f"eth_getLogs failed: {payload['error']}")
        return payload["result"]

    def fetch_range(left: int, right: int) -> list[dict]:
        try:
            return fetch(left, right)
        except Exception as full_error:
            if left == right:
                raise RuntimeError(
                    f"eth_getLogs failed at block {left}; no block was skipped"
                ) from full_error
            midpoint = (left + right) // 2
            return fetch_range(left, midpoint) + fetch_range(midpoint + 1, right)

    return fetch_range(start, end)


def _load_swap_prices(path: Path) -> pd.DataFrame:
    rows = []
    with path.open() as handle:
        for line in handle:
            item = json.loads(line)
            sqrt_price = int(item["sqrtPriceX96"])
            rows.append({
                "block_number": int(item["block_number"]),
                "log_index": int(item["log_index"]),
                "chain_order_key": int(item["block_number"]) * 1_000_000 + int(item["log_index"]),
                "price_weth_per_turbo": (sqrt_price / 2**96) ** 2,
            })
    return pd.DataFrame(rows).sort_values("chain_order_key")


def decode_pool_log(raw: dict, event_type: str, pool: dict) -> dict:
    topics = raw["topics"]
    data = bytes.fromhex(_hex(raw["data"])[2:])
    if event_type == "Mint":
        sender, liquidity, amount0, amount1 = decode(
            ["address", "uint128", "uint256", "uint256"], data
        )
        pool_owner = _topic_address(topics[1])
        tick_lower, tick_upper = _topic_int24(topics[2]), _topic_int24(topics[3])
    else:
        liquidity, amount0, amount1 = decode(["uint128", "uint256", "uint256"], data)
        sender = None
        pool_owner = _topic_address(topics[1])
        tick_lower, tick_upper = _topic_int24(topics[2]), _topic_int24(topics[3])
    block = _int(raw["blockNumber"])
    transaction_index = _int(raw["transactionIndex"])
    log_index = _int(raw["logIndex"])
    tx_hash = _hex(raw["transactionHash"]).lower()
    return {
        "event_id": f"{pool['pool_address'].lower()}:{block}:{transaction_index}:{log_index}",
        "event_type": event_type,
        "pool_address": pool["pool_address"],
        "pair_key": "TURBO/WETH",
        "fee": int(pool["fee"]),
        "block_number": block,
        "transaction_index": transaction_index,
        "log_index": log_index,
        "transaction_hash": tx_hash,
        "pool_owner_address": pool_owner,
        "pool_sender_address": Web3.to_checksum_address(sender) if sender else None,
        "tick_lower": tick_lower,
        "tick_upper": tick_upper,
        "liquidity_delta_raw": str(int(liquidity)),
        "amount0_raw": str(int(amount0)),
        "amount1_raw": str(int(amount1)),
        "turbo_amount": int(amount0) / 1e18,
        "weth_amount": int(amount1) / 1e18,
    }


def _normalize_hash(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().str.removeprefix("0x")


def _receipt_identity(w3: Web3, manager, row: dict) -> tuple[str, int | None, str]:
    receipt = w3.eth.get_transaction_receipt(row["transaction_hash"])
    tx_from = Web3.to_checksum_address(receipt["from"])
    target_name = "IncreaseLiquidity" if row["event_type"] == "Mint" else "DecreaseLiquidity"
    manager_event = getattr(manager.events, target_name)()
    candidates = manager_event.process_receipt(receipt, errors=DISCARD)
    matched = None
    for candidate in candidates:
        args = candidate["args"]
        if (
            int(args["liquidity"]) == int(row["liquidity_delta_raw"])
            and int(args["amount0"]) == int(row["amount0_raw"])
            and int(args["amount1"]) == int(row["amount1_raw"])
        ):
            matched = candidate
            break
    if matched is None:
        return tx_from, None, "unmatched_pool_event"
    token_id = int(matched["args"]["tokenId"])
    if row["event_type"] == "Burn":
        try:
            wallet = manager.functions.ownerOf(token_id).call(
                block_identifier=int(row["block_number"]) - 1
            )
            return Web3.to_checksum_address(wallet), token_id, "position_manager_matched"
        except Exception:
            return tx_from, token_id, "position_manager_matched_owner_fallback"

    transfers = manager.events.Transfer().process_receipt(receipt, errors=DISCARD)
    for transfer in transfers:
        args = transfer["args"]
        if int(args["tokenId"]) == token_id and int(args["from"], 16) == 0:
            return Web3.to_checksum_address(args["to"]), token_id, "position_manager_matched"
    return tx_from, token_id, "position_manager_matched_sender_fallback"


def _atomic_parquet(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".parquet", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        frame.to_parquet(temporary, index=False)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True
        ).strip()
    except Exception:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--factory-pools", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--rpc-url")
    parser.add_argument("--cohort-from-block", type=int, default=COHORT_FROM_BLOCK)
    parser.add_argument("--cohort-to-block", type=int, default=COHORT_TO_BLOCK)
    parser.add_argument("--followup-to-block", type=int, default=DEFAULT_FOLLOWUP_TO_BLOCK)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    factory_payload = json.loads(args.factory_pools.read_text())
    pools = factory_payload["pools"]
    rpc_url = args.rpc_url or os.environ.get("ETH_RPC_URL") or os.environ.get("RPC_URL")
    if not rpc_url:
        raise ValueError("ETH_RPC_URL, RPC_URL, or --rpc-url is required")
    w3 = get_web3(rpc_url)
    manager = get_contract(w3, POSITION_MANAGER, "uniswap_v3_position_manager")

    rows: list[dict] = []
    for pool in pools:
        for event_type in ("Mint", "Burn"):
            raw_logs = _rpc_logs(
                rpc_url, pool["pool_address"], event_type,
                args.cohort_from_block, args.followup_to_block,
            )
            rows.extend(decode_pool_log(raw, event_type, pool) for raw in raw_logs)
    raw = pd.DataFrame(rows)
    raw["transaction_hash_key"] = _normalize_hash(raw.transaction_hash)

    matched_path = MAIN_CACHE / f"matched_position_events_{args.cohort_from_block}_{args.cohort_to_block}.csv"
    states_path = MAIN_CACHE / f"withdrawal_states_{args.cohort_from_block}_{args.cohort_to_block}.csv"
    matched = pd.read_csv(matched_path)
    matched["transaction_hash_key"] = _normalize_hash(matched.transaction_hash)
    matched = matched.rename(columns={
        "pool_event": "event_type", "pool_log_index": "log_index",
        "tx_from": "cached_tx_from", "token_id": "cached_token_id",
        "timestamp": "cached_timestamp",
    })
    matched = matched[[
        "transaction_hash_key", "event_type", "log_index", "cached_tx_from",
        "cached_token_id", "cached_timestamp", "manager_event",
    ]]
    raw = raw.merge(matched, on=["transaction_hash_key", "event_type", "log_index"], how="left")

    states = pd.read_csv(states_path)
    # The original cache predates the displayed candidate columns.  Recreate
    # the exact documented feasibility gates when those convenience columns
    # are absent; the underlying S/E measurements are the source facts.
    if "candidate_main" not in states:
        states["candidate_main"] = (states["S_nft_pct"] >= 5.0) & (states["E_pct"] >= 1.0)
    if "candidate_control" not in states:
        states["candidate_control"] = (states["S_nft_pct"] >= 3.0) & (states["E_pct"] >= 0.5)
    states["transaction_hash_key"] = _normalize_hash(states.transaction_hash)
    states = states.rename(columns={
        "token_id": "state_token_id", "owner_before": "state_owner_before",
        "tick_current": "state_tick_current",
    })
    states = states[[
        "transaction_hash_key", "state_token_id", "state_owner_before",
        "state_tick_current", "candidate_main", "candidate_control",
    ]]
    raw = raw.merge(
        states,
        left_on=["transaction_hash_key", "cached_token_id"],
        right_on=["transaction_hash_key", "state_token_id"],
        how="left",
    )

    timestamp_cache = {
        int(row.block_number): int(row.cached_timestamp)
        for row in raw.itertuples()
        if pd.notna(row.cached_timestamp)
    }
    for block in sorted(set(raw.block_number) - set(timestamp_cache)):
        timestamp_cache[int(block)] = int(w3.eth.get_block(int(block))["timestamp"])
    raw["timestamp"] = raw.block_number.map(timestamp_cache).astype("int64")
    raw["datetime_utc"] = pd.to_datetime(raw.timestamp, unit="s", utc=True)

    identities: dict[tuple[str, int], tuple[str, int | None, str]] = {}
    for row in raw.itertuples(index=False):
        if pd.notna(row.cached_tx_from):
            if row.event_type == "Burn" and pd.notna(row.state_owner_before):
                wallet = Web3.to_checksum_address(row.state_owner_before)
            else:
                wallet = Web3.to_checksum_address(row.cached_tx_from)
            token_id = int(row.cached_token_id) if pd.notna(row.cached_token_id) else None
            status = "position_manager_matched" if token_id is not None else "unmatched_pool_event"
            identities[(row.event_id, row.log_index)] = (wallet, token_id, status)
        else:
            identities[(row.event_id, row.log_index)] = _receipt_identity(w3, manager, row._asdict())
    raw["wallet_address"] = [identities[(row.event_id, row.log_index)][0] for row in raw.itertuples()]
    raw["nft_id"] = [identities[(row.event_id, row.log_index)][1] for row in raw.itertuples()]
    raw["position_match_status"] = [identities[(row.event_id, row.log_index)][2] for row in raw.itertuples()]

    raw["in_cohort"] = raw.block_number.between(args.cohort_from_block, args.cohort_to_block)
    raw["candidate_main"] = raw.candidate_main.fillna(False).astype(bool)
    raw["candidate_control"] = raw.candidate_control.fillna(False).astype(bool)
    raw["starts_campaign"] = (
        raw.event_type.eq("Burn") & raw.in_cohort & raw.candidate_main
        & raw.position_match_status.str.startswith("position_manager_matched")
    )
    raw["price_weth_per_turbo"] = raw.state_tick_current.map(
        lambda tick: 1.0001 ** float(tick) if pd.notna(tick) else float("nan")
    )
    raw["price_source"] = raw.state_tick_current.map(
        lambda tick: "historical_state_previous_block" if pd.notna(tick) else None
    )
    swaps = _load_swap_prices(
        MAIN_CACHE / f"Swap_{args.cohort_from_block}_{args.cohort_to_block}.jsonl"
    )
    swap_keys = swaps.chain_order_key.to_numpy()
    swap_prices = swaps.price_weth_per_turbo.to_numpy()
    main_pool = pools[0]["pool_address"].lower()
    for index, row in raw[raw.starts_campaign & raw.pool_address.str.lower().eq(main_pool)].iterrows():
        order_key = int(row.block_number) * 1_000_000 + int(row.log_index)
        position = int(swap_keys.searchsorted(order_key, side="left")) - 1
        if position >= 0:
            raw.at[index, "price_weth_per_turbo"] = float(swap_prices[position])
            raw.at[index, "price_source"] = "last_prior_pool_swap"

    followup_block = w3.eth.get_block(args.followup_to_block)
    followup_end_timestamp = int(followup_block["timestamp"])
    campaigns, campaign_flows = build_campaign_ledger(raw, followup_end_timestamp)
    links = build_event_readd_links(raw)

    drop_columns = [
        "transaction_hash_key", "cached_tx_from", "cached_token_id",
        "cached_timestamp", "manager_event", "state_token_id",
    ]
    raw = raw.drop(columns=[column for column in drop_columns if column in raw.columns])
    raw = raw.sort_values(["block_number", "transaction_index", "log_index"], kind="stable")

    files = {
        "raw_events": output_dir / "lp_raw_events_v1.parquet",
        "readd_links": output_dir / "lp_readd_links_v1.parquet",
        "campaign_ledger": output_dir / "lp_campaign_ledger_v1.parquet",
    }
    _atomic_parquet(raw, files["raw_events"])
    _atomic_parquet(links, files["readd_links"])
    _atomic_parquet(campaigns, files["campaign_ledger"])

    cohort_from_block = w3.eth.get_block(args.cohort_from_block)
    cohort_to_block = w3.eth.get_block(args.cohort_to_block)
    manifest = {
        "schema_version": "turbo_lp_event_ledger_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "chain_id": int(w3.eth.chain_id),
        "token": Web3.to_checksum_address(TURBO),
        "quote_token": Web3.to_checksum_address(WETH),
        "position_manager": Web3.to_checksum_address(POSITION_MANAGER),
        "cohort_from_block": args.cohort_from_block,
        "cohort_from_time": datetime.fromtimestamp(int(cohort_from_block["timestamp"]), timezone.utc).isoformat(),
        "cohort_end_block": args.cohort_to_block,
        "cohort_end_time": datetime.fromtimestamp(int(cohort_to_block["timestamp"]), timezone.utc).isoformat(),
        "followup_data_end_block": args.followup_to_block,
        "followup_data_end_time": datetime.fromtimestamp(followup_end_timestamp, timezone.utc).isoformat(),
        "followup_block_tag_at_freeze": "finalized",
        "recovery_value_unit": "WETH equivalent at origin Burn price",
        "primary_net_recovery_threshold": 0.90,
        "sensitivity_threshold": 0.80,
        "windows": ["1h", "6h", "24h", "7d", "30d"],
        "controller_scope": "exact wallet address; lower-bound attribution",
        "factory_pool_file": str(args.factory_pools),
        "scanned_pools": pools,
        "row_counts": {
            "raw_events": len(raw), "readd_links": len(links), "campaigns": len(campaigns),
            "campaign_start_burns": int(raw.starts_campaign.sum()),
            "campaign_flow_events": len(campaign_flows),
        },
        "sha256": {name: _sha256(path) for name, path in files.items()},
        "git_commit_at_generation": _git_commit(),
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(manifest["row_counts"], ensure_ascii=False))
    print(f"Frozen event ledger -> {output_dir}")


if __name__ == "__main__":
    main()
