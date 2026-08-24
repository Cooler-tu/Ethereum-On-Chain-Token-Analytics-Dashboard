import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.indexer.indexer import index_pool_token_transfers


POOL_A = "0x00000000000000000000000000000000000000a1"
POOL_B = "0x00000000000000000000000000000000000000b2"
TOKEN = "0x00000000000000000000000000000000000000c3"


class _Events:
    Transfer = object()


class _Contract:
    events = _Events()


class _Stream:
    filters = []

    def __init__(self, *args, argument_filters=None, **kwargs):
        self.filters.append(argument_filters)

    def run(self, _event):
        return [
            {
                "transaction_hash": "0xabc",
                "log_index": 7,
                "event_type": "TOKEN_TRANSFER",
            }
        ]


class PoolTransferIndexingTest(unittest.TestCase):
    def setUp(self):
        _Stream.filters = []

    def test_indexes_both_directions_per_pool_and_dedupes(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "src.indexer.indexer.get_contract", return_value=_Contract()
        ), patch("src.indexer.indexer._StreamIndexer", _Stream):
            rows = index_pool_token_transfers(
                object(),
                TOKEN,
                [POOL_A, POOL_B, POOL_A],
                1,
                2,
                {"streams": {}},
                Path(tmp) / "checkpoint.json",
                Path(tmp),
                {},
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(len(_Stream.filters), 4)
        self.assertEqual(
            {tuple(item.keys()) for item in _Stream.filters},
            {("to",), ("from",)},
        )
