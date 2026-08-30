#!/usr/bin/env python3
"""Build one exploratory evidence ledger across FTT, CEL, and GALA windows.

The ledger applies one fixed 1-hour/24-hour/Spearman specification to all six
existing windows.  It is a synthesis, not a new confirmation: FTT and CEL were
already inspected before this 18-test family was defined, and their windows end
at the incident while GALA also has a post-incident window.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.correlation_robustness import (  # noqa: E402
    benjamini_hochberg,
    block_permutation_p_value,
    moving_block_bootstrap_ci,
)
from scripts.crash_control_validation import (  # noqa: E402
    build_future_return_pairs,
    select_token_total_rows,
)
from scripts.time_series_correlation import spearman  # noqa: E402


SEED = 20260830
WINDOWS = (
    ("FTT", "baseline", Path("output-ftt-control-30d")),
    ("FTT", "incident_preceding", Path("output-ftt-crash-30d")),
    ("CEL", "baseline", Path("output-cel-control-30d")),
    ("CEL", "incident_preceding", Path("output-cel-crash-30d")),
    ("GALA", "incident_preceding", Path("output-gala-control-30d")),
    ("GALA", "incident_following", Path("output-gala-event-30d")),
)
TESTS = (
    ("pool_transfer_net", "actual_transfer_net_ratio", False),
    ("net_lp_flow", "net_lp_flow_ratio", False),
    ("gross_lp_activity", "gross_lp_activity_ratio", True),
)


def _seed(label: str) -> int:
    digest = hashlib.sha256(f"{SEED}:{label}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_ledger(
    windows: tuple[tuple[str, str, Path], ...] = WINDOWS,
    *,
    bootstrap_repetitions: int = 1999,
    permutation_repetitions: int = 4999,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case, phase, output_dir in windows:
        series = select_token_total_rows(output_dir)
        for test_id, predictor, absolute_outcome in TESTS:
            xs, ys, _ = build_future_return_pairs(
                series, predictor, 24, absolute_outcome=absolute_outcome
            )
            value = spearman(xs, ys)
            low, high, valid = moving_block_bootstrap_ci(
                xs, ys, spearman,
                repetitions=bootstrap_repetitions,
                alpha=0.05,
                block_length=24,
                seed=_seed(f"{case}:{phase}:{test_id}:bootstrap"),
            )
            p_value = block_permutation_p_value(
                xs, ys, spearman,
                repetitions=permutation_repetitions,
                block_length=24,
                seed=_seed(f"{case}:{phase}:{test_id}:permutation"),
            )
            rows.append({
                "case": case,
                "phase": phase,
                "test_id": test_id,
                "predictor": predictor,
                "outcome": "future_abs_24h_log_return" if absolute_outcome else "future_24h_log_return",
                "n": len(xs),
                "spearman": value,
                "bootstrap_ci_low": low,
                "bootstrap_ci_high": high,
                "bootstrap_valid": valid,
                "block_permutation_p": p_value,
            })

    q_values = benjamini_hochberg([row["block_permutation_p"] for row in rows])
    for row, q_value in zip(rows, q_values):
        row["bh_q_global_18"] = q_value
        row["global_q_below_0_05"] = q_value is not None and q_value < 0.05

    preceding = [row for row in rows if row["phase"] == "incident_preceding"]
    transport = []
    for test_id, _, _ in TESTS:
        selected = [row for row in preceding if row["test_id"] == test_id]
        values = [row["spearman"] for row in selected if row["spearman"] is not None]
        signs = ["positive" if value > 0 else "negative" if value < 0 else "zero" for value in values]
        same_sign = len(values) == 3 and (all(value > 0 for value in values) or all(value < 0 for value in values))
        significant_cases = [row["case"] for row in selected if row["global_q_below_0_05"]]
        transport.append({
            "test_id": test_id,
            "incident_preceding_values": {row["case"]: row["spearman"] for row in selected},
            "incident_preceding_signs": dict(zip((row["case"] for row in selected), signs)),
            "same_sign_all_three": same_sign,
            "global_q_significant_cases": significant_cases,
            "transportable_single_variable_signal": same_sign and len(significant_cases) >= 2,
        })

    summary = {
        "design": "exploratory cross-case evidence ledger",
        "seed": SEED,
        "bootstrap_repetitions": bootstrap_repetitions,
        "permutation_repetitions": permutation_repetitions,
        "global_test_count": len(rows),
        "globally_significant_rows": [
            {"case": row["case"], "phase": row["phase"], "test_id": row["test_id"]}
            for row in rows if row["global_q_below_0_05"]
        ],
        "incident_preceding_transport": transport,
        "decision": (
            "retain_transportable_single_variable_signal"
            if any(row["transportable_single_variable_signal"] for row in transport)
            else "retire_liquidity_single_variables_as_standalone_predictors"
        ),
        "comparability_guardrail": (
            "FTT/CEL incident windows end at the public cutoff; GALA has separate "
            "pre- and post-incident windows. Associations are listed by phase and are not pooled."
        ),
    }
    return rows, summary


def _fmt(value: Any) -> str:
    if value is None or not math.isfinite(float(value)):
        return "—"
    return f"{float(value):.4f}"


def render_summary(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    preceding = [row for row in rows if row["phase"] == "incident_preceding"]
    lookup = {(row["case"], row["test_id"]): row for row in preceding}
    lines = [
        "# FTT / CEL / GALA cross-case evidence ledger",
        "",
        "This exploratory ledger applies the same one-hour predictor and future 24-hour outcome to all existing windows. It uses 24-observation moving-block bootstrap intervals, 4,999 two-sided block permutations, and one BH correction across all 18 rows. It is a synthesis, not a new pre-registered confirmation.",
        "",
        "## Incident-preceding comparison",
        "",
        "| Predictor | FTT ρ | CEL ρ | GALA ρ | Same sign in all three? | Globally significant cases |",
        "|---|---:|---:|---:|---|---|",
    ]
    for test_id, _, _ in TESTS:
        transport = next(item for item in summary["incident_preceding_transport"] if item["test_id"] == test_id)
        lines.append(
            "| {test} | {ftt} | {cel} | {gala} | {same} | {significant} |".format(
                test=test_id,
                ftt=_fmt(lookup[("FTT", test_id)]["spearman"]),
                cel=_fmt(lookup[("CEL", test_id)]["spearman"]),
                gala=_fmt(lookup[("GALA", test_id)]["spearman"]),
                same="yes" if transport["same_sign_all_three"] else "no",
                significant=", ".join(transport["global_q_significant_cases"]) or "none",
            )
        )
    lines += [
        "",
        "## Full 18-row ledger",
        "",
        "| Case | Phase | Predictor | N | ρ | 95% block CI | p | global BH q |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {case} | {phase} | {test} | {n} | {rho} | [{low}, {high}] | {p} | {q} |".format(
                case=row["case"], phase=row["phase"], test=row["test_id"], n=row["n"],
                rho=_fmt(row["spearman"]), low=_fmt(row["bootstrap_ci_low"]),
                high=_fmt(row["bootstrap_ci_high"]), p=_fmt(row["block_permutation_p"]),
                q=_fmt(row["bh_q_global_18"]),
            )
        )
    lines += [
        "",
        "## Decision",
        "",
        f"`{summary['decision']}`",
        "",
        "A feature is not retained merely because one selected case is significant. For incident-preceding transport, it must keep the same sign in FTT, CEL, and GALA and survive the global family in at least two cases. None meets that bar. The project should stop treating pool Transfer net flow, net LP flow, or gross LP activity as standalone 24-hour price predictors.",
        "",
        "The remaining high-value direction is an incident-centered market-response study with identical pre/post geometry and objective case inclusion. That study should ask how price, turnover, and pool inventory jointly respond after an external incident—not search for another single LP variable or another favorable token.",
        "",
        "## 中文结论",
        "",
        "统一 18 项检验后，没有一个单变量在 FTT、CEL、GALA 三个事前窗口中保持同一方向并在至少两个案例通过全局校正。FTT/CEL 的净 LP 流负相关在 GALA 事前窗口变为正值，因此不具备跨案例可迁移性。项目应正式停止把池 Transfer 净流、净 LP 流或累计 LP 活动当作独立的 24 小时价格预测器。下一条值得研究的路线，是使用完全一致的事件前后窗口和客观入样规则，研究价格、成交周转与池库存的联合事件响应，而不是继续寻找另一个“显著”的 LP 指标或代币。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output-cross-case-synthesis"))
    parser.add_argument("--bootstrap-repetitions", type=int, default=1999)
    parser.add_argument("--permutation-repetitions", type=int, default=4999)
    args = parser.parse_args()
    rows, summary = run_ledger(
        bootstrap_repetitions=args.bootstrap_repetitions,
        permutation_repetitions=args.permutation_repetitions,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "association_ledger.csv", rows)
    _write_json(args.output_dir / "results.json", {"rows": rows, "summary": summary})
    markdown = render_summary(rows, summary)
    (args.output_dir / "summary.md").write_text(markdown, encoding="utf-8")
    print(markdown)


if __name__ == "__main__":
    main()
