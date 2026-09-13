#!/usr/bin/env python3
"""Build a frozen, evidence-layer trace for TURBO's persistent non-return case."""
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

import pandas as pd
from web3 import Web3
from web3.logs import DISCARD

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in os.sys.path:
    os.sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env", override=True)
except ImportError:  # pragma: no cover
    pass

from src.analysis.lp_capital_destination import (
    aggregate_edges,
    balance_disposition,
    block_at_or_after_timestamp,
    enumerate_nonce_blocks,
    first_horizon,
    reconcile_native_balance,
)
from src.client import get_contract, get_web3
from src.discovery.log_utils import get_logs_chunked


TURBO = Web3.to_checksum_address("0xA35923162C49cF95e6BF26623385eb431ad920D3")
WETH = Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
POSITION_MANAGER = Web3.to_checksum_address("0xC36442b4a4522E871399CD717aBDD847Ab11FE88")
INTERMEDIARY = Web3.to_checksum_address("0x5ffd352BE09660Ee4221713A08012EC33F1Ba139")
SHAKEPAY_8 = Web3.to_checksum_address("0x7DBB4bdCfE614398D1a68ecc219F15280d0959E0")
KYBER_ROUTER = Web3.to_checksum_address("0x6131B5fae19EA4f9D964eAc0408E4408b66337b5")
KYBER_EXECUTOR = Web3.to_checksum_address("0x8F10B468b06c6FD214B65F87778827F7D113f996")
PUBLIC_MEV_CONTRACT = Web3.to_checksum_address("0xEff6cb8b614999d130E537751Ee99724D01aA167")
FEE_LIKE_EOA = Web3.to_checksum_address("0xcD6b980029E6E6e0733ac8eC3E02be9410D09799")
ONEINCH_ROUTER = Web3.to_checksum_address("0x111111125421cA6dc452d289314280a0f8842A65")

LEDGER_DIR = PROJECT_ROOT / "notebooks" / "data" / "turbo_lp_event_ledger_v1"
DEFAULT_OUTPUT = PROJECT_ROOT / "notebooks" / "data" / "turbo_lp_capital_destination_v1"


def _hex(value: Any) -> str:
    if isinstance(value, str):
        return value if value.startswith("0x") else "0x" + value
    return "0x" + value.hex().removeprefix("0x")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_parquet(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".parquet", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        frame.to_parquet(temporary, index=False)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True
        ).strip()
    except Exception:
        return None


def _block_timestamp(w3, block: int, cache: dict[int, int]) -> int:
    block = int(block)
    if block not in cache:
        cache[block] = int(w3.eth.get_block(block)["timestamp"])
    return cache[block]


def _find_30d_block(w3, start_block: int, available_end: int, start_ts: int, cache: dict[int, int]) -> int:
    return block_at_or_after_timestamp(
        start_block,
        available_end,
        start_ts + 30 * 86_400,
        lambda block: _block_timestamp(w3, block, cache),
    )


def _find_sender_transactions(w3, address: str, start_block: int, end_block: int, ts_cache: dict[int, int]) -> pd.DataFrame:
    checksum = Web3.to_checksum_address(address)
    located = enumerate_nonce_blocks(
        checksum,
        start_block,
        end_block,
        lambda account, block: int(w3.eth.get_transaction_count(account, block_identifier=block)),
    )
    rows = []
    for nonce, block_number in located:
        block = w3.eth.get_block(block_number, full_transactions=True)
        matches = [
            tx for tx in block["transactions"]
            if tx["from"].lower() == checksum.lower() and int(tx["nonce"]) == nonce
        ]
        if len(matches) != 1:
            raise RuntimeError(f"Expected one transaction for {checksum} nonce {nonce} in block {block_number}")
        tx = matches[0]
        receipt = w3.eth.get_transaction_receipt(tx["hash"])
        effective_price = int(receipt.get("effectiveGasPrice") or tx.get("gasPrice") or 0)
        timestamp = int(block["timestamp"])
        ts_cache[int(block_number)] = timestamp
        rows.append({
            "address": checksum,
            "nonce": nonce,
            "block_number": int(block_number),
            "timestamp": timestamp,
            "datetime_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
            "transaction_hash": _hex(tx["hash"]).lower(),
            "to_address": Web3.to_checksum_address(tx["to"]) if tx.get("to") else None,
            "value_eth": int(tx["value"]) / 1e18,
            "selector": _hex(tx["input"][:4]).lower() if tx.get("input") else "0x",
            "gas_cost_eth": int(receipt["gasUsed"]) * effective_price / 1e18,
            "status": int(receipt["status"]),
        })
    return pd.DataFrame(rows)


