#!/usr/bin/env python3
"""Build frozen Swap, gap-exposure, and matched price-impact tables for TURBO."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eth_abi import decode
import numpy as np
import pandas as pd
import requests
from web3 import Web3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in os.sys.path:
    os.sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env", override=True)
except ImportError:  # pragma: no cover
    pass

from src.analysis.lp_gap_impact import (
    build_gap_intervals,
    campaign_cluster_bootstrap,
    greedy_size_match,
    label_gap_swaps,
    mark_full_gap_contamination,
)
from src.client import get_contract, get_web3


SWAP_SIGNATURE = "Swap(address,address,int256,int256,uint160,uint128,int24)"
CALIPERS = (0.10, 0.25, 0.50)


def _hex(value: Any) -> str:
    if isinstance(value, str):
        return value if value.startswith("0x") else f"0x{value}"
    text = value.hex()
    return text if text.startswith("0x") else f"0x{text}"


def _int(value: Any) -> int:
    return int(value, 16) if isinstance(value, str) else int(value)


def _topic_address(value: Any) -> str:
    return Web3.to_checksum_address("0x" + _hex(value)[-40:])


def _rpc_logs(rpc_url: str, pool: str, start: int, end: int) -> list[dict]:
    topic = "0x" + Web3.keccak(text=SWAP_SIGNATURE).hex().removeprefix("0x")

    def fetch(left: int, right: int) -> list[dict]:
        params = {
            "address": Web3.to_checksum_address(pool),
            "fromBlock": hex(left), "toBlock": hex(right), "topics": [topic],
        }
        response = requests.post(
            rpc_url,
            json={"jsonrpc": "2.0", "id": 1, "method": "eth_getLogs", "params": [params]},
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        if "error" in payload:
            raise RuntimeError(str(payload["error"]))
        return payload["result"]

    def lossless(left: int, right: int) -> list[dict]:
        try:
            return fetch(left, right)
        except Exception as exc:
            if left == right:
                raise RuntimeError(f"Swap scan failed at block {left}; no block was skipped") from exc
            midpoint = (left + right) // 2
            return lossless(left, midpoint) + lossless(midpoint + 1, right)

    return lossless(start, end)


def decode_swap(raw: dict, pool: dict) -> dict:
    amount0, amount1, sqrt_price, liquidity, tick = decode(
        ["int256", "int256", "uint160", "uint128", "int24"],
        bytes.fromhex(_hex(raw["data"])[2:]),
    )
    block = _int(raw["blockNumber"])
    tx_index = _int(raw["transactionIndex"])
    log_index = _int(raw["logIndex"])
    return {
        "swap_event_id": f"{pool['pool_address'].lower()}:{block}:{tx_index}:{log_index}",
        "pool_address": pool["pool_address"],
        "fee": int(pool["fee"]),
        "block_number": block,
        "transaction_index": tx_index,
        "log_index": log_index,
        "transaction_hash": _hex(raw["transactionHash"]).lower(),
        "sender": _topic_address(raw["topics"][1]),
        "recipient": _topic_address(raw["topics"][2]),
        "amount0_raw": str(int(amount0)),
        "amount1_raw": str(int(amount1)),
        "turbo_amount_signed": int(amount0) / 1e18,
        "weth_amount_signed": int(amount1) / 1e18,
        "sqrt_price_x96_after": str(int(sqrt_price)),
        "active_liquidity_after_raw": str(int(liquidity)),
        "tick_after": int(tick),
        "spot_price_after_weth_per_turbo": (int(sqrt_price) / 2**96) ** 2,
    }


def add_price_impact(w3: Web3, swaps: pd.DataFrame) -> pd.DataFrame:
    output = []
    for pool_address, frame in swaps.groupby("pool_address", sort=False):
        frame = frame.sort_values(["block_number", "transaction_index", "log_index"], kind="stable").copy()
        frame["spot_price_before_weth_per_turbo"] = frame.spot_price_after_weth_per_turbo.shift(1)
        first_index = frame.index[0]
        pool = get_contract(w3, pool_address, "uniswap_v3_pool")
        sqrt_before = int(pool.functions.slot0().call(
            block_identifier=int(frame.loc[first_index, "block_number"]) - 1
        )[0])
        frame.loc[first_index, "spot_price_before_weth_per_turbo"] = (sqrt_before / 2**96) ** 2
        frame["direction"] = np.where(frame.turbo_amount_signed > 0, "sell_turbo", "buy_turbo")
        frame["execution_price_weth_per_turbo"] = (
            frame.weth_amount_signed.abs() / frame.turbo_amount_signed.abs()
        )
        buy = frame.direction.eq("buy_turbo")
        frame["price_impact_bps"] = np.where(
            buy,
            (frame.spot_price_after_weth_per_turbo / frame.spot_price_before_weth_per_turbo - 1) * 10_000,
            (1 - frame.spot_price_after_weth_per_turbo / frame.spot_price_before_weth_per_turbo) * 10_000,
        )
        frame["execution_deviation_bps"] = np.where(
            buy,
            (frame.execution_price_weth_per_turbo / frame.spot_price_before_weth_per_turbo - 1) * 10_000,
            (1 - frame.execution_price_weth_per_turbo / frame.spot_price_before_weth_per_turbo) * 10_000,
        )
        frame["notional_weth"] = np.where(
            buy,
            frame.weth_amount_signed.clip(lower=0),
            frame.turbo_amount_signed.clip(lower=0) * frame.spot_price_before_weth_per_turbo,
        )
        output.append(frame)
    return pd.concat(output, ignore_index=True).sort_values(
        ["block_number", "transaction_index", "log_index"], kind="stable"
    ).reset_index(drop=True)


def fetch_block_timestamps_cached(
    rpc_url: str,
    block_numbers: set[int],
    cache_path: Path,
    batch_size: int = 20,
    pause_seconds: float = 0.8,
    workers: int = 1,
) -> dict[int, int]:
    """Fetch exact timestamps in rate-safe batches with an on-disk checkpoint."""
    if cache_path.exists():
        cached_payload = json.loads(cache_path.read_text())
        timestamps = {int(key): int(value) for key, value in cached_payload.items()}
    else:
        timestamps = {}
    missing = [block for block in sorted(block_numbers) if block not in timestamps]
    chunks = [missing[offset:offset + batch_size] for offset in range(0, len(missing), batch_size)]

    def fetch_chunk(chunk: list[int]) -> dict[int, int]:
        payload = [
            {"jsonrpc": "2.0", "id": block, "method": "eth_getBlockByNumber", "params": [hex(block), False]}
            for block in chunk
        ]
        for attempt in range(8):
            response = requests.post(rpc_url, json=payload, timeout=45)
            body = response.json()
            if response.status_code == 200 and isinstance(body, list):
                returned = {
                    int(item["id"]): int(item["result"]["timestamp"], 16)
                    for item in body if item.get("result") and item["result"].get("timestamp")
                }
                if len(returned) == len(chunk):
                    time.sleep(pause_seconds)
                    return returned
            if attempt == 7:
                raise RuntimeError(f"Timestamp batch failed after retries: blocks {chunk[0]}-{chunk[-1]}")
            time.sleep(min(8.0, 0.75 * 2**attempt))
        raise AssertionError("unreachable")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for returned in executor.map(fetch_chunk, chunks):
            timestamps.update(returned)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps({str(k): v for k, v in sorted(timestamps.items())}) + "\n")
    return {block: timestamps[block] for block in block_numbers}


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
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--rpc-url")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ledger_manifest = json.loads((args.ledger_dir / "manifest.json").read_text())
    campaigns = pd.read_parquet(args.ledger_dir / "lp_campaign_ledger_v1.parquet")
    rpc_url = args.rpc_url or os.environ.get("ETH_RPC_URL") or os.environ.get("RPC_URL")
    if not rpc_url:
        raise ValueError("ETH_RPC_URL, RPC_URL, or --rpc-url is required")
    w3 = get_web3(rpc_url)

    rows = []
    for pool in ledger_manifest["scanned_pools"]:
        logs = _rpc_logs(
            rpc_url, pool["pool_address"], ledger_manifest["cohort_from_block"],
            ledger_manifest["followup_data_end_block"],
        )
        rows.extend(decode_swap(raw, pool) for raw in logs)
    swaps = pd.DataFrame(rows)
    timestamp_rpc_url = os.environ.get("TASK_TIMESTAMP_RPC_URL") or rpc_url
    separate_timestamp_rpc = timestamp_rpc_url != rpc_url
    timestamps = fetch_block_timestamps_cached(
        timestamp_rpc_url,
        set(swaps.block_number.astype(int)),
        args.output_dir / "block_timestamps_checkpoint.json",
        batch_size=20,
        pause_seconds=1.0 if separate_timestamp_rpc else 0.8,
        workers=2 if separate_timestamp_rpc else 1,
    )
    if not all(timestamps.values()):
        missing = [block for block, value in timestamps.items() if not value]
        raise RuntimeError(f"Missing timestamps for {len(missing)} Swap blocks")
    swaps["timestamp"] = swaps.block_number.map(timestamps).astype("int64")
    swaps["datetime_utc"] = pd.to_datetime(swaps.timestamp, unit="s", utc=True)
    swaps = add_price_impact(w3, swaps)
    valid = (
        swaps.notional_weth.gt(0) & np.isfinite(swaps.price_impact_bps)
        & swaps.price_impact_bps.ge(0)
    )
    swaps["price_impact_eligible"] = valid

    followup_timestamp = int(pd.Timestamp(ledger_manifest["followup_data_end_time"]).timestamp())
    intervals = build_gap_intervals(campaigns, followup_timestamp)
    exposures = label_gap_swaps(swaps[valid].copy(), intervals)
    swaps["excluded_from_controls_any_90pct_gap_24h"] = mark_full_gap_contamination(
        swaps, campaigns, followup_timestamp, threshold=90, cap_seconds=86_400
    )
    controls = swaps[valid & ~swaps.excluded_from_controls_any_90pct_gap_24h].copy()

    pair_frames = []
    summaries = []
    for threshold in (80, 90):
        for horizon in ("1h", "6h", "24h"):
            treated = exposures[
                exposures.threshold_pct.eq(threshold) & exposures.horizon.eq(horizon)
            ].copy()
            for caliper in CALIPERS:
                pairs = greedy_size_match(treated, controls, caliper)
                if not pairs.empty:
                    pair_frames.append(pairs)
                bootstrap = campaign_cluster_bootstrap(pairs)
                summaries.append({
                    "threshold_pct": threshold,
                    "horizon": horizon,
                    "caliper_pct": caliper,
                    "treated_swap_count": len(treated),
                    "treated_campaign_count": treated.primary_campaign_id.nunique() if not treated.empty else 0,
                    "matched_pair_count": len(pairs),
                    "match_rate": len(pairs) / len(treated) if len(treated) else np.nan,
                    "treated_median_price_impact_bps": treated.price_impact_bps.median() if len(treated) else np.nan,
                    "control_median_price_impact_bps": pairs.control_price_impact_bps.median() if len(pairs) else np.nan,
                    "median_excess_price_impact_bps": pairs.excess_price_impact_bps.median() if len(pairs) else np.nan,
                    "mean_cluster_excess_price_impact_bps": bootstrap["estimate"],
                    "cluster_bootstrap_ci_low": bootstrap["ci_low"],
                    "cluster_bootstrap_ci_high": bootstrap["ci_high"],
                    "campaign_day_clusters": bootstrap["campaigns"],
                    "positive_excess_share": pairs.excess_price_impact_bps.gt(0).mean() if len(pairs) else np.nan,
                })
    pairs_all = pd.concat(pair_frames, ignore_index=True) if pair_frames else pd.DataFrame()
    summary = pd.DataFrame(summaries)

    files = {
        "swaps": args.output_dir / "swaps_with_price_impact_v1.parquet",
        "gap_intervals": args.output_dir / "gap_intervals_v1.parquet",
        "gap_swap_exposure": args.output_dir / "gap_swap_exposure_v1.parquet",
        "matched_pairs": args.output_dir / "matched_swap_pairs_v1.parquet",
        "summary": args.output_dir / "gap_impact_summary_v1.csv",
    }
    _atomic_parquet(swaps, files["swaps"])
    _atomic_parquet(intervals, files["gap_intervals"])
    _atomic_parquet(exposures, files["gap_swap_exposure"])
    _atomic_parquet(pairs_all, files["matched_pairs"])
    summary.to_csv(files["summary"], index=False)

    manifest = {
        "schema_version": "turbo_lp_gap_impact_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_ledger_manifest_sha256": _sha256(args.ledger_dir / "manifest.json"),
        "source_ledger_schema": ledger_manifest["schema_version"],
        "cohort_from_block": ledger_manifest["cohort_from_block"],
        "cohort_end_block": ledger_manifest["cohort_end_block"],
        "followup_data_end_block": ledger_manifest["followup_data_end_block"],
        "thresholds_pct": [80, 90],
        "horizons": ["1h", "6h", "24h"],
        "control_rule": "same pool, same direction, one-to-one nearest WETH notional, no reuse, outside every 90%-gap capped at 24h",
        "size_calipers": list(CALIPERS),
        "primary_caliper": 0.25,
        "outcome": "direction-normalized pre-to-post pool mid-price movement in basis points",
        "auxiliary_outcome": "execution-price deviation from pre-swap spot; includes fee and is not user slippage",
        "inference": "campaign-by-UTC-day cluster bootstrap, 5000 deterministic draws",
        "row_counts": {
            "swaps": len(swaps), "eligible_swaps": int(valid.sum()),
            "control_swaps": len(controls), "gap_intervals": len(intervals),
            "gap_swap_exposures": len(exposures), "matched_pair_rows_all_sensitivities": len(pairs_all),
        },
        "sha256": {name: _sha256(path) for name, path in files.items()},
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(manifest["row_counts"], ensure_ascii=False))
    primary = summary[summary.caliper_pct.eq(.25)]
    print(primary.to_string(index=False))


if __name__ == "__main__":
    main()
