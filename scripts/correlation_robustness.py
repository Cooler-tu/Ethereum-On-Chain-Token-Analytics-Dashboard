#!/usr/bin/env python3
"""Robustness checks for exploratory correlation and lead/lag candidates.

The utility resamples a matched analysis-series panel into coarser fixed
buckets, scans explicit lags, estimates circular-shift null p-values, applies a
global Benjamini-Hochberg false-discovery-rate correction, and adds moving-block
bootstrap confidence intervals to each bucket/pair/method's selected lag.

These checks reduce common short-series false positives. They do not establish
causality or replace validation on independent token/control cases.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.time_series_correlation import (  # noqa: E402
    _aligned,
    _feature,
    _timestamp,
    pearson,
    spearman,
)
from src.data.artifacts import read_table  # noqa: E402


Method = Callable[[list[float], list[float]], Optional[float]]
METHODS: tuple[tuple[str, Method], ...] = (
    ("pearson", pearson),
    ("spearman", spearman),
)

FLOW_FIELDS = (
    "volume_token",
    "liquidity_added_token",
    "liquidity_removed_token",
    "net_lp_flow_token",
)
COUNT_FIELDS = (
    "swap_count",
    "price_trade_count",
    "lp_add_event_count",
    "lp_remove_event_count",
)


def _number(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _sum_nullable(rows: Iterable[dict[str, Any]], field: str) -> Optional[float]:
    values = [_number(row.get(field)) for row in rows]
    present = [value for value in values if value is not None]
    return sum(present) if present else None


def _first_number(rows: Iterable[dict[str, Any]], field: str) -> Optional[float]:
    for row in rows:
        value = _number(row.get(field))
        if value is not None:
            return value
    return None


def _last_number(rows: Iterable[dict[str, Any]], field: str) -> Optional[float]:
    for row in reversed(list(rows)):
        value = _number(row.get(field))
        if value is not None:
            return value
    return None


def aggregate_rows(
    rows: list[dict[str, Any]], factor: int
) -> list[dict[str, Any]]:
    """Aggregate contiguous base rows and recompute state/flow derivatives."""
    if factor < 1:
        raise ValueError("bucket factor must be positive")
    complete = len(rows) // factor
    grouped: list[dict[str, Any]] = []
    for group_index in range(complete):
        chunk = rows[group_index * factor:(group_index + 1) * factor]
        volumes = [_number(row.get("volume_token")) or 0.0 for row in chunk]
        vwaps = [_number(row.get("price_vwap")) for row in chunk]
        vwap_weight = sum(
            volume for volume, value in zip(volumes, vwaps) if value is not None
        )
        vwap = (
            sum(
                volume * float(value)
                for volume, value in zip(volumes, vwaps) if value is not None
            ) / vwap_weight
            if vwap_weight else None
        )
        highs = [
            value for row in chunk
            if (value := _number(row.get("price_high"))) is not None
        ]
        lows = [
            value for row in chunk
            if (value := _number(row.get("price_low"))) is not None
        ]
        combined: dict[str, Any] = {
            "bucket_start": chunk[0].get("bucket_start"),
            "bucket_end": chunk[-1].get("bucket_end"),
            "bucket_seconds": sum(int(row.get("bucket_seconds") or 0) for row in chunk),
            "price_open": _first_number(chunk, "price_open"),
            "price_high": max(highs) if highs else None,
            "price_low": min(lows) if lows else None,
            "price_close": _last_number(chunk, "price_close"),
            "price_vwap": vwap,
            "tvl_token_close": _last_number(chunk, "tvl_token_close"),
        }
        for field in FLOW_FIELDS:
            combined[field] = _sum_nullable(chunk, field)
        for field in COUNT_FIELDS:
            combined[field] = int(sum(_number(row.get(field)) or 0 for row in chunk))
        grouped.append(combined)

    for index, row in enumerate(grouped):
        previous = grouped[index - 1] if index else None
        previous_price = _number(previous.get("price_close")) if previous else None
        current_price = _number(row.get("price_close"))
        previous_tvl = _number(previous.get("tvl_token_close")) if previous else None
        current_tvl = _number(row.get("tvl_token_close"))
        row["price_return"] = (
            current_price / previous_price - 1
            if current_price is not None and previous_price not in (None, 0)
            else None
        )
        row["tvl_change"] = (
            current_tvl / previous_tvl - 1
            if current_tvl is not None and previous_tvl not in (None, 0)
            else None
        )
        row["volume_turnover"] = (
            (_number(row.get("volume_token")) or 0) / previous_tvl
            if previous_tvl not in (None, 0) else None
        )
        net_lp = _number(row.get("net_lp_flow_token"))
        removed = _number(row.get("liquidity_removed_token"))
        row["net_lp_flow_ratio"] = (
            net_lp / previous_tvl
            if net_lp is not None and previous_tvl not in (None, 0) else None
        )
        row["withdrawal_ratio"] = (
            removed / previous_tvl
            if removed is not None and previous_tvl not in (None, 0) else None
        )
    return grouped


def circular_shift_p_value(
    xs: list[float], ys: list[float], method: Method
) -> Optional[float]:
    """Two-sided circular-shift test preserving each series' internal order."""
    observed = method(xs, ys)
    n = len(xs)
    if observed is None or n < 4:
        return None
    exceed = 0
    valid = 0
    for shift in range(1, n):
        shifted = ys[shift:] + ys[:shift]
        value = method(xs, shifted)
        if value is None:
            continue
        valid += 1
        if abs(value) >= abs(observed) - 1e-15:
            exceed += 1
    return (exceed + 1) / (valid + 1) if valid else None


