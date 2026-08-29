#!/usr/bin/env python3
"""Run the frozen GALA LP-inventory mechanism validation.

This script deliberately implements only the three hypotheses registered in
research-notes/gala-inventory-mechanism-preregistration.md.  It values each
Mint from the latest same-pool Swap at or before the Mint within one hour,
keeps no-add hours missing, and uses 24-hour calendar blocks for inference.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.correlation_robustness import benjamini_hochberg, _percentile  # noqa: E402
from scripts.time_series_correlation import spearman, _timestamp  # noqa: E402
from src.data.artifacts import read_table  # noqa: E402


WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
HOUR = 3600
BLOCK_HOURS = 24
SEED = 20260829


def _number(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _event_timestamp(row: dict[str, Any]) -> int:
    value = row.get("block_timestamp")
    if isinstance(value, datetime):
        return int(value.timestamp())
    return int(value or 0)


def _hour(timestamp: int) -> int:
    return timestamp // HOUR * HOUR


def _iso(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace("+00:00", "Z")


def _seed(label: str) -> int:
    digest = hashlib.sha256(f"{SEED}:{label}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def _load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
    temporary.replace(path)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with open(path, "w", newline="", encoding="utf-8") as handle:
        if fields:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def _pool_map(config_path: Path) -> tuple[str, dict[str, dict[str, Any]]]:
    config = _load_json(config_path)
    token = str(config["token"]).lower()
    pools = {
        str(row["pool_address"]).lower(): {
            **row,
            "pool_address": str(row["pool_address"]).lower(),
            "token0": str(row["token0"]).lower(),
            "token1": str(row["token1"]).lower(),
            "version": str(row["version"]).lower(),
        }
        for row in config["pools"]
    }
    return token, pools


def _amounts(
    row: dict[str, Any], pool: dict[str, Any], target: str, target_decimals: int
) -> tuple[Decimal, Decimal]:
    target_is_token0 = pool["token0"] == target
    quote = pool["token1"] if target_is_token0 else pool["token0"]
    if quote != WETH:
        raise ValueError(f"expected WETH quote, got {quote}")
    target_raw = row["token0_amount"] if target_is_token0 else row["token1_amount"]
    quote_raw = row["token1_amount"] if target_is_token0 else row["token0_amount"]
    target_amount = Decimal(str(target_raw)) / (Decimal(10) ** target_decimals)
    quote_amount = Decimal(str(quote_raw)) / (Decimal(10) ** 18)
    return abs(target_amount), abs(quote_amount)


def _swap_price(
    row: dict[str, Any], pool: dict[str, Any], target: str, target_decimals: int
) -> Optional[Decimal]:
    target_amount, quote_amount = _amounts(row, pool, target, target_decimals)
    if target_amount <= 0 or quote_amount <= 0:
        return None
    return quote_amount / target_amount


def _last_swap_indexes(
    swaps: list[dict[str, Any]], pools: dict[str, dict[str, Any]]
) -> dict[str, tuple[list[tuple[int, int]], list[dict[str, Any]]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in swaps:
        pool_id = str(row.get("pool_address") or "").lower()
        if pool_id in pools:
            grouped[pool_id].append(row)
    output = {}
    for pool_id, rows in grouped.items():
        rows.sort(key=lambda row: (int(row["block_number"]), int(row["log_index"])))
        output[pool_id] = (
            [(int(row["block_number"]), int(row["log_index"])) for row in rows],
            rows,
        )
    return output


def build_hour_features(
    output_dir: Path,
    config_path: Path,
) -> tuple[dict[int, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Build Mint-valued hourly features without filling no-add hours with zero."""
    profile = _load_json(output_dir / "token_profile.json")
    target_decimals = int(profile["decimals"])
    target, pools = _pool_map(config_path)
    liquidity = read_table("liquidity_events", output_dir, prefer="parquet", legacy_rows=False)
    swaps = read_table("swaps", output_dir, prefer="parquet", legacy_rows=False)
    mints = [row for row in liquidity if str(row.get("source_event") or "").lower() == "mint"]
    indexes = _last_swap_indexes(swaps, pools)

    details: list[dict[str, Any]] = []
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    quantified = 0
    priced = 0
    for mint in sorted(mints, key=lambda row: (int(row["block_number"]), int(row["log_index"]))):
        pool_id = str(mint.get("pool_address") or "").lower()
        pool = pools.get(pool_id)
        amounts_available = mint.get("amounts_available") is True and pool is not None
        if amounts_available:
            quantified += 1
            target_amount, quote_amount = _amounts(mint, pool, target, target_decimals)
        else:
            target_amount = quote_amount = Decimal(0)

        price: Optional[Decimal] = None
        price_source = "unpriced"
        mint_ts = _event_timestamp(mint)
        index = indexes.get(pool_id)
        if amounts_available and index:
            keys, rows = index
            position = bisect.bisect_right(
                keys, (int(mint["block_number"]), int(mint["log_index"]))
            ) - 1
            if position >= 0:
                swap = rows[position]
                age = mint_ts - _event_timestamp(swap)
                if 0 <= age <= HOUR:
                    price = _swap_price(swap, pool, target, target_decimals)
                    if price is not None:
                        price_source = "prior_same_pool_swap"
        if price is not None:
            priced += 1
        target_value = target_amount * price if price is not None else None
        total_value = target_value + quote_amount if target_value is not None else None
        detail = {
            "hour_timestamp": _hour(mint_ts),
            "hour_utc": _iso(_hour(mint_ts)),
            "block_number": int(mint["block_number"]),
            "log_index": int(mint["log_index"]),
            "transaction_hash": str(mint["transaction_hash"]),
            "pool_address": pool_id,
            "version": pool.get("version") if pool else None,
            "target_amount": float(target_amount),
            "quote_weth": float(quote_amount),
            "price_weth_per_target": float(price) if price is not None else None,
            "price_source": price_source,
            "target_value_weth": float(target_value) if target_value is not None else None,
            "total_add_value_weth": float(total_value) if total_value is not None else None,
            "amounts_available": amounts_available,
        }
        details.append(detail)
        if amounts_available and total_value is not None and total_value > 0:
            grouped[detail["hour_timestamp"]].append(detail)

    features: dict[int, dict[str, Any]] = {}
    for hour, rows in grouped.items():
        target_value = sum(float(row["target_value_weth"] or 0) for row in rows)
        total_value = sum(float(row["total_add_value_weth"] or 0) for row in rows)
        by_tx: dict[str, float] = defaultdict(float)
        v3_value = 0.0
        for row in rows:
            value = float(row["total_add_value_weth"] or 0)
            by_tx[str(row["transaction_hash"])] += value
            if row["version"] == "v3":
                v3_value += value
        features[hour] = {
            "hour_timestamp": hour,
            "hour_utc": _iso(hour),
            "mint_count": len(rows),
            "add_transaction_count": len(by_tx),
            "target_inventory_share": target_value / total_value if total_value else None,
            "largest_add_tx_share": max(by_tx.values()) / total_value if total_value else None,
            "v3_add_value_share": v3_value / total_value if total_value else None,
            "target_add_value_weth": target_value,
            "total_add_value_weth": total_value,
        }

    coverage = {
        "mint_rows": len(mints),
        "quantified_mint_rows": quantified,
        "quantified_mint_row_coverage": quantified / len(mints) if mints else 0.0,
        "priced_mint_rows": priced,
        "priced_mint_row_coverage": priced / len(mints) if mints else 0.0,
        # Every Mint in this frozen dataset is priced, so row and value coverage
        # are both exact.  If a future rerun leaves any Mint unpriced, fail the
        # value-coverage gate conservatively instead of inventing its value.
        "priced_add_value_coverage": 1.0 if priced == len(mints) and quantified == len(mints) else None,
        "eligible_add_hours": len(features),
        "price_source_counts": dict(sorted(
            (source, sum(row["price_source"] == source for row in details))
            for source in {row["price_source"] for row in details}
        )),
    }
    return features, details, coverage


