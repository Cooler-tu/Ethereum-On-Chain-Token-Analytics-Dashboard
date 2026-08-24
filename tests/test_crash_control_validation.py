import unittest

from scripts.crash_control_validation import (
    build_future_return_pairs,
    independent_moving_block_difference_ci,
)
from scripts.time_series_correlation import spearman


class CrashControlValidationTests(unittest.TestCase):
    def test_pairs_require_observed_prices_at_both_endpoints(self):
        rows = []
        for hour in range(27):
            rows.append({
                "bucket_start": hour * 3600,
                "price_close": 1.0 + hour / 100,
                "price_trade_count": 1 if hour in {0, 1, 24} else 0,
                "actual_transfer_net_ratio": float(hour),
            })
        xs, ys, timestamps = build_future_return_pairs(
            rows, "actual_transfer_net_ratio", 24, absolute_outcome=False
        )
        self.assertEqual(xs, [0.0])
        self.assertEqual(len(ys), 1)
        self.assertEqual(timestamps, [0])

    def test_absolute_return_is_used_for_activity_test(self):
        rows = [
            {"bucket_start": 0, "price_close": 2.0, "price_trade_count": 1, "gross_lp_activity_ratio": 3.0},
            {"bucket_start": 3600, "price_close": 1.0, "price_trade_count": 1, "gross_lp_activity_ratio": 0.0},
        ]
        xs, ys, _ = build_future_return_pairs(
            rows, "gross_lp_activity_ratio", 1, absolute_outcome=True
        )
        self.assertEqual(xs, [3.0])
        self.assertGreater(ys[0], 0)

    def test_difference_bootstrap_is_deterministic(self):
        xs = [float(value) for value in range(20)]
        positive = [value + (value % 3) / 10 for value in xs]
        negative = [-value + (value % 2) / 10 for value in xs]
        first = independent_moving_block_difference_ci(
            xs, positive, xs, negative, spearman,
            repetitions=100, alpha=0.05, block_length=4, seed=7,
        )
        second = independent_moving_block_difference_ci(
            xs, positive, xs, negative, spearman,
            repetitions=100, alpha=0.05, block_length=4, seed=7,
        )
        self.assertEqual(first, second)
        self.assertGreater(first[0], 0)


if __name__ == "__main__":
    unittest.main()