def block_permutation_p_value(
    xs: list[float],
    ys: list[float],
    method: Method,
    *,
    repetitions: int,
    block_length: int,
    seed: int,
) -> Optional[float]:
    """Two-sided random block-permutation test with finer p-value resolution."""
    observed = method(xs, ys)
    n = len(xs)
    if observed is None or n < 4 or repetitions < 1:
        return None
    block = max(1, min(int(block_length), n))
    blocks = [ys[start:start + block] for start in range(0, n, block)]
    if len(blocks) < 2:
        return None
    rng = random.Random(seed)
    exceed = 0
    valid = 0
    order = list(range(len(blocks)))
    for _ in range(repetitions):
        shuffled = list(order)
        rng.shuffle(shuffled)
        permuted = [value for index in shuffled for value in blocks[index]][:n]
        value = method(xs, permuted)
        if value is None:
            continue
        valid += 1
        if abs(value) >= abs(observed) - 1e-15:
            exceed += 1
    return (exceed + 1) / (valid + 1) if valid else None


def benjamini_hochberg(p_values: list[Optional[float]]) -> list[Optional[float]]:
    """Return monotone BH q-values while preserving original positions."""
    indexed = [
        (index, float(value))
        for index, value in enumerate(p_values) if value is not None
    ]
    indexed.sort(key=lambda item: item[1])
    total = len(indexed)
    output: list[Optional[float]] = [None] * len(p_values)
    running = 1.0
    for rank_index in range(total - 1, -1, -1):
        original, value = indexed[rank_index]
        rank = rank_index + 1
        running = min(running, value * total / rank)
        output[original] = min(1.0, running)
    return output


def _percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires values")
    position = (len(ordered) - 1) * probability
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def moving_block_bootstrap_ci(
    xs: list[float],
    ys: list[float],
    method: Method,
    *,
    repetitions: int,
    alpha: float,
    block_length: int,
    seed: int,
) -> tuple[Optional[float], Optional[float], int]:
    """Percentile CI from paired circular moving-block bootstrap samples."""
    n = len(xs)
    if n < 4 or repetitions < 1:
        return None, None, 0
    block = max(1, min(int(block_length), n))
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(repetitions):
        indices: list[int] = []
        while len(indices) < n:
            start = rng.randrange(n)
            indices.extend((start + offset) % n for offset in range(block))
        indices = indices[:n]
        value = method([xs[i] for i in indices], [ys[i] for i in indices])
        if value is not None:
            estimates.append(value)
    if not estimates:
        return None, None, 0
    return (
        _percentile(estimates, alpha / 2),
        _percentile(estimates, 1 - alpha / 2),
        len(estimates),
    )


