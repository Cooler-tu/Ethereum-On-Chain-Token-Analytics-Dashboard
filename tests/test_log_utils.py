import os
import unittest
from unittest.mock import patch

from src.discovery.log_utils import _configured_chunk_size
from src.indexer.indexer import _fetch_block_timestamps, _load_timestamp_cache


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class _Eth:
    def get_block(self, _block):
        raise AssertionError("batch results should avoid individual fallback")


class _Web3:
    provider = type("Provider", (), {"endpoint_uri": "https://rpc.invalid"})()
    eth = _Eth()


class LogUtilsTest(unittest.TestCase):
    def test_configured_chunk_size_uses_positive_override(self):
        with patch.dict(os.environ, {"ETH_LOG_CHUNK_SIZE": "10000"}):
            self.assertEqual(_configured_chunk_size(), 10000)

    def test_configured_chunk_size_falls_back_for_invalid_value(self):
        with patch.dict(os.environ, {"ETH_LOG_CHUNK_SIZE": "invalid"}):
            self.assertEqual(_configured_chunk_size(), 2000)

    def test_timestamp_batches_can_run_in_parallel(self):
        def fake_post(_endpoint, *, json, timeout):
            self.assertEqual(timeout, 60)
            return _Response(
                [
                    {
                        "id": item["id"],
                        "result": {"timestamp": hex(item["id"] * 10)},
                    }
                    for item in json
                ]
            )

        env = {"ETH_BLOCK_BATCH_SIZE": "2", "ETH_BLOCK_BATCH_WORKERS": "2"}
        with patch.dict(os.environ, env), patch(
            "src.indexer.indexer.requests.post", side_effect=fake_post
        ) as post:
            result = _fetch_block_timestamps(_Web3(), {1, 2, 3}, {})

        self.assertEqual(result, {1: 10, 2: 20, 3: 30})
        self.assertEqual(post.call_count, 2)

    def test_timestamp_cache_recovers_prior_jsonl_chunks(self):
        import json
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp)
            (cache_dir / "stream.jsonl").write_text(
                "\n".join(
                    json.dumps(row)
                    for row in (
                        {"block_number": 10, "block_timestamp": 100},
                        {"block_number": 11, "block_timestamp": 110},
                        {"block_number": 12, "block_timestamp": 0},
                    )
                ),
                encoding="utf-8",
            )
            result = _load_timestamp_cache(cache_dir)

        self.assertEqual(result, {10: 100, 11: 110})
