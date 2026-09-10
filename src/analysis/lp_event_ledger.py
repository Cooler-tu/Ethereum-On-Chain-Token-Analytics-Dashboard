"""Pure helpers for a non-overlapping LP Burn/re-add campaign ledger.

The module contains no RPC access.  It turns an ordered table of already
decoded facts into two derived fact tables: one-to-many event links and a
campaign ledger.  Each Mint can be assigned to at most one open campaign.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import pandas as pd


WINDOW_SECONDS = {
    "1h": 3_600,
    "6h": 6 * 3_600,
    "24h": 24 * 3_600,
    "7d": 7 * 86_400,
    "30d": 30 * 86_400,
}


def weth_equivalent(turbo_amount: float, weth_amount: float, anchor_price: float) -> float:
    """Value two token legs in WETH using one campaign's fixed Burn price."""
    return float(turbo_amount) * float(anchor_price) + float(weth_amount)


def chain_order_columns() -> list[str]:
    return ["block_number", "transaction_index", "log_index"]


@dataclass
class _Campaign:
    campaign_id: str
    origin: dict
    anchor_price: float
    initial_burn_value: float
    links: list[dict] = field(default_factory=list)
    closed_at: int | None = None

    def ratios_at(self, horizon_seconds: int) -> tuple[float, float]:
        cutoff = int(self.origin["timestamp"]) + horizon_seconds
        eligible = [link for link in self.links if int(link["timestamp"]) <= cutoff]
        gross = sum(link["weth_value_at_anchor"] for link in eligible if link["event_type"] == "Mint")
        later_burn = sum(link["weth_value_at_anchor"] for link in eligible if link["event_type"] == "Burn")
        if self.initial_burn_value <= 0:
            return float("nan"), float("nan")
        return gross / self.initial_burn_value, (gross - later_burn) / self.initial_burn_value

    def first_net_crossing(self, threshold: float) -> dict | None:
        """Return the first linked event where cumulative net recovery crosses a line."""
        if self.initial_burn_value <= 0:
            return None
        running = 0.0
        for link in self.links:
            sign = 1.0 if link["event_type"] == "Mint" else -1.0
            running += sign * float(link["weth_value_at_anchor"])
            if running / self.initial_burn_value >= threshold:
                return link
        return None


def _return_scope(origin_pool: str, origin_pair: str, row: dict) -> str:
    if str(row["pool_address"]).lower() == str(origin_pool).lower():
        return "Same_Pool"
    if str(row.get("pair_key", "")).lower() == str(origin_pair).lower():
        return "Cross_Fee_Tier"
    return "Cross_Pair"


def build_event_readd_links(raw_events: pd.DataFrame) -> pd.DataFrame:
    """Link each Mint once to the latest eligible same-wallet Burn event.

    This is the event-level descriptive table, deliberately separate from the
    campaign state machine below.  A later eligible Burn supersedes an earlier
    one for event pairing; one Burn may still receive multiple Mints before the
    next Burn.  No motive or campaign classification is added here.
    """
    ordered = raw_events.sort_values(chain_order_columns(), kind="stable")
    latest_burn: dict[str, dict] = {}
    links: list[dict] = []
    for row in ordered.to_dict("records"):
        wallet = str(row["wallet_address"]).lower()
        if row["event_type"] == "Burn" and bool(row["starts_campaign"]):
            latest_burn[wallet] = row
            continue
        if row["event_type"] != "Mint" or wallet not in latest_burn:
            continue
        origin = latest_burn[wallet]
        gap = int(row["timestamp"]) - int(origin["timestamp"])
        if gap < 0 or gap > WINDOW_SECONDS["30d"]:
            continue
        anchor = float(origin["price_weth_per_turbo"])
        links.append({
            "origin_burn_event_id": origin["event_id"],
            "mint_event_id": row["event_id"],
            "wallet_address": origin["wallet_address"],
            "burn_nft_id": origin.get("nft_id"),
            "mint_nft_id": row.get("nft_id"),
            "burn_pool_address": origin["pool_address"],
            "mint_pool_address": row["pool_address"],
            "mint_transaction_hash": row["transaction_hash"],
            "mint_block_number": int(row["block_number"]),
            "mint_transaction_index": int(row["transaction_index"]),
            "mint_log_index": int(row["log_index"]),
            "burn_timestamp": int(origin["timestamp"]),
            "mint_timestamp": int(row["timestamp"]),
            "time_gap_seconds": gap,
            "block_gap": int(row["block_number"]) - int(origin["block_number"]),
            "same_transaction": str(row["transaction_hash"]).lower() == str(origin["transaction_hash"]).lower(),
            "same_block": int(row["block_number"]) == int(origin["block_number"]),
            "return_scope": _return_scope(origin["pool_address"], origin["pair_key"], row),
            "mint_turbo_amount": float(row["turbo_amount"]),
            "mint_weth_amount": float(row["weth_amount"]),
            "anchor_price_weth_per_turbo": anchor,
            "mint_weth_value_at_burn_price": weth_equivalent(
                row["turbo_amount"], row["weth_amount"], anchor
            ),
        })
    frame = pd.DataFrame(links)
    if not frame.empty and frame.mint_event_id.duplicated().any():
        raise AssertionError("A Mint was linked to more than one Burn event")
    return frame


