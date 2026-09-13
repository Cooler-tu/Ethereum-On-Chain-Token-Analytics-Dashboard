import unittest

from src.analysis.lp_capital_destination import (
    aggregate_edges,
    balance_disposition,
    block_at_or_after_timestamp,
    enumerate_nonce_blocks,
    first_horizon,
    reconcile_native_balance,
)


class CapitalDestinationTests(unittest.TestCase):
    def test_first_horizon(self):
        self.assertEqual(first_horizon(10, same_transaction=True), "same_transaction")
        self.assertEqual(first_horizon(3_600), "1h")
        self.assertEqual(first_horizon(3_601), "24h")
        self.assertEqual(first_horizon(31 * 86_400), "after_30d")

    def test_block_at_or_after_timestamp(self):
        times = {10: 100, 11: 112, 12: 112, 13: 130}
        got = block_at_or_after_timestamp(10, 13, 112, times.__getitem__)
        self.assertEqual(got, 11)

    def test_nonce_blocks_use_binary_search(self):
        consumed = {100: 7, 101: 7, 102: 8, 103: 8, 104: 9}
        got = enumerate_nonce_blocks("0xabc", 100, 104, lambda _a, b: consumed[b])
        self.assertEqual(got, [(7, 102), (8, 104)])

    def test_edges_do_not_merge_assets(self):
        rows = [
            {"source": "a", "target": "b", "asset": "ETH", "amount": 2,
             "evidence_type": "native_tx", "transaction_hash": "x"},
            {"source": "a", "target": "b", "asset": "ETH", "amount": 3,
             "evidence_type": "native_tx", "transaction_hash": "y"},
            {"source": "a", "target": "b", "asset": "WETH", "amount": 4,
             "evidence_type": "erc20_transfer", "transaction_hash": "z"},
        ]
        got = sorted(aggregate_edges(rows), key=lambda x: x["asset"])
        self.assertEqual(got[0]["amount"], 5)
        self.assertEqual(got[0]["event_count"], 2)
        self.assertEqual(got[1]["amount"], 4)

    def test_balance_disposition_does_not_claim_unit_provenance(self):
        got = balance_disposition(10, 90, 100, 0)
        self.assertTrue(got["wallet_balance_fully_disposed"])
        self.assertAlmostEqual(got["outbound_over_collected_ratio"], 100 / 90)

    def test_native_balance_reconciliation_keeps_other_inflow_unattributed(self):
        got = reconcile_native_balance(
            post_collect_eth=0.07,
            weth_unwrapped=2.78,
            other_native_inflow=20.56,
            native_sent=23.40,
            subsequent_gas=0.009,
            closing_eth=0.001,
        )
        self.assertAlmostEqual(got["expected_closing_eth"], 0.001)
        self.assertAlmostEqual(got["reconciliation_error_eth"], 0.0)


if __name__ == "__main__":
    unittest.main()
