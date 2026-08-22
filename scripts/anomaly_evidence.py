#!/usr/bin/env python3
"""Build a transaction-evidence bundle for a matched Uniswap V3 pool window.

The script combines a directional Swap/Transfer audit with raw pool Mint/Burn
logs and the canonical daily analysis series.  It deliberately matches
remove->mint cycles at the pool-position-key level (owner + tick range), not at
the beneficial-LP level: a shared Position Manager can own many NFT positions.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

from scripts.directional_swap_flow import (  # noqa: E402
    _fetch_tx_from,
    _iso,
    _load_indexed_timestamps,
    _safe_call,
    _tx_hash,
)
from src.client import get_contract, get_web3  # noqa: E402
from src.data.artifacts import read_table  # noqa: E402
from src.discovery.log_utils import get_logs_chunked  # noqa: E402
from src.indexer.indexer import _fetch_block_timestamps  # noqa: E402
from src.models import VerifiedPool  # noqa: E402


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


def _decimal(raw: Any, decimals: int) -> Decimal:
    return Decimal(str(raw or 0)) / (Decimal(10) ** decimals)


def _decimal_text(value: Decimal) -> str:
    return format(value, "f")


def _day(value: Any) -> str:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).date().isoformat()
    text = str(value or "")
    return text[:10]


def build_liquidity_rows(
    mint_logs: Iterable[Any],
    burn_logs: Iterable[Any],
    *,
    pool: VerifiedPool,
    target_token: str,
    target_symbol: str,
    target_decimals: int,
    quote_symbol: str,
    quote_decimals: int,
    timestamps: dict[int, int],
    tx_from: dict[str, str],
) -> list[dict[str, Any]]:
    """Normalize raw V3 Mint/Burn logs while retaining owner and tick range."""
    target_is_token0 = pool.token0.lower() == target_token.lower()
    rows: list[dict[str, Any]] = []
    for event_type, logs in (("ADD", mint_logs), ("REMOVE", burn_logs)):
        for event in logs:
            args = event["args"]
            block = int(event["blockNumber"])
            timestamp = int(timestamps.get(block) or 0)
            tx = _tx_hash(event["transactionHash"])
            amount0 = int(args["amount0"])
            amount1 = int(args["amount1"])
            target_raw = amount0 if target_is_token0 else amount1
            quote_raw = amount1 if target_is_token0 else amount0
            rows.append({
                "date_utc": _day(_iso(timestamp)),
                "block_number": block,
                "block_timestamp": timestamp,
                "timestamp_utc": _iso(timestamp),
                "transaction_hash": tx,
                "log_index": int(event.get("logIndex") or 0),
                "event_type": event_type,
                "pool_address": pool.pool_address.lower(),
                "pool_position_owner": str(args.get("owner") or "").lower(),
                "sender": str(args.get("sender") or "").lower(),
                "tx_from": tx_from.get(tx, ""),
                "tick_lower": int(args.get("tickLower") or 0),
                "tick_upper": int(args.get("tickUpper") or 0),
                "liquidity_raw": str(int(args.get("amount") or 0)),
                "target_symbol": target_symbol,
                "target_amount": _decimal_text(_decimal(target_raw, target_decimals)),
                "quote_symbol": quote_symbol,
                "quote_amount": _decimal_text(_decimal(quote_raw, quote_decimals)),
            })
    return sorted(rows, key=lambda row: (row["block_number"], row["log_index"]))


def match_remove_mint_cycles(
    liquidity_rows: Iterable[dict[str, Any]],
    *,
    max_block_gap: int = 300,
    max_liquidity_delta_ratio: Decimal = Decimal("0.15"),
) -> list[dict[str, Any]]:
    """Match later adds to removes sharing the raw V3 pool position key.

    A match is evidence of pool-level position recreation.  It is not evidence
    that the same beneficial LP controlled both actions when the owner is a
    shared Position Manager.
    """
    rows = list(liquidity_rows)
    adds = [row for row in rows if row.get("event_type") == "ADD"]
    removes = [row for row in rows if row.get("event_type") == "REMOVE"]
    used: set[int] = set()
    output: list[dict[str, Any]] = []
    for remove in removes:
        remove_liq = Decimal(str(remove.get("liquidity_raw") or 0))
        candidates: list[tuple[Decimal, int, int, dict[str, Any]]] = []
        for index, add in enumerate(adds):
            if index in used:
                continue
            block_gap = int(add["block_number"]) - int(remove["block_number"])
            if block_gap < 0 or block_gap > max_block_gap:
                continue
            if (
                add.get("pool_position_owner") != remove.get("pool_position_owner")
                or int(add.get("tick_lower") or 0) != int(remove.get("tick_lower") or 0)
                or int(add.get("tick_upper") or 0) != int(remove.get("tick_upper") or 0)
            ):
                continue
            add_liq = Decimal(str(add.get("liquidity_raw") or 0))
            if remove_liq <= 0:
                continue
            delta_ratio = abs(add_liq - remove_liq) / remove_liq
            if delta_ratio <= max_liquidity_delta_ratio:
                candidates.append((delta_ratio, block_gap, index, add))
        if not candidates:
            continue
        delta_ratio, block_gap, index, add = min(
            candidates, key=lambda item: (item[1], item[0])
        )
        used.add(index)
        remove_target = Decimal(str(remove.get("target_amount") or 0))
        add_target = Decimal(str(add.get("target_amount") or 0))
        output.append({
            "remove_date_utc": remove["date_utc"],
            "remove_block": remove["block_number"],
            "mint_block": add["block_number"],
            "block_gap": block_gap,
            "seconds_gap": int(add["block_timestamp"]) - int(remove["block_timestamp"]),
            "pool_position_owner": remove.get("pool_position_owner") or "",
            "tick_lower": remove["tick_lower"],
            "tick_upper": remove["tick_upper"],
            "remove_transaction_hash": remove["transaction_hash"],
            "mint_transaction_hash": add["transaction_hash"],
            "remove_tx_from": remove.get("tx_from") or "",
            "mint_tx_from": add.get("tx_from") or "",
            "remove_target_amount": _decimal_text(remove_target),
            "mint_target_amount": _decimal_text(add_target),
            "target_amount_recreated_ratio": (
                _decimal_text(add_target / remove_target) if remove_target else ""
            ),
            "liquidity_recreated_ratio": _decimal_text(
                Decimal(str(add.get("liquidity_raw") or 0)) / remove_liq
            ),
            "liquidity_delta_ratio": _decimal_text(delta_ratio),
            "beneficial_owner_proven": False,
            "match_basis": "same pool owner+tick range; similar liquidity; later mint",
        })
    return sorted(
        output,
        key=lambda row: (row["remove_block"], row["mint_block"]),
    )


def _pool_series(source: Path, pool_address: str) -> dict[str, dict[str, Any]]:
    rows = read_table("analysis_series", source, prefer="parquet", legacy_rows=False)
    return {
        _day(row.get("bucket_start")): row
        for row in rows
        if row.get("scope") == "pool"
        and str(row.get("pool_identifier") or "").lower() == pool_address.lower()
    }


def build_daily_ledger(
    days: Iterable[str],
    swap_rows: Iterable[dict[str, Any]],
    transfer_rows: Iterable[dict[str, Any]],
    liquidity_rows: Iterable[dict[str, Any]],
    cycles: Iterable[dict[str, Any]],
    series: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    swaps_by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    transfers_by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    liquidity_by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cycles_by_day: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in swap_rows:
        swaps_by_day[_day(row.get("timestamp_utc"))].append(row)
    for row in transfer_rows:
        transfers_by_day[_day(row.get("timestamp_utc"))].append(row)
    for row in liquidity_rows:
        liquidity_by_day[_day(row.get("date_utc"))].append(row)
    for row in cycles:
        cycles_by_day[_day(row.get("remove_date_utc"))].append(row)

    output: list[dict[str, Any]] = []
    for day in days:
        swaps = swaps_by_day.get(day, [])
        transfers = transfers_by_day.get(day, [])
        liquidities = liquidity_by_day.get(day, [])
        matched = cycles_by_day.get(day, [])
        signed_swaps: list[Decimal] = []
        for row in swaps:
            amount = Decimal(str(row.get("target_amount_abs") or 0))
            direction = str(row.get("direction") or "").upper()
            signed_swaps.append(
                amount if direction.startswith("SELL_")
                else -amount if direction.startswith("BUY_")
                else Decimal(0)
            )
        transfer_values = [Decimal(str(row.get("pool_delta_signed") or 0)) for row in transfers]
        adds = [Decimal(str(row.get("target_amount") or 0)) for row in liquidities if row.get("event_type") == "ADD"]
        removes = [Decimal(str(row.get("target_amount") or 0)) for row in liquidities if row.get("event_type") == "REMOVE"]
        cycle_removed = sum(
            (Decimal(str(row.get("remove_target_amount") or 0)) for row in matched),
            Decimal(0),
        )
        current = series.get(day, {})
        forward: dict[int, Any] = {}
        current_price = current.get("price_close")
        current_date = date.fromisoformat(day)
        for lag in (1, 2, 3):
            later_day = date.fromordinal(current_date.toordinal() + lag).isoformat()
            later_price = series.get(later_day, {}).get("price_close")
            forward[lag] = (
                float(later_price) / float(current_price) - 1
                if current_price not in (None, 0) and later_price is not None
                else None
            )
        gross_remove = sum(removes, Decimal(0))
        net_swap = sum(signed_swaps, Decimal(0))
        net_lp = sum(adds, Decimal(0)) - gross_remove
        actual_transfer_net = sum(transfer_values, Decimal(0))
        explained_flow = net_swap + net_lp
        output.append({
            "date_utc": day,
            "swap_events": len(swaps),
            "sell_events": sum(value > 0 for value in signed_swaps),
            "buy_events": sum(value < 0 for value in signed_swaps),
            "sell_volume_target": _decimal_text(sum((v for v in signed_swaps if v > 0), Decimal(0))),
            "buy_volume_target": _decimal_text(-sum((v for v in signed_swaps if v < 0), Decimal(0))),
            "net_swap_to_pool_target": _decimal_text(net_swap),
            "actual_transfer_in_target": _decimal_text(sum((v for v in transfer_values if v > 0), Decimal(0))),
            "actual_transfer_out_target": _decimal_text(-sum((v for v in transfer_values if v < 0), Decimal(0))),
            "actual_transfer_net_to_pool_target": _decimal_text(actual_transfer_net),
            "lp_add_events": len(adds),
            "lp_remove_events": len(removes),
            "gross_lp_add_target": _decimal_text(sum(adds, Decimal(0))),
            "gross_lp_remove_target": _decimal_text(gross_remove),
            "net_lp_flow_target": _decimal_text(net_lp),
            "swap_plus_lp_explained_flow_target": _decimal_text(explained_flow),
            "unexplained_transfer_residual_target": _decimal_text(
                actual_transfer_net - explained_flow
            ),
            "matched_remove_mint_cycles": len(matched),
            "matched_removed_target": _decimal_text(cycle_removed),
            "matched_remove_share": (
                float(cycle_removed / gross_remove) if gross_remove else None
            ),
            "price_close_weth_per_target": current_price,
            "daily_price_return": current.get("price_return"),
            "forward_return_1d": forward[1],
            "forward_return_2d": forward[2],
            "forward_return_3d": forward[3],
            "reserve_target_close": current.get("tvl_token_close"),
            "volume_turnover": current.get("volume_turnover"),
            "withdrawal_ratio": current.get("withdrawal_ratio"),
        })
    return output


def summarize_bundle(
    daily_rows: list[dict[str, Any]],
    cycles: list[dict[str, Any]],
    directional_summary: dict[str, Any],
) -> dict[str, Any]:
    gross_remove = sum(
        (Decimal(str(row["gross_lp_remove_target"])) for row in daily_rows),
        Decimal(0),
    )
    matched_remove = sum(
        (Decimal(str(row["matched_removed_target"])) for row in daily_rows),
        Decimal(0),
    )
    unique_owner_keys = {
        (row["pool_position_owner"], row["tick_lower"], row["tick_upper"])
        for row in cycles
    }
    return {
        "window_start": daily_rows[0]["date_utc"] if daily_rows else None,
        "window_end": daily_rows[-1]["date_utc"] if daily_rows else None,
        "daily_observations": len(daily_rows),
        "swap_event_count": directional_summary.get("swap_event_count"),
        "actual_transfer_net_to_pool": directional_summary.get("actual_transfer_net_to_pool"),
        "pool_balance_delta": directional_summary.get("pool_balance_delta"),
        "transfer_balance_reconciliation": directional_summary.get("transfer_balance_reconciliation"),
        "gross_lp_remove_target": _decimal_text(gross_remove),
        "matched_remove_mint_cycle_count": len(cycles),
        "matched_pool_position_key_count": len(unique_owner_keys),
        "matched_removed_target": _decimal_text(matched_remove),
        "matched_remove_share": float(matched_remove / gross_remove) if gross_remove else None,
        "identity_guardrail": (
            "Matches prove reuse of a raw V3 pool position key (owner + ticks), "
            "not common beneficial ownership; Position Manager NFT identity was not scanned."
        ),
    }


def _pct(value: Any) -> str:
    return "—" if value is None else "{:+.2f}%".format(float(value) * 100)


def _millions(value: Any) -> str:
    scaled = Decimal(str(value or 0)) / Decimal(1_000_000)
    if abs(scaled) < Decimal("0.0005"):
        scaled = Decimal(0)
    return "{:.3f}M".format(scaled)


def write_summary_md(
    path: Path,
    *,
    pool_address: str,
    from_block: int,
    to_block: int,
    daily_rows: list[dict[str, Any]],
    cycles: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    lines = [
        "# Matched-pool anomaly evidence bundle",
        "",
        "- Pool: `{}`".format(pool_address.lower()),
        "- Blocks: `{}`–`{}`".format(from_block, to_block),
        "- UTC window: `{}` through `{}`".format(summary["window_start"], summary["window_end"]),
        "- Transfer/balance reconciliation: **{}**".format(summary["transfer_balance_reconciliation"]),
        "",
        "## Four-ledger daily view",
        "",
        "| Date | Swap sell / buy | Actual transfer net | LP add / remove | Residual | Matched remove→mint | +1d | +2d | +3d |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in daily_rows:
        share = row.get("matched_remove_share")
        cycle = "{} ({})".format(
            row["matched_remove_mint_cycles"],
            "—" if share is None else "{:.1%}".format(float(share)),
        )
        lines.append(
            "| {date} | {sell} / {buy} | {transfer} | {add} / {remove} | {residual} | {cycle} | {r1} | {r2} | {r3} |".format(
                date=row["date_utc"],
                sell=_millions(row["sell_volume_target"]),
                buy=_millions(row["buy_volume_target"]),
                transfer=_millions(row["actual_transfer_net_to_pool_target"]),
                add=_millions(row["gross_lp_add_target"]),
                remove=_millions(row["gross_lp_remove_target"]),
                residual=_millions(row["unexplained_transfer_residual_target"]),
                cycle=cycle,
                r1=_pct(row["forward_return_1d"]),
                r2=_pct(row["forward_return_2d"]),
                r3=_pct(row["forward_return_3d"]),
            )
        )
    lines.extend([
        "",
        "Positive transfer net means TURBO entered the pool; negative means it left the pool.",
        "Forward returns use the daily WETH-per-TURBO close, so they are ETH-relative, not USD returns.",
        "Residual is actual Transfer net minus signed Swap net minus raw Mint/Burn principal net; it can include collected fees or other pool movements.",
        "",
        "## Remove→mint candidates",
        "",
        "- Matched cycles: **{}**".format(summary["matched_remove_mint_cycle_count"]),
        "- Gross removed: **{}**".format(_millions(summary["gross_lp_remove_target"])),
        "- Removed amount covered by matched cycles: **{} ({})**".format(
            _millions(summary["matched_removed_target"]),
            "—" if summary["matched_remove_share"] is None else "{:.1%}".format(summary["matched_remove_share"]),
        ),
        "",
        "| Remove tx | Mint tx | Blocks / seconds | Ticks | Removed / minted | Liquidity recreated |",
        "|---|---|---:|---:|---:|---:|",
    ])
    ranked = sorted(
        cycles,
        key=lambda row: -Decimal(str(row.get("remove_target_amount") or 0)),
    )[:20]
    for row in ranked:
        lines.append(
            "| `{}` | `{}` | {} / {} | {}→{} | {} / {} | {} |".format(
                row["remove_transaction_hash"], row["mint_transaction_hash"],
                row["block_gap"], row["seconds_gap"], row["tick_lower"], row["tick_upper"],
                _millions(row["remove_target_amount"]), _millions(row["mint_target_amount"]),
                "{:.2%}".format(Decimal(row["liquidity_recreated_ratio"])),
            )
        )
    lines.extend([
        "",
        "## Evidence reading",
        "",
        "- **{:.1%}** of gross removed target-token amount was followed by a matched "
        "pool-position-key Mint under the strict one-hour / similar-liquidity rule.".format(
            summary["matched_remove_share"] or 0
        ),
        "- This makes gross removal primarily an activity/cycling measure in this "
        "window; use net LP flow and actual Transfer net to identify real inventory exit.",
        "- The exact Transfer/balance reconciliation makes actual Transfer net the "
        "cash-flow control ledger. Swap direction alone misses non-Swap liquidity movements.",
        "- The five-day window is transaction evidence for the pilot, not an independent "
        "statistical sample and not proof of causality.",
        "",
        "## Interpretation boundary",
        "",
        "A cycle match uses the same raw V3 pool position key (`owner`, `tickLower`, "
        "`tickUpper`), a later Mint within the configured block gap, and similar "
        "liquidity. When `owner` is the shared NonfungiblePositionManager, this does "
        "**not** prove that the same wallet or NFT position performed both actions. "
        "Beneficial-owner attribution requires a targeted Position Manager/NFT trace.",
        "",
        "Gross removal is activity, not permanent exit. Actual ERC-20 Transfer net "
        "flow and the end-minus-start pool balance are the cash-flow control ledger.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def _date_range(start: str, end: str) -> list[str]:
    first = date.fromisoformat(start)
    last = date.fromisoformat(end)
    if last < first:
        raise ValueError("end date precedes start date")
    return [
        date.fromordinal(ordinal).isoformat()
        for ordinal in range(first.toordinal(), last.toordinal() + 1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a four-ledger anomaly evidence bundle for a V3 pool"
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--directional-dir", required=True)
    parser.add_argument("--pool", required=True)
    parser.add_argument("--from-block", type=int, required=True)
    parser.add_argument("--to-block", type=int, required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-cycle-block-gap", type=int, default=300)
    parser.add_argument("--max-liquidity-delta-ratio", type=Decimal, default=Decimal("0.15"))
    parser.add_argument(
        "--with-tx-from",
        action="store_true",
        help="Fetch transaction senders; slower and not required for pool-position-key matching.",
    )
    parser.add_argument("--rpc-url", default="")
    args = parser.parse_args()

    source = Path(args.output_dir)
    directional = Path(args.directional_dir)
    out = Path(args.out_dir)
    if args.from_block <= 0 or args.to_block < args.from_block:
        parser.error("invalid block window")
    days = _date_range(args.start_date, args.end_date)
    profile = _load_json(source / "token_profile.json")
    pools = [VerifiedPool(**row) for row in _load_json(source / "verified_pools.json")]
    selected = next((
        pool for pool in pools
        if pool.verified and pool.pool_address.lower() == args.pool.lower()
    ), None)
    if selected is None or selected.version != "v3":
        parser.error("selected pool must be a verified Uniswap V3 pool")

    target_token = str(profile.get("address") or "")
    target_symbol = str(profile.get("symbol") or "TARGET")
    target_decimals = int(profile.get("decimals") or 18)
    quote_token = selected.token1 if selected.token0.lower() == target_token.lower() else selected.token0
    rpc_url = args.rpc_url or os.environ.get("ETH_RPC_URL") or os.environ.get("RPC_URL")
    w3 = get_web3(rpc_url)
    pool_contract = get_contract(w3, selected.pool_address, "uniswap_v3_pool")
    quote_contract = get_contract(w3, quote_token, "erc20")
    quote_symbol = str(_safe_call(quote_contract, "symbol", "QUOTE"))
    quote_decimals = int(_safe_call(quote_contract, "decimals", 18))

    mint_logs = get_logs_chunked(
        pool_contract.events.Mint(), args.from_block, args.to_block
    )
    burn_logs = get_logs_chunked(
        pool_contract.events.Burn(), args.from_block, args.to_block
    )
    raw_logs = list(mint_logs) + list(burn_logs)
    liquidity_blocks = {int(event["blockNumber"]) for event in raw_logs}
    timestamps = _load_indexed_timestamps(source, liquidity_blocks)
    missing_timestamp_blocks = liquidity_blocks.difference(timestamps)
    if missing_timestamp_blocks:
        timestamps.update(_fetch_block_timestamps(w3, missing_timestamp_blocks))
    tx_from = (
        _fetch_tx_from(
            w3, {_tx_hash(event["transactionHash"]) for event in raw_logs}
        )
        if args.with_tx_from else {}
    )
    liquidity_rows = build_liquidity_rows(
        mint_logs, burn_logs,
        pool=selected,
        target_token=target_token,
        target_symbol=target_symbol,
        target_decimals=target_decimals,
        quote_symbol=quote_symbol,
        quote_decimals=quote_decimals,
        timestamps=timestamps,
        tx_from=tx_from,
    )
    cycles = match_remove_mint_cycles(
        liquidity_rows,
        max_block_gap=args.max_cycle_block_gap,
        max_liquidity_delta_ratio=args.max_liquidity_delta_ratio,
    )
    swaps = _read_csv(directional / "signed_swaps.csv")
    transfers = _read_csv(directional / "pool_target_transfers.csv")
    directional_summary = _load_json(directional / "summary.json")
    series = _pool_series(source, selected.pool_address)
    daily = build_daily_ledger(
        days, swaps, transfers, liquidity_rows, cycles, series
    )
    summary = summarize_bundle(daily, cycles, directional_summary)

    _write_csv(out / "daily_ledger.csv", daily)
    _write_csv(out / "raw_v3_liquidity.csv", liquidity_rows)
    _write_csv(out / "remove_mint_cycles.csv", cycles)
    _write_json(out / "summary.json", summary)
    write_summary_md(
        out / "summary.md",
        pool_address=selected.pool_address,
        from_block=args.from_block,
        to_block=args.to_block,
        daily_rows=daily,
        cycles=cycles,
        summary=summary,
    )
    print(json.dumps({"out_dir": str(out), **summary}, indent=2))


if __name__ == "__main__":
    main()
