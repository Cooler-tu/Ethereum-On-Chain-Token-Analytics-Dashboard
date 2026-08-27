"""Tests for targeted V3 position tracing helpers."""
from __future__ import annotations

import unittest

from scripts.trace_v3_positions import (
    build_selected_position_cycles,
    inventory_shape,
    match_position_manager_event,
    tick_range_weth_per_target,
)


class TraceV3PositionsTest(unittest.TestCase):
    def test_exact_amount_match_respects_direction(self):
        manager = [
            {"event_type": "DecreaseLiquidity", "tokenId": 1, "amount0": 10, "amount1": 20},
            {"event_type": "IncreaseLiquidity", "tokenId": 2, "amount0": 10, "amount1": 20},
        ]
        used: set[int] = set()
        matched = match_position_manager_event(
            {"event_type": "Mint", "amount0": 10, "amount1": 20}, manager, used
        )
        self.assertEqual(matched["tokenId"], 2)
        self.assertEqual(used, {1})

    def test_tick_range_and_inventory_shape_for_target_token0(self):
        low, high = tick_range_weth_per_target(
            0, 100, target_is_token0=True, target_decimals=18
        )
        self.assertAlmostEqual(low, 1.0)
        self.assertGreater(high, 1.0)
        self.assertEqual(inventory_shape(0.9, low, high), "target_only_below_range")
        self.assertEqual(inventory_shape(1.005, low, high), "two_sided_in_range")
        self.assertEqual(inventory_shape(2.0, low, high), "weth_only_above_range")

    def test_target_token1_reverses_tick_price(self):
        low, high = tick_range_weth_per_target(
            0, 100, target_is_token0=False, target_decimals=18
        )
        self.assertLess(low, 1.0)
        self.assertAlmostEqual(high, 1.0)

    def test_builds_same_nft_opposite_action_cycle(self):
        base = {
            "case": "FTT",
            "nft_token_id": 12,
            "owner_at_block": "0xabc",
            "tx_from": "0xabc",
            "tick_lower": -100,
            "tick_upper": 100,
        }
        cycles = build_selected_position_cycles([
            {**base, "pool_event": "Mint", "block_number": 10, "transaction_hash": "0x1"},
            {**base, "pool_event": "Burn", "block_number": 15, "transaction_hash": "0x2"},
        ])
        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0]["block_gap"], 5)
        self.assertTrue(cycles[0]["same_owner_at_block"])


if __name__ == "__main__":
    unittest.main()
