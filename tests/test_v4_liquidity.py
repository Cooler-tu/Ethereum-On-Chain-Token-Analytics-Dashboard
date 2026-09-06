"""V4 ModifyLiquidity amount enrichment from ticks + sqrt price."""
from __future__ import annotations

import unittest

from src.analysis.v3_math import get_amounts_for_liquidity, tick_to_sqrt_price_x96

TARGET = "0x44b28991B167582F18BA0259e0173176ca125505"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
from src.indexer.dune_index import (
    _normalize_liquidity,
    apply_v3_npm_nft_owners,
    apply_v3_tx_senders,
    apply_v4_pm_nft_owners,
    attach_v3_burn_token_ids,
    enrich_v4_modify_amounts,
    sqrt_price_rows_from_swaps,
    unpack_balance_delta,
)


class V4ModifyAmountTest(unittest.TestCase):
    def test_unpack_balance_delta_splits_packed_int256(self):
        amount0, amount1 = unpack_balance_delta(
            "398809966090958707568410893300400072990188708905592551"
        )
        self.assertEqual(amount0, 1171997155478875)
        self.assertEqual(amount1, 102357410430298964600551)

    def test_caller_delta_includes_fees_and_beats_tick_math(self):
        rows = enrich_v4_modify_amounts(
            [{
                "pool_id": "0x" + "ab" * 32,
                "block_number": 100,
                "liquidity_delta": str(10**18),
                "tick_lower": -60,
                "tick_upper": 60,
                "caller_delta": str((5 * 10**18 << 128) + (7 * 10**18)),
                "fees_accrued": str((10**17 << 128) + (2 * 10**17)),
            }],
            [],
        )
        self.assertEqual(rows[0]["amount_source"], "caller_delta")
        self.assertEqual(rows[0]["token0_amount"], str(5 * 10**18))
        self.assertEqual(rows[0]["token1_amount"], str(7 * 10**18))
        self.assertEqual(rows[0]["fee0_amount"], str(10**17))
        self.assertEqual(rows[0]["fee1_amount"], str(2 * 10**17))
        normalized = _normalize_liquidity(rows[0], "liquidity_uniswap_v4_modify")
        self.assertEqual(normalized["amount_source"], "caller_delta")
        self.assertEqual(normalized["fee0_amount"], str(10**17))
        self.assertEqual(normalized["fee1_amount"], str(2 * 10**17))

    def test_in_range_modify_gets_both_token_amounts_and_keeps_sender(self):
        sqrt_price = tick_to_sqrt_price_x96(0)
        amount0, amount1 = get_amounts_for_liquidity(sqrt_price, -60, 60, 10**18)
        self.assertGreater(amount0, 0)
        self.assertGreater(amount1, 0)

        rows = enrich_v4_modify_amounts(
            [
                {
                    "pool_id": "0x" + "ab" * 32,
                    "block_number": 100,
                    "liquidity_delta": str(10**18),
                    "tick_lower": -60,
                    "tick_upper": 60,
                    "actor": "0x1111111111111111111111111111111111111111",
                }
            ],
            [{"pool_id": "0x" + "ab" * 32, "block_number": 90, "sqrt_price_x96": str(sqrt_price)}],
        )
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["amounts_available"])
        self.assertEqual(rows[0]["token0_amount"], str(amount0))
        self.assertEqual(rows[0]["token1_amount"], str(amount1))

        normalized = _normalize_liquidity(rows[0], "liquidity_uniswap_v4_modify")
        self.assertTrue(normalized["amounts_available"])
        self.assertEqual(normalized["quantification_status"], "quantified")
        self.assertEqual(
            normalized["actor"], "0x1111111111111111111111111111111111111111"
        )
        self.assertEqual(normalized["event_type"], "LIQUIDITY_ADD")

    def test_swap_implied_sqrt_enriches_same_pair_pool(self):
        pool_id = "0x" + "ab" * 32
        prices = sqrt_price_rows_from_swaps(
            [{
                "block_number": 90,
                "token0_address": TARGET,
                "token1_address": WETH,
                "token0_amount": str(10**18),
                "token1_amount": str(2 * 10**18),
            }],
            {pool_id: (TARGET.lower(), WETH.lower())},
        )
        self.assertEqual(len(prices), 1)
        rows = enrich_v4_modify_amounts(
            [{
                "pool_id": pool_id,
                "block_number": 100,
                "liquidity_delta": str(10**18),
                "tick_lower": -60,
                "tick_upper": 60,
            }],
            prices,
        )
        self.assertTrue(rows[0]["amounts_available"])

    def test_missing_price_stays_delta_only(self):
        rows = enrich_v4_modify_amounts(
            [
                {
                    "pool_id": "0x" + "cd" * 32,
                    "block_number": 100,
                    "liquidity_delta": "123",
                    "tick_lower": -60,
                    "tick_upper": 60,
                    "actor": "0x2222222222222222222222222222222222222222",
                }
            ],
            [],
        )
        normalized = _normalize_liquidity(rows[0], "liquidity_uniswap_v4_modify")
        self.assertFalse(normalized["amounts_available"])
        self.assertEqual(normalized["quantification_status"], "liquidity_delta_only")
        self.assertEqual(
            normalized["actor"], "0x2222222222222222222222222222222222222222"
        )


