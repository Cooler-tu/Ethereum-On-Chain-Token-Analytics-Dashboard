import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

from src.data.dune import (
    DuneCreditError,
    DuneResultSizeError,
    _execute_remote,
    _http_limit_kind,
    _is_quota_http,
    query,
)


def _response(status: int, payload) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response.url = "https://api.dune.test/example"
    response.request = requests.Request("GET", response.url).prepare()
    if isinstance(payload, (dict, list)):
        response._content = json.dumps(payload).encode("utf-8")
        response.headers["Content-Type"] = "application/json"
    else:
        response._content = str(payload).encode("utf-8")
    return response


class DuneLimitClassificationTests(unittest.TestCase):
    def test_http_402_is_credit_error_and_not_result_size(self):
        error = requests.HTTPError(
            response=_response(402, "Payment Required: not enough credits")
        )

        self.assertEqual(_http_limit_kind(error), "credit")
        self.assertTrue(_is_quota_http(error))

    def test_http_429_rate_limit_is_not_credit_or_size_error(self):
        error = requests.HTTPError(
            response=_response(429, "rate limit exceeded")
        )

        self.assertIsNone(_http_limit_kind(error))
        self.assertFalse(_is_quota_http(error))

    def test_explicit_result_size_message_is_splittable(self):
        error = requests.HTTPError(
            response=_response(400, "Result too large: too many rows")
        )

        self.assertEqual(_http_limit_kind(error), "size")
        self.assertTrue(_is_quota_http(error))

    def test_datapoint_limit_is_result_size_not_credit(self):
        error = requests.HTTPError(
            response=_response(400, "Datapoint limit exceeded")
        )

        self.assertEqual(_http_limit_kind(error), "size")

    def test_generic_credit_message_is_not_splittable(self):
        error = requests.HTTPError(
            response=_response(400, "Monthly credit limit exceeded")
        )

        self.assertEqual(_http_limit_kind(error), "credit")


class DuneRemoteLimitTests(unittest.TestCase):
    def test_http_402_stops_after_one_request(self):
        session = Mock()
        session.request.return_value = _response(
            402, "Payment Required: not enough credits"
        )

        with patch("src.data.dune.requests.Session", return_value=session):
            with self.assertRaises(DuneCreditError):
                _execute_remote("select 1", label="test", api_key="test-key")

        self.assertEqual(session.request.call_count, 1)

    def test_http_429_retries_then_completes(self):
        session = Mock()
        session.request.side_effect = [
            _response(429, "rate limit exceeded"),
            _response(200, {"execution_id": "exec-1"}),
            _response(200, {"state": "QUERY_STATE_COMPLETED"}),
            _response(200, {"result": {"rows": [{"value": 1}]}}),
        ]

        with patch("src.data.dune.requests.Session", return_value=session), patch(
            "src.data.dune.time.sleep"
        ):
            rows = _execute_remote(
                "select 1",
                label="test",
                api_key="test-key",
                poll_seconds=0,
            )

        self.assertEqual(rows, [{"value": 1}])
        self.assertEqual(session.request.call_count, 4)


class DuneQuerySplittingTests(unittest.TestCase):
    def test_credit_error_never_splits_block_window(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(
            os.environ, {"DUNE_API_KEY": "test-key"}
        ), patch(
            "src.data.dune._query_once",
            side_effect=DuneCreditError("credits exhausted"),
        ) as query_once:
            with self.assertRaises(DuneCreditError):
                query(
                    "swaps",
                    cache_dir=tmp,
                    from_block=1,
                    to_block=4000,
                    chunk_blocks=1000,
                    chunk_pause_s=0,
                )

        self.assertEqual(query_once.call_count, 1)

    def test_result_size_error_still_splits_and_merges(self):
        ranges = []

        def fake_query_once(*_args, **kwargs):
            prepared = kwargs["prepared"]
            block_range = (prepared["from_block"], prepared["to_block"])
            ranges.append(block_range)
            if len(ranges) == 1:
                raise DuneResultSizeError("result too large")
            return [{"range": block_range}]

        with tempfile.TemporaryDirectory() as tmp, patch.dict(
            os.environ, {"DUNE_API_KEY": "test-key"}
        ), patch("src.data.dune._query_once", side_effect=fake_query_once):
            rows = query(
                "swaps",
                cache_dir=tmp,
                from_block=1,
                to_block=1000,
                chunk_blocks=0,
                min_chunk_blocks=200,
                chunk_pause_s=0,
            )

        self.assertEqual(ranges, [(1, 1000), (1, 500), (501, 1000)])
        self.assertEqual(
            rows,
            [{"range": (1, 500)}, {"range": (501, 1000)}],
        )


if __name__ == "__main__":
    unittest.main()
