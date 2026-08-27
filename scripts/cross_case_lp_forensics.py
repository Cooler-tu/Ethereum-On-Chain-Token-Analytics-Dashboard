#!/usr/bin/env python3
"""Rank and decompose counter-directional LP-flow hours across crash cases.

The selection rule is intentionally deterministic: among hourly token-total
observations with an observed price at t and t+24h, retain hours where net LP
flow is positive and the future 24-hour log return is negative, then rank by
net-LP-flow / prior target-token reserve.  The script decomposes those hours
into pools, transactions, target/quote inventory, signed Swaps, and actual
pool-endpoint Transfers using already-indexed artifacts; it does not rescan the
chain or infer beneficial LP identity from a shared Position Manager.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.crash_control_validation import (  # noqa: E402
    build_future_return_pairs,
    select_token_total_rows,
)
from src.data.artifacts import read_table  # noqa: E402


WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"


def _load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


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


def _timestamp(value: Any) -> int:
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def _iso_hour(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%dT%H:00:00Z")


def _decimal(raw: Any, decimals: int) -> Decimal:
    return Decimal(str(raw or 0)) / (Decimal(10) ** decimals)


def _float(value: Any) -> float:
    return float(value or 0)


def select_anomaly_hours(
    rows: list[dict[str, Any]],
    *,
    horizon_hours: int = 24,
) -> list[dict[str, Any]]:
    """Return positive-net-LP / negative-future-return hours in rank order."""
    xs, ys, timestamps = build_future_return_pairs(
        rows,
        "net_lp_flow_ratio",
        horizon_hours,
        absolute_outcome=False,
    )
    candidates = [
        {
            "hour_timestamp": timestamp,
            "net_lp_flow_ratio": predictor,
            "future_log_return": outcome,
        }
        for predictor, outcome, timestamp in zip(xs, ys, timestamps)
        if predictor > 0 and outcome < 0
    ]
    candidates.sort(
        key=lambda row: (
            -float(row["net_lp_flow_ratio"]),
            int(row["hour_timestamp"]),
        )
    )
    for rank, row in enumerate(candidates, 1):
        row["rank"] = rank
    return candidates


def _target_quote_amounts(
    event: dict[str, Any],
    pool: dict[str, Any],
    *,
    target_token: str,
    target_decimals: int,
) -> tuple[Decimal, Decimal]:
    target_is_token0 = str(pool.get("token0") or "").lower() == target_token
    quote_token = str(pool.get("token1") if target_is_token0 else pool.get("token0") or "").lower()
    if quote_token != WETH:
        raise ValueError(
            f"cross-case forensics currently requires WETH quote pools; got {quote_token}"
        )
    target_raw = event.get("token0_amount") if target_is_token0 else event.get("token1_amount")
    quote_raw = event.get("token1_amount") if target_is_token0 else event.get("token0_amount")
    return _decimal(target_raw, target_decimals), _decimal(quote_raw, 18)


def _event_hour(row: dict[str, Any]) -> int:
    return int(row.get("block_timestamp") or 0) // 3600 * 3600


def _signed_swap_target(
    event: dict[str, Any],
    pool: dict[str, Any],
    *,
    target_token: str,
    target_decimals: int,
) -> Decimal:
    target, _ = _target_quote_amounts(
        event,
        pool,
        target_token=target_token,
        target_decimals=target_decimals,
    )
    return target


def analyze_case(
    label: str,
    output_dir: Path,
    *,
    top_n: int = 5,
    horizon_hours: int = 24,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    profile = _load_json(output_dir / "token_profile.json")
    target_token = str(profile.get("address") or "").lower()
    target_decimals = int(profile.get("decimals") or 18)
    pools = {
        str(row.get("pool_address") or "").lower(): row
        for row in _load_json(output_dir / "verified_pools.json")
        if row.get("verified")
    }
    token_rows = select_token_total_rows(output_dir)
    token_by_hour = {_timestamp(row["bucket_start"]): row for row in token_rows}
    pool_series = read_table(
        "analysis_series", output_dir, prefer="parquet", legacy_rows=False
    )
    pool_by_hour = {
        (_timestamp(row["bucket_start"]), str(row.get("pool_identifier") or "").lower()): row
        for row in pool_series
        if row.get("scope") == "pool"
    }
    candidates = select_anomaly_hours(token_rows, horizon_hours=horizon_hours)
    candidate_hours = {int(row["hour_timestamp"]) for row in candidates}
    selected_hours = {
        int(row["hour_timestamp"]) for row in candidates if int(row["rank"]) <= top_n
    }

    liquidity_by_hour: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for event in _load_json(output_dir / "liquidity_events.json"):
        if str(event.get("source_event") or "").lower() not in {"mint", "burn"}:
            continue
        hour = _event_hour(event)
        if hour in candidate_hours:
            liquidity_by_hour[hour].append(event)

    swaps_by_hour_pool: dict[tuple[int, str], Decimal] = defaultdict(Decimal)
    for event in _load_json(output_dir / "swaps.json"):
        hour = _event_hour(event)
        if hour not in candidate_hours:
            continue
        pool_id = str(event.get("pool_address") or "").lower()
        pool = pools.get(pool_id)
        if pool is None:
            continue
        swaps_by_hour_pool[(hour, pool_id)] += _signed_swap_target(
            event,
            pool,
            target_token=target_token,
            target_decimals=target_decimals,
        )

    hour_rows: list[dict[str, Any]] = []
    pool_rows: list[dict[str, Any]] = []
    transaction_rows: list[dict[str, Any]] = []
    for candidate in candidates:
        hour = int(candidate["hour_timestamp"])
        current = token_by_hour[hour]
        price = Decimal(str(current.get("price_close") or 0))
        events = liquidity_by_hour.get(hour, [])
        tx_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        pool_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            pool_id = str(event.get("pool_address") or "").lower()
            tx = str(event.get("transaction_hash") or "").lower()
            tx_groups[(pool_id, tx)].append(event)
            pool_groups[pool_id].append(event)

        gross_add_target = Decimal(0)
        gross_remove_target = Decimal(0)
        gross_add_quote = Decimal(0)
        gross_remove_quote = Decimal(0)
        target_only_add = Decimal(0)
        same_tx_recycled_target = Decimal(0)
        add_by_tx: list[Decimal] = []
        versions: set[str] = set()

        for (pool_id, tx_hash), tx_events in sorted(tx_groups.items()):
            pool = pools[pool_id]
            version = str(pool.get("version") or "")
            versions.add(version)
            add_target = Decimal(0)
            remove_target = Decimal(0)
            add_quote = Decimal(0)
            remove_quote = Decimal(0)
            actors: set[str] = set()
            recipients: set[str] = set()
            for event in tx_events:
                target, quote = _target_quote_amounts(
                    event,
                    pool,
                    target_token=target_token,
                    target_decimals=target_decimals,
                )
                if str(event.get("source_event") or "").lower() == "mint":
                    add_target += target
                    add_quote += quote
                else:
                    remove_target += target
                    remove_quote += quote
                if event.get("actor"):
                    actors.add(str(event["actor"]).lower())
                if event.get("recipient"):
                    recipients.add(str(event["recipient"]).lower())
            target_value_quote = add_target * price
            total_add_value_quote = target_value_quote + add_quote
            target_value_share = (
                float(target_value_quote / total_add_value_quote)
                if total_add_value_quote > 0 else None
            )
            recycled = min(add_target, remove_target)
            same_tx_recycled_target += recycled
            if add_target > 0:
                add_by_tx.append(add_target)
            if add_target > 0 and add_quote == 0:
                target_only_add += add_target
            gross_add_target += add_target
            gross_remove_target += remove_target
            gross_add_quote += add_quote
            gross_remove_quote += remove_quote
            if hour in selected_hours:
                transaction_rows.append({
                    "case": label,
                    "hour_rank": candidate["rank"],
                    "hour_utc": _iso_hour(hour),
                    "pool_address": pool_id,
                    "version": version,
                    "transaction_hash": tx_hash,
                    "lp_event_count": len(tx_events),
                    "add_target": float(add_target),
                    "remove_target": float(remove_target),
                    "net_lp_target": float(add_target - remove_target),
                    "add_weth": float(add_quote),
                    "remove_weth": float(remove_quote),
                    "target_value_share_of_add": target_value_share,
                    "target_only_add": add_target > 0 and add_quote == 0,
                    "same_tx_add_remove": add_target > 0 and remove_target > 0,
                    "same_tx_recycled_target": float(recycled),
                    "contract_facing_actors": ";".join(sorted(actors)),
                    "contract_facing_recipients": ";".join(sorted(recipients)),
                    "beneficial_owner_known": False,
                })

        for pool_id, pool_events in sorted(pool_groups.items()):
            pool = pools[pool_id]
            series_row = pool_by_hour.get((hour, pool_id), {})
            add_target = Decimal(0)
            remove_target = Decimal(0)
            add_quote = Decimal(0)
            remove_quote = Decimal(0)
            for event in pool_events:
                target, quote = _target_quote_amounts(
                    event,
                    pool,
                    target_token=target_token,
                    target_decimals=target_decimals,
                )
                if str(event.get("source_event") or "").lower() == "mint":
                    add_target += target
                    add_quote += quote
                else:
                    remove_target += target
                    remove_quote += quote
            pool_rows.append({
                "case": label,
                "hour_rank": candidate["rank"],
                "selected_top_n": int(candidate["rank"]) <= top_n,
                "hour_utc": _iso_hour(hour),
                "pool_address": pool_id,
                "version": pool.get("version"),
                "lp_add_target": float(add_target),
                "lp_remove_target": float(remove_target),
                "net_lp_target": float(add_target - remove_target),
                "lp_add_weth": float(add_quote),
                "lp_remove_weth": float(remove_quote),
                "signed_swap_net_to_pool_target": float(swaps_by_hour_pool[(hour, pool_id)]),
                "actual_transfer_net_to_pool_target": _float(series_row.get("actual_transfer_net_token")),
                "end_reserve_target": _float(series_row.get("tvl_token_close")),
            })

        signed_swap_net = sum(
            (value for (event_hour, _), value in swaps_by_hour_pool.items() if event_hour == hour),
            Decimal(0),
        )
        actual_transfer_net = Decimal(str(current.get("actual_transfer_net_token") or 0))
        net_lp = gross_add_target - gross_remove_target
        largest_add_share = (
            float(max(add_by_tx) / gross_add_target)
            if gross_add_target > 0 and add_by_tx else None
        )
        target_add_value_quote = gross_add_target * price
        total_add_value_quote = target_add_value_quote + gross_add_quote
        target_value_share_of_add = (
            float(target_add_value_quote / total_add_value_quote)
            if total_add_value_quote > 0 else None
        )
        prior_reserve = (
            net_lp / Decimal(str(candidate["net_lp_flow_ratio"]))
            if candidate["net_lp_flow_ratio"] else Decimal(0)
        )
        hour_rows.append({
            "case": label,
            "rank": candidate["rank"],
            "selected_top_n": int(candidate["rank"]) <= top_n,
            "hour_utc": _iso_hour(hour),
            "net_lp_flow_ratio": candidate["net_lp_flow_ratio"],
            "future_24h_log_return": candidate["future_log_return"],
            "future_24h_simple_return": math.exp(float(candidate["future_log_return"])) - 1,
            "price_close_weth_per_target": float(price),
            "prior_reserve_target": float(prior_reserve),
            "lp_add_target": float(gross_add_target),
            "lp_remove_target": float(gross_remove_target),
            "net_lp_target": float(net_lp),
            "lp_add_weth": float(gross_add_quote),
            "lp_remove_weth": float(gross_remove_quote),
            "lp_add_target_value_weth": float(target_add_value_quote),
            "target_value_share_of_add": target_value_share_of_add,
            "target_only_add_target": float(target_only_add),
            "target_only_add_share": (
                float(target_only_add / gross_add_target) if gross_add_target > 0 else None
            ),
            "actual_transfer_net_to_pool_target": float(actual_transfer_net),
            "signed_swap_net_to_pool_target": float(signed_swap_net),
            "transfer_minus_swap_minus_lp_target": float(
                actual_transfer_net - signed_swap_net - net_lp
            ),
            "lp_event_count": len(events),
            "lp_transaction_count": len(tx_groups),
            "largest_add_transaction_share": largest_add_share,
            "same_tx_recycled_target": float(same_tx_recycled_target),
            "versions_with_lp_events": ";".join(sorted(versions)),
            "beneficial_owner_known": False,
        })

    selected = [row for row in hour_rows if row["selected_top_n"]]
    summary = {
        "case": label,
        "output_dir": str(output_dir),
        "selection_rule": (
            f"net_lp_flow_ratio > 0 and observed future {horizon_hours}h log return < 0; "
            "rank descending by net_lp_flow_ratio"
        ),
        "candidate_hour_count": len(hour_rows),
        "selected_hour_count": len(selected),
        "selected_all_v3": bool(selected) and all(
            row["versions_with_lp_events"] == "v3" for row in selected
        ),
        "selected_target_only_add_target": sum(row["target_only_add_target"] for row in selected),
        "selected_gross_add_target": sum(row["lp_add_target"] for row in selected),
        "selected_target_add_value_weth": sum(row["lp_add_target_value_weth"] for row in selected),
        "selected_quote_add_weth": sum(row["lp_add_weth"] for row in selected),
        "selected_same_tx_recycled_target": sum(row["same_tx_recycled_target"] for row in selected),
        "identity_guardrail": (
            "Indexed Mint/Burn actors are contract-facing identities. Beneficial LP wallet/NFT "
            "identity and cross-transaction repositioning require targeted Position Manager tracing."
        ),
    }
    gross = float(summary["selected_gross_add_target"])
    summary["selected_target_only_add_share"] = (
        float(summary["selected_target_only_add_target"]) / gross if gross else None
    )
    selected_total_value = (
        float(summary["selected_target_add_value_weth"])
        + float(summary["selected_quote_add_weth"])
    )
    summary["selected_target_value_share_of_add"] = (
        float(summary["selected_target_add_value_weth"]) / selected_total_value
        if selected_total_value else None
    )
    return hour_rows, pool_rows, transaction_rows, summary


def _pct(value: Any) -> str:
    return "—" if value is None else f"{float(value):+.2%}"


def _num(value: Any) -> str:
    number = float(value or 0)
    if abs(number) >= 1_000_000:
        return f"{number / 1_000_000:.3f}M"
    if abs(number) >= 1_000:
        return f"{number / 1_000:.3f}K"
    return f"{number:.3f}"


def write_summary_md(
    path: Path,
    hour_rows: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    *,
    top_n: int,
) -> None:
    lines = [
        "# FTT + CEL opposite-direction LP-flow forensics",
        "",
        "The deterministic candidate rule is: positive hourly net LP flow, negative observed future 24-hour log return, ranked by net LP flow divided by prior target-token reserve. The first `{}` hours per case receive transaction-level decomposition.".format(top_n),
        "",
        "## Ranked hours",
        "",
        "| Case | Rank | UTC hour | Net LP / prior reserve | Future 24h | LP add / remove | WETH add / remove | Target value share | Target-only add | Largest add tx | Pool version |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    selected = [row for row in hour_rows if row["selected_top_n"]]
    for row in selected:
        lines.append(
                "| {case} | {rank} | {hour} | {ratio} | {future} | {add} / {remove} | {wadd:.4f} / {wremove:.4f} | {value_share} | {one} | {largest} | {version} |".format(
                case=row["case"], rank=row["rank"], hour=row["hour_utc"],
                ratio=_pct(row["net_lp_flow_ratio"]), future=_pct(row["future_24h_simple_return"]),
                add=_num(row["lp_add_target"]), remove=_num(row["lp_remove_target"]),
                wadd=row["lp_add_weth"], wremove=row["lp_remove_weth"],
                value_share=_pct(row["target_value_share_of_add"]),
                one=_pct(row["target_only_add_share"]),
                largest=_pct(row["largest_add_transaction_share"]),
                version=row["versions_with_lp_events"] or "—",
            )
        )
    lines.extend([
        "",
        "## What the decomposition establishes",
        "",
    ])
    by_case = {summary["case"]: summary for summary in summaries}
    for label in sorted(by_case):
        summary = by_case[label]
        lines.append(
            "- **{}:** {} candidate hours; top {} are {}. Target inventory represents {} of added WETH-equivalent value at each hour close; fully target-only deposits are {} of target tokens added.".format(
                label,
                summary["candidate_hour_count"],
                summary["selected_hour_count"],
                "all V3" if summary["selected_all_v3"] else "not exclusively V3",
                _pct(summary["selected_target_value_share_of_add"]),
                _pct(summary["selected_target_only_add_share"]),
            )
        )
    lines.extend([
        "- A positive target-token LP flow is not automatically equivalent to fresh quote capital or price support. A V3 Mint can be target-only, balanced, or quote-only depending on its range and the current price.",
        "- `actual Transfer net − signed Swap net − Mint/Burn net` is a reconciliation diagnostic, not unexplained profit: V3 Burn and Collect can occur at different times, and fees or other pool movements can enter the residual.",
        "- Same-transaction add/remove is measured directly. Cross-transaction range repositioning is deliberately not inferred from the shared NonfungiblePositionManager address.",
        "",
        "## Current mechanism boundary",
        "",
        "The repeated negative correlation is now better described as **target-token inventory provision during falling prices**, not generic capital inflow. FTT includes an extreme one-sided V3 inventory placement, while CEL's largest hour is a two-sided V3 Mint. This heterogeneity means the cross-case correlation does not yet identify one common wallet strategy. Targeted V3 owner/tick/NFT tracing is the next evidentiary step before pre-registering a third case.",
        "",
        "## 中文结论",
        "",
        "筛选规则固定为：小时净 LP 流为正、未来 24 小时价格为负，并按净 LP 流占前一小时目标代币储备的比例排序。FTT 与 CEL 的前五名异常小时都由 V3 事件主导，但两者机制并不完全相同。FTT 最大异常小时主要是单边加入 FTT、没有同步加入 WETH；CEL 最大异常小时则是双边加入。因此，原先的“净 LP 流入”更准确地说是下跌期间向池中配置目标代币库存，不能直接解释成外部资金托价。下一步需要针对这些交易追踪 V3 tick 区间、Position Manager NFT 和真实控制钱包，区分单边挂单、正常做市与撤出后重建。",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-case transaction forensics for counter-directional LP-flow hours"
    )
    parser.add_argument(
        "--case",
        action="append",
        required=True,
        metavar="LABEL=OUTPUT_DIR",
        help="Repeat for each case, for example FTT=output-ftt-crash-30d",
    )
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--horizon-hours", type=int, default=24)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    if args.top_n < 1 or args.horizon_hours < 1:
        parser.error("top-n and horizon-hours must be positive")

    all_hours: list[dict[str, Any]] = []
    all_pools: list[dict[str, Any]] = []
    all_transactions: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for spec in args.case:
        if "=" not in spec:
            parser.error(f"invalid --case {spec!r}; expected LABEL=OUTPUT_DIR")
        label, raw_path = spec.split("=", 1)
        hours, pools, transactions, summary = analyze_case(
            label.strip().upper(),
            Path(raw_path),
            top_n=args.top_n,
            horizon_hours=args.horizon_hours,
        )
        all_hours.extend(hours)
        all_pools.extend(pools)
        all_transactions.extend(transactions)
        summaries.append(summary)

    out = Path(args.out_dir)
    _write_csv(out / "ranked_hours.csv", all_hours)
    _write_csv(out / "pool_decomposition.csv", all_pools)
    _write_csv(out / "top_hour_transactions.csv", all_transactions)
    _write_json(out / "summary.json", {
        "top_n": args.top_n,
        "horizon_hours": args.horizon_hours,
        "cases": summaries,
    })
    write_summary_md(out / "summary.md", all_hours, summaries, top_n=args.top_n)
    print(json.dumps({
        "out_dir": str(out),
        "ranked_hours": len(all_hours),
        "selected_transactions": len(all_transactions),
        "cases": summaries,
    }, indent=2))


if __name__ == "__main__":
    main()