class V4PositionManagerOwnerTest(unittest.TestCase):
    def test_same_tx_transfer_replaces_position_manager_sender(self):
        pm = "0xbd216513d74C8cf14cf4747E6AaA6420FF64ee9e"
        owner = "0x1111111111111111111111111111111111111111"
        events = [{
            "version": "v4",
            "actor": pm,
            "salt": hex(99),
            "block_number": 50,
            "log_index": 3,
            "transaction_hash": "0xabc",
        }]
        resolved = apply_v4_pm_nft_owners(
            events,
            [{
                "nft_token_id": "99",
                "owner": owner,
                "transaction_hash": "0xABC",
                "block_number": 50,
                "log_index": 8,
            }],
        )
        self.assertEqual(resolved, 1)
        self.assertEqual(events[0]["actor"], owner)
        self.assertEqual(events[0]["actor_source"], "v4_pm_nft_owner")


class V3PositionManagerOwnerTest(unittest.TestCase):
    def test_decrease_liquidity_token_id_replaces_npm_and_collect_recipient(self):
        npm = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        owner = "0x1111111111111111111111111111111111111111"
        collect = "0x2222222222222222222222222222222222222222"
        pool = "0x3333333333333333333333333333333333333333"
        events = [
            {
                "version": "v3",
                "event_type": "LIQUIDITY_REMOVE",
                "actor": npm,
                "pool_address": pool,
                "transaction_hash": "0xabc",
                "block_number": 50,
                "log_index": 3,
            },
            {
                "version": "v3",
                "event_type": "LIQUIDITY_REMOVE",
                "actor": collect,
                "pool_address": pool,
                "transaction_hash": "0xdef",
                "block_number": 51,
                "log_index": 4,
            },
        ]
        attached = attach_v3_burn_token_ids(
            events,
            [
                {
                    "transaction_hash": "0xABC",
                    "log_index": 3,
                    "pool_address": pool,
                    "nft_token_id": "88",
                },
                {
                    "transaction_hash": "0xDEF",
                    "log_index": 4,
                    "pool_address": pool,
                    "nft_token_id": "89",
                },
            ],
        )
        self.assertEqual(attached, 2)
        resolved = apply_v3_npm_nft_owners(
            events,
            [
                {
                    "nft_token_id": "88",
                    "owner": owner,
                    "transaction_hash": "0xabc",
                    "block_number": 50,
                    "log_index": 9,
                },
                {
                    "nft_token_id": "89",
                    "owner": owner,
                    "transaction_hash": "0xdef",
                    "block_number": 51,
                    "log_index": 10,
                },
            ],
        )
        self.assertEqual(resolved, 2)
        self.assertEqual(events[0]["actor"], owner)
        self.assertEqual(events[1]["actor"], owner)
        self.assertEqual(events[0]["actor_source"], "v3_npm_nft_owner")
        self.assertEqual(events[0]["nft_token_id"], 88)

    def test_contract_actor_replaced_by_tx_signer(self):
        bot = "0x1f2F10D1C40777AE1Da742455c65828FF36Df387"
        signer = "0xae2Fc483527B8EF99EB5D9B44875F005ba1FaE13"
        events = [{
            "version": "v3",
            "event_type": "LIQUIDITY_REMOVE",
            "actor": bot,
            "transaction_hash": "0xabc",
        }]
        resolved = apply_v3_tx_senders(
            events,
            [{"tx_hash": "0xABC", "gas_payer": signer}],
            contract_actors={bot.lower()},
        )
        self.assertEqual(resolved, 1)
        self.assertEqual(events[0]["actor"], signer)
        self.assertEqual(events[0]["actor_source"], "v3_tx_from")
