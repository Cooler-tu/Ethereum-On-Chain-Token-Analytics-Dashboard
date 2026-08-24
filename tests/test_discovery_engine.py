import json
import tempfile
import unittest
from pathlib import Path

from src.discovery.engine import load_pools_file


class DiscoveryEngineTest(unittest.TestCase):
    def test_load_pools_file_preserves_v3_fee(self):
        token = "0x50D1C9771902476076eCFc8B2A83Ad6b9355a4c9"
        with tempfile.TemporaryDirectory() as tmp:
            pools_file = Path(tmp) / "pools.json"
            pools_file.write_text(
                json.dumps(
                    {
                        "token": token,
                        "pools": [
                            {
                                "project": "uniswap",
                                "version": "v3",
                                "pool_address": "0xb404057EE4B1d7359Ca5a57aC1C020B74c23E56b",
                                "token0": token,
                                "token1": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                                "fee": "3000",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = load_pools_file(pools_file, token, 1, 2, 1)

        self.assertEqual(len(result["pools"]), 1)
        self.assertEqual(result["pools"][0]["fee"], 3000)
