import unittest

import pandas as pd

from src.analysis.lp_gap_impact import (
    build_gap_intervals,
    campaign_cluster_bootstrap,
    greedy_size_match,
    label_gap_swaps,
    mark_full_gap_contamination,
)


class LpGapImpactTests(unittest.TestCase):
    def campaigns(self):
        return pd.DataFrame([{
            "campaign_id": "c1", "wallet_address": "w", "origin_pool_address": "p",
            "burn_timestamp": 100, "burn_block_number": 10,
            "burn_transaction_index": 1, "burn_log_index": 5,
            "first_recovery_80_event_id": "m80", "first_recovery_80_timestamp": 200,
            "first_recovery_80_block_number": 20, "first_recovery_80_transaction_index": 1,
            "first_recovery_80_log_index": 5,
            "first_recovery_90_event_id": "m90", "first_recovery_90_timestamp": 300,
            "first_recovery_90_block_number": 30, "first_recovery_90_transaction_index": 1,
            "first_recovery_90_log_index": 5,
        }])

    def swaps(self):
        return pd.DataFrame([
            {"swap_event_id": "before", "pool_address": "p", "block_number": 10, "transaction_index": 1, "log_index": 4, "timestamp": 100},
            {"swap_event_id": "inside", "pool_address": "p", "block_number": 15, "transaction_index": 0, "log_index": 1, "timestamp": 150},
            {"swap_event_id": "at80", "pool_address": "p", "block_number": 20, "transaction_index": 1, "log_index": 5, "timestamp": 200},
            {"swap_event_id": "between", "pool_address": "p", "block_number": 25, "transaction_index": 0, "log_index": 1, "timestamp": 250},
        ])

    def test_exact_chain_boundaries_distinguish_80_and_90(self):
        intervals = build_gap_intervals(self.campaigns(), followup_end_timestamp=100_000)
        labeled = label_gap_swaps(self.swaps(), intervals)
        at_1h = labeled[labeled.horizon.eq("1h")]
        self.assertEqual(set(at_1h[at_1h.threshold_pct.eq(80)].swap_event_id), {"inside"})
        self.assertEqual(set(at_1h[at_1h.threshold_pct.eq(90)].swap_event_id), {"inside", "at80", "between"})

    def test_full_gap_contamination_uses_90_boundary(self):
        marked = mark_full_gap_contamination(self.swaps(), self.campaigns(), 100_000)
        self.assertEqual(self.swaps().loc[marked, "swap_event_id"].tolist(), ["inside", "at80", "between"])

    def test_no_return_campaign_is_not_in_treated_gap_swaps(self):
        campaign = self.campaigns().copy()
        for name in [
            "first_recovery_80_event_id", "first_recovery_80_timestamp",
            "first_recovery_80_block_number", "first_recovery_80_transaction_index",
            "first_recovery_80_log_index", "first_recovery_90_event_id",
            "first_recovery_90_timestamp", "first_recovery_90_block_number",
            "first_recovery_90_transaction_index", "first_recovery_90_log_index",
        ]:
            campaign[name] = None
        intervals = build_gap_intervals(campaign, followup_end_timestamp=100_000)
        self.assertTrue(label_gap_swaps(self.swaps(), intervals).empty)

    def test_matching_is_same_direction_pool_and_without_reuse(self):
        treated = pd.DataFrame([
            {"swap_event_id": "t1", "pool_address": "p", "direction": "buy", "notional_weth": 10.0, "timestamp": 10, "threshold_pct": 90, "horizon": "1h", "primary_campaign_id": "c1", "price_impact_bps": 5.0},
            {"swap_event_id": "t2", "pool_address": "p", "direction": "buy", "notional_weth": 9.0, "timestamp": 20, "threshold_pct": 90, "horizon": "1h", "primary_campaign_id": "c2", "price_impact_bps": 4.0},
        ])
        controls = pd.DataFrame([
            {"swap_event_id": "x", "pool_address": "p", "direction": "buy", "notional_weth": 9.5, "timestamp": 30, "price_impact_bps": 2.0},
            {"swap_event_id": "wrong", "pool_address": "p", "direction": "sell", "notional_weth": 10.0, "timestamp": 30, "price_impact_bps": 1.0},
        ])
        pairs = greedy_size_match(treated, controls, .25)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs.iloc[0].control_swap_event_id, "x")

    def test_cluster_bootstrap_reports_campaign_count(self):
        pairs = pd.DataFrame({
            "primary_campaign_id": ["a", "a", "b"],
            "excess_price_impact_bps": [1.0, 3.0, 5.0],
        })
        result = campaign_cluster_bootstrap(pairs, iterations=200, seed=1)
        self.assertEqual(result["campaigns"], 2)
        self.assertAlmostEqual(result["estimate"], 3.5)


if __name__ == "__main__":
    unittest.main()