def _token_total_rows(output_dir: Path) -> list[dict[str, Any]]:
    rows = read_table("analysis_series", output_dir, prefer="parquet", legacy_rows=False)
    selected = [row for row in rows if row.get("scope") == "token_total"]
    selected.sort(key=lambda row: _timestamp(row["bucket_start"]))
    if not selected:
        raise ValueError(f"no token_total rows in {output_dir}")
    for previous, current in zip(selected, selected[1:]):
        if _timestamp(current["bucket_start"]) - _timestamp(previous["bucket_start"]) != HOUR:
            raise ValueError(f"non-contiguous hourly grid in {output_dir}")
    return selected


def _feature_grid(
    rows: list[dict[str, Any]], features: dict[int, dict[str, Any]], name: str
) -> list[Optional[float]]:
    return [_number(features.get(_timestamp(row["bucket_start"]), {}).get(name)) for row in rows]


def _future_return_grid(rows: list[dict[str, Any]], horizon: int = 24) -> list[Optional[float]]:
    output: list[Optional[float]] = [None] * len(rows)
    for index in range(len(rows) - horizon):
        start, end = rows[index], rows[index + horizon]
        if int(start.get("price_trade_count") or 0) <= 0 or int(end.get("price_trade_count") or 0) <= 0:
            continue
        first, last = _number(start.get("price_close")), _number(end.get("price_close"))
        if first is not None and last is not None and first > 0 and last > 0:
            output[index] = math.log(last / first)
    return output


