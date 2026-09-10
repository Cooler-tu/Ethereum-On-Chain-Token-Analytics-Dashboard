#!/usr/bin/env python3
"""Discover every Uniswap V3 pool for one exact token pair.

This research helper deliberately reads ``PoolCreated`` logs instead of
looping over a hard-coded fee list.  A full-range query is attempted first;
providers that reject it are handled by an adaptive, lossless chunk scan.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from eth_abi import decode
import requests
from web3 import Web3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in os.sys.path:
    os.sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:  # pragma: no cover - optional convenience
    pass

from src.client import get_contract, get_web3, has_bytecode
from src.discovery.log_utils import POOL_CREATED_TOPIC, address_topic


UNISWAP_V3_FACTORY = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
UNISWAP_V3_FACTORY_DEPLOYMENT_BLOCK = 12_369_621
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@dataclass(frozen=True)
class FactoryPool:
    pool_address: str
    token0: str
    token1: str
    fee: int
    tick_spacing: int
    creation_block: int
    creation_transaction: str
    creation_log_index: int
    verified_at_block: int


def _as_hex(value: Any) -> str:
    if isinstance(value, str):
        return value if value.startswith("0x") else f"0x{value}"
    if hasattr(value, "hex"):
        text = value.hex()
        return text if text.startswith("0x") else f"0x{text}"
    raise TypeError(f"Cannot convert {type(value).__name__} to hex")


def _as_int(value: Any) -> int:
    return int(value, 16) if isinstance(value, str) else int(value)


def exact_pair_topics(token_a: str, token_b: str) -> list[list[Any]]:
    """Return the two exact topic filters required for the sorted V3 pair."""
    token0, token1 = sorted(
        (Web3.to_checksum_address(token_a), Web3.to_checksum_address(token_b)),
        key=lambda item: int(item, 16),
    )
    return [
        [POOL_CREATED_TOPIC, address_topic(token0), address_topic(token1)],
    ]


def decode_pool_created(raw: dict[str, Any], verified_at_block: int) -> FactoryPool:
    """Decode a raw Uniswap V3 ``PoolCreated`` log."""
    topics = raw["topics"]
    if _as_hex(topics[0]).lower() != POOL_CREATED_TOPIC.lower():
        raise ValueError("Log is not a Uniswap V3 PoolCreated event")
    token0 = Web3.to_checksum_address("0x" + _as_hex(topics[1])[-40:])
    token1 = Web3.to_checksum_address("0x" + _as_hex(topics[2])[-40:])
    fee = int(_as_hex(topics[3]), 16)
    data = bytes.fromhex(_as_hex(raw["data"])[2:])
    tick_spacing, pool_address = decode(["int24", "address"], data)
    return FactoryPool(
        pool_address=Web3.to_checksum_address(pool_address),
        token0=token0,
        token1=token1,
        fee=fee,
        tick_spacing=int(tick_spacing),
        creation_block=_as_int(raw["blockNumber"]),
        creation_transaction=_as_hex(raw["transactionHash"]),
        creation_log_index=_as_int(raw["logIndex"]),
        verified_at_block=int(verified_at_block),
    )


def get_logs_lossless(
    fetch: Callable[[int, int, list[Any]], Iterable[dict[str, Any]]],
    from_block: int,
    to_block: int,
    topics: list[Any],
    initial_chunk: int = 1_000_000,
) -> list[dict[str, Any]]:
    """Fetch every block, reducing the range on failure and never skipping one."""
    if from_block > to_block:
        return []
    try:
        return list(fetch(from_block, to_block, topics))
    except Exception:
        pass

    rows: list[dict[str, Any]] = []
    start = from_block
    chunk = max(1, min(initial_chunk, to_block - from_block + 1))
    successes = 0
    while start <= to_block:
        end = min(to_block, start + chunk - 1)
        try:
            rows.extend(fetch(start, end, topics))
            start = end + 1
            successes += 1
            if successes >= 4:
                chunk = min(initial_chunk, chunk * 2)
                successes = 0
        except Exception as exc:
            successes = 0
            if chunk == 1:
                raise RuntimeError(
                    f"PoolCreated scan failed at block {start}; no block was skipped"
                ) from exc
            chunk = max(1, chunk // 2)
    return rows


def discover_pair_pools(
    w3: Web3,
    factory_address: str,
    token_a: str,
    token_b: str,
    from_block: int,
    to_block: int,
    initial_chunk: int = 1_000_000,
) -> list[FactoryPool]:
    """Discover and validate all V3 pools created for the exact pair."""
    factory_address = Web3.to_checksum_address(factory_address)
    expected_tokens = {
        Web3.to_checksum_address(token_a),
        Web3.to_checksum_address(token_b),
    }
    rpc_url = getattr(w3.provider, "endpoint_uri", None)
    request_id = 0

    def fetch(start: int, end: int, topics: list[Any]):
        nonlocal request_id
        request_id += 1
        params = {
            "address": factory_address,
            "fromBlock": hex(start),
            "toBlock": hex(end),
            "topics": topics,
        }
        if not rpc_url:
            return w3.eth.get_logs(params)
        response = requests.post(
            rpc_url,
            json={"jsonrpc": "2.0", "id": request_id, "method": "eth_getLogs", "params": [params]},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        if "error" in payload:
            raise RuntimeError(str(payload["error"]))
        return payload["result"]

    decoded: dict[str, FactoryPool] = {}
    for topics in exact_pair_topics(token_a, token_b):
        for raw in get_logs_lossless(
            fetch, from_block, to_block, topics, initial_chunk=initial_chunk
        ):
            row = decode_pool_created(raw, to_block)
            decoded[row.pool_address.lower()] = row

    factory = get_contract(w3, factory_address, "uniswap_v3_factory")
    verified: list[FactoryPool] = []
    for row in decoded.values():
        if {row.token0, row.token1} != expected_tokens:
            raise ValueError(f"Factory log returned an unexpected pair: {row}")
        registered = factory.functions.getPool(
            row.token0, row.token1, row.fee
        ).call(block_identifier=to_block)
        if Web3.to_checksum_address(registered) != row.pool_address:
            raise ValueError(f"Factory getPool validation failed for {row.pool_address}")
        if registered == ZERO_ADDRESS or not has_bytecode(w3, row.pool_address, to_block):
            raise ValueError(f"Pool has no bytecode at block {to_block}: {row.pool_address}")
        pool = get_contract(w3, row.pool_address, "uniswap_v3_pool")
        actual = {
            Web3.to_checksum_address(pool.functions.token0().call(block_identifier=to_block)),
            Web3.to_checksum_address(pool.functions.token1().call(block_identifier=to_block)),
        }
        actual_fee = int(pool.functions.fee().call(block_identifier=to_block))
        if actual != expected_tokens or actual_fee != row.fee:
            raise ValueError(f"Pool contract validation failed for {row.pool_address}")
        verified.append(row)
    return sorted(verified, key=lambda item: (item.creation_block, item.fee))


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token-a", required=True)
    parser.add_argument("--token-b", required=True)
    parser.add_argument("--factory", default=UNISWAP_V3_FACTORY)
    parser.add_argument("--from-block", type=int, default=UNISWAP_V3_FACTORY_DEPLOYMENT_BLOCK)
    parser.add_argument("--to-block", type=int)
    parser.add_argument("--rpc-url")
    parser.add_argument("--initial-chunk", type=int, default=1_000_000)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    w3 = get_web3(args.rpc_url or os.environ.get("RPC_URL"))
    to_block = args.to_block
    if to_block is None:
        to_block = int(w3.eth.get_block("finalized")["number"])
    pools = discover_pair_pools(
        w3=w3,
        factory_address=args.factory,
        token_a=args.token_a,
        token_b=args.token_b,
        from_block=max(args.from_block, UNISWAP_V3_FACTORY_DEPLOYMENT_BLOCK),
        to_block=to_block,
        initial_chunk=args.initial_chunk,
    )
    payload = {
        "schema_version": "uniswap_v3_pair_pools_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "chain_id": int(w3.eth.chain_id),
        "factory_address": Web3.to_checksum_address(args.factory),
        "token_a": Web3.to_checksum_address(args.token_a),
        "token_b": Web3.to_checksum_address(args.token_b),
        "scan_from_block": max(args.from_block, UNISWAP_V3_FACTORY_DEPLOYMENT_BLOCK),
        "scan_to_block": to_block,
        "pool_count": len(pools),
        "pools": [asdict(pool) for pool in pools],
    }
    write_json_atomic(args.output, payload)
    print(f"Discovered and validated {len(pools)} pools -> {args.output}")


if __name__ == "__main__":
    main()
