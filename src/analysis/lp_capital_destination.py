"""Pure helpers for LP capital-destination case studies.

The functions in this module deliberately separate observable transfers from
identity or ownership claims.  A token is fungible, so a post-Collect balance
path can support a balance-disposition statement but not unit-level provenance.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


HORIZONS_SECONDS = {
    "same_transaction": 0,
    "1h": 60 * 60,
    "24h": 24 * 60 * 60,
    "7d": 7 * 24 * 60 * 60,
    "30d": 30 * 24 * 60 * 60,
}


def first_horizon(delta_seconds: int, *, same_transaction: bool = False) -> str:
    """Return the smallest reporting horizon containing an observed action."""
    if same_transaction:
        return "same_transaction"
    if delta_seconds < 0:
        raise ValueError("follow-up action cannot precede the origin event")
    for label in ("1h", "24h", "7d", "30d"):
        if delta_seconds <= HORIZONS_SECONDS[label]:
            return label
    return "after_30d"


def block_at_or_after_timestamp(
    start_block: int,
    end_block: int,
    target_timestamp: int,
    timestamp_for_block: Callable[[int], int],
) -> int:
    """Find the first block whose timestamp is at least ``target_timestamp``."""
    if start_block > end_block:
        raise ValueError("start_block must not exceed end_block")
    if timestamp_for_block(end_block) < target_timestamp:
        raise ValueError("target timestamp lies after the available block range")
    left, right = int(start_block), int(end_block)
    while left < right:
        middle = (left + right) // 2
        if timestamp_for_block(middle) < target_timestamp:
            left = middle + 1
        else:
            right = middle
    return left


def enumerate_nonce_blocks(
    address: str,
    start_block: int,
    end_block: int,
    transaction_count: Callable[[str, int], int],
) -> list[tuple[int, int]]:
    """Locate each sender nonce without scanning every block.

    Returns ``(nonce, first block where that nonce has been consumed)``.  The
    caller still verifies the transaction sender and nonce in that block.
    """
    first_nonce = int(transaction_count(address, start_block))
    final_nonce = int(transaction_count(address, end_block))
    located: list[tuple[int, int]] = []
    floor = int(start_block)
    for nonce in range(first_nonce, final_nonce):
        left, right = floor, int(end_block)
        while left < right:
            middle = (left + right) // 2
            if int(transaction_count(address, middle)) >= nonce + 1:
                right = middle
            else:
                left = middle + 1
        located.append((nonce, left))
        floor = left
    return located


def aggregate_edges(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate observable edges without merging different assets or evidence."""
    grouped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (
            str(row["source"]),
            str(row["target"]),
            str(row["asset"]),
            str(row["evidence_type"]),
        )
        if key not in grouped:
            grouped[key] = {
                "source": key[0],
                "target": key[1],
                "asset": key[2],
                "evidence_type": key[3],
                "amount": 0.0,
                "event_count": 0,
                "transaction_hashes": [],
            }
        item = grouped[key]
        item["amount"] += float(row["amount"])
        item["event_count"] += 1
        tx_hash = str(row.get("transaction_hash") or "")
        if tx_hash and tx_hash not in item["transaction_hashes"]:
            item["transaction_hashes"].append(tx_hash)
    return list(grouped.values())


def balance_disposition(
    opening_balance: float,
    collected_amount: float,
    outbound_amount: float,
    closing_balance: float,
) -> dict[str, float | bool]:
    """Summarize wallet-level disposition while preserving fungibility limits."""
    available = float(opening_balance) + float(collected_amount)
    tolerance = max(1e-12, abs(available) * 1e-9)
    return {
        "opening_balance": float(opening_balance),
        "collected_amount": float(collected_amount),
        "available_after_collect": available,
        "outbound_amount": float(outbound_amount),
        "closing_balance": float(closing_balance),
        "wallet_balance_fully_disposed": closing_balance <= tolerance,
        "outbound_over_collected_ratio": (
            float(outbound_amount) / float(collected_amount)
            if collected_amount > 0
            else float("nan")
        ),
    }


def reconcile_native_balance(
    post_collect_eth: float,
    weth_unwrapped: float,
    other_native_inflow: float,
    native_sent: float,
    subsequent_gas: float,
    closing_eth: float,
) -> dict[str, float]:
    """Reconcile the wallet's native-ETH balance without assigning provenance.

    ``other_native_inflow`` is deliberately a residual balance-flow term.  It
    may be consistent with nearby swaps, but the balance equation alone cannot
    attribute it to a particular token or internal contract call.
    """
    expected_closing = (
        float(post_collect_eth)
        + float(weth_unwrapped)
        + float(other_native_inflow)
        - float(native_sent)
        - float(subsequent_gas)
    )
    return {
        "post_collect_eth": float(post_collect_eth),
        "weth_unwrapped": float(weth_unwrapped),
        "other_native_inflow": float(other_native_inflow),
        "native_sent": float(native_sent),
        "subsequent_gas": float(subsequent_gas),
        "expected_closing_eth": expected_closing,
        "observed_closing_eth": float(closing_eth),
        "reconciliation_error_eth": expected_closing - float(closing_eth),
    }