def _paired_statistic(
    xs: list[Optional[float]], ys: list[Optional[float]]
) -> tuple[Optional[float], int]:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None, len(pairs)
    return spearman([x for x, _ in pairs], [y for _, y in pairs]), len(pairs)


def _median(values: list[Optional[float]]) -> Optional[float]:
    observed = [value for value in values if value is not None]
    return statistics.median(observed) if observed else None


def _calendar_indices(n: int, rng: random.Random, block: int = BLOCK_HOURS) -> list[int]:
    indices: list[int] = []
    while len(indices) < n:
        start = rng.randrange(n)
        indices.extend((start + offset) % n for offset in range(block))
    return indices[:n]


def _bootstrap_ci(
    statistic: Callable[[list[int]], Optional[float]], n: int, repetitions: int, seed: int
) -> tuple[Optional[float], Optional[float], int]:
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(repetitions):
        value = statistic(_calendar_indices(n, rng))
        if value is not None and math.isfinite(value):
            estimates.append(value)
    if not estimates:
        return None, None, 0
    return _percentile(estimates, 0.025), _percentile(estimates, 0.975), len(estimates)


def _blocks(values: list[Optional[float]], block: int = BLOCK_HOURS) -> list[list[Optional[float]]]:
    padded = list(values)
    remainder = len(padded) % block
    if remainder:
        padded.extend([None] * (block - remainder))
    return [padded[start:start + block] for start in range(0, len(padded), block)]


def _permutation_p_h1(
    xs: list[Optional[float]], ys: list[Optional[float]], repetitions: int, seed: int
) -> Optional[float]:
    observed, _ = _paired_statistic(xs, ys)
    blocks = _blocks(ys)
    if observed is None or len(blocks) < 2:
        return None
    rng = random.Random(seed)
    exceed = valid = 0
    for _ in range(repetitions):
        shuffled = list(blocks)
        rng.shuffle(shuffled)
        permuted = [value for block in shuffled for value in block][:len(ys)]
        value, _ = _paired_statistic(xs, permuted)
        if value is not None:
            valid += 1
            exceed += abs(value) >= abs(observed) - 1e-15
    return (exceed + 1) / (valid + 1) if valid else None


def _permutation_p_difference(
    control: list[Optional[float]], event: list[Optional[float]], repetitions: int, seed: int
) -> Optional[float]:
    control_median, event_median = _median(control), _median(event)
    if control_median is None or event_median is None:
        return None
    observed = event_median - control_median
    combined = control + event
    blocks = _blocks(combined)
    rng = random.Random(seed)
    exceed = valid = 0
    for _ in range(repetitions):
        shuffled = list(blocks)
        rng.shuffle(shuffled)
        values = [value for block in shuffled for value in block][:len(combined)]
        first, second = values[:len(control)], values[len(control):]
        first_median, second_median = _median(first), _median(second)
        if first_median is not None and second_median is not None:
            valid += 1
            exceed += abs(second_median - first_median) >= abs(observed) - 1e-15
    return (exceed + 1) / (valid + 1) if valid else None


