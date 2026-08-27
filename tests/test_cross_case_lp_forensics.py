"""Tests for cross-case LP-flow forensic selection and amount handling."""
from __future__ import annotations

import unittest

from scripts.cross_case_lp_forensics import (
    _target_quote_amounts,
    select_anomaly_hours,
)


TARGET = "0x00000000000000000000000000000000000000aa"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"


class CrossCaseLPForensicsTest(unittest.TestCase):
    def test_selects_positive_lp_negative_future_return_and_ranks_ratio(self):
        rows = []
        prices = [10, 9, 10, 8, 12]
        ratios = [0.1, -0.4, 0.3, 0.2, 0.0]
        for hour, (price, ratio) in enumerate(zip(prices, ratios)):
            rows.append({
                "bucket_start": f"2026-01-01T0{hour}:00:00+00:00",
                "price_trade_count": 1,
                "price_close": price,
                "net_lp_flow_ratio": ratio,
            })
        selected = select_anomaly_hours(rows, horizon_hours=1)
        self.assertEqual([row["net_lp_flow_ratio"] for row in selected], [0.3, 0.1])
        self.assertEqual([row["rank"] for row in selected], [1, 2])

    def test_target_quote_amounts_supports_target_on_either_side(self):
        event = {"token0_amount": "2500000", "token1_amount": "3000000000000000000"}
        target, quote = _target_quote_amounts(
            event,
            {"token0": TARGET, "token1": WETH},
            target_token=TARGET,
            target_decimals=6,
        )
        self.assertEqual(str(target), "2.5")
        self.assertEqual(str(quote), "3")
        target, quote = _target_quote_amounts(
            event,
            {"token0": WETH, "token1": TARGET},
            target_token=TARGET,
            target_decimals=18,
        )
        self.assertEqual(str(target), "3")
        self.assertEqual(str(quote), "2.5E-12")


if __name__ == "__main__":
    unittest.main()
