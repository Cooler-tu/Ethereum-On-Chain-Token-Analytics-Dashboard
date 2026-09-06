"""Dune-backed event indexing: call ``query(sql_name)`` and normalize rows."""
from __future__ import annotations

import bisect
import json
import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from web3 import Web3

from decimal import Decimal

import requests
from eth_abi import decode as abi_decode

from ..analysis.v3_math import get_amounts_for_liquidity
from ..data.artifacts import validate_artifact_environment, write_table
from ..data.dune import DuneError, query
from ..models import VerifiedPool

ProgressFn = Callable[[str], None]
_V3_POSITION_MANAGER = "0xc36442b4a4522e871399cd717abdd847ab11fe88"
_V4_POSITION_MANAGER = "0xbd216513d74c8cf14cf4747e6aaa6420ff64ee9e"
_ZERO_ADDR = "0x0000000000000000000000000000000000000000"

_LIQ_SQL = (
    "liquidity_uniswap_v2_mint",
    "liquidity_uniswap_v2_burn",
    "liquidity_uniswap_v3_mint",
    "liquidity_uniswap_v3_burn",
)

# SQL no longer returns these constants — fill locally from the template name.
_LIQ_META: dict[str, dict[str, str]] = {
    "liquidity_uniswap_v2_mint": {
        "protocol": "uniswap",
        "version": "v2",
        "event_type": "LIQUIDITY_ADD",
        "source_event": "Mint",
    },
    "liquidity_uniswap_v2_burn": {
        "protocol": "uniswap",
        "version": "v2",
        "event_type": "LIQUIDITY_REMOVE",
        "source_event": "Burn",
    },
    "liquidity_uniswap_v3_mint": {
        "protocol": "uniswap",
        "version": "v3",
        "event_type": "LIQUIDITY_ADD",
        "source_event": "Mint",
    },
    "liquidity_uniswap_v3_burn": {
        "protocol": "uniswap",
        "version": "v3",
        "event_type": "LIQUIDITY_REMOVE",
        "source_event": "Burn",
    },
    "liquidity_uniswap_v4_modify": {
        "protocol": "uniswap",
        "version": "v4",
        "event_type": "",
        "source_event": "ModifyLiquidity",
    },
}


def _progress(msg: str, on_progress: Optional[ProgressFn] = None) -> None:
    if on_progress is not None:
        on_progress(msg)
    else:
        print("  {}".format(msg), flush=True)


