"""Pure interval, matching, and inference helpers for LP gap analysis."""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np
import pandas as pd


HORIZON_SECONDS = {"1h": 3_600, "6h": 21_600, "24h": 86_400}


def _position(row, prefix: str = "") -> tuple[int, int, int]:
    return (
        int(row[f"{prefix}block_number"]),
        int(row[f"{prefix}transaction_index"]),
        int(row[f"{prefix}log_index"]),
    )


def build_gap_intervals(
    campaigns: pd.DataFrame,
    followup_end_timestamp: int,
    thresholds: Iterable[int] = (80, 90),
) -> pd.DataFrame:
    """Create nested 1h/6h/24h gap intervals for the frozen campaigns."""
    rows: list[dict] = []
    for campaign in campaigns.to_dict("records"):
        start_position = (
            int(campaign["burn_block_number"]),
            int(campaign["burn_transaction_index"]),
            int(campaign["burn_log_index"]),
        )
        for threshold in thresholds:
            recovery_block = campaign.get(f"first_recovery_{threshold}_block_number")
            recovery_position = None
            if pd.notna(recovery_block):
                recovery_position = (
                    int(recovery_block),
                    int(campaign[f"first_recovery_{threshold}_transaction_index"]),
                    int(campaign[f"first_recovery_{threshold}_log_index"]),
                )
            recovery_timestamp = campaign.get(f"first_recovery_{threshold}_timestamp")
            recovery_timestamp = int(recovery_timestamp) if pd.notna(recovery_timestamp) else None
            threshold_recovery_observed = recovery_timestamp is not None
            for horizon, seconds in HORIZON_SECONDS.items():
                horizon_end = int(campaign["burn_timestamp"]) + seconds
                observed_end = min(horizon_end, int(followup_end_timestamp))
                recovered = recovery_timestamp is not None and recovery_timestamp <= horizon_end
                rows.append({
                    "campaign_id": campaign["campaign_id"],
                    "wallet_address": campaign["wallet_address"],
                    "origin_pool_address": campaign["origin_pool_address"],
                    "threshold_pct": threshold,
                    "horizon": horizon,
                    "burn_timestamp": int(campaign["burn_timestamp"]),
                    "burn_block_number": start_position[0],
                    "burn_transaction_index": start_position[1],
                    "burn_log_index": start_position[2],
                    "recovery_event_id": campaign.get(f"first_recovery_{threshold}_event_id"),
                    "recovery_timestamp": recovery_timestamp,
                    "threshold_recovery_observed": threshold_recovery_observed,
                    "recovery_block_number": recovery_position[0] if recovery_position else None,
                    "recovery_transaction_index": recovery_position[1] if recovery_position else None,
                    "recovery_log_index": recovery_position[2] if recovery_position else None,
                    "interval_end_timestamp": recovery_timestamp if recovered else observed_end,
                    "recovered_within_horizon": recovered,
                    "observation_complete": bool(recovered or followup_end_timestamp >= horizon_end),
                })
    return pd.DataFrame(rows)


def swap_is_in_interval(swap: dict, interval: dict) -> bool:
    """Return whether a Swap is after Burn and before the interval's end."""
    swap_position = (
        int(swap["block_number"]),
        int(swap["transaction_index"]),
        int(swap["log_index"]),
    )
    start_position = (
        int(interval["burn_block_number"]),
        int(interval["burn_transaction_index"]),
        int(interval["burn_log_index"]),
    )
    if swap_position <= start_position:
        return False
    recovery_block = interval.get("recovery_block_number")
    recovered = bool(interval.get("recovered_within_horizon")) and pd.notna(recovery_block)
    if recovered:
        end_position = (
            int(recovery_block),
            int(interval["recovery_transaction_index"]),
            int(interval["recovery_log_index"]),
        )
        return swap_position < end_position
    return int(swap["timestamp"]) <= int(interval["interval_end_timestamp"])


def label_gap_swaps(swaps: pd.DataFrame, intervals: pd.DataFrame) -> pd.DataFrame:
    """Return one row per unique Swap/threshold/horizon with campaign provenance."""
    exposure: dict[tuple[str, int, str], list[dict]] = defaultdict(list)
    swaps_by_pool = {
        str(pool).lower(): frame.to_dict("records")
        for pool, frame in swaps.groupby(swaps.pool_address.str.lower())
    }
    eligible = intervals[
        intervals.observation_complete & intervals.threshold_recovery_observed
    ]
    for interval in eligible.to_dict("records"):
        for swap in swaps_by_pool.get(str(interval["origin_pool_address"]).lower(), []):
            if swap_is_in_interval(swap, interval):
                exposure[(swap["swap_event_id"], int(interval["threshold_pct"]), interval["horizon"])].append(interval)

    swap_lookup = swaps.set_index("swap_event_id").to_dict("index")
    rows = []
    for (swap_id, threshold, horizon), matched_intervals in exposure.items():
        swap = {"swap_event_id": swap_id, **swap_lookup[swap_id]}
        latest = max(matched_intervals, key=lambda item: (
            item["burn_block_number"], item["burn_transaction_index"], item["burn_log_index"]
        ))
        swap.update({
            "threshold_pct": threshold,
            "horizon": horizon,
            "campaign_ids": "|".join(sorted({item["campaign_id"] for item in matched_intervals})),
            "campaign_count": len({item["campaign_id"] for item in matched_intervals}),
            "primary_campaign_id": latest["campaign_id"],
        })
        rows.append(swap)
    return pd.DataFrame(rows)