def build_campaign_ledger(
    raw_events: pd.DataFrame,
    followup_data_end_time: int,
    recovery_threshold: float = 0.90,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build non-overlapping campaigns for each exact wallet.

    Required columns are documented in ``REQUIRED_COLUMNS`` below.  A campaign
    begins at an eligible cohort Burn.  Later same-wallet Mint/Burn facts within
    30 days are assigned to that one campaign until net recovery first reaches
    ``recovery_threshold``.  Consequently, a Mint is never reused as recovery
    evidence for multiple Burns.
    """
    required = {
        "event_id", "event_type", "wallet_address", "pool_address", "pair_key",
        "block_number", "transaction_index", "log_index", "transaction_hash",
        "timestamp", "turbo_amount", "weth_amount", "price_weth_per_turbo",
        "starts_campaign",
    }
    missing = sorted(required - set(raw_events.columns))
    if missing:
        raise ValueError(f"raw_events is missing required columns: {missing}")

    ordered = raw_events.sort_values(chain_order_columns(), kind="stable")
    open_by_wallet: dict[str, _Campaign] = {}
    finished: list[_Campaign] = []
    all_links: list[dict] = []
    ordinal = 0

    def expire(wallet: str, now: int) -> None:
        campaign = open_by_wallet.get(wallet)
        if campaign and now > int(campaign.origin["timestamp"]) + WINDOW_SECONDS["30d"]:
            finished.append(open_by_wallet.pop(wallet))

    for row in ordered.to_dict("records"):
        wallet = str(row["wallet_address"]).lower()
        timestamp = int(row["timestamp"])
        expire(wallet, timestamp)
        campaign = open_by_wallet.get(wallet)

        if row["event_type"] == "Burn" and bool(row["starts_campaign"]) and campaign is None:
            ordinal += 1
            initial_value = weth_equivalent(
                row["turbo_amount"], row["weth_amount"], row["price_weth_per_turbo"]
            )
            campaign = _Campaign(
                campaign_id=f"lp-campaign-{ordinal:05d}",
                origin=row,
                anchor_price=float(row["price_weth_per_turbo"]),
                initial_burn_value=initial_value,
            )
            open_by_wallet[wallet] = campaign
            continue

        if campaign is None or row["event_type"] not in {"Mint", "Burn"}:
            continue

        # The origin Burn is not a follow-up link.  Every later fact is ordered
        # by its exact chain position, so same-block and same-tx links are valid.
        value = weth_equivalent(
            row["turbo_amount"], row["weth_amount"], campaign.anchor_price
        )
        origin = campaign.origin
        link = {
            "campaign_id": campaign.campaign_id,
            "origin_burn_event_id": origin["event_id"],
            "linked_event_id": row["event_id"],
            "event_type": row["event_type"],
            "wallet_address": origin["wallet_address"],
            "pool_address": row["pool_address"],
            "transaction_hash": row["transaction_hash"],
            "block_number": int(row["block_number"]),
            "transaction_index": int(row["transaction_index"]),
            "log_index": int(row["log_index"]),
            "timestamp": timestamp,
            "time_gap_seconds": timestamp - int(origin["timestamp"]),
            "block_gap": int(row["block_number"]) - int(origin["block_number"]),
            "same_transaction": str(row["transaction_hash"]).lower() == str(origin["transaction_hash"]).lower(),
            "same_block": int(row["block_number"]) == int(origin["block_number"]),
            "return_scope": _return_scope(origin["pool_address"], origin["pair_key"], row),
            "turbo_amount": float(row["turbo_amount"]),
            "weth_amount": float(row["weth_amount"]),
            "anchor_price_weth_per_turbo": campaign.anchor_price,
            "weth_value_at_anchor": value,
        }
        campaign.links.append(link)
        all_links.append(link)

        _, net = campaign.ratios_at(WINDOW_SECONDS["30d"])
        if row["event_type"] == "Mint" and net >= recovery_threshold:
            campaign.closed_at = timestamp
            finished.append(open_by_wallet.pop(wallet))

    finished.extend(open_by_wallet.values())

    campaign_rows: list[dict] = []
    for campaign in finished:
        origin = campaign.origin
        followup_seconds = max(0, int(followup_data_end_time) - int(origin["timestamp"]))
        crossing_80 = campaign.first_net_crossing(0.80)
        crossing_90 = campaign.first_net_crossing(0.90)
        row = {
            "campaign_id": campaign.campaign_id,
            "origin_burn_event_id": origin["event_id"],
            "wallet_address": origin["wallet_address"],
            "nft_id": origin.get("nft_id"),
            "origin_pool_address": origin["pool_address"],
            "origin_fee": origin.get("fee"),
            "burn_block_number": int(origin["block_number"]),
            "burn_transaction_index": int(origin["transaction_index"]),
            "burn_log_index": int(origin["log_index"]),
            "burn_transaction_hash": origin["transaction_hash"],
            "burn_timestamp": int(origin["timestamp"]),
            "burn_price_weth_per_turbo": campaign.anchor_price,
            "burn_turbo_amount": float(origin["turbo_amount"]),
            "burn_weth_amount": float(origin["weth_amount"]),
            "burn_weth_value_at_burn_price": campaign.initial_burn_value,
            "followup_days": followup_seconds / 86_400,
            "linked_event_count": len(campaign.links),
            "linked_mint_count": sum(link["event_type"] == "Mint" for link in campaign.links),
            "linked_later_burn_count": sum(link["event_type"] == "Burn" for link in campaign.links),
            "first_recovery_80_event_id": crossing_80["linked_event_id"] if crossing_80 else None,
            "first_recovery_80_block_number": crossing_80["block_number"] if crossing_80 else None,
            "first_recovery_80_transaction_index": crossing_80["transaction_index"] if crossing_80 else None,
            "first_recovery_80_log_index": crossing_80["log_index"] if crossing_80 else None,
            "first_recovery_80_timestamp": crossing_80["timestamp"] if crossing_80 else None,
            "first_recovery_90_event_id": crossing_90["linked_event_id"] if crossing_90 else None,
            "first_recovery_90_block_number": crossing_90["block_number"] if crossing_90 else None,
            "first_recovery_90_transaction_index": crossing_90["transaction_index"] if crossing_90 else None,
            "first_recovery_90_log_index": crossing_90["log_index"] if crossing_90 else None,
            "first_recovery_90_timestamp": crossing_90["timestamp"] if crossing_90 else None,
            # Backward-compatible alias.  The explicit 80/90 fields above are
            # the preferred inputs for the gap notebook.
            "first_recovery_timestamp": crossing_90["timestamp"] if crossing_90 else None,
        }
        for label, seconds in WINDOW_SECONDS.items():
            gross, net = campaign.ratios_at(seconds)
            row[f"gross_readd_ratio_{label}"] = gross
            row[f"net_recovery_ratio_{label}"] = net

        net30 = row["net_recovery_ratio_30d"]
        observed_full_30d = followup_seconds >= WINDOW_SECONDS["30d"]
        row["is_censored_30d"] = bool(not observed_full_30d and net30 < recovery_threshold)
        row["persistent_non_return_scanned_pair_30d"] = bool(
            observed_full_30d and row["gross_readd_ratio_30d"] == 0
        )
        if net30 >= recovery_threshold:
            row["net_status_30d"] = "recovered_90"
        elif row["is_censored_30d"]:
            row["net_status_30d"] = "censored"
        elif net30 >= 0.80:
            row["net_status_30d"] = "recovered_80_to_90"
        else:
            row["net_status_30d"] = "partial_below_80"

        mint_scopes = [link["return_scope"] for link in campaign.links if link["event_type"] == "Mint"]
        row["same_pool_returned_within_30d"] = "Same_Pool" in mint_scopes
        row["cross_fee_returned_within_30d"] = "Cross_Fee_Tier" in mint_scopes
        campaign_rows.append(row)

    campaigns = pd.DataFrame(campaign_rows).sort_values("burn_block_number", kind="stable")
    links = pd.DataFrame(all_links)
    if not links.empty:
        links = links.sort_values(chain_order_columns(), kind="stable")
        if links.loc[links.event_type.eq("Mint"), "linked_event_id"].duplicated().any():
            raise AssertionError("A Mint was linked to more than one campaign")
    return campaigns.reset_index(drop=True), links.reset_index(drop=True)