def _parse_block_timestamp(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip()
    if not s:
        return 0
    try:
        return int(s)
    except ValueError:
        pass
    s2 = s.replace(" UTC", "").replace("Z", "+00:00")
    for fmt in (
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
    ):
        try:
            dt = datetime.strptime(s2, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            continue
    try:
        return int(datetime.fromisoformat(s2).timestamp())
    except Exception:
        return 0


def _checksum(addr: str) -> str:
    if not addr:
        return ""
    try:
        return Web3.to_checksum_address(addr)
    except Exception:
        return str(addr)


def _salt_to_token_id(salt: Any) -> Optional[int]:
    if salt is None:
        return None
    try:
        if isinstance(salt, int):
            return int(salt)
        s = str(salt).strip().lower()
        if s.startswith("\\x"):
            s = "0x" + s[2:]
        if s.startswith("0x"):
            return int(s, 16)
        return int(s)
    except (TypeError, ValueError):
        return None


def apply_pm_nft_owners(
    events: list[dict[str, Any]],
    transfers: list[dict[str, Any]],
    *,
    position_manager: str,
    versions: set[str],
    actor_source: str,
    require_pm_actor: bool = True,
) -> int:
    """Replace a Position Manager (or Collect recipient) with the NFT owner."""
    pm = (position_manager or "").lower()
    wanted = {str(v).lower() for v in versions}
    by_tid: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for raw in transfers or []:
        tid = _salt_to_token_id(raw.get("nft_token_id") or raw.get("token_id"))
        owner = _checksum(str(raw.get("owner") or ""))
        if tid is None or tid < 0 or not owner or owner.lower() == _ZERO_ADDR:
            continue
        try:
            block_number = int(raw.get("block_number") or 0)
            log_index = int(raw.get("log_index") or 0)
        except (TypeError, ValueError):
            continue
        by_tid[tid].append(
            {
                "owner": owner,
                "block_number": block_number,
                "log_index": log_index,
                "tx": str(raw.get("transaction_hash") or "").lower(),
            }
        )
    for rows in by_tid.values():
        rows.sort(key=lambda item: (item["block_number"], item["log_index"]))

    resolved = 0
    for event in events or []:
        if str(event.get("version") or "").lower() not in wanted:
            continue
        actor = str(event.get("actor") or "").lower()
        if require_pm_actor and actor != pm:
            continue
        tid = _salt_to_token_id(event.get("nft_token_id") or event.get("salt"))
        if tid is None:
            continue
        history = by_tid.get(tid) or []
        if not history:
            continue
        try:
            block_number = int(event.get("block_number") or 0)
            log_index = int(event.get("log_index") or 0)
        except (TypeError, ValueError):
            block_number = 0
            log_index = 0
        tx = str(event.get("transaction_hash") or "").lower()
        owner = ""
        if tx:
            same_tx = [row for row in history if row["tx"] == tx]
            if same_tx:
                owner = same_tx[-1]["owner"]
        if not owner:
            prior = [
                row
                for row in history
                if row["block_number"] < block_number
                or (
                    row["block_number"] == block_number
                    and row["log_index"] <= log_index
                )
            ]
            if prior:
                owner = prior[-1]["owner"]
            elif history[0]["block_number"] == block_number:
                owner = history[0]["owner"]
        if not owner or owner.lower() == pm:
            continue
        event["actor"] = owner
        event["actor_source"] = actor_source
        if event.get("nft_token_id") is None:
            event["nft_token_id"] = tid
        resolved += 1
    return resolved


def apply_v4_pm_nft_owners(
    events: list[dict[str, Any]],
    transfers: list[dict[str, Any]],
    *,
    position_manager: str = _V4_POSITION_MANAGER,
) -> int:
    """Replace V4 Position Manager sender with the NFT owner at that modify."""
    return apply_pm_nft_owners(
        events,
        transfers,
        position_manager=position_manager or _V4_POSITION_MANAGER,
        versions={"v4", "4"},
        actor_source="v4_pm_nft_owner",
        require_pm_actor=True,
    )


def attach_v3_burn_token_ids(
    events: list[dict[str, Any]],
    token_rows: list[dict[str, Any]],
) -> int:
    """Stamp V3 burns with the NPM DecreaseLiquidity tokenId."""
    index: dict[tuple[str, int, str], int] = {}
    for raw in token_rows or []:
        tid = _salt_to_token_id(raw.get("nft_token_id") or raw.get("token_id"))
        if tid is None or tid < 0:
            continue
        try:
            log_index = int(raw.get("log_index") or 0)
        except (TypeError, ValueError):
            continue
        key = (
            str(raw.get("transaction_hash") or "").lower(),
            log_index,
            str(raw.get("pool_address") or "").lower(),
        )
        index[key] = tid
    attached = 0
    for event in events or []:
        if str(event.get("version") or "").lower() not in {"v3", "3"}:
            continue
        if str(event.get("event_type") or "").upper() != "LIQUIDITY_REMOVE":
            continue
        try:
            log_index = int(event.get("log_index") or 0)
        except (TypeError, ValueError):
            continue
        key = (
            str(event.get("transaction_hash") or "").lower(),
            log_index,
            str(event.get("pool_address") or "").lower(),
        )
        tid = index.get(key)
        if tid is None:
            continue
        event["nft_token_id"] = tid
        attached += 1
    return attached


def apply_v3_npm_nft_owners(
    events: list[dict[str, Any]],
    transfers: list[dict[str, Any]],
    *,
    position_manager: str = _V3_POSITION_MANAGER,
) -> int:
    """Replace V3 NPM / Collect recipient with the NFT owner at that burn."""
    return apply_pm_nft_owners(
        events,
        transfers,
        position_manager=position_manager or _V3_POSITION_MANAGER,
        versions={"v3", "3"},
        actor_source="v3_npm_nft_owner",
        require_pm_actor=False,
    )


def _normalize_swap(row: dict[str, Any]) -> dict[str, Any]:
    bought = str(row.get("token_bought_amount_raw") or row.get("token1_amount") or "0")
    sold = str(row.get("token_sold_amount_raw") or row.get("token0_amount") or "0")
    return {
        "block_number": int(row.get("block_number") or 0),
        "block_timestamp": _parse_block_timestamp(
            row.get("block_timestamp") or row.get("block_time")
        ),
        "transaction_hash": str(row.get("transaction_hash") or ""),
        "log_index": int(row.get("log_index") or 0),
        "protocol": str(row.get("protocol") or "").lower(),
        "version": str(row.get("version") or "").lower(),
        "pool_address": _checksum(row.get("pool_address") or ""),
        "event_type": "SWAP",
        "actor": _checksum(row.get("actor") or row.get("tx_from") or ""),
        "recipient": _checksum(row.get("recipient") or row.get("actor") or ""),
        "token0_address": _checksum(row.get("token_sold") or row.get("token0_address") or ""),
        "token1_address": _checksum(row.get("token_bought") or row.get("token1_address") or ""),
        "amount_usd": float(row.get("amount_usd") or 0),
        "token0_amount": sold,
        "token1_amount": bought,
        "liquidity_delta": "0",
        "source_event": str(row.get("source_event") or "dex.trades"),
        "verified": True,
        "nft_token_id": None,
    }


def _parse_uint(value: Any) -> int:
    if value in (None, ""):
        return 0
    text = str(value).strip()
    if not text:
        return 0
    try:
        return int(text, 16) if text.startswith("0x") else int(text)
    except (TypeError, ValueError):
        return 0


def _sqrt_price_series(
    price_rows: list[dict[str, Any]] | None,
    init_rows: list[dict[str, Any]] | None = None,
) -> dict[str, list[tuple[int, int]]]:
    """Last known sqrtPriceX96 per pool, sorted by block."""
    latest: dict[str, dict[int, int]] = {}
    for row in list(init_rows or []) + list(price_rows or []):
        pool_id = str(row.get("pool_id") or "").lower()
        block_number = int(row.get("block_number") or 0)
        sqrt_price = _parse_uint(row.get("sqrt_price_x96"))
        if not pool_id or block_number <= 0 or sqrt_price <= 0:
            continue
        latest.setdefault(pool_id, {})[block_number] = sqrt_price
    return {
        pool_id: sorted(points.items())
        for pool_id, points in latest.items()
    }


def _sqrt_at_or_before(points: list[tuple[int, int]], block_number: int) -> int:
    if not points:
        return 0
    blocks = [item[0] for item in points]
    idx = bisect.bisect_right(blocks, int(block_number)) - 1
    if idx < 0:
        return 0
    return int(points[idx][1])


def unpack_balance_delta(raw: Any) -> tuple[int, int]:
    """Split Uniswap V4 packed ``int256`` BalanceDelta into signed amount0/1."""
    try:
        value = int(str(raw).strip() or 0)
    except (TypeError, ValueError):
        return 0, 0
    if value < 0:
        value += 1 << 256
    value &= (1 << 256) - 1
    amount0 = value >> 128
    amount1 = value & ((1 << 128) - 1)
    if amount0 >= 1 << 127:
        amount0 -= 1 << 128
    if amount1 >= 1 << 127:
        amount1 -= 1 << 128
    return int(amount0), int(amount1)


def enrich_v4_modify_amounts(
    rows: list[dict[str, Any]],
    price_rows: list[dict[str, Any]] | None = None,
    init_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Fill token0/token1 from callerDelta (principal+fees) or tick math."""
    series = _sqrt_price_series(price_rows, init_rows)
    enriched: list[dict[str, Any]] = []
    for raw in rows or []:
        row = dict(raw)
        fee0, fee1 = unpack_balance_delta(row.get("fees_accrued"))
        row["fee0_amount"] = str(abs(fee0))
        row["fee1_amount"] = str(abs(fee1))
        caller0, caller1 = unpack_balance_delta(row.get("caller_delta"))
        if caller0 != 0 or caller1 != 0:
            row["token0_amount"] = str(abs(caller0))
            row["token1_amount"] = str(abs(caller1))
            row["amount_source"] = "caller_delta"
            row["amounts_available"] = True
            row["quantification_status"] = "quantified"
            enriched.append(row)
            continue
        if fee0 != 0 or fee1 != 0:
            row["token0_amount"] = str(abs(fee0))
            row["token1_amount"] = str(abs(fee1))
            row["amount_source"] = "fees_accrued"
            row["amounts_available"] = True
            row["quantification_status"] = "quantified"
            enriched.append(row)
            continue
        pool_id = str(row.get("pool_id") or row.get("pool_address") or "").lower()
        try:
            tick_lower = int(row.get("tick_lower"))
            tick_upper = int(row.get("tick_upper"))
            delta = abs(int(row.get("liquidity_delta") or 0))
            block_number = int(row.get("block_number") or 0)
        except (TypeError, ValueError):
            row["amounts_available"] = False
            enriched.append(row)
            continue
        sqrt_price = _sqrt_at_or_before(series.get(pool_id) or [], block_number)
        if sqrt_price <= 0 or delta <= 0 or tick_lower >= tick_upper:
            row["amounts_available"] = False
            enriched.append(row)
            continue
        amount0, amount1 = get_amounts_for_liquidity(
            sqrt_price, tick_lower, tick_upper, delta
        )
        row["token0_amount"] = str(amount0)
        row["token1_amount"] = str(amount1)
        row["sqrt_price_x96"] = str(sqrt_price)
        row["amount_source"] = "tick_estimate"
        row["amounts_available"] = True
        row["quantification_status"] = "quantified"
        enriched.append(row)
    return enriched


def _normalize_liquidity(
    row: dict[str, Any],
    sql_name: str = "",
) -> dict[str, Any]:
    meta = _LIQ_META.get(sql_name, {})
    version = str(row.get("version") or meta.get("version") or "").lower()
    delta_raw = str(row.get("liquidity_delta") or "0")
    if row.get("amounts_available") is True:
        amounts_available = True
    elif row.get("amounts_available") is False:
        amounts_available = False
    else:
        amounts_available = any(
            key in row and row.get(key) not in (None, "", "0")
            for key in ("token0_amount", "token1_amount", "amount0", "amount1")
        )
    if row.get("quantification_status"):
        quantification_status = str(row["quantification_status"])
    elif amounts_available:
        quantification_status = "quantified"
    elif version in ("v4", "4") and delta_raw not in ("", "0"):
        quantification_status = "liquidity_delta_only"
    else:
        quantification_status = "unmapped"
    event_type = str(row.get("event_type") or meta.get("event_type") or "")
    if not event_type and version in ("v4", "4"):
        try:
            delta = int(delta_raw)
            event_type = "LIQUIDITY_ADD" if delta >= 0 else "LIQUIDITY_REMOVE"
        except (TypeError, ValueError):
            event_type = "LIQUIDITY_ADD"
    nft_id = row.get("nft_token_id")
    if nft_id is None and row.get("salt") is not None:
        try:
            s = str(row["salt"])
            nft_id = int(s, 16) if s.startswith("0x") else int(s)
        except Exception:
            nft_id = None
    pool_addr = str(row.get("pool_address") or row.get("pool_id") or "")
    # V4 poolId is bytes32 — do not EIP-55 checksum it.
    if pool_addr.startswith("0x") and len(pool_addr) == 66:
        pool_out = pool_addr.lower()
    else:
        pool_out = _checksum(pool_addr)
    actor = _checksum(row.get("actor") or "")
    recipient = _checksum(row.get("recipient") or "") or actor
    return {
        "block_number": int(row.get("block_number") or 0),
        "block_timestamp": _parse_block_timestamp(
            row.get("block_timestamp") or row.get("block_time")
        ),
        "transaction_hash": str(row.get("transaction_hash") or ""),
        "log_index": int(row.get("log_index") or 0),
        "protocol": str(row.get("protocol") or meta.get("protocol") or "").lower(),
        "version": version,
        "pool_address": pool_out,
        "event_type": event_type,
        "actor": actor,
        "recipient": recipient,
        "token0_amount": str(row.get("token0_amount") or "0"),
        "token1_amount": str(row.get("token1_amount") or "0"),
        "liquidity_delta": delta_raw,
        "source_event": str(
            row.get("source_event") or meta.get("source_event") or ""
        ),
        "tick_lower": row.get("tick_lower"),
        "tick_upper": row.get("tick_upper"),
        "salt": row.get("salt"),
        "nft_token_id": nft_id,
        "event_count": max(1, int(row.get("event_count") or 1)),
        "aggregation_scope": str(row.get("aggregation_scope") or ""),
        "amounts_available": amounts_available,
        "quantification_status": quantification_status,
        "amount_source": str(row.get("amount_source") or ""),
        "fee0_amount": str(row.get("fee0_amount") or "0"),
        "fee1_amount": str(row.get("fee1_amount") or "0"),
        "verified": True,
    }


def _normalize_transfer(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "block_number": int(row.get("block_number") or 0),
        "block_timestamp": _parse_block_timestamp(
            row.get("block_timestamp") or row.get("block_time")
        ),
        "transaction_hash": str(row.get("transaction_hash") or ""),
        "log_index": int(row.get("log_index") or 0),
        "protocol": "",
        "version": "",
        "pool_address": "",
        "event_type": "TOKEN_TRANSFER",
        "actor": _checksum(row.get("actor") or ""),
        "recipient": _checksum(row.get("recipient") or ""),
        "token0_amount": str(row.get("token0_amount") or row.get("amount_raw") or "0"),
        "token1_amount": "0",
        "liquidity_delta": "0",
        "source_event": "Transfer",
        "verified": True,
        "nft_token_id": None,
    }


def _pool_addrs_for_liquidity(verified_pools: list[VerifiedPool]) -> list[str]:
    out: list[str] = []
    for p in verified_pools:
        if not p.verified:
            continue
        if p.protocol == "uniswap" and p.version in ("v2", "v3", "v1"):
            if p.pool_address:
                out.append(p.pool_address)
        elif p.protocol == "curve" and p.pool_address:
            out.append(p.pool_address)
    return out


def _v4_pool_ids(verified_pools: list[VerifiedPool]) -> list[str]:
    out: list[str] = []
    for p in verified_pools:
        if not p.verified:
            continue
        if p.protocol == "uniswap" and str(p.version).lower() in ("v4", "4"):
            pid = p.pool_id or p.pool_address
            if pid and str(pid).startswith("0x") and len(str(pid)) == 66:
                out.append(str(pid).lower())
    return out


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, default=str)
    tmp.replace(path)


def index_events_from_dune(
    verified_pools: list[VerifiedPool],
    target_token: str,
    from_block: int,
    to_block: int,
    output_dir: str | Path = "output",
    index_token_transfer: bool = True,
    force_refresh: bool = False,
    artifact_format: str = "json",
    on_progress: Optional[ProgressFn] = None,
) -> dict[str, list]:
    """Pull swaps / liquidity / transfers from Dune and write indexer outputs."""
    artifact_mode = validate_artifact_environment(artifact_format)
    if artifact_mode == "parquet":
        raise ValueError(
            "Parquet-only analysis is not available during migration; use "
            "artifact_format='both' so legacy JSON readers keep working"
        )
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dune_dir = out / "dune_cache" / "index_{}_{}".format(from_block, to_block)
    token = Web3.to_checksum_address(target_token)
    common = dict(
        cache_dir=dune_dir,
        force_refresh=force_refresh,
        token=token,
        from_block=int(from_block),
        to_block=int(to_block),
    )

    _progress(
        "Dune index: swaps + pool/block liquidity aggregates + ERC20 Transfer "
        "(cache {}) ...".format(dune_dir),
        on_progress,
    )

    liq_pools = _pool_addrs_for_liquidity(verified_pools)
    v4_ids = _v4_pool_ids(verified_pools)

    # Heavy event pulls: always chunk by block so free-tier quotas don't
    # force an RPC fallback on wide windows.
    heavy = dict(common, chunk_blocks=2000, min_chunk_blocks=200)

    # Wave 1 — independent sections (no cross-deps):
    #   swaps | V2/V3 mint/burn ×4 | transfers | V4 modify batches
    jobs: list[tuple[str, Callable[[], Any]]] = []

    def _fetch_swaps() -> list[dict]:
        return [_normalize_swap(r) for r in query("swaps", pool_filter="", **heavy)]

    jobs.append(("swaps", _fetch_swaps))

    if liq_pools:
        pools_slice = liq_pools[:40]

        def _make_liq(sql_name: str):
            def _run() -> tuple[str, list[dict]]:
                rows = query(sql_name, pool_list=pools_slice, **heavy)
                return sql_name, [_normalize_liquidity(r, sql_name) for r in rows]

            return _run

        for sql_name in _LIQ_SQL:
            jobs.append((sql_name, _make_liq(sql_name)))

    if v4_ids:
        batch = 8
        v4_name = "liquidity_uniswap_v4_modify"
        for i in range(0, len(v4_ids[:40]), batch):
            chunk_ids = v4_ids[i : i + batch]
            start = i

            def _make_v4(ids: list[str], idx: int):
                def _run() -> tuple[str, list[dict]]:
                    rows = query(v4_name, pool_id_list=ids, **heavy)
                    prices = query(
                        "v4_sqrt_price_by_block", pool_id_list=ids, **heavy
                    )
                    inits = query(
                        "v4_sqrt_price_init",
                        pool_id_list=ids,
                        cache_dir=common["cache_dir"],
                        force_refresh=bool(common.get("force_refresh")),
                        chunk_blocks=0,
                    )
                    enriched = enrich_v4_modify_amounts(rows, prices, inits)
                    return (
                        "{}[{}]".format(v4_name, idx),
                        [_normalize_liquidity(r, v4_name) for r in enriched],
                    )

                return _run

            jobs.append(
                ("{}[{}]".format(v4_name, start), _make_v4(chunk_ids, start))
            )

    if index_token_transfer:
        def _fetch_transfers() -> list[dict]:
            return [
                _normalize_transfer(r) for r in query("transfers", **heavy)
            ]

        jobs.append(("transfers", _fetch_transfers))

    _progress(
        "Dune: fetching {} independent query job(s) in parallel ...".format(
            len(jobs)
        ),
        on_progress,
    )

    swaps: list[dict] = []
    liquidity: list[dict] = []
    transfers: list[dict] = []
    position_events: list[dict] = []

    def _consume(label: str, payload: Any) -> None:
        nonlocal swaps, liquidity, transfers
        if label == "swaps":
            swaps = payload
            return
        if label == "transfers":
            transfers = payload
            return
        # liquidity helpers return (name, rows)
        if isinstance(payload, tuple) and len(payload) == 2:
            _name, rows = payload
            liquidity.extend(rows)
            return
        if isinstance(payload, list):
            liquidity.extend(payload)

    max_workers = min(6, max(1, len(jobs)))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        fut_map = {ex.submit(fn): label for label, fn in jobs}
        for fut in as_completed(fut_map):
            label = fut_map[fut]
            try:
                _consume(label, fut.result())
                _progress("Dune: {} done".format(label), on_progress)
            except DuneError as exc:
                # Soft-fail liquidity / transfers; swaps failure is fatal.
                if label == "swaps":
                    raise
                _progress(
                    "Dune: skip {}: {}".format(label, exc), on_progress
                )

    _progress("Dune: {} swap(s)".format(len(swaps)), on_progress)
    _progress("Dune: {} liquidity event(s)".format(len(liquidity)), on_progress)
    if index_token_transfer:
        _progress("Dune: {} transfer(s)".format(len(transfers)), on_progress)

    table_artifacts = {
        "swaps": write_table(
            "swaps", swaps, out, artifact_format=artifact_mode
        ),
        "liquidity_events": write_table(
            "liquidity_events", liquidity, out, artifact_format=artifact_mode
        ),
        "transfers": write_table(
            "transfers", transfers, out, artifact_format=artifact_mode
        ),
        "position_events": write_table(
            "position_events", position_events, out, artifact_format=artifact_mode
        ),
    }
    _write_json(
        out / "index_source.json",
        {
            "source": "dune",
            "from_block": from_block,
            "to_block": to_block,
            "token": token,
            "artifact_format": artifact_mode,
            "artifacts": table_artifacts,
            "dune_cache": str(dune_dir),
            "parallel_jobs": [label for label, _ in jobs],
            "counts": {
                "swaps": len(swaps),
                "liquidity_events": len(liquidity),
                "transfers": len(transfers),
                "position_events": len(position_events),
            },
            "notes": [
                "Swaps from dex.trades (all DEXes, filtered by token).",
                (
                    "V2/V3 Mint/Burn stay pool/block aggregates. V4 "
                    "ModifyLiquidity is row-level (sender + ticks); token "
                    "amounts are estimated from liquidityDelta and the last "
                    "pool sqrt price."
                ),
                "V4 poolIds from pools_v4.sql (Swap⋈Initialize), not PoolManager.",
                "Independent Dune sections fetched in parallel.",
            ],
        },
    )

    _progress(
        "Dune indexing done: {} swaps, {} liquidity, {} transfers".format(
            len(swaps), len(liquidity), len(transfers)
        ),
        on_progress,
    )
    return {
        "swaps": swaps,
        "liquidity_events": liquidity,
        "transfers": transfers,
        "position_events": position_events,
    }


def _rpc_hex(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return "0x" + value.hex()
    text = str(value)
    return text if text.startswith("0x") else "0x" + text


_V4_MODIFY_TOPIC = (
    "0xf208f4912782fd25c7f114ca3723a2d5dd6f3bcc3ac8db5af63baa85f711d5ec"
)
_V4_POOL_MANAGER = "0x000000000004444c5dc75cB358380D2e3dE08A90"
_ALCHEMY_FREE_LOG_BLOCKS = 10


def sqrt_price_rows_from_swaps(
    swaps: list[dict[str, Any]],
    pool_tokens: dict[str, tuple[str, str]],
) -> list[dict[str, Any]]:
    """Last swap-implied sqrtPriceX96 per pool pair, reused across same-pair V4 pools."""
    pair_to_pools: dict[tuple[str, str], list[str]] = {}
    for pool_id, tokens in (pool_tokens or {}).items():
        token0 = (tokens[0] or "").lower()
        token1 = (tokens[1] or "").lower()
        if token0 and token1 and token0 != token1:
            pair_to_pools.setdefault((token0, token1), []).append(pool_id.lower())
    latest: dict[tuple[str, int], int] = {}
    for swap in swaps or []:
        sold = (swap.get("token0_address") or "").lower()
        bought = (swap.get("token1_address") or "").lower()
        try:
            sold_raw = abs(int(swap.get("token0_amount") or 0))
            bought_raw = abs(int(swap.get("token1_amount") or 0))
            block_number = int(swap.get("block_number") or 0)
        except (TypeError, ValueError):
            continue
        if not sold or not bought or sold_raw <= 0 or bought_raw <= 0 or block_number <= 0:
            continue
        for (token0, token1), pool_ids in pair_to_pools.items():
            if {sold, bought} != {token0, token1}:
                continue
            raw0, raw1 = (
                (sold_raw, bought_raw) if sold == token0 else (bought_raw, sold_raw)
            )
            if raw0 <= 0 or raw1 <= 0:
                continue
            sqrt_price = int(
                (Decimal(raw1) / Decimal(raw0)).sqrt() * (Decimal(2) ** 96)
            )
            for pool_id in pool_ids:
                latest[(pool_id, block_number)] = sqrt_price
    return [
        {
            "pool_id": pool_id,
            "block_number": block_number,
            "sqrt_price_x96": str(sqrt_price),
        }
        for (pool_id, block_number), sqrt_price in latest.items()
    ]


def fetch_v4_modify_via_rpc(
    pool_ids: list[str],
    from_block: int,
    to_block: int,
    *,
    pool_manager: str = _V4_POOL_MANAGER,
    timestamps: Optional[dict[int, int]] = None,
    rpc_url: Optional[str] = None,
    workers: int = 8,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """Row-level V4 ModifyLiquidity via 10-block eth_getLogs (Alchemy free tier)."""
    import os

    url = rpc_url or os.environ.get("ETH_RPC_URL") or ""
    if not url or not pool_ids:
        return [], [], []
    ids = [pid.lower() if pid.startswith("0x") else "0x" + pid.lower() for pid in pool_ids]
    ranges = [
        (start, min(start + _ALCHEMY_FREE_LOG_BLOCKS - 1, int(to_block)))
        for start in range(int(from_block), int(to_block) + 1, _ALCHEMY_FREE_LOG_BLOCKS)
    ]
    _progress(
        "RPC ModifyLiquidity {} pool(s), {} 10-block chunks, {} workers".format(
            len(ids), len(ranges), workers
        )
    )

    def _one(chunk: tuple[int, int]) -> list[dict[str, Any]]:
        start, end = chunk
        payload = {
            "jsonrpc": "2.0",
            "id": start,
            "method": "eth_getLogs",
            "params": [{
                "address": pool_manager,
                "fromBlock": hex(start),
                "toBlock": hex(end),
                "topics": [_V4_MODIFY_TOPIC, ids],
            }],
        }
        last_error = None
        for attempt in range(3):
            try:
                response = requests.post(url, json=payload, timeout=12)
                body = response.json()
                if response.status_code == 200 and "result" in body:
                    return body.get("result") or []
                last_error = body.get("error") or response.text
            except Exception as exc:
                last_error = exc
            time.sleep(0.25 * (attempt + 1))
        _progress("RPC skip [{}, {}]: {}".format(start, end, last_error))
        return []

    logs: list[dict[str, Any]] = []
    done = 0
    wave = max(1, int(workers) * 3)
    with ThreadPoolExecutor(max_workers=max(1, int(workers))) as pool:
        for offset in range(0, len(ranges), wave):
            batch = ranges[offset:offset + wave]
            futures = [pool.submit(_one, chunk) for chunk in batch]
            for fut in as_completed(futures):
                logs.extend(fut.result() or [])
                done += 1
            if done % 2000 < len(batch) or done == len(ranges):
                _progress(
                    "RPC ModifyLiquidity {}/{} chunks, {} logs".format(
                        done, len(ranges), len(logs)
                    )
                )

    ts_cache = dict(timestamps or {})
    modify_rows: list[dict[str, Any]] = []
    for evt in logs:
        topics = evt.get("topics") or []
        if len(topics) < 3:
            continue
        pool_id = str(topics[1]).lower()
        sender = "0x" + str(topics[2])[-40:]
        data = str(evt.get("data") or "")
        if data.startswith("0x"):
            data = data[2:]
        try:
            tick_lower, tick_upper, delta, salt = abi_decode(
                ["int24", "int24", "int256", "bytes32"],
                bytes.fromhex(data),
            )
        except Exception:
            continue
        block_number = int(evt.get("blockNumber") or "0x0", 16)
        log_index = int(evt.get("logIndex") or "0x0", 16)
        modify_rows.append({
            "block_number": block_number,
            "block_time": ts_cache.get(block_number, 0),
            "transaction_hash": str(evt.get("transactionHash") or ""),
            "log_index": log_index,
            "pool_id": pool_id,
            "actor": _checksum(sender),
            "tick_lower": int(tick_lower),
            "tick_upper": int(tick_upper),
            "liquidity_delta": str(int(delta)),
            "salt": _rpc_hex(salt),
            "event_count": 1,
            "aggregation_scope": "row",
        })
    _progress("RPC V4 decoded {} ModifyLiquidity log(s)".format(len(modify_rows)))
    return modify_rows, [], []


def refresh_v4_liquidity_events(
    verified_pools: list[VerifiedPool],
    from_block: int,
    to_block: int,
    output_dir: str | Path = "output",
    *,
    force_refresh: bool = True,
    pool_ids: Optional[list[str]] = None,
    chunk_blocks: int = 20_000,
) -> dict[str, Any]:
    """Re-fetch V4 ModifyLiquidity only and merge it into liquidity_events."""
    out = Path(output_dir)
    existing = []
    legacy = out / "liquidity_events.json"
    if legacy.exists():
        existing = json.loads(legacy.read_text())
        if not isinstance(existing, list):
            existing = []
    kept = [
        row
        for row in existing
        if str(row.get("version") or "").lower() not in {"v4", "4"}
    ]
    ids = [str(item).lower() for item in (pool_ids or _v4_pool_ids(verified_pools))]
    if not ids:
        return {"kept": len(kept), "v4": 0, "quantified": 0}

    cache = out / "dune_cache" / "index_{}_{}".format(from_block, to_block)
    v4_rows: list[dict] = []
    source = "dune"
    try:
        batch = 8
        for i in range(0, len(ids), batch):
            chunk_ids = ids[i : i + batch]
            raw = query(
                "liquidity_uniswap_v4_modify",
                pool_id_list=chunk_ids,
                from_block=from_block,
                to_block=to_block,
                cache_dir=cache,
                force_refresh=force_refresh,
                chunk_blocks=chunk_blocks,
                min_chunk_blocks=200,
            )
            prices = query(
                "v4_sqrt_price_by_block",
                pool_id_list=chunk_ids,
                from_block=from_block,
                to_block=to_block,
                cache_dir=cache,
                force_refresh=False,
                chunk_blocks=chunk_blocks,
                min_chunk_blocks=200,
            )
            inits = query(
                "v4_sqrt_price_init",
                pool_id_list=chunk_ids,
                cache_dir=cache,
                force_refresh=False,
                chunk_blocks=0,
            )
            enriched = enrich_v4_modify_amounts(raw, prices, inits)
            v4_rows.extend(
                _normalize_liquidity(row, "liquidity_uniswap_v4_modify")
                for row in enriched
            )
    except DuneError as exc:
        _progress("Dune V4 refresh failed ({}); falling back to RPC".format(exc))
        source = "rpc"
        timestamps: dict[int, int] = {}
        for row in existing:
            try:
                block_number = int(row.get("block_number") or 0)
                block_ts = int(row.get("block_timestamp") or 0)
            except (TypeError, ValueError):
                continue
            if block_number > 0 and block_ts > 0:
                timestamps[block_number] = block_ts
        raw, prices, inits = fetch_v4_modify_via_rpc(
            ids,
            from_block,
            to_block,
            timestamps=timestamps,
        )
        swaps_path = out / "swaps.json"
        if swaps_path.exists():
            swaps = json.loads(swaps_path.read_text())
            pool_tokens = {}
            for pool in verified_pools:
                pid = str(pool.pool_id or pool.pool_address or "").lower()
                if pid in set(ids):
                    pool_tokens[pid] = (
                        (pool.token0 or "").lower(),
                        (pool.token1 or "").lower(),
                    )
            prices = sqrt_price_rows_from_swaps(swaps, pool_tokens)
            for swap in swaps:
                try:
                    block_number = int(swap.get("block_number") or 0)
                    block_ts = int(swap.get("block_timestamp") or 0)
                except (TypeError, ValueError):
                    continue
                if block_number > 0 and block_ts > 0:
                    timestamps[block_number] = block_ts
            for row in raw:
                if not row.get("block_time"):
                    row["block_time"] = timestamps.get(int(row.get("block_number") or 0), 0)
        enriched = enrich_v4_modify_amounts(raw, prices, inits)
        v4_rows = [
            _normalize_liquidity(row, "liquidity_uniswap_v4_modify")
            for row in enriched
        ]

    merged = kept + v4_rows
    write_table("liquidity_events", merged, out, artifact_format="json")
    quantified = sum(1 for row in v4_rows if row.get("amounts_available"))
    with_actor = sum(1 for row in v4_rows if row.get("actor"))
    sources: dict[str, int] = {}
    for row in v4_rows:
        key = str(row.get("amount_source") or "none")
        sources[key] = sources.get(key, 0) + 1
    return {
        "kept": len(kept),
        "v4": len(v4_rows),
        "quantified": quantified,
        "with_actor": with_actor,
        "amount_sources": sources,
        "total": len(merged),
        "source": source,
    }


def refresh_v2_v3_burn_events(
    verified_pools: list[VerifiedPool],
    from_block: int,
    to_block: int,
    output_dir: str | Path = "output",
    *,
    force_refresh: bool = True,
    chunk_blocks: int = 20_000,
) -> dict[str, Any]:
    """Re-fetch V2/V3 burns with actors and replace existing remove rows."""
    out = Path(output_dir)
    existing = []
    legacy = out / "liquidity_events.json"
    if legacy.exists():
        existing = json.loads(legacy.read_text())
        if not isinstance(existing, list):
            existing = []
    kept = [
        row
        for row in existing
        if not (
            str(row.get("event_type") or "").upper() == "LIQUIDITY_REMOVE"
            and str(row.get("version") or "").lower() in {"v2", "v3", "2", "3"}
        )
    ]
    pools = _pool_addrs_for_liquidity(verified_pools)
    if not pools:
        return {"kept": len(kept), "burns": 0, "with_actor": 0}

    cache = out / "dune_cache" / "index_{}_{}".format(from_block, to_block)
    burn_rows: list[dict] = []
    for sql_name in ("liquidity_uniswap_v2_burn", "liquidity_uniswap_v3_burn"):
        raw = query(
            sql_name,
            pool_list=pools,
            from_block=from_block,
            to_block=to_block,
            cache_dir=cache,
            force_refresh=force_refresh,
            chunk_blocks=chunk_blocks,
            min_chunk_blocks=200,
        )
        burn_rows.extend(_normalize_liquidity(row, sql_name) for row in raw)

    merged = kept + burn_rows
    write_table("liquidity_events", merged, out, artifact_format="json")
    with_actor = sum(1 for row in burn_rows if row.get("actor"))
    return {
        "kept": len(kept),
        "burns": len(burn_rows),
        "with_actor": with_actor,
        "total": len(merged),
    }


def resolve_v4_position_manager_actors(
    from_block: int,
    to_block: int,
    output_dir: str | Path = "output",
    *,
    position_manager: str = _V4_POSITION_MANAGER,
    force_refresh: bool = False,
) -> dict[str, Any]:
    """Rewrite V4 PM senders on liquidity_events to the NFT owner."""
    out = Path(output_dir)
    path = out / "liquidity_events.json"
    events = json.loads(path.read_text()) if path.exists() else []
    if not isinstance(events, list):
        events = []
    pm = (position_manager or _V4_POSITION_MANAGER).lower()
    token_ids = sorted(
        {
            tid
            for row in events
            if str(row.get("version") or "").lower() in {"v4", "4"}
            and str(row.get("actor") or "").lower() == pm
            for tid in [_salt_to_token_id(row.get("nft_token_id") or row.get("salt"))]
            if tid is not None and tid >= 0
        }
    )
    if not token_ids:
        return {"candidates": 0, "resolved": 0, "token_ids": 0}

    cache = out / "dune_cache" / "index_{}_{}".format(from_block, to_block)
    transfers: list[dict] = []
    for i in range(0, len(token_ids), 400):
        batch = token_ids[i : i + 400]
        transfers.extend(
            query(
                "v4_pm_nft_transfers",
                npm=position_manager or _V4_POSITION_MANAGER,
                token_id_list=batch,
                to_block=to_block,
                cache_dir=cache,
                force_refresh=force_refresh,
                chunk_blocks=0,
            )
        )
    resolved = apply_v4_pm_nft_owners(
        events, transfers, position_manager=position_manager
    )
    write_table("liquidity_events", events, out, artifact_format="json")
    remaining = sum(
        1
        for row in events
        if str(row.get("version") or "").lower() in {"v4", "4"}
        and str(row.get("actor") or "").lower() == pm
    )
    return {
        "candidates": len(token_ids),
        "transfers": len(transfers),
        "resolved": resolved,
        "remaining_pm": remaining,
    }


def resolve_v3_position_manager_actors(
    from_block: int,
    to_block: int,
    output_dir: str | Path = "output",
    *,
    position_manager: str = _V3_POSITION_MANAGER,
    force_refresh: bool = False,
) -> dict[str, Any]:
    """Rewrite V3 NPM / Collect-recipient actors to the NFT owner."""
    out = Path(output_dir)
    path = out / "liquidity_events.json"
    events = json.loads(path.read_text()) if path.exists() else []
    if not isinstance(events, list):
        events = []
    pools = sorted(
        {
            str(row.get("pool_address") or "")
            for row in events
            if str(row.get("version") or "").lower() in {"v3", "3"}
            and str(row.get("event_type") or "").upper() == "LIQUIDITY_REMOVE"
            and str(row.get("pool_address") or "").startswith("0x")
            and len(str(row.get("pool_address") or "")) == 42
        }
    )
    if not pools:
        return {"pools": 0, "token_rows": 0, "attached": 0, "resolved": 0}

    cache = out / "dune_cache" / "index_{}_{}".format(from_block, to_block)
    token_rows = query(
        "v3_npm_burn_token_ids",
        pool_list=pools,
        from_block=from_block,
        to_block=to_block,
        cache_dir=cache,
        force_refresh=force_refresh,
        chunk_blocks=50_000,
        min_chunk_blocks=200,
    )
    attached = attach_v3_burn_token_ids(events, token_rows)
    token_ids = sorted(
        {
            tid
            for row in events
            if str(row.get("version") or "").lower() in {"v3", "3"}
            for tid in [_salt_to_token_id(row.get("nft_token_id"))]
            if tid is not None and tid >= 0
        }
    )
    transfers: list[dict] = []
    npm = position_manager or _V3_POSITION_MANAGER
    for i in range(0, len(token_ids), 400):
        batch = token_ids[i : i + 400]
        transfers.extend(
            query(
                "v4_pm_nft_transfers",
                npm=npm,
                token_id_list=batch,
                to_block=to_block,
                cache_dir=cache,
                force_refresh=force_refresh,
                chunk_blocks=0,
            )
        )
    resolved = apply_v3_npm_nft_owners(
        events, transfers, position_manager=npm
    )
    write_table("liquidity_events", events, out, artifact_format="json")
    remaining = sum(
        1
        for row in events
        if str(row.get("version") or "").lower() in {"v3", "3"}
        and str(row.get("event_type") or "").upper() == "LIQUIDITY_REMOVE"
        and str(row.get("actor") or "").lower() == (npm or "").lower()
    )
    return {
        "pools": len(pools),
        "token_rows": len(token_rows),
        "attached": attached,
        "candidates": len(token_ids),
        "transfers": len(transfers),
        "resolved": resolved,
        "remaining_npm": remaining,
    }


def apply_v3_tx_senders(
    events: list[dict[str, Any]],
    gas_rows: list[dict[str, Any]],
    *,
    contract_actors: set[str],
) -> int:
    """Replace a V3 contract actor (not an NFT owner) with the tx signer."""
    contracts = {str(addr).lower() for addr in contract_actors if addr}
    by_tx: dict[str, str] = {}
    for raw in gas_rows or []:
        tx = str(raw.get("tx_hash") or raw.get("transaction_hash") or "").lower()
        sender = _checksum(str(raw.get("gas_payer") or raw.get("tx_from") or ""))
        if tx and sender:
            by_tx[tx] = sender
    resolved = 0
    for event in events or []:
        if str(event.get("version") or "").lower() not in {"v3", "3"}:
            continue
        if str(event.get("event_type") or "").upper() != "LIQUIDITY_REMOVE":
            continue
        if event.get("actor_source") == "v3_npm_nft_owner":
            continue
        actor = str(event.get("actor") or "").lower()
        if actor not in contracts:
            continue
        sender = by_tx.get(str(event.get("transaction_hash") or "").lower())
        if not sender or sender.lower() == actor:
            continue
        event["actor"] = sender
        event["actor_source"] = "v3_tx_from"
        resolved += 1
    return resolved


def _code_contracts(addresses: list[str]) -> set[str]:
    """Return addresses that have bytecode (best-effort RPC)."""
    rpc = (os.environ.get("ETH_RPC_URL") or os.environ.get("WEB3_PROVIDER_URI") or "").strip()
    unique = []
    seen: set[str] = set()
    for addr in addresses:
        low = str(addr or "").lower()
        if not low.startswith("0x") or len(low) != 42 or low in seen:
            continue
        seen.add(low)
        unique.append(low)
    if not unique:
        return set()
    if not rpc:
        return set()
    w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 20}))
    found: set[str] = set()
    for addr in unique:
        try:
            code = w3.eth.get_code(Web3.to_checksum_address(addr))
        except Exception:
            continue
        if code:
            found.add(addr)
    return found


def resolve_v3_contract_actors(
    from_block: int,
    to_block: int,
    output_dir: str | Path = "output",
    *,
    force_refresh: bool = False,
) -> dict[str, Any]:
    """Rewrite leftover V3 contract actors to the transaction signer."""
    out = Path(output_dir)
    path = out / "liquidity_events.json"
    events = json.loads(path.read_text()) if path.exists() else []
    if not isinstance(events, list):
        events = []
    pending = [
        row
        for row in events
        if str(row.get("version") or "").lower() in {"v3", "3"}
        and str(row.get("event_type") or "").upper() == "LIQUIDITY_REMOVE"
        and row.get("actor_source") != "v3_npm_nft_owner"
        and str(row.get("actor") or "")
        and str(row.get("actor") or "").lower() != _V3_POSITION_MANAGER
    ]
    actors = [str(row.get("actor") or "") for row in pending]
    contracts = _code_contracts(actors)
    txs = sorted(
        {
            str(row.get("transaction_hash") or "").lower()
            for row in pending
            if str(row.get("actor") or "").lower() in contracts
            and str(row.get("transaction_hash") or "").startswith("0x")
        }
    )
    if not txs:
        return {"contracts": len(contracts), "txs": 0, "resolved": 0}

    cache = out / "dune_cache" / "index_{}_{}".format(from_block, to_block)
    gas_rows: list[dict] = []
    for i in range(0, len(txs), 200):
        gas_rows.extend(
            query(
                "cluster_gas_payers",
                tx_hash_list=txs[i : i + 200],
                cache_dir=cache,
                force_refresh=force_refresh,
                chunk_blocks=0,
            )
        )
    resolved = apply_v3_tx_senders(events, gas_rows, contract_actors=contracts)
    write_table("liquidity_events", events, out, artifact_format="json")
    return {
        "contracts": len(contracts),
        "txs": len(txs),
        "senders": len(gas_rows),
        "resolved": resolved,
    }
