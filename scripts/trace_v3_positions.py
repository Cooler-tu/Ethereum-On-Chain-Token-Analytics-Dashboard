#!/usr/bin/env python3
"""Targeted V3 position trace for selected LP-forensic transactions.

Only receipts named by the offline forensic bundle are fetched. Pool Mint/Burn
events are matched to Position Manager Increase/DecreaseLiquidity events by
direction and exact token amounts, yielding tokenId, raw tick range, tx sender,
and owner-at-block where the RPC supports historical calls.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from web3.logs import DISCARD

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

from src.client import get_contract, get_web3  # noqa: E402


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def _load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with open(path, "w", newline="", encoding="utf-8") as handle:
        if fields:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
    tmp.replace(path)


def tick_range_weth_per_target(
    tick_lower: int,
    tick_upper: int,
    *,
    target_is_token0: bool,
    target_decimals: int,
) -> tuple[float, float]:
    """Convert a V3 raw tick interval to human WETH per target token."""
    exponent_lower = tick_lower if target_is_token0 else -tick_upper
    exponent_upper = tick_upper if target_is_token0 else -tick_lower
    decimal_scale = 10 ** (target_decimals - 18)
    low = math.pow(1.0001, exponent_lower) * decimal_scale
    high = math.pow(1.0001, exponent_upper) * decimal_scale
    return min(low, high), max(low, high)


def inventory_shape(
    current_price: float,
    lower_price: float,
    upper_price: float,
) -> str:
    if current_price < lower_price:
        return "target_only_below_range"
    if current_price > upper_price:
        return "weth_only_above_range"
    return "two_sided_in_range"


def match_position_manager_event(
    pool_event: dict[str, Any],
    manager_events: list[dict[str, Any]],
    used: set[int],
) -> dict[str, Any] | None:
    expected = "IncreaseLiquidity" if pool_event["event_type"] == "Mint" else "DecreaseLiquidity"
    candidates: list[tuple[int, dict[str, Any]]] = []
    for index, event in enumerate(manager_events):
        if index in used or event.get("event_type") != expected:
            continue
        if (
            int(event.get("amount0") or 0) == int(pool_event.get("amount0") or 0)
            and int(event.get("amount1") or 0) == int(pool_event.get("amount1") or 0)
        ):
            candidates.append((index, event))
    if not candidates:
        return None
    index, event = candidates[0]
    used.add(index)
    return event


def build_selected_position_cycles(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find opposite actions on the same NFT within the selected transaction set."""
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in traces:
        if row.get("nft_token_id") not in (None, ""):
            grouped[(str(row.get("case") or ""), str(row["nft_token_id"]))].append(row)
    output: list[dict[str, Any]] = []
    for (case, token_id), rows in grouped.items():
        ordered = sorted(rows, key=lambda row: (int(row["block_number"]), row["transaction_hash"]))
        for first, second in zip(ordered, ordered[1:]):
            if first["pool_event"] == second["pool_event"]:
                continue
            output.append({
                "case": case,
                "nft_token_id": token_id,
                "first_action": first["pool_event"],
                "second_action": second["pool_event"],
                "first_block": first["block_number"],
                "second_block": second["block_number"],
                "block_gap": int(second["block_number"]) - int(first["block_number"]),
                "same_owner_at_block": (
                    bool(first.get("owner_at_block"))
                    and first.get("owner_at_block") == second.get("owner_at_block")
                ),
                "same_tx_sender": first.get("tx_from") == second.get("tx_from"),
                "same_tick_range": (
                    first.get("tick_lower") == second.get("tick_lower")
                    and first.get("tick_upper") == second.get("tick_upper")
                ),
                "first_transaction_hash": first["transaction_hash"],
                "second_transaction_hash": second["transaction_hash"],
            })
    return output


def _decode_receipt_events(contract: Any, event_names: tuple[str, ...], receipt: Any) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for name in event_names:
        for event in getattr(contract.events, name)().process_receipt(receipt, errors=DISCARD):
            args = event["args"]
            output.append({
                "event_type": name,
                "log_index": int(event.get("logIndex") or 0),
                **{key: value for key, value in args.items()},
            })
    return sorted(output, key=lambda row: int(row["log_index"]))


