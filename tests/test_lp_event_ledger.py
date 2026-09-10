import unittest

import pandas as pd

from src.analysis.lp_event_ledger import (
    build_campaign_ledger,
    build_event_readd_links,
    weth_equivalent,
)


def event(
    event_id,
    kind,
    timestamp,
    block,
    *,
    starts=False,
    turbo=0.0,
    weth=0.0,
    pool="pool-a",
    wallet="wallet-a",
    tx=None,
    tx_index=0,
    log_index=0,
):
    return {
        "event_id": event_id,
        "event_type": kind,
        "wallet_address": wallet,
        "pool_address": pool,
        "pair_key": "turbo/weth",
        "fee": 10_000 if pool == "pool-a" else 3_000,
        "block_number": block,
        "transaction_index": tx_index,
        "log_index": log_index,
        "transaction_hash": tx or f"tx-{event_id}",
        "timestamp": timestamp,
        "turbo_amount": turbo,
        "weth_amount": weth,
        "price_weth_per_turbo": 0.01,
        "starts_campaign": starts,
        "nft_id": event_id,
    }


class LpEventLedgerTests(unittest.TestCase):
    def test_weth_equivalent_uses_fixed_anchor_price(self):
        self.assertAlmostEqual(weth_equivalent(20, 3, 0.1), 5.0)

    def test_multiple_mints_are_used_once_and_recover_one_campaign(self):
        rows = [
            event("b1", "Burn", 0, 1, starts=True, weth=10),
            event("m1", "Mint", 100, 2, weth=4),
            event("m2", "Mint", 200, 3, weth=5),
            event("b2", "Burn", 300, 4, starts=True, weth=8),
            event("m3", "Mint", 400, 5, weth=8),
        ]
        campaigns, links = build_campaign_ledger(pd.DataFrame(rows), 40 * 86_400)
        self.assertEqual(len(campaigns), 2)
        self.assertEqual(links.loc[links.event_type.eq("Mint"), "linked_event_id"].nunique(), 3)
        self.assertAlmostEqual(campaigns.iloc[0].net_recovery_ratio_30d, 0.9)
        self.assertEqual(campaigns.iloc[0].net_status_30d, "recovered_90")
        self.assertEqual(campaigns.iloc[0].first_recovery_80_event_id, "m2")
        self.assertEqual(campaigns.iloc[0].first_recovery_90_event_id, "m2")
        self.assertEqual(campaigns.iloc[1].net_status_30d, "recovered_90")

    def test_later_burn_reduces_net_but_not_gross_ratio(self):
        rows = [
            event("b1", "Burn", 0, 1, starts=True, weth=10),
            event("m1", "Mint", 100, 2, weth=8),
            event("b2", "Burn", 200, 3, starts=False, weth=3),
        ]
        campaigns, _ = build_campaign_ledger(pd.DataFrame(rows), 40 * 86_400)
        self.assertAlmostEqual(campaigns.iloc[0].gross_readd_ratio_30d, 0.8)
        self.assertAlmostEqual(campaigns.iloc[0].net_recovery_ratio_30d, 0.5)
        self.assertEqual(campaigns.iloc[0].first_recovery_80_event_id, "m1")
        self.assertIsNone(campaigns.iloc[0].first_recovery_90_event_id)

    def test_partial_late_campaign_is_censored(self):
        rows = [
            event("b1", "Burn", 20 * 86_400, 1, starts=True, weth=10),
            event("m1", "Mint", 21 * 86_400, 2, weth=5),
        ]
        campaigns, _ = build_campaign_ledger(pd.DataFrame(rows), 25 * 86_400)
        self.assertTrue(campaigns.iloc[0].is_censored_30d)
        self.assertEqual(campaigns.iloc[0].net_status_30d, "censored")

    def test_same_transaction_and_cross_fee_are_preserved(self):
        rows = [
            event("b1", "Burn", 100, 10, starts=True, weth=10, tx="same", log_index=1),
            event("m1", "Mint", 100, 10, weth=10, pool="pool-b", tx="same", log_index=2),
        ]
        campaigns, links = build_campaign_ledger(pd.DataFrame(rows), 40 * 86_400)
        self.assertTrue(links.iloc[0].same_transaction)
        self.assertTrue(links.iloc[0].same_block)
        self.assertEqual(links.iloc[0].return_scope, "Cross_Fee_Tier")
        self.assertTrue(campaigns.iloc[0].cross_fee_returned_within_30d)

    def test_event_links_use_latest_burn_and_never_reuse_a_mint(self):
        rows = [
            event("b1", "Burn", 0, 1, starts=True, weth=10),
            event("m1", "Mint", 100, 2, weth=4),
            event("b2", "Burn", 200, 3, starts=True, weth=8),
            event("m2", "Mint", 300, 4, weth=8),
        ]
        links = build_event_readd_links(pd.DataFrame(rows))
        self.assertEqual(links.origin_burn_event_id.tolist(), ["b1", "b2"])
        self.assertEqual(links.mint_event_id.nunique(), 2)


if __name__ == "__main__":
    unittest.main()
