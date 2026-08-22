"""Tests for the matched-pool anomaly evidence helpers."""
from __future__ import annotations

import unittest
from decimal import Decimal

from scripts.anomaly_evidence import (
    build_daily_ledger,
    build_liquidity_rows,
    match_remove_mint_cycles,
)
from src.models import VerifiedPool


TARGET = "0x00000000000000000000000000000000000000aa"
QUOTE = "0x00000000000000000000000000000000000000bb"
POOL = "0x0000000000000000000000000000000000000101"
OWNER = "0x0000000000000000000000000000000000000202"
USER = "0x0000000000000000000000000000000000000303"


class _Hash(str):
    def hex(self):
        return str(self).removeprefix("0x")


def _pool() -> VerifiedPool:
    return VerifiedPool(
        chain_id=1,
        protocol="uniswap",
        version="v3",
        architecture="concentrated_pool",
        factory_address="0x0000000000000000000000000000000000000000",
        pool_address=POOL,
        custody_address=POOL,
        token0=TARGET,
        token1=QUOTE,
        verified=True,
    )


def _liquidity_log(
    tx: str,
    block: int,
    *,
    amount: int,
    amount0: int,
    amount1: int,
    tick_lower: int = -120,
    tick_upper: int = 120,
):
    return {
        "args": {
            "owner": OWNER,
            "sender": USER,
            "tickLower": tick_lower,
            "tickUpper": tick_upper,
            "amount": amount,
            "amount0": amount0,
            "amount1": amount1,
        },
        "blockNumber": block,
        "transactionHash": _Hash(tx),
        "logIndex": 1,
    }


class AnomalyEvidenceTest(unittest.TestCase):
    def test_raw_liquidity_keeps_position_key_and_matches_recreation(self):
        burn = _liquidity_log(
            "0x01", 10, amount=1_000, amount0=10_000_000, amount1=20_000_000
        )
        mint = _liquidity_log(
            "0x02", 12, amount=950, amount0=9_500_000, amount1=19_000_000
        )
        rows = build_liquidity_rows(
            [mint], [burn],
            pool=_pool(),
            target_token=TARGET,
            target_symbol="TEST",
            target_decimals=6,
            quote_symbol="QUOTE",
            quote_decimals=6,
            timestamps={10: 1_700_000_000, 12: 1_700_000_024},
            tx_from={"0x01": USER, "0x02": USER},
        )
        self.assertEqual(rows[0]["tick_lower"], -120)
        self.assertEqual(rows[0]["target_amount"], "10")
        cycles = match_remove_mint_cycles(rows, max_block_gap=10)
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0]["block_gap"], 2)
        self.assertEqual(cycles[0]["liquidity_recreated_ratio"], "0.95")
        self.assertFalse(cycles[0]["beneficial_owner_proven"])

    def test_cycle_rejects_different_ticks_or_large_liquidity_change(self):
        burn = _liquidity_log(
            "0x01", 10, amount=1_000, amount0=10_000_000, amount1=20_000_000
        )
        wrong_ticks = _liquidity_log(
            "0x02", 11, amount=1_000, amount0=10_000_000,
            amount1=20_000_000, tick_lower=-60, tick_upper=60,
        )
        large_change = _liquidity_log(
            "0x03", 12, amount=500, amount0=5_000_000, amount1=10_000_000
        )
        rows = build_liquidity_rows(
            [wrong_ticks, large_change], [burn],
            pool=_pool(), target_token=TARGET, target_symbol="TEST",
            target_decimals=6, quote_symbol="QUOTE", quote_decimals=6,
            timestamps={10: 1_700_000_000, 11: 1_700_000_012, 12: 1_700_000_024},
            tx_from={},
        )
        self.assertEqual(match_remove_mint_cycles(rows), [])

    def test_daily_ledger_uses_human_swap_amounts_and_forward_returns(self):
        swaps = [
            {"timestamp_utc": "2026-08-05T01:00:00+00:00", "direction": "SELL_TEST", "target_amount_abs": "5"},
            {"timestamp_utc": "2026-08-05T02:00:00+00:00", "direction": "BUY_TEST", "target_amount_abs": "2"},
        ]
        transfers = [
            {"timestamp_utc": "2026-08-05T01:00:00+00:00", "pool_delta_signed": "4"}
        ]
        liquidity = [
            {"date_utc": "2026-08-05", "event_type": "ADD", "target_amount": "9"},
            {"date_utc": "2026-08-05", "event_type": "REMOVE", "target_amount": "10"},
        ]
        cycles = [{"remove_date_utc": "2026-08-05", "remove_target_amount": "8"}]
        series = {
            "2026-08-05": {"price_close": 1.0, "price_return": 0.01},
            "2026-08-06": {"price_close": 1.1},
            "2026-08-07": {"price_close": 0.9},
            "2026-08-08": {"price_close": 1.2},
        }
        rows = build_daily_ledger(
            ["2026-08-05"], swaps, transfers, liquidity, cycles, series
        )
        row = rows[0]
        self.assertEqual(row["sell_volume_target"], "5")
        self.assertEqual(row["buy_volume_target"], "2")
        self.assertEqual(row["net_swap_to_pool_target"], "3")
        self.assertEqual(row["actual_transfer_net_to_pool_target"], "4")
        self.assertEqual(row["net_lp_flow_target"], "-1")
        self.assertEqual(row["swap_plus_lp_explained_flow_target"], "2")
        self.assertEqual(row["unexplained_transfer_residual_target"], "2")
        self.assertEqual(row["matched_remove_share"], 0.8)
        self.assertAlmostEqual(row["forward_return_1d"], 0.1)
        self.assertAlmostEqual(row["forward_return_2d"], -0.1)
        self.assertAlmostEqual(row["forward_return_3d"], 0.2)


if __name__ == "__main__":
    unittest.main()