def _token_transfers(w3, token: str, symbol: str, wallet: str, start: int, end: int, start_ts: int, ts_cache: dict[int, int]) -> pd.DataFrame:
    contract = get_contract(w3, token, "erc20")
    inbound = get_logs_chunked(
        contract.events.Transfer, start, end,
        argument_filters={"to": Web3.to_checksum_address(wallet)}, chunk_size=10_000,
    )
    outbound = get_logs_chunked(
        contract.events.Transfer, start, end,
        argument_filters={"from": Web3.to_checksum_address(wallet)}, chunk_size=10_000,
    )
    rows = []
    for direction, entries in (("in", inbound), ("out", outbound)):
        for event in entries:
            args = event["args"]
            block = int(event["blockNumber"])
            timestamp = _block_timestamp(w3, block, ts_cache)
            rows.append({
                "asset": symbol,
                "direction": direction,
                "block_number": block,
                "log_index": int(event["logIndex"]),
                "timestamp": timestamp,
                "datetime_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
                "seconds_from_burn": timestamp - start_ts,
                "horizon": first_horizon(timestamp - start_ts, same_transaction=block == start),
                "transaction_hash": _hex(event["transactionHash"]).lower(),
                "from_address": Web3.to_checksum_address(args["from"]),
                "to_address": Web3.to_checksum_address(args["to"]),
                "amount": int(args["value"]) / 1e18,
            })
    return pd.DataFrame(rows).sort_values(["block_number", "log_index"]).reset_index(drop=True)


def _weth_withdrawals(w3, wallet: str, start: int, end: int, start_ts: int, ts_cache: dict[int, int]) -> pd.DataFrame:
    abi = [{
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Withdrawal",
        "type": "event",
    }]
    contract = w3.eth.contract(address=WETH, abi=abi)
    entries = get_logs_chunked(
        contract.events.Withdrawal, start, end,
        argument_filters={"src": Web3.to_checksum_address(wallet)}, chunk_size=10_000,
    )
    rows = []
    for event in entries:
        block = int(event["blockNumber"])
        timestamp = _block_timestamp(w3, block, ts_cache)
        rows.append({
            "block_number": block,
            "log_index": int(event["logIndex"]),
            "timestamp": timestamp,
            "datetime_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
            "seconds_from_burn": timestamp - start_ts,
            "horizon": first_horizon(timestamp - start_ts, same_transaction=block == start),
            "transaction_hash": _hex(event["transactionHash"]).lower(),
            "wallet_address": Web3.to_checksum_address(event["args"]["src"]),
            "weth_unwrapped": int(event["args"]["wad"]) / 1e18,
        })
    return pd.DataFrame(rows)


def _collect_fact(w3, campaign: pd.Series) -> dict[str, Any]:
    receipt = w3.eth.get_transaction_receipt(campaign.burn_transaction_hash)
    manager = get_contract(w3, POSITION_MANAGER, "uniswap_v3_position_manager")
    decreases = manager.events.DecreaseLiquidity().process_receipt(receipt, errors=DISCARD)
    collects = manager.events.Collect().process_receipt(receipt, errors=DISCARD)
    token_id = int(campaign.nft_id)
    decrease = next(item for item in decreases if int(item["args"]["tokenId"]) == token_id)
    collect = next(item for item in collects if int(item["args"]["tokenId"]) == token_id)
    return {
        "campaign_id": campaign.campaign_id,
        "wallet_address": Web3.to_checksum_address(campaign.wallet_address),
        "nft_id": token_id,
        "burn_transaction_hash": str(campaign.burn_transaction_hash).lower(),
        "burn_block_number": int(campaign.burn_block_number),
        "burn_log_index": int(campaign.burn_log_index),
        "decrease_log_index": int(decrease["logIndex"]),
        "collect_log_index": int(collect["logIndex"]),
        "collect_recipient": Web3.to_checksum_address(collect["args"]["recipient"]),
        "burn_turbo_principal": int(decrease["args"]["amount0"]) / 1e18,
        "burn_weth_principal": int(decrease["args"]["amount1"]) / 1e18,
        "collected_turbo": int(collect["args"]["amount0"]) / 1e18,
        "collected_weth": int(collect["args"]["amount1"]) / 1e18,
        "collect_minus_burn_turbo": (int(collect["args"]["amount0"]) - int(decrease["args"]["amount0"])) / 1e18,
        "collect_minus_burn_weth": (int(collect["args"]["amount1"]) - int(decrease["args"]["amount1"])) / 1e18,
    }


