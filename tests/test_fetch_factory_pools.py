import importlib.util
from pathlib import Path
import sys
import unittest

from eth_abi import encode
from web3 import Web3


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fetch_factory_pools.py"
SPEC = importlib.util.spec_from_file_location("fetch_factory_pools", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FactoryPoolTests(unittest.TestCase):
    def test_exact_pair_topics_are_sorted_and_fee_is_not_hardcoded(self):
        high = "0x9999999999999999999999999999999999999999"
        low = "0x1111111111111111111111111111111111111111"
        topics = MODULE.exact_pair_topics(high, low)
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0][1], MODULE.address_topic(low))
        self.assertEqual(topics[0][2], MODULE.address_topic(high))
        self.assertEqual(len(topics[0]), 3)

    def test_decode_pool_created(self):
        token0 = "0x1111111111111111111111111111111111111111"
        token1 = "0x9999999999999999999999999999999999999999"
        pool = "0x2222222222222222222222222222222222222222"
        raw = {
            "topics": [
                MODULE.POOL_CREATED_TOPIC,
                MODULE.address_topic(token0),
                MODULE.address_topic(token1),
                hex(500),
            ],
            "data": "0x" + encode(["int24", "address"], [10, pool]).hex(),
            "blockNumber": hex(123),
            "transactionHash": "0x" + "ab" * 32,
            "logIndex": hex(4),
        }
        row = MODULE.decode_pool_created(raw, verified_at_block=999)
        self.assertEqual(row.pool_address, Web3.to_checksum_address(pool))
        self.assertEqual(row.fee, 500)
        self.assertEqual(row.tick_spacing, 10)
        self.assertEqual(row.creation_block, 123)
        self.assertEqual(row.creation_log_index, 4)

    def test_adaptive_fetch_covers_every_block_without_duplicates(self):
        calls = []

        def fetch(start, end, _topics):
            calls.append((start, end))
            if end - start + 1 > 2:
                raise ValueError("provider range limit")
            return [{"block": block} for block in range(start, end + 1)]

        rows = MODULE.get_logs_lossless(fetch, 10, 17, ["topic"], initial_chunk=8)
        self.assertEqual([row["block"] for row in rows], list(range(10, 18)))
        self.assertTrue(any(end - start + 1 == 2 for start, end in calls))

    def test_single_block_failure_is_not_silently_skipped(self):
        def fetch(_start, _end, _topics):
            raise ValueError("down")

        with self.assertRaisesRegex(RuntimeError, "no block was skipped"):
            MODULE.get_logs_lossless(fetch, 10, 10, ["topic"], initial_chunk=1)


if __name__ == "__main__":
    unittest.main()