def scan_tests(
    variants: dict[int, list[dict[str, Any]]],
    features: tuple[str, ...],
    *,
    max_horizon_base_buckets: int,
    min_pairs: int,
    permutation_repetitions: int,
    permutation_block_length: int,
    seed: int,
) -> list[dict[str, Any]]:
    tests: list[dict[str, Any]] = []
    for factor, rows in sorted(variants.items()):
        max_lag = max_horizon_base_buckets // factor
        bucket_seconds = int(rows[0].get("bucket_seconds") or 0) if rows else 0
        for index, x_name in enumerate(features):
            for y_name in features[index + 1:]:
                for method_name, method in METHODS:
                    for lag in range(-max_lag, max_lag + 1):
                        xs, ys = _aligned(rows, x_name, y_name, lag)
                        correlation = (
                            method(xs, ys) if len(xs) >= min_pairs else None
                        )
                        effective_block = (
                            permutation_block_length
                            or max(2, round(len(xs) ** (1 / 3)))
                        )
                        digest = hashlib.sha256(
                            "perm:{}:{}:{}:{}:{}".format(
                                seed, factor, x_name, y_name,
                                "{}:{}".format(method_name, lag),
                            ).encode("utf-8")
                        ).digest()
                        p_value = (
                            block_permutation_p_value(
                                xs, ys, method,
                                repetitions=permutation_repetitions,
                                block_length=effective_block,
                                seed=int.from_bytes(digest[:8], "big"),
                            )
                            if correlation is not None else None
                        )
                        tests.append({
                            "bucket_factor": factor,
                            "bucket_seconds": bucket_seconds,
                            "bucket_count": len(rows),
                            "x": x_name,
                            "y": y_name,
                            "method": method_name,
                            "lag": lag,
                            "lag_seconds": lag * bucket_seconds,
                            "correlation": correlation,
                            "n": len(xs),
                            "permutation_block_length": effective_block,
                            "p_value_block_permutation": p_value,
                        })
    q_values = benjamini_hochberg([
        row.get("p_value_block_permutation") for row in tests
    ])
    for row, q_value in zip(tests, q_values):
        row["q_value_bh_global"] = q_value
    for family_name, predicate in (
        ("zero_lag", lambda row: int(row["lag"]) == 0),
        ("lead_lag", lambda row: int(row["lag"]) != 0),
    ):
        family_indices = [index for index, row in enumerate(tests) if predicate(row)]
        family_q = benjamini_hochberg([
            tests[index].get("p_value_block_permutation")
            for index in family_indices
        ])
        key = "q_value_bh_{}_family".format(family_name)
        for index, q_value in zip(family_indices, family_q):
            tests[index][key] = q_value
    return tests