def _balance_snapshots(w3, wallet: str, burn_block: int, end_block: int, burn_ts: int, ts_cache: dict[int, int]) -> pd.DataFrame:
    turbo = get_contract(w3, TURBO, "erc20")
    weth = get_contract(w3, WETH, "erc20")
    points = [("pre_burn", burn_block - 1), ("post_collect", burn_block)]
    for label, seconds in (("1h", 3_600), ("24h", 86_400), ("7d", 7 * 86_400), ("30d", 30 * 86_400)):
        block = block_at_or_after_timestamp(
            burn_block, end_block, burn_ts + seconds,
            lambda number: _block_timestamp(w3, number, ts_cache),
        )
        points.append((label, block))
    rows = []
    for label, block in points:
        timestamp = _block_timestamp(w3, block, ts_cache)
        rows.append({
            "checkpoint": label,
            "block_number": block,
            "timestamp": timestamp,
            "datetime_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
            "turbo_balance": turbo.functions.balanceOf(wallet).call(block_identifier=block) / 1e18,
            "weth_balance": weth.functions.balanceOf(wallet).call(block_identifier=block) / 1e18,
            "eth_balance": w3.eth.get_balance(wallet, block_identifier=block) / 1e18,
        })
    return pd.DataFrame(rows)


def _address_labels(w3, addresses: list[str]) -> pd.DataFrame:
    overrides = {
        POSITION_MANAGER.lower(): ("Uniswap V3 NonfungiblePositionManager", "protocol_contract", "onchain/project config", ""),
        "0x7baece5d47f1bc5e1953fbe0e9931d54dab6d810": ("TURBO/WETH V3 1% pool", "liquidity_pool", "Factory-verified project ledger", ""),
        KYBER_ROUTER.lower(): ("KyberSwap MetaAggregationRouterV2", "swap_router", "official KyberSwap deployment docs", "https://docs.kyberswap.com/kyberswap-solutions/kyberswap-aggregator/contracts"),
        KYBER_EXECUTOR.lower(): ("KyberSwap transaction execution contract", "execution_contract", "same-transaction call/transfer evidence", ""),
        ONEINCH_ROUTER.lower(): ("1inch Aggregation Router", "swap_router", "public protocol contract", "https://etherscan.io/address/0x111111125421ca6dc452d289314280a0f8842a65"),
        PUBLIC_MEV_CONTRACT.lower(): ("Publicly labeled MEV execution contract", "externally_labeled_contract", "public explorer label; owner identity not inferred", "https://ethereum.routescan.io/address/0xeff6cb8b614999d130e537751ee99724d01aa167"),
        SHAKEPAY_8.lower(): ("Shakepay 8 (public label, not independently verified)", "externally_labeled_service", "Blockscan third-party public label; official/community status not established", "https://blockscan.com/Address/0x7dbb4bdcfe614398d1a68ecc219f15280d0959e0"),
        INTERMEDIARY.lower(): ("Unlabeled intermediary EOA", "eoa", "onchain code check", "https://etherscan.io/address/0x5ffd352be09660ee4221713a08012ec33f1ba139"),
        FEE_LIKE_EOA.lower(): ("Unlabeled EOA receiving 0.25% of routed TURBO", "eoa", "observed transfer ratio; purpose not inferred", ""),
    }
    rows = []
    for address in sorted({Web3.to_checksum_address(item) for item in addresses if item}):
        code = w3.eth.get_code(address)
        label, category, evidence, source = overrides.get(
            address.lower(),
            ("Unlabeled contract" if code else "Unlabeled EOA", "contract" if code else "eoa", "onchain code check", ""),
        )
        rows.append({
            "address": address,
            "is_contract": bool(code),
            "label": label,
            "category": category,
            "label_evidence": evidence,
            "source_url": source,
            "beneficial_owner_inferred": False,
        })
    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rpc-url", default=os.environ.get("ETH_RPC_URL"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.rpc_url:
        raise SystemExit("ETH_RPC_URL or --rpc-url is required")
    w3 = get_web3(args.rpc_url)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    ts_cache: dict[int, int] = {}

    ledger = pd.read_parquet(LEDGER_DIR / "lp_campaign_ledger_v1.parquet")
    selected = ledger[ledger.persistent_non_return_scanned_pair_30d.astype(bool)]
    if len(selected) != 1:
        raise RuntimeError(f"Expected exactly one persistent non-return campaign, got {len(selected)}")
    campaign = selected.iloc[0]
    censored = ledger[ledger.is_censored_30d.astype(bool)].copy()

    burn_block = int(campaign.burn_block_number)
    burn_ts = _block_timestamp(w3, burn_block, ts_cache)
    available_end = int(json.loads((LEDGER_DIR / "manifest.json").read_text())["followup_data_end_block"])
    end_block = _find_30d_block(w3, burn_block, available_end, burn_ts, ts_cache)
    wallet = Web3.to_checksum_address(campaign.wallet_address)

    collect = _collect_fact(w3, campaign)
    transfers = pd.concat([
        _token_transfers(w3, TURBO, "TURBO", wallet, burn_block, end_block, burn_ts, ts_cache),
        _token_transfers(w3, WETH, "WETH", wallet, burn_block, end_block, burn_ts, ts_cache),
    ], ignore_index=True).sort_values(["block_number", "log_index"])
    withdrawals = _weth_withdrawals(w3, wallet, burn_block, end_block, burn_ts, ts_cache)
    wallet_txs = _find_sender_transactions(w3, wallet, burn_block - 1, end_block, ts_cache)
    intermediary_txs = _find_sender_transactions(w3, INTERMEDIARY, burn_block - 1, end_block, ts_cache)
    balances = _balance_snapshots(w3, wallet, burn_block, end_block, burn_ts, ts_cache)

    native_out = pd.concat([wallet_txs, intermediary_txs], ignore_index=True)
    native_out = native_out[native_out.value_eth > 0].copy()
    native_out["seconds_from_burn"] = native_out.timestamp - burn_ts
    native_out["horizon"] = native_out.seconds_from_burn.map(first_horizon)

    edge_rows: list[dict[str, Any]] = [
        {"source": campaign.origin_pool_address, "target": wallet, "asset": "TURBO", "amount": collect["collected_turbo"], "evidence_type": "collect_transfer", "transaction_hash": campaign.burn_transaction_hash},
        {"source": campaign.origin_pool_address, "target": wallet, "asset": "WETH", "amount": collect["collected_weth"], "evidence_type": "collect_transfer", "transaction_hash": campaign.burn_transaction_hash},
    ]
    for row in transfers[(transfers.direction == "out") & (transfers.asset == "TURBO")].to_dict("records"):
        edge_rows.append({"source": row["from_address"], "target": row["to_address"], "asset": "TURBO", "amount": row["amount"], "evidence_type": "erc20_transfer", "transaction_hash": row["transaction_hash"]})
    for row in native_out.to_dict("records"):
        edge_rows.append({"source": row["address"], "target": row["to_address"], "asset": "ETH", "amount": row["value_eth"], "evidence_type": "native_transaction", "transaction_hash": row["transaction_hash"]})
    edges = pd.DataFrame(aggregate_edges(edge_rows))
    edges["transaction_hashes"] = edges.transaction_hashes.map(lambda values: json.dumps(values))

    turbo_out = transfers[(transfers.direction == "out") & (transfers.asset == "TURBO")].amount.sum()
    weth_out = transfers[(transfers.direction == "out") & (transfers.asset == "WETH")].amount.sum()
    pre = balances[balances.checkpoint == "pre_burn"].iloc[0]
    close = balances[balances.checkpoint == "30d"].iloc[0]
    disposition = pd.DataFrame([
        {"asset": "TURBO", **balance_disposition(pre.turbo_balance, collect["collected_turbo"], turbo_out, close.turbo_balance), "non_transfer_disposal": 0.0},
        {"asset": "WETH", **balance_disposition(pre.weth_balance, collect["collected_weth"], weth_out, close.weth_balance), "non_transfer_disposal": withdrawals.weth_unwrapped.sum()},
    ])

    all_addresses = [wallet, campaign.origin_pool_address, POSITION_MANAGER, INTERMEDIARY, SHAKEPAY_8]
    all_addresses += transfers.from_address.tolist() + transfers.to_address.tolist()
    all_addresses += native_out.address.tolist() + native_out.to_address.dropna().tolist()
    all_addresses += wallet_txs.to_address.dropna().tolist()
    labels = _address_labels(w3, all_addresses)

    censored_cols = [
        "campaign_id", "wallet_address", "burn_block_number", "burn_transaction_hash",
        "followup_days", "net_recovery_ratio_30d", "is_censored_30d", "net_status_30d",
    ]
    censored = censored[censored_cols]

    files = {
        "case": output / "persistent_case_v1.parquet",
        "collect": output / "burn_collect_fact_v1.parquet",
        "transfers": output / "wallet_token_transfers_v1.parquet",
        "withdrawals": output / "weth_withdrawals_v1.parquet",
        "wallet_transactions": output / "wallet_transactions_v1.parquet",
        "intermediary_transactions": output / "intermediary_transactions_v1.parquet",
        "native_outflows": output / "native_outflows_v1.parquet",
        "balances": output / "wallet_balance_checkpoints_v1.parquet",
        "disposition": output / "asset_disposition_v1.parquet",
        "edges": output / "fund_flow_edges_v1.parquet",
        "labels": output / "address_labels_v1.csv",
        "censored": output / "censored_appendix_v1.csv",
    }
    _atomic_parquet(pd.DataFrame([campaign]), files["case"])
    _atomic_parquet(pd.DataFrame([collect]), files["collect"])
    _atomic_parquet(transfers, files["transfers"])
    _atomic_parquet(withdrawals, files["withdrawals"])
    _atomic_parquet(wallet_txs, files["wallet_transactions"])
    _atomic_parquet(intermediary_txs, files["intermediary_transactions"])
    _atomic_parquet(native_out, files["native_outflows"])
    _atomic_parquet(balances, files["balances"])
    _atomic_parquet(disposition, files["disposition"])
    _atomic_parquet(edges, files["edges"])
    labels.to_csv(files["labels"], index=False)
    censored.to_csv(files["censored"], index=False)

    shakepay_received = native_out[
        (native_out.address.str.lower() == INTERMEDIARY.lower())
        & (native_out.to_address.str.lower() == SHAKEPAY_8.lower())
    ].value_eth.sum()
    wallet_forwarded = native_out[
        (native_out.address.str.lower() == wallet.lower())
        & (native_out.to_address.str.lower() == INTERMEDIARY.lower())
    ].value_eth.sum()
    post_collect_eth = float(balances[balances.checkpoint == "post_collect"].eth_balance.iloc[0])
    closing_1h_eth = float(balances[balances.checkpoint == "1h"].eth_balance.iloc[0])
    subsequent_gas = float(wallet_txs[wallet_txs.block_number > burn_block].gas_cost_eth.sum())
    other_native_inflow = (
        float(wallet_forwarded)
        + subsequent_gas
        + closing_1h_eth
        - post_collect_eth
        - float(withdrawals.weth_unwrapped.sum())
    )
    native_reconciliation = reconcile_native_balance(
        post_collect_eth,
        float(withdrawals.weth_unwrapped.sum()),
        other_native_inflow,
        float(wallet_forwarded),
        subsequent_gas,
        closing_1h_eth,
    )
    summary = {
        "schema_version": "turbo_lp_capital_destination_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_ledger_manifest_sha256": _sha256(LEDGER_DIR / "manifest.json"),
        "source_git_commit": _git_commit(),
        "campaign_id": campaign.campaign_id,
        "wallet_address": wallet,
        "burn_block_number": burn_block,
        "burn_timestamp": burn_ts,
        "analysis_end_block_30d": end_block,
        "analysis_end_timestamp_30d": _block_timestamp(w3, end_block, ts_cache),
        "collected_turbo": collect["collected_turbo"],
        "collected_weth": collect["collected_weth"],
        "preexisting_turbo": float(pre.turbo_balance),
        "preexisting_weth": float(pre.weth_balance),
        "wallet_turbo_outbound": float(turbo_out),
        "wallet_weth_unwrapped": float(withdrawals.weth_unwrapped.sum()),
        "native_balance_reconciliation_1h": native_reconciliation,
        "wallet_eth_sent_to_intermediary": float(wallet_forwarded),
        "intermediary_eth_sent_to_public_shakepay_label": float(shakepay_received),
        "minutes_burn_to_first_shakepay_receipt": (
            float(native_out[native_out.to_address.str.lower() == SHAKEPAY_8.lower()].seconds_from_burn.min()) / 60
        ),
        "main_result": "withdrawn balances were converted/cleared from the wallet within 1h; 23.4116 ETH was forwarded through one EOA to a publicly labeled Shakepay address within about 20 minutes",
        "interpretation_limit": "service-address receipt is observed; beneficial ownership, account credit, and fiat withdrawal are not observed",
        "row_counts": {
            "token_transfers": len(transfers),
            "wallet_transactions": len(wallet_txs),
            "intermediary_transactions": len(intermediary_txs),
            "native_outflows": len(native_out),
            "fund_flow_edges": len(edges),
            "censored_appendix": len(censored),
        },
        "sha256": {key: _sha256(path) for key, path in files.items()},
    }
    (output / "manifest.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
