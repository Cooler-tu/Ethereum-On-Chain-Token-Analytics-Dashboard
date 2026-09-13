"""Preserve the mixed aggregate-Mint / row-level withdrawal SQL contract."""
from __future__ import annotations

import unittest

from src.data.dune import _load_sections


class LiquidityAggregationSqlTest(unittest.TestCase):
    def test_v2_v3_mints_are_pool_block_aggregates_without_actors(self):
        sections = _load_sections()
        for name in (
            "liquidity_uniswap_v2_mint",
            "liquidity_uniswap_v3_mint",
        ):
            sql = sections[name].lower()
            self.assertIn("group by evt_block_number, contract_address", sql)
            self.assertIn("count(*) as event_count", sql)
            self.assertIn("'pool_block' as aggregation_scope", sql)
            self.assertNotIn(" as actor", sql)
            self.assertNotIn(" as recipient", sql)

    def test_burns_keep_transaction_and_actor_evidence(self):
        for name in ('liquidity_uniswap_v2_burn','liquidity_uniswap_v3_burn'):
            sql = _load_sections()[name].lower()
            self.assertIn('evt_tx_hash',sql)
            self.assertIn('evt_index as log_index',sql)
            self.assertIn(' as actor',sql)
            self.assertIn("'row' as aggregation_scope",sql)
            self.assertNotIn('sum(',sql)

    def test_v4_keeps_pool_position_and_transaction_evidence(self):
        sql = _load_sections()["liquidity_uniswap_v4_modify"].lower()
        self.assertIn('e.evt_tx_hash',sql)
        self.assertIn('e.evt_index as log_index',sql)
        self.assertIn('e.id as varchar',sql)
        self.assertIn(' as actor',sql)
        self.assertIn(' as salt',sql)
        self.assertIn("'row' as aggregation_scope",sql)
        self.assertNotIn('group by',sql)


if __name__ == "__main__":
    unittest.main()
