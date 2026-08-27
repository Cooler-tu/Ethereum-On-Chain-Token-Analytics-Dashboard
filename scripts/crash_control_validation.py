#!/usr/bin/env python3
"""Pre-registered same-token crash/control correlation validation.

The primary design compares three hourly liquidity/flow predictors with an
observed-price 24-hour token return in a frozen control window and crash window.
It deliberately avoids a lag search: secondary horizons, methods, and bucket
sizes are written separately and remain exploratory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.correlation_robustness import (  # noqa: E402
    aggregate_rows,
    benjamini_hochberg,
    block_permutation_p_value,
    moving_block_bootstrap_ci,
    _percentile,
)
from scripts.time_series_correlation import pearson, spearman, _timestamp  # noqa: E402
from src.data.artifacts import read_table  # noqa: E402


Method = Callable[[list[float], list[float]], Optional[float]]
PRIMARY_TESTS = (
    ("pool_transfer_net", "actual_transfer_net_ratio", False, "negative"),
    ("net_lp_flow", "net_lp_flow_ratio", False, "positive"),
    ("gross_lp_activity", "gross_lp_activity_ratio", True, "positive"),
)


def _number(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _seed(base: int, label: str) -> int:
    digest = hashlib.sha256(f"{base}:{label}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def select_token_total_rows(output_dir: Path) -> list[dict[str, Any]]:
    rows = read_table("analysis_series", output_dir, prefer="parquet", legacy_rows=False)
    selected = [row for row in rows if row.get("scope") == "token_total"]
    selected.sort(key=lambda row: _timestamp(row.get("bucket_start")))
    if not selected:
        raise ValueError(f"no token_total analysis-series rows in {output_dir}")
    seconds = int(selected[0].get("bucket_seconds") or 0)
    if seconds <= 0:
        raise ValueError(f"invalid bucket size in {output_dir}")
    for previous, current in zip(selected, selected[1:]):
        gap = _timestamp(current.get("bucket_start")) - _timestamp(previous.get("bucket_start"))
        if gap != seconds:
            raise ValueError(f"analysis series is not contiguous in {output_dir}")
    return selected


def build_future_return_pairs(
    rows: list[dict[str, Any]],
    predictor: str,
    horizon_buckets: int,
    *,
    absolute_outcome: bool,
) -> tuple[list[float], list[float], list[int]]:
    """Pair X[t] with log(P[t+h]/P[t]) using observed endpoints only."""
    if horizon_buckets < 1:
        raise ValueError("horizon_buckets must be positive")
    xs: list[float] = []
    ys: list[float] = []
    timestamps: list[int] = []
    for index in range(0, len(rows) - horizon_buckets):
        start = rows[index]
        end = rows[index + horizon_buckets]
        if int(start.get("price_trade_count") or 0) <= 0:
            continue
        if int(end.get("price_trade_count") or 0) <= 0:
            continue
        x = _number(start.get(predictor))
        start_price = _number(start.get("price_close"))
        end_price = _number(end.get("price_close"))
        if x is None or start_price is None or end_price is None:
            continue
        if start_price <= 0 or end_price <= 0:
            continue
        outcome = math.log(end_price / start_price)
        xs.append(x)
        ys.append(abs(outcome) if absolute_outcome else outcome)
        timestamps.append(_timestamp(start.get("bucket_start")))
    return xs, ys, timestamps


def independent_moving_block_difference_ci(
    crash_xs: list[float],
    crash_ys: list[float],
    control_xs: list[float],
    control_ys: list[float],
    method: Method,
    *,
    repetitions: int,
    alpha: float,
    block_length: int,
    seed: int,
) -> tuple[Optional[float], Optional[float], int]:
    """Bootstrap crash-control correlation differences independently by window."""
    if min(len(crash_xs), len(control_xs)) < 4 or repetitions < 1:
        return None, None, 0
    rng = random.Random(seed)
    estimates: list[float] = []

    def indices(n: int) -> list[int]:
        block = max(1, min(int(block_length), n))
        sampled: list[int] = []
        while len(sampled) < n:
            start = rng.randrange(n)
            sampled.extend((start + offset) % n for offset in range(block))
        return sampled[:n]

    for _ in range(repetitions):
        crash_indices = indices(len(crash_xs))
        control_indices = indices(len(control_xs))
        crash_value = method(
            [crash_xs[i] for i in crash_indices],
            [crash_ys[i] for i in crash_indices],
        )
        control_value = method(
            [control_xs[i] for i in control_indices],
            [control_ys[i] for i in control_indices],
        )
        if crash_value is not None and control_value is not None:
            estimates.append(crash_value - control_value)
    if not estimates:
        return None, None, 0
    return (
        _percentile(estimates, alpha / 2),
        _percentile(estimates, 1 - alpha / 2),
        len(estimates),
    )


def coverage(output_dir: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    liquidity = read_table("liquidity_events", output_dir, prefer="parquet", legacy_rows=False)
    lp_events = [
        row for row in liquidity
        if str(row.get("source_event") or "").lower() in {"mint", "burn"}
    ]
    quantified = [row for row in lp_events if row.get("amounts_available") is True]
    reserve_rows = sum(_number(row.get("tvl_token_close")) is not None for row in rows)
    return {
        "hourly_rows": len(rows),
        "observed_price_rows": sum(int(row.get("price_trade_count") or 0) > 0 for row in rows),
        "reserve_rows": reserve_rows,
        "reserve_coverage": reserve_rows / len(rows) if rows else 0.0,
        "lp_events": len(lp_events),
        "quantified_lp_events": len(quantified),
        "lp_amount_coverage": len(quantified) / len(lp_events) if lp_events else 0.0,
    }


def _ci_excludes_zero(low: Optional[float], high: Optional[float]) -> bool:
    return low is not None and high is not None and (low > 0 or high < 0)


def _direction_matches(value: Optional[float], expected: str) -> bool:
    if value is None:
        return False
    return value < 0 if expected == "negative" else value > 0


def run_primary(
    control_rows: list[dict[str, Any]],
    crash_rows: list[dict[str, Any]],
    *,
    min_pairs: int,
    repetitions: int,
    permutation_repetitions: int,
    alpha: float,
    block_length: int,
    seed: int,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for test_id, predictor, absolute_outcome, expected in PRIMARY_TESTS:
        control_xs, control_ys, _ = build_future_return_pairs(
            control_rows, predictor, 24, absolute_outcome=absolute_outcome
        )
        crash_xs, crash_ys, _ = build_future_return_pairs(
            crash_rows, predictor, 24, absolute_outcome=absolute_outcome
        )
        underpowered = min(len(control_xs), len(crash_xs)) < min_pairs
        control_corr = spearman(control_xs, control_ys) if not underpowered else None
        crash_corr = spearman(crash_xs, crash_ys) if not underpowered else None
        control_low, control_high, control_valid = moving_block_bootstrap_ci(
            control_xs, control_ys, spearman,
            repetitions=repetitions, alpha=alpha, block_length=block_length,
            seed=_seed(seed, f"{test_id}:control"),
        ) if not underpowered else (None, None, 0)
        crash_low, crash_high, crash_valid = moving_block_bootstrap_ci(
            crash_xs, crash_ys, spearman,
            repetitions=repetitions, alpha=alpha, block_length=block_length,
            seed=_seed(seed, f"{test_id}:crash"),
        ) if not underpowered else (None, None, 0)
        permutation_p = block_permutation_p_value(
            crash_xs, crash_ys, spearman,
            repetitions=permutation_repetitions,
            block_length=block_length,
            seed=_seed(seed, f"{test_id}:permutation"),
        ) if not underpowered else None
        difference = (
            crash_corr - control_corr
            if crash_corr is not None and control_corr is not None else None
        )
        difference_low, difference_high, difference_valid = (
            independent_moving_block_difference_ci(
                crash_xs, crash_ys, control_xs, control_ys, spearman,
                repetitions=repetitions, alpha=alpha, block_length=block_length,
                seed=_seed(seed, f"{test_id}:difference"),
            ) if not underpowered else (None, None, 0)
        )
        output.append({
            "test_id": test_id,
            "predictor": predictor,
            "outcome": "future_abs_log_return" if absolute_outcome else "future_log_return",
            "horizon_hours": 24,
            "bucket_hours": 1,
            "method": "spearman",
            "expected_direction": expected,
            "control_n": len(control_xs),
            "control_correlation": control_corr,
            "control_ci_low": control_low,
            "control_ci_high": control_high,
            "control_bootstrap_valid": control_valid,
            "crash_n": len(crash_xs),
            "crash_correlation": crash_corr,
            "crash_ci_low": crash_low,
            "crash_ci_high": crash_high,
            "crash_bootstrap_valid": crash_valid,
            "crash_block_permutation_p": permutation_p,
            "difference_crash_minus_control": difference,
            "difference_ci_low": difference_low,
            "difference_ci_high": difference_high,
            "difference_bootstrap_valid": difference_valid,
            "block_length_paired_observations": block_length,
            "underpowered": underpowered,
        })
    q_values = benjamini_hochberg([
        row.get("crash_block_permutation_p") for row in output
    ])
    for row, q_value in zip(output, q_values):
        row["crash_q_value_bh_primary"] = q_value
        row["direction_matches"] = _direction_matches(
            row.get("crash_correlation"), str(row["expected_direction"])
        )
        row["crash_ci_excludes_zero"] = _ci_excludes_zero(
            row.get("crash_ci_low"), row.get("crash_ci_high")
        )
        row["difference_ci_excludes_zero"] = _ci_excludes_zero(
            row.get("difference_ci_low"), row.get("difference_ci_high")
        )
        row["confirmatory"] = bool(
            not row["underpowered"]
            and row["direction_matches"]
            and row["crash_ci_excludes_zero"]
            and q_value is not None and q_value < alpha
            and row["difference_ci_excludes_zero"]
        )
    return output


def run_secondary(
    control_rows: list[dict[str, Any]], crash_rows: list[dict[str, Any]], *, min_pairs: int
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    methods: tuple[tuple[str, Method], ...] = (("spearman", spearman), ("pearson", pearson))
    for factor in (1, 6, 12, 24):
        control_variant = control_rows if factor == 1 else aggregate_rows(control_rows, factor)
        crash_variant = crash_rows if factor == 1 else aggregate_rows(crash_rows, factor)
        for horizon_hours in (24, 48, 72):
            horizon_buckets = horizon_hours // factor
            for test_id, predictor, absolute_outcome, expected in PRIMARY_TESTS:
                for method_name, method in methods:
                    if factor == 1 and horizon_hours == 24 and method_name == "spearman":
                        continue
                    control_xs, control_ys, _ = build_future_return_pairs(
                        control_variant, predictor, horizon_buckets,
                        absolute_outcome=absolute_outcome,
                    )
                    crash_xs, crash_ys, _ = build_future_return_pairs(
                        crash_variant, predictor, horizon_buckets,
                        absolute_outcome=absolute_outcome,
                    )
                    control_corr = method(control_xs, control_ys) if len(control_xs) >= 3 else None
                    crash_corr = method(crash_xs, crash_ys) if len(crash_xs) >= 3 else None
                    output.append({
                        "test_id": test_id,
                        "predictor": predictor,
                        "outcome": "future_abs_log_return" if absolute_outcome else "future_log_return",
                        "expected_direction": expected,
                        "bucket_hours": factor,
                        "horizon_hours": horizon_hours,
                        "method": method_name,
                        "control_n": len(control_xs),
                        "control_correlation": control_corr,
                        "crash_n": len(crash_xs),
                        "crash_correlation": crash_corr,
                        "difference_crash_minus_control": (
                            crash_corr - control_corr
                            if crash_corr is not None and control_corr is not None else None
                        ),
                        "below_primary_min_pairs": min(len(control_xs), len(crash_xs)) < min_pairs,
                        "exploratory_only": True,
                    })
    return output


def _format(value: Any) -> str:
    if value is None:
        return "—"
    return f"{float(value):.4f}"


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = sorted({key for row in rows for key in row})
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(
    path: Path,
    primary: list[dict[str, Any]],
    coverage_rows: dict[str, dict[str, Any]],
    *,
    alpha: float,
    min_pairs: int,
    block_length: int,
    study_label: str,
    pool_count: int,
) -> None:
    passed = [row for row in primary if row["confirmatory"]]
    lines = [
        f"# {study_label} crash/control validation",
        "",
        f"- Confirmatory primary tests: **{len(passed)}/{len(primary)}**.",
        "- Primary design: hourly predictors vs observed-endpoint future 24h return; Spearman correlation.",
        f"- Dependence handling: {block_length}-paired-observation moving-block bootstrap and block permutation.",
        f"- Multiplicity: BH-FDR across the three crash-window primary tests at q < {alpha}.",
        f"- Minimum paired observations: {min_pairs} per window.",
        "",
        "## Data quality",
        "",
        "| Window | Hourly rows | Observed price rows | Reserve coverage | Quantified Mint/Burn |",
        "|---|---:|---:|---:|---:|",
    ]
    for label in ("control", "crash"):
        row = coverage_rows[label]
        lines.append(
            "| {label} | {hourly_rows} | {observed_price_rows} | {reserve:.1%} | {quantified}/{events} ({coverage:.1%}) |".format(
                label=label.title(), hourly_rows=row["hourly_rows"],
                observed_price_rows=row["observed_price_rows"],
                reserve=row["reserve_coverage"], quantified=row["quantified_lp_events"],
                events=row["lp_events"], coverage=row["lp_amount_coverage"],
            )
        )
    lines.extend([
        "",
        "All return pairs require an actual trade in both endpoint buckets; carried-forward-only prices are excluded.",
        "",
        "## Primary tests",
        "",
        "| Predictor | Expected | Control ρ [95% CI] | Crash ρ [95% CI] | Crash p / BH q | Crash−control [95% CI] | Verdict | N control/crash |",
        "|---|---|---:|---:|---:|---:|---|---:|",
    ])
    for row in primary:
        verdict = "CONFIRMATORY" if row["confirmatory"] else "not confirmed"
        if row["underpowered"]:
            verdict = "underpowered"
        lines.append(
            "| {predictor} | {direction} | {control} [{cl}, {ch}] | {crash} [{xl}, {xh}] | {p} / {q} | {diff} [{dl}, {dh}] | {verdict} | {cn}/{xn} |".format(
                predictor=row["predictor"], direction=row["expected_direction"],
                control=_format(row["control_correlation"]), cl=_format(row["control_ci_low"]), ch=_format(row["control_ci_high"]),
                crash=_format(row["crash_correlation"]), xl=_format(row["crash_ci_low"]), xh=_format(row["crash_ci_high"]),
                p=_format(row["crash_block_permutation_p"]), q=_format(row["crash_q_value_bh_primary"]),
                diff=_format(row["difference_crash_minus_control"]), dl=_format(row["difference_ci_low"]), dh=_format(row["difference_ci_high"]),
                verdict=verdict, cn=row["control_n"], xn=row["crash_n"],
            )
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "A primary hypothesis is confirmed only when the crash association has the frozen direction, its bootstrap CI excludes zero, its crash permutation p-value survives the three-test BH correction, and the crash-minus-control bootstrap CI excludes zero.",
        "",
        f"This is an Ethereum Uniswap study of {pool_count} pre-selected {study_label}/WETH pool(s). It does not observe complete centralized-venue order flow and does not establish causality. Secondary horizons, Pearson results, and coarser buckets are saved separately and must not be promoted to confirmatory findings.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a frozen same-token crash/control validation")
    parser.add_argument("--control-dir", required=True)
    parser.add_argument("--crash-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--study-label", default="", help="Token label for the report")
    parser.add_argument("--min-pairs", type=int, default=80)
    parser.add_argument("--bootstrap-repetitions", type=int, default=1999)
    parser.add_argument("--permutation-repetitions", type=int, default=4999)
    parser.add_argument("--block-length", type=int, default=24)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260824)
    args = parser.parse_args()
    if args.min_pairs < 3 or args.block_length < 1:
        parser.error("--min-pairs must be >= 3 and --block-length must be >= 1")

    control_dir = Path(args.control_dir)
    crash_dir = Path(args.crash_dir)
    control_profile = json.loads((control_dir / "token_profile.json").read_text(encoding="utf-8"))
    crash_profile = json.loads((crash_dir / "token_profile.json").read_text(encoding="utf-8"))
    control_address = str(control_profile.get("address") or "").lower()
    crash_address = str(crash_profile.get("address") or "").lower()
    if not control_address or control_address != crash_address:
        parser.error("control and crash directories must contain the same token address")
    study_label = args.study_label.strip() or str(crash_profile.get("symbol") or "token")
    verified_pools = json.loads((crash_dir / "verified_pools.json").read_text(encoding="utf-8"))
    pool_count = sum(bool(row.get("verified", True)) for row in verified_pools)
    control_rows = select_token_total_rows(control_dir)
    crash_rows = select_token_total_rows(crash_dir)
    coverage_rows = {
        "control": coverage(control_dir, control_rows),
        "crash": coverage(crash_dir, crash_rows),
    }
    failures = []
    for label, row in coverage_rows.items():
        if row["reserve_coverage"] < 0.90:
            failures.append(f"{label} reserve coverage below 90%")
        if row["lp_amount_coverage"] < 0.90:
            failures.append(f"{label} LP amount coverage below 90%")
    if failures:
        parser.error("; ".join(failures))

    primary = run_primary(
        control_rows, crash_rows, min_pairs=args.min_pairs,
        repetitions=args.bootstrap_repetitions,
        permutation_repetitions=args.permutation_repetitions,
        alpha=args.alpha, block_length=args.block_length, seed=args.seed,
    )
    secondary = run_secondary(control_rows, crash_rows, min_pairs=args.min_pairs)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    _write_csv(out / "primary_tests.csv", primary)
    _write_csv(out / "secondary_tests.csv", secondary)
    (out / "results.json").write_text(json.dumps({
        "design": {
            "study_label": study_label,
            "token_address": crash_address,
            "pool_count": pool_count,
            "primary_horizon_hours": 24,
            "primary_method": "spearman",
            "observed_price_endpoints_only": True,
            "bootstrap_repetitions": args.bootstrap_repetitions,
            "permutation_repetitions": args.permutation_repetitions,
            "block_length_paired_observations": args.block_length,
            "alpha": args.alpha,
            "min_pairs": args.min_pairs,
            "seed": args.seed,
        },
        "coverage": coverage_rows,
        "primary": primary,
        "secondary": secondary,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    write_summary(
        out / "summary.md", primary, coverage_rows,
        alpha=args.alpha, min_pairs=args.min_pairs, block_length=args.block_length,
        study_label=study_label, pool_count=pool_count,
    )
    print(f"Wrote {out / 'summary.md'}")
    print(f"Confirmatory primary tests: {sum(row['confirmatory'] for row in primary)}/{len(primary)}")


if __name__ == "__main__":
    main()