def select_best_tests(
    tests: list[dict[str, Any]],
    variants: dict[int, list[dict[str, Any]]],
    *,
    bootstrap_repetitions: int,
    alpha: float,
    block_length: int,
    seed: int,
) -> list[dict[str, Any]]:
    groups: dict[tuple[int, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in tests:
        if row.get("correlation") is not None:
            groups[(row["bucket_factor"], row["x"], row["y"], row["method"])].append(row)
    output: list[dict[str, Any]] = []
    method_map = dict(METHODS)
    for key, candidates in sorted(groups.items()):
        factor, x_name, y_name, method_name = key
        best = dict(max(candidates, key=lambda row: abs(row["correlation"])))
        xs, ys = _aligned(variants[factor], x_name, y_name, int(best["lag"]))
        effective_block = block_length or max(2, round(len(xs) ** (1 / 3)))
        digest = hashlib.sha256(
            "{}:{}:{}:{}:{}".format(seed, *key).encode("utf-8")
        ).digest()
        row_seed = int.from_bytes(digest[:8], "big")
        low, high, valid = moving_block_bootstrap_ci(
            xs, ys, method_map[method_name],
            repetitions=bootstrap_repetitions,
            alpha=alpha,
            block_length=effective_block,
            seed=row_seed,
        )
        best.update({
            "bootstrap_ci_low": low,
            "bootstrap_ci_high": high,
            "bootstrap_valid_repetitions": valid,
            "bootstrap_block_length": effective_block,
            "ci_excludes_zero": (
                low is not None and high is not None and (low > 0 or high < 0)
            ),
            "fdr_significant_global": (
                best.get("q_value_bh_global") is not None
                and float(best["q_value_bh_global"]) <= alpha
            ),
            "low_power": len(xs) < 20,
        })
        family_q_key = (
            "q_value_bh_zero_lag_family"
            if int(best["lag"]) == 0
            else "q_value_bh_lead_lag_family"
        )
        best["q_value_bh_selected_family"] = best.get(family_q_key)
        best["fdr_significant_family"] = (
            best.get(family_q_key) is not None
            and float(best[family_q_key]) <= alpha
        )
        output.append(best)
    return output


def build_stability_rows(best_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in best_rows:
        groups[(row["x"], row["y"], row["method"])].append(row)
    output: list[dict[str, Any]] = []
    for (x_name, y_name, method), rows in sorted(groups.items()):
        signs = [1 if row["correlation"] > 0 else -1 for row in rows]
        positive_leads = sum(int(row["lag"]) > 0 for row in rows)
        negative_leads = sum(int(row["lag"]) < 0 for row in rows)
        output.append({
            "x": x_name,
            "y": y_name,
            "method": method,
            "bucket_variants": len(rows),
            "same_correlation_sign_all_buckets": len(set(signs)) == 1,
            "positive_lag_variants": positive_leads,
            "negative_lag_variants": negative_leads,
            "zero_lag_variants": len(rows) - positive_leads - negative_leads,
            "ci_excludes_zero_variants": sum(bool(row["ci_excludes_zero"]) for row in rows),
            "fdr_significant_family_variants": sum(
                bool(row["fdr_significant_family"]) for row in rows
            ),
            "fdr_significant_global_variants": sum(
                bool(row["fdr_significant_global"]) for row in rows
            ),
            "correlation_min": min(row["correlation"] for row in rows),
            "correlation_max": max(row["correlation"] for row in rows),
            "lags_seconds": ";".join(str(row["lag_seconds"]) for row in rows),
        })
    return output


def _format(value: Any) -> str:
    return "—" if value is None else "{:.4f}".format(float(value))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
    tmp.replace(path)


def write_summary(
    path: Path,
    *,
    scope_label: str,
    base_bucket_seconds: int,
    factors: tuple[int, ...],
    features: tuple[str, ...],
    tests: list[dict[str, Any]],
    best_rows: list[dict[str, Any]],
    alpha: float,
) -> None:
    valid_tests = [row for row in tests if row.get("correlation") is not None]
    significant = [
        row for row in valid_tests
        if row.get("q_value_bh_global") is not None
        and float(row["q_value_bh_global"]) <= alpha
    ]
    zero_lag = [row for row in valid_tests if int(row["lag"]) == 0]
    lead_lag = [row for row in valid_tests if int(row["lag"]) != 0]
    zero_significant = [
        row for row in zero_lag
        if row.get("q_value_bh_zero_lag_family") is not None
        and float(row["q_value_bh_zero_lag_family"]) <= alpha
    ]
    lead_significant = [
        row for row in lead_lag
        if row.get("q_value_bh_lead_lag_family") is not None
        and float(row["q_value_bh_lead_lag_family"]) <= alpha
    ]
    ranked = sorted(
        best_rows,
        key=lambda row: (
            row.get("q_value_bh_global") is None,
            row.get("q_value_bh_global") or 1,
            -abs(row["correlation"]),
        ),
    )
    lines = [
        "# Correlation robustness audit",
        "",
        "- Scope: `{}`".format(scope_label),
        "- Base bucket seconds: `{}`".format(base_bucket_seconds),
        "- Bucket factors: `{}`".format(", ".join(map(str, factors))),
        "- Features: `{}`".format(", ".join(features)),
        "- Valid lag tests: `{}`".format(len(valid_tests)),
        "- Global BH-FDR threshold: `{}`".format(alpha),
        "- Tests surviving global BH-FDR: `{}`".format(len(significant)),
        "- Zero-lag family BH-FDR: `{}/{}`".format(len(zero_significant), len(zero_lag)),
        "- Exploratory lead-lag family BH-FDR: `{}/{}`".format(len(lead_significant), len(lead_lag)),
        "- Null test: two-sided block permutation; CI: paired moving-block bootstrap.",
        "",
        "## Best lag per bucket / feature pair",
        "",
        "| Bucket | X | Y | Method | Lag | Correlation | 95% CI | Block p | Family q | Global q | Verdict | N |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|",
    ]
    for row in ranked:
        verdict_parts = []
        if row["ci_excludes_zero"]:
            verdict_parts.append("CI excludes 0")
        if row["fdr_significant_family"]:
            verdict_parts.append("family FDR pass")
        if row["fdr_significant_global"]:
            verdict_parts.append("global FDR pass")
        if row["low_power"]:
            verdict_parts.append("low power")
        verdict = ", ".join(verdict_parts) or "exploratory"
        lines.append(
            "| {bucket}s | {x} | {y} | {method} | {lag} | {corr} | [{low}, {high}] | {p} | {family_q} | {global_q} | {verdict} | {n} |".format(
                bucket=row["bucket_seconds"], x=row["x"], y=row["y"],
                method=row["method"], lag=row["lag"], corr=_format(row["correlation"]),
                low=_format(row.get("bootstrap_ci_low")), high=_format(row.get("bootstrap_ci_high")),
                p=_format(row.get("p_value_block_permutation")),
                family_q=_format(row.get("q_value_bh_selected_family")),
                global_q=_format(row.get("q_value_bh_global")),
                verdict=verdict, n=row["n"],
            )
        )
    lines.extend([
        "",
        "## Interpretation guardrails",
        "",
        "- Selecting the largest absolute lag is exploratory; the global BH correction covers all tested feature pairs, lags, methods, and bucket variants in this run.",
        "- Block permutation and moving-block bootstrap retain short-range dependence better than iid resampling. Neither corrects unmeasured confounding.",
        "- Coarse variants with fewer than 20 aligned observations are labelled low power even if their point estimate is large.",
        "- Stability requires direction and plausible horizon to persist across bucket sizes, not merely one significant cell.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def _parse_ints(value: str) -> tuple[int, ...]:
    result = tuple(sorted({int(item.strip()) for item in value.split(",") if item.strip()}))
    if not result or result[0] < 1:
        raise ValueError("bucket factors must be positive integers")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bootstrap/FDR/multi-bucket robustness for analysis_series"
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--scope", choices=("pool", "token_total"), default="pool")
    parser.add_argument("--pool", default="")
    parser.add_argument("--features", required=True)
    parser.add_argument("--bucket-factors", default="1,2,3")
    parser.add_argument("--max-horizon-base-buckets", type=int, default=3)
    parser.add_argument("--min-pairs", type=int, default=8)
    parser.add_argument("--bootstrap-repetitions", type=int, default=1000)
    parser.add_argument("--bootstrap-block-length", type=int, default=0)
    parser.add_argument("--permutation-repetitions", type=int, default=999)
    parser.add_argument("--permutation-block-length", type=int, default=0)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260824)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    if args.scope == "pool" and not args.pool:
        parser.error("--pool is required when --scope pool")
    if args.max_horizon_base_buckets < 0:
        parser.error("--max-horizon-base-buckets must be non-negative")
    if args.min_pairs < 4:
        parser.error("--min-pairs must be at least 4")
    if args.bootstrap_repetitions < 100:
        parser.error("--bootstrap-repetitions must be at least 100")
    if args.permutation_repetitions < 100:
        parser.error("--permutation-repetitions must be at least 100")
    if not 0 < args.alpha < 1:
        parser.error("--alpha must be between zero and one")
    try:
        factors = _parse_ints(args.bucket_factors)
    except ValueError as exc:
        parser.error(str(exc))
    features = tuple(item.strip() for item in args.features.split(",") if item.strip())
    if len(features) < 2:
        parser.error("at least two features are required")

    source = Path(args.output_dir)
    pool = args.pool.lower()
    rows = read_table("analysis_series", source, prefer="parquet", legacy_rows=False)
    selected = [
        row for row in rows
        if row.get("scope") == args.scope
        and (args.scope != "pool" or str(row.get("pool_identifier") or "").lower() == pool)
    ]
    selected.sort(key=lambda row: _timestamp(row.get("bucket_start")))
    if not selected:
        parser.error("no analysis-series rows matched scope/pool")
    base_bucket_seconds = int(selected[0].get("bucket_seconds") or 0)
    for previous, current in zip(selected, selected[1:]):
        if base_bucket_seconds and (
            _timestamp(current.get("bucket_start"))
            - _timestamp(previous.get("bucket_start")) != base_bucket_seconds
        ):
            parser.error("selected rows are not a contiguous fixed-bucket series")

    variants = {factor: aggregate_rows(selected, factor) for factor in factors}
    variants = {
        factor: rows for factor, rows in variants.items()
        if len(rows) >= args.min_pairs
    }
    if not variants:
        parser.error("no bucket variant retains the minimum number of rows")
    tests = scan_tests(
        variants, features,
        max_horizon_base_buckets=args.max_horizon_base_buckets,
        min_pairs=args.min_pairs,
        permutation_repetitions=args.permutation_repetitions,
        permutation_block_length=args.permutation_block_length,
        seed=args.seed,
    )
    best = select_best_tests(
        tests, variants,
        bootstrap_repetitions=args.bootstrap_repetitions,
        alpha=args.alpha,
        block_length=args.bootstrap_block_length,
        seed=args.seed,
    )
    stability = build_stability_rows(best)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    _write_csv(out / "all_lag_tests.csv", tests)
    _write_csv(out / "best_lag_by_bucket.csv", best)
    _write_csv(out / "stability_by_pair.csv", stability)
    scope_label = pool if args.scope == "pool" else "token_total"
    write_summary(
        out / "summary.md",
        scope_label=scope_label,
        base_bucket_seconds=base_bucket_seconds,
        factors=tuple(variants),
        features=features,
        tests=tests,
        best_rows=best,
        alpha=args.alpha,
    )
    _write_json(out / "results.json", {
        "scope": args.scope,
        "pool": pool or None,
        "base_bucket_seconds": base_bucket_seconds,
        "bucket_factors": list(variants),
        "features": list(features),
        "max_horizon_base_buckets": args.max_horizon_base_buckets,
        "min_pairs": args.min_pairs,
        "bootstrap_repetitions": args.bootstrap_repetitions,
        "permutation_repetitions": args.permutation_repetitions,
        "alpha": args.alpha,
        "test_count": len(tests),
        "valid_test_count": sum(row.get("correlation") is not None for row in tests),
        "global_fdr_significant_count": sum(
            row.get("q_value_bh_global") is not None
            and float(row["q_value_bh_global"]) <= args.alpha
            for row in tests
        ),
        "zero_lag_family_fdr_significant_count": sum(
            row.get("q_value_bh_zero_lag_family") is not None
            and float(row["q_value_bh_zero_lag_family"]) <= args.alpha
            for row in tests
        ),
        "lead_lag_family_fdr_significant_count": sum(
            row.get("q_value_bh_lead_lag_family") is not None
            and float(row["q_value_bh_lead_lag_family"]) <= args.alpha
            for row in tests
        ),
        "best_lag_by_bucket": best,
        "stability_by_pair": stability,
    })
    print("Analyzed {} base buckets for {}".format(len(selected), scope_label))
    print("Bucket variants:", ", ".join(
        "{}×={} rows".format(factor, len(rows)) for factor, rows in variants.items()
    ))
    print("Saved:", out / "summary.md")


if __name__ == "__main__":
    main()