def mark_full_gap_contamination(
    swaps: pd.DataFrame,
    campaigns: pd.DataFrame,
    followup_end_timestamp: int,
    threshold: int = 90,
    cap_seconds: int = 86_400,
) -> pd.Series:
    """Mark Swaps inside any studied gap, capped at the maximum analysis window."""
    contaminated: set[str] = set()
    swaps_by_pool = {
        str(pool).lower(): frame.to_dict("records")
        for pool, frame in swaps.groupby(swaps.pool_address.str.lower())
    }
    for campaign in campaigns.to_dict("records"):
        recovery_block = campaign.get(f"first_recovery_{threshold}_block_number")
        recovery_timestamp = campaign.get(f"first_recovery_{threshold}_timestamp")
        recovered_within_cap = (
            pd.notna(recovery_block)
            and pd.notna(recovery_timestamp)
            and int(recovery_timestamp) <= int(campaign["burn_timestamp"]) + cap_seconds
        )
        interval = {
            "burn_block_number": campaign["burn_block_number"],
            "burn_transaction_index": campaign["burn_transaction_index"],
            "burn_log_index": campaign["burn_log_index"],
            "recovered_within_horizon": recovered_within_cap,
            "recovery_block_number": recovery_block,
            "recovery_transaction_index": campaign.get(f"first_recovery_{threshold}_transaction_index"),
            "recovery_log_index": campaign.get(f"first_recovery_{threshold}_log_index"),
            "interval_end_timestamp": (
                int(recovery_timestamp)
                if recovered_within_cap
                else min(int(campaign["burn_timestamp"]) + cap_seconds, int(followup_end_timestamp))
            ),
        }
        for swap in swaps_by_pool.get(str(campaign["origin_pool_address"]).lower(), []):
            if swap_is_in_interval(swap, interval):
                contaminated.add(swap["swap_event_id"])
    return swaps.swap_event_id.isin(contaminated)


def greedy_size_match(
    treated: pd.DataFrame,
    controls: pd.DataFrame,
    caliper_pct: float,
) -> pd.DataFrame:
    """One-to-one match by pool, direction, and nearest WETH notional."""
    available = set(controls.swap_event_id)
    control_lookup = controls.set_index("swap_event_id")
    pairs: list[dict] = []
    # Hard-to-match large trades go first so small trades do not consume their controls.
    for item in treated.sort_values("notional_weth", ascending=False).to_dict("records"):
        candidates = controls[
            controls.swap_event_id.isin(available)
            & controls.pool_address.str.lower().eq(str(item["pool_address"]).lower())
            & controls.direction.eq(item["direction"])
        ].copy()
        if not item["notional_weth"] or candidates.empty:
            continue
        candidates["size_ratio"] = candidates.notional_weth / float(item["notional_weth"])
        lower, upper = 1 - caliper_pct, 1 + caliper_pct
        candidates = candidates[candidates.size_ratio.between(lower, upper)]
        if candidates.empty:
            continue
        candidates["log_size_distance"] = np.abs(
            np.log(candidates.notional_weth) - np.log(float(item["notional_weth"]))
        )
        candidates["time_distance"] = np.abs(candidates.timestamp - int(item["timestamp"]))
        chosen = candidates.sort_values(["log_size_distance", "time_distance"]).iloc[0]
        available.remove(chosen.swap_event_id)
        pairs.append({
            "threshold_pct": int(item["threshold_pct"]),
            "horizon": item["horizon"],
            "caliper_pct": caliper_pct,
            "primary_campaign_id": item["primary_campaign_id"],
            "cluster_id": f"{item['primary_campaign_id']}|{pd.to_datetime(int(item['timestamp']), unit='s', utc=True).date().isoformat()}",
            "treated_swap_event_id": item["swap_event_id"],
            "control_swap_event_id": chosen.swap_event_id,
            "pool_address": item["pool_address"],
            "direction": item["direction"],
            "treated_timestamp": int(item["timestamp"]),
            "control_timestamp": int(chosen.timestamp),
            "treated_notional_weth": float(item["notional_weth"]),
            "control_notional_weth": float(chosen.notional_weth),
            "size_ratio": float(chosen.size_ratio),
            "treated_price_impact_bps": float(item["price_impact_bps"]),
            "control_price_impact_bps": float(chosen.price_impact_bps),
            "excess_price_impact_bps": float(item["price_impact_bps"] - chosen.price_impact_bps),
        })
    return pd.DataFrame(pairs)


def campaign_cluster_bootstrap(
    pairs: pd.DataFrame,
    iterations: int = 5_000,
    seed: int = 20260910,
) -> dict:
    """Bootstrap the mean matched excess after aggregating within campaign."""
    if pairs.empty:
        return {"estimate": np.nan, "ci_low": np.nan, "ci_high": np.nan, "campaigns": 0}
    cluster_column = "cluster_id" if "cluster_id" in pairs else "primary_campaign_id"
    clustered = pairs.groupby(cluster_column).excess_price_impact_bps.mean()
    values = clustered.to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(values, size=(iterations, len(values)), replace=True).mean(axis=1)
    return {
        "estimate": float(values.mean()),
        "ci_low": float(np.quantile(draws, 0.025)),
        "ci_high": float(np.quantile(draws, 0.975)),
        "campaigns": int(len(values)),
    }