def run_validation(
    control_dir: Path,
    event_dir: Path,
    config_path: Path,
    *,
    bootstrap_repetitions: int = 1999,
    permutation_repetitions: int = 4999,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    control_features, control_details, control_coverage = build_hour_features(control_dir, config_path)
    event_features, event_details, event_coverage = build_hour_features(event_dir, config_path)
    for row in control_details:
        row["window"] = "control"
    for row in event_details:
        row["window"] = "event"
    control_rows, event_rows = _token_total_rows(control_dir), _token_total_rows(event_dir)

    control_target = _feature_grid(control_rows, control_features, "target_inventory_share")
    event_target = _feature_grid(event_rows, event_features, "target_inventory_share")
    control_largest = _feature_grid(control_rows, control_features, "largest_add_tx_share")
    event_largest = _feature_grid(event_rows, event_features, "largest_add_tx_share")
    future_return = _future_return_grid(event_rows)

    h1_value, h1_n = _paired_statistic(event_target, future_return)
    h1_underpowered = h1_n < 30
    h1_ci = _bootstrap_ci(
        lambda indices: _paired_statistic(
            [event_target[i] for i in indices], [future_return[i] for i in indices]
        )[0],
        len(event_target), bootstrap_repetitions, _seed("H1-bootstrap"),
    ) if not h1_underpowered else (None, None, 0)
    h1_p = _permutation_p_h1(
        event_target, future_return, permutation_repetitions, _seed("H1-permutation")
    ) if not h1_underpowered else None

    tests: list[dict[str, Any]] = [{
        "test_id": "H1",
        "estimand": "event Spearman(target_inventory_share[t], future_24h_log_return)",
        "expected_direction": "negative",
        "control_n": None,
        "event_n": h1_n,
        "control_value": None,
        "event_value": h1_value,
        "effect": h1_value,
        "bootstrap_ci_low": h1_ci[0],
        "bootstrap_ci_high": h1_ci[1],
        "bootstrap_valid": h1_ci[2],
        "block_permutation_p_two_sided": h1_p,
        "underpowered": h1_underpowered,
    }]

    for test_id, name in (("H2", "target_inventory_share"), ("H3", "largest_add_tx_share")):
        control_grid = control_target if test_id == "H2" else control_largest
        event_grid = event_target if test_id == "H2" else event_largest
        control_n = sum(value is not None for value in control_grid)
        event_n = sum(value is not None for value in event_grid)
        control_value, event_value = _median(control_grid), _median(event_grid)
        effect = (
            event_value - control_value
            if event_value is not None and control_value is not None else None
        )
        underpowered = min(control_n, event_n) < 30

        def difference(indices: list[int]) -> Optional[float]:
            # Draw the two calendar windows independently while using the same
            # RNG stream; missing hours travel with their 24-hour blocks.
            split = len(control_grid)
            control_indices = indices[:split]
            event_indices = indices[split:]
            first = _median([control_grid[i % split] for i in control_indices])
            second = _median([event_grid[i % len(event_grid)] for i in event_indices])
            return second - first if first is not None and second is not None else None

        if not underpowered:
            rng = random.Random(_seed(f"{test_id}-bootstrap-indices"))
            estimates = []
            for _ in range(bootstrap_repetitions):
                ci = _calendar_indices(len(control_grid), rng) + _calendar_indices(len(event_grid), rng)
                value = difference(ci)
                if value is not None:
                    estimates.append(value)
            low = _percentile(estimates, 0.025) if estimates else None
            high = _percentile(estimates, 0.975) if estimates else None
            p_value = _permutation_p_difference(
                control_grid, event_grid, permutation_repetitions, _seed(f"{test_id}-permutation")
            )
        else:
            low = high = p_value = None
            estimates = []
        tests.append({
            "test_id": test_id,
            "estimand": f"event minus control median {name}",
            "expected_direction": "positive",
            "control_n": control_n,
            "event_n": event_n,
            "control_value": control_value,
            "event_value": event_value,
            "effect": effect,
            "bootstrap_ci_low": low,
            "bootstrap_ci_high": high,
            "bootstrap_valid": len(estimates),
            "block_permutation_p_two_sided": p_value,
            "underpowered": underpowered,
        })

    q_values = benjamini_hochberg([row["block_permutation_p_two_sided"] for row in tests])
    coverage_pass = all(
        coverage["quantified_mint_row_coverage"] >= 0.90
        and coverage["priced_add_value_coverage"] is not None
        and coverage["priced_add_value_coverage"] >= 0.80
        for coverage in (control_coverage, event_coverage)
    )
    for row, q_value in zip(tests, q_values):
        row["bh_q_primary"] = q_value
        direction = (
            row["effect"] is not None
            and (row["effect"] < 0 if row["expected_direction"] == "negative" else row["effect"] > 0)
        )
        ci_excludes_zero = (
            row["bootstrap_ci_low"] is not None
            and row["bootstrap_ci_high"] is not None
            and (row["bootstrap_ci_low"] > 0 or row["bootstrap_ci_high"] < 0)
        )
        row["direction_matches"] = direction
        row["bootstrap_ci_excludes_zero"] = ci_excludes_zero
        row["confirmatory"] = bool(
            coverage_pass and not row["underpowered"] and direction and ci_excludes_zero
            and q_value is not None and q_value < 0.05
        )

    hour_rows = []
    for window, rows, features in (
        ("control", control_rows, control_features), ("event", event_rows, event_features)
    ):
        returns = _future_return_grid(rows)
        for index, row in enumerate(rows):
            timestamp = _timestamp(row["bucket_start"])
            feature = features.get(timestamp)
            if feature:
                hour_rows.append({
                    "window": window,
                    **feature,
                    "future_24h_log_return": returns[index],
                    "price_endpoint_observed": returns[index] is not None,
                })

    summary = {
        "design": "pre-registered GALA inventory mechanism validation",
        "seed": SEED,
        "bootstrap_repetitions": bootstrap_repetitions,
        "permutation_repetitions": permutation_repetitions,
        "calendar_block_hours": BLOCK_HOURS,
        "permutation_sidedness": "two-sided",
        "control_coverage": control_coverage,
        "event_coverage": event_coverage,
        "coverage_pass": coverage_pass,
        "confirmed_hypotheses": [row["test_id"] for row in tests if row["confirmatory"]],
        "decision": (
            "advance_to_batch_validation"
            if any(row["confirmatory"] for row in tests)
            else "close_hand_selected_mechanism_line_as_unconfirmed"
        ),
    }
    return tests, summary, control_details + event_details, hour_rows


def _format(value: Any, digits: int = 4) -> str:
    return "—" if value is None else f"{float(value):.{digits}f}"


def render_summary(tests: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# GALA inventory mechanism validation",
        "",
        "This is the frozen third and final hand-selected case. Two-sided 24-hour block-permutation p-values are BH-adjusted across H1–H3; confidence intervals use 24-hour calendar moving blocks.",
        "",
        "| Test | Control n | Event n | Control | Event | Effect | 95% block CI | p | BH q | Confirmed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in tests:
        lines.append(
            "| {id} | {cn} | {en} | {control} | {event} | {effect} | [{low}, {high}] | {p} | {q} | {confirmed} |".format(
                id=row["test_id"], cn=row["control_n"] if row["control_n"] is not None else "—",
                en=row["event_n"], control=_format(row["control_value"]),
                event=_format(row["event_value"]), effect=_format(row["effect"]),
                low=_format(row["bootstrap_ci_low"]), high=_format(row["bootstrap_ci_high"]),
                p=_format(row["block_permutation_p_two_sided"]), q=_format(row["bh_q_primary"]),
                confirmed="yes" if row["confirmatory"] else "no",
            )
        )
    control = summary["control_coverage"]
    event = summary["event_coverage"]
    lines += [
        "",
        "## Coverage",
        "",
        f"- Control: {control['mint_rows']} Mint rows, {control['eligible_add_hours']} eligible add hours, {control['quantified_mint_row_coverage']:.1%} quantified, {control['priced_mint_row_coverage']:.1%} priced.",
        f"- Event: {event['mint_rows']} Mint rows, {event['eligible_add_hours']} eligible add hours, {event['quantified_mint_row_coverage']:.1%} quantified, {event['priced_mint_row_coverage']:.1%} priced.",
        f"- Frozen coverage gate: {'PASS' if summary['coverage_pass'] else 'FAIL'}.",
        "",
        "## Decision",
        "",
        f"`{summary['decision']}`",
        "",
        "A non-confirmation means this hand-selected mechanism line stops; it does not prove LP inventory behavior never matters. Confirmation advances to a broad batch validation rather than a fourth selected case.",
        "",
        "## 中文结论",
        "",
        "这是第三个、也是最后一个人工挑选案例。H1–H3 使用 24 小时日历区块 bootstrap 与双侧区块置换检验，并对三个主检验做 BH 校正。若没有主假设同时满足预设方向、q < 0.05 且置信区间不跨 0，则按预注册规则停止继续挑案例；若有确认，则下一步转向批量样本验证。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-dir", type=Path, default=Path("output-gala-control-30d"))
    parser.add_argument("--event-dir", type=Path, default=Path("output-gala-event-30d"))
    parser.add_argument("--pools-file", type=Path, default=Path("research-inputs/gala-primary-pools.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("output-gala-inventory-validation"))
    parser.add_argument("--bootstrap-repetitions", type=int, default=1999)
    parser.add_argument("--permutation-repetitions", type=int, default=4999)
    args = parser.parse_args()
    tests, summary, mint_rows, hour_rows = run_validation(
        args.control_dir, args.event_dir, args.pools_file,
        bootstrap_repetitions=args.bootstrap_repetitions,
        permutation_repetitions=args.permutation_repetitions,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(args.output_dir / "primary_tests.json", tests)
    _write_json(args.output_dir / "summary.json", summary)
    _write_csv(args.output_dir / "mint_valuations.csv", mint_rows)
    _write_csv(args.output_dir / "hourly_features.csv", hour_rows)
    markdown = render_summary(tests, summary)
    (args.output_dir / "summary.md").write_text(markdown, encoding="utf-8")
    print(markdown)


if __name__ == "__main__":
    main()
