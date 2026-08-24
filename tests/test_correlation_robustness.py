"""Tests for correlation robustness helpers."""
from __future__ import annotations

import unittest

from scripts.correlation_robustness import (
    aggregate_rows,
    benjamini_hochberg,
    block_permutation_p_value,
    circular_shift_p_value,
    moving_block_bootstrap_ci,
    scan_tests,
    select_best_tests,
)
from scripts.time_series_correlation import pearson


def _row(index: int) -> dict:
    return {
        "bucket_start": index * 3600,
        "bucket_end": (index + 1) * 3600,
        "bucket_seconds": 3600,
        "price_open": 10 + index,
        "price_high": 11 + index,
        "price_low": 9 + index,
        "price_close": 10 + index,
        "price_vwap": 10 + index,
        "tvl_token_close": 100 + index * 10,
        "volume_token": 5 + index,
        "liquidity_added_token": 3 + index,
        "liquidity_removed_token": 1 + index,
        "net_lp_flow_token": 2,
        "swap_count": 1,
        "price_trade_count": 1,
        "lp_add_event_count": 1,
        "lp_remove_event_count": 1,
    }


class CorrelationRobustnessTest(unittest.TestCase):
    def test_aggregate_recomputes_state_flow_and_derivatives(self):
        rows = aggregate_rows([_row(i) for i in range(4)], 2)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["bucket_seconds"], 7200)
        self.assertEqual(rows[0]["price_open"], 10)
        self.assertEqual(rows[0]["price_close"], 11)
        self.assertEqual(rows[0]["volume_token"], 11)
        self.assertEqual(rows[0]["tvl_token_close"], 110)
        self.assertIsNone(rows[0]["price_return"])
        self.assertAlmostEqual(rows[1]["price_return"], 13 / 11 - 1)
        self.assertAlmostEqual(rows[1]["tvl_change"], 130 / 110 - 1)
        self.assertAlmostEqual(rows[1]["volume_turnover"], 15 / 110)
        self.assertAlmostEqual(rows[1]["net_lp_flow_ratio"], 4 / 110)
        self.assertAlmostEqual(rows[1]["withdrawal_ratio"], 7 / 110)

    def test_nullable_lp_flows_remain_unknown(self):
        rows = [_row(0), _row(1)]
        for row in rows:
            row["liquidity_added_token"] = None
            row["liquidity_removed_token"] = None
            row["net_lp_flow_token"] = None
        combined = aggregate_rows(rows, 2)[0]
        self.assertIsNone(combined["liquidity_added_token"])
        self.assertIsNone(combined["liquidity_removed_token"])
        self.assertIsNone(combined["net_lp_flow_token"])

    def test_bh_q_values_are_monotone_and_keep_missing(self):
        q = benjamini_hochberg([0.01, 0.04, 0.03, None])
        self.assertAlmostEqual(q[0], 0.03)
        self.assertAlmostEqual(q[1], 0.04)
        self.assertAlmostEqual(q[2], 0.04)
        self.assertIsNone(q[3])

    def test_circular_shift_and_block_bootstrap(self):
        xs = [float(i) for i in range(12)]
        ys = [2 * value + 1 for value in xs]
        self.assertAlmostEqual(circular_shift_p_value(xs, ys, pearson), 1 / 12)
        low, high, valid = moving_block_bootstrap_ci(
            xs, ys, pearson,
            repetitions=200, alpha=0.05, block_length=3, seed=7,
        )
        self.assertEqual(valid, 200)
        self.assertAlmostEqual(low, 1.0)
        self.assertAlmostEqual(high, 1.0)
        p_value = block_permutation_p_value(
            xs, ys, pearson,
            repetitions=199, block_length=3, seed=9,
        )
        self.assertIsNotNone(p_value)
        self.assertLessEqual(p_value, 0.05)

    def test_scan_applies_fdr_and_best_rows_get_ci(self):
        base = []
        for index in range(24):
            row = _row(index)
            row["price_close"] = 100 + index * index
            row["tvl_token_close"] = 200 - index
            base.append(row)
        variants = {1: aggregate_rows(base, 1), 2: aggregate_rows(base, 2)}
        tests = scan_tests(
            variants,
            ("price_return", "tvl_change", "volume_turnover"),
            max_horizon_base_buckets=2,
            min_pairs=6,
            permutation_repetitions=199,
            permutation_block_length=2,
            seed=11,
        )
        self.assertTrue(tests)
        self.assertTrue(any(row["q_value_bh_global"] is not None for row in tests))
        self.assertTrue(any("q_value_bh_zero_lag_family" in row for row in tests))
        best = select_best_tests(
            tests, variants,
            bootstrap_repetitions=200,
            alpha=0.05,
            block_length=2,
            seed=11,
        )
        self.assertEqual(len(best), 12)
        self.assertTrue(all("bootstrap_ci_low" in row for row in best))
        self.assertTrue(all("fdr_significant_family" in row for row in best))


if __name__ == "__main__":
    unittest.main()