def trace_transactions(
    transaction_rows: list[dict[str, str]],
    case_dirs: dict[str, Path],
    *,
    rpc_url: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    w3 = get_web3(rpc_url)
    case_context: dict[str, dict[str, Any]] = {}
    for label, output_dir in case_dirs.items():
        profile = _load_json(output_dir / "token_profile.json")
        pools = {
            str(row.get("pool_address") or "").lower(): row
            for row in _load_json(output_dir / "verified_pools.json")
        }
        case_context[label] = {"profile": profile, "pools": pools}

    traces: list[dict[str, Any]] = []
    receipt_cache: dict[str, Any] = {}
    transaction_cache: dict[str, Any] = {}
    manager_cache: dict[str, Any] = {}
    for selected in transaction_rows:
        if str(selected.get("version") or "").lower() != "v3":
            continue
        label = str(selected["case"]).upper()
        context = case_context[label]
        profile = context["profile"]
        target = str(profile["address"]).lower()
        target_decimals = int(profile["decimals"])
        pool_address = str(selected["pool_address"]).lower()
        pool = context["pools"][pool_address]
        manager_address = str(pool.get("position_manager_address") or "")
        if not manager_address:
            raise ValueError(f"missing Position Manager for {pool_address}")
        tx_hash = str(selected["transaction_hash"]).lower()
        receipt = receipt_cache.setdefault(tx_hash, w3.eth.get_transaction_receipt(tx_hash))
        transaction = transaction_cache.setdefault(tx_hash, w3.eth.get_transaction(tx_hash))
        pool_contract = get_contract(w3, pool_address, "uniswap_v3_pool")
        manager_contract = manager_cache.setdefault(
            manager_address.lower(),
            get_contract(w3, manager_address, "uniswap_v3_position_manager"),
        )
        pool_events = _decode_receipt_events(pool_contract, ("Mint", "Burn"), receipt)
        manager_events = _decode_receipt_events(
            manager_contract,
            ("IncreaseLiquidity", "DecreaseLiquidity", "Transfer"),
            receipt,
        )
        transfers_by_token: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for event in manager_events:
            if event["event_type"] == "Transfer":
                transfers_by_token[int(event["tokenId"])].append(event)
        used: set[int] = set()
        current_price = float(selected.get("price_close_weth_per_target") or 0)
        # Older forensic CSVs do not carry price; recover it from the hour file later in main.
        for event in pool_events:
            normalized = {
                "event_type": event["event_type"],
                "amount0": int(event.get("amount0") or 0),
                "amount1": int(event.get("amount1") or 0),
            }
            matched = match_position_manager_event(normalized, manager_events, used)
            token_id = int(matched["tokenId"]) if matched else None
            owner_at_block = ""
            owner_source = "unavailable"
            if token_id is not None:
                token_transfers = transfers_by_token.get(token_id, [])
                if token_transfers:
                    last = token_transfers[-1]
                    destination = str(last.get("to") or "").lower()
                    if destination != ZERO_ADDRESS:
                        owner_at_block = destination
                        owner_source = "same_receipt_transfer"
                if not owner_at_block:
                    try:
                        owner_at_block = str(
                            manager_contract.functions.ownerOf(token_id).call(
                                block_identifier=int(receipt["blockNumber"])
                            )
                        ).lower()
                        owner_source = "historical_ownerOf"
                    except Exception:
                        pass
            tick_lower = int(event.get("tickLower") or 0)
            tick_upper = int(event.get("tickUpper") or 0)
            target_is_token0 = str(pool.get("token0") or "").lower() == target
            lower_price, upper_price = tick_range_weth_per_target(
                tick_lower,
                tick_upper,
                target_is_token0=target_is_token0,
                target_decimals=target_decimals,
            )
            shape = inventory_shape(current_price, lower_price, upper_price) if current_price else "price_unavailable"
            traces.append({
                "case": label,
                "hour_rank": int(selected["hour_rank"]),
                "hour_utc": selected["hour_utc"],
                "transaction_hash": tx_hash,
                "block_number": int(receipt["blockNumber"]),
                "tx_from": str(transaction["from"]).lower(),
                "tx_to": str(transaction.get("to") or "").lower(),
                "pool_address": pool_address,
                "fee": int(pool.get("fee") or 0),
                "pool_event": event["event_type"],
                "pool_position_owner": str(event.get("owner") or "").lower(),
                "tick_lower": tick_lower,
                "tick_upper": tick_upper,
                "position_manager_event": matched["event_type"] if matched else "",
                "nft_token_id": token_id if token_id is not None else "",
                "owner_at_block": owner_at_block,
                "owner_source": owner_source,
                "current_price_weth_per_target": current_price,
                "range_lower_weth_per_target": lower_price,
                "range_upper_weth_per_target": upper_price,
                "inventory_shape_at_hour_close": shape,
                "amount0_raw": normalized["amount0"],
                "amount1_raw": normalized["amount1"],
                "manager_match_exact_amounts": matched is not None,
            })

    token_ids = {str(row["nft_token_id"]) for row in traces if row["nft_token_id"] != ""}
    owner_ids = {row["owner_at_block"] for row in traces if row["owner_at_block"]}
    senders = {row["tx_from"] for row in traces if row["tx_from"]}
    cycles = build_selected_position_cycles(traces)
    summary = {
        "transaction_count": len({row["transaction_hash"] for row in traces}),
        "pool_event_count": len(traces),
        "exact_manager_match_count": sum(bool(row["manager_match_exact_amounts"]) for row in traces),
        "unique_nft_token_ids": len(token_ids),
        "known_owner_count": len(owner_ids),
        "unique_tx_senders": len(senders),
        "target_only_range_events": sum(
            row["inventory_shape_at_hour_close"] == "target_only_below_range" for row in traces
        ),
        "two_sided_range_events": sum(
            row["inventory_shape_at_hour_close"] == "two_sided_in_range" for row in traces
        ),
        "quote_only_range_events": sum(
            row["inventory_shape_at_hour_close"] == "weth_only_above_range" for row in traces
        ),
        "selected_position_cycle_count": len(cycles),
        "selected_position_cycles": cycles,
        "guardrail": (
            "Owner is resolved at the transaction block when possible. No common-control "
            "claim is made across different owner addresses or tokenIds. Hour-close price "
            "classifies the range approximately; exact intra-block price may differ."
        ),
    }
    return traces, summary


def write_summary_md(path: Path, traces: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines = [
        "# Targeted V3 position trace",
        "",
        "- Transactions traced: **{}**".format(summary["transaction_count"]),
        "- Pool Mint/Burn events decoded: **{}**".format(summary["pool_event_count"]),
        "- Exact Position Manager amount matches: **{}/{}**".format(
            summary["exact_manager_match_count"], summary["pool_event_count"]
        ),
        "- Unique NFT tokenIds: **{}**".format(summary["unique_nft_token_ids"]),
        "- Unique transaction senders: **{}**".format(summary["unique_tx_senders"]),
        "- Range shape at hour close: target-only **{}**, two-sided **{}**, WETH-only **{}**".format(
            summary["target_only_range_events"], summary["two_sided_range_events"],
            summary["quote_only_range_events"],
        ),
        "- Same-NFT opposite-action pairs inside the selected transaction set: **{}**".format(
            summary["selected_position_cycle_count"]
        ),
        "",
        "| Case | Rank | Event | NFT | Tx sender | Owner at block | Ticks | Range shape | Tx |",
        "|---|---:|---|---:|---|---|---:|---|---|",
    ]
    for row in traces:
        lines.append(
            "| {case} | {rank} | {event} | {nft} | `{sender}` | `{owner}` | {lower}→{upper} | {shape} | `{tx}` |".format(
                case=row["case"], rank=row["hour_rank"], event=row["pool_event"],
                nft=row["nft_token_id"] or "—", sender=row["tx_from"],
                owner=row["owner_at_block"] or "unavailable", lower=row["tick_lower"],
                upper=row["tick_upper"], shape=row["inventory_shape_at_hour_close"],
                tx=row["transaction_hash"],
            )
        )
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        summary["guardrail"],
        "A shared Position Manager pool owner is not treated as the LP identity; tokenId, owner-at-block, and transaction sender are reported separately.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Trace V3 positions for selected forensic transactions")
    parser.add_argument("--transactions", required=True)
    parser.add_argument("--ranked-hours", required=True)
    parser.add_argument("--case", action="append", required=True, metavar="LABEL=OUTPUT_DIR")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--rpc-url", default="")
    args = parser.parse_args()
    case_dirs: dict[str, Path] = {}
    for spec in args.case:
        if "=" not in spec:
            parser.error(f"invalid --case {spec!r}")
        label, raw_path = spec.split("=", 1)
        case_dirs[label.strip().upper()] = Path(raw_path)
    transactions = _read_csv(Path(args.transactions))
    prices = {
        (row["case"].upper(), row["hour_utc"]): row["price_close_weth_per_target"]
        for row in _read_csv(Path(args.ranked_hours))
    }
    for row in transactions:
        row["price_close_weth_per_target"] = prices.get(
            (row["case"].upper(), row["hour_utc"]), ""
        )
    rpc_url = args.rpc_url or os.environ.get("ETH_RPC_URL") or os.environ.get("RPC_URL") or ""
    if not rpc_url:
        parser.error("ETH_RPC_URL, RPC_URL, or --rpc-url is required")
    traces, summary = trace_transactions(transactions, case_dirs, rpc_url=rpc_url)
    out = Path(args.out_dir)
    _write_csv(out / "v3_position_traces.csv", traces)
    _write_csv(out / "v3_selected_position_cycles.csv", summary["selected_position_cycles"])
    _write_json(out / "v3_position_trace_summary.json", summary)
    write_summary_md(out / "v3_position_trace_summary.md", traces, summary)
    print(json.dumps({"out_dir": str(out), **summary}, indent=2))


if __name__ == "__main__":
    main()
