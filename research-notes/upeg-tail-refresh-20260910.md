# uPEG June to August data repair

The canonical local run remains `output-upeg-may-sep-2026/`, for Ethereum token
`0x44b28991B167582F18BA0259e0173176ca125505`, blocks 24996368–25878705.
The refresh boundary is block 25218798, the first block on or after
2026-06-01 00:00 UTC. May is reused from the existing output and Dune caches.

## Why a completed run could still be incomplete

The Dune indexer previously caught liquidity/Transfer query failures and wrote
the other sections anyway. It also queried only the first 40 verified V4 pools.
This run has 96 verified V4 pools. The repair makes section failures fatal before
artifact writes and removes the V4 truncation. Empty successful query results
still require coverage checks; successful execution alone is not completeness.

The notebook's withdrawal chart also read a separate September 6 cache. It now
derives its plot inputs from the current canonical liquidity and reserve files,
and stores its regenerated chart cache under the same output directory.

## Reproduction

```bash
python3 -u scripts/refresh_upeg_tail.py
python3 -u scripts/verify_upeg_tail.py
python3 scripts/rebuild_upeg_tail_views.py
python3 scripts/publish_site.py
```

The refresh uses 528 checked RPC chunks covering the ten verified V2/V3 pools,
all 96 verified V4 pool IDs, and all uPEG ERC20 Transfer events from June onward.
It retains other-DEX swaps from the original dataset. Raw logs, resumable caches,
the frozen boundary, validation results and original-file backups are below
`output-upeg-may-sep-2026/tail_refresh_20260910/`. Failed requests are not recorded
as successful empty chunks. RPC headers use the configured endpoint; log retrieval
uses Ethereum dRPC because the configured provider permits only ten blocks per
log request. The fallback's chain ID was checked as Ethereum mainnet.

## Interpretation limits

- May was reused, not independently re-scanned. Missing May V4 and Transfer rows
  were recovered from existing local caches where available.
- June onward V4 Swap logs identify actual pool IDs. Matching Dune swaps retain
  their USD valuation; new RPC-only swaps have no invented USD valuation.
- V4 liquidity principal amounts use the preceding observed pool price and tick
  math; unavailable prices remain unquantified. Zero-liquidity modifications are
  classified separately from additions/removals. May cached call deltas may
  include fees and hook effects, so amount sources are not homogeneous.
- Pool-event sender/owner fields are not automatically beneficial owners. Existing
  V3 NFT identity evidence is retained; a complete LP ownership reconstruction is
  a separate task. Cumulative gross removals are not permanent capital exit.
- Existing historical holder/reserve snapshots are retained. This refresh does
  not extend the original end block or re-rank holders from full wallet history.
- Exact Transfer-to-balance reconciliation verifies net consistency, not the
  absence of every possible offsetting omission.

## 中文

本次保留五月缓存，六月起补抓原始日志，统一合并到原来的长窗口目录。
修复了查询失败后仍覆盖输出、V4 仅取前 40 个池，以及撤资图读取旧缓存的问题。
补齐事件不等于已经识别最终 LP 所有人；累计撤出也不等于永久离场。
五月覆盖沿用缓存，V4 金额中存在估算与旧缓存不同口径，仍须保留来源说明。

## Completed validation

The merged output contains 248,515 swaps, 15,362 liquidity/collection records,
and 360,542 Transfers. All 167,163 May swaps are unchanged. The tail scan
verifies 81,154 Uniswap swaps; 198 other retained tail swaps remain outside that
RPC pool scope. June/July/August liquidity/collection counts are 879/486/1,065,
and Transfer counts are 37,368/25,509/45,455. All twelve checked custody addresses
reconcile the June–August Transfer net to historical balance changes exactly.
Tests: 147 passed, 20 skipped.

六月、七月、八月已分别恢复 879、486、1,065 条流动性/领取记录，
以及 37,368、25,509、45,455 条 Transfer。十二个托管/池地址的净流量
均与期初期末链上余额变化精确一致；五月 167,163 条 Swap 保持不变。

An extreme-tick QA check caught an additional amount-calculation defect: at
block 25680626, decimal tick boundaries inflated a V4 withdrawal estimate to
1.85038 billion uPEG. Protocol-exact integer boundaries yield approximately
0.00988002 uPEG for that side. The integer TickMath calculation and observed-price
regression vector now prevent this numerical artifact. See the source reference
in `src/analysis/v3_math.py`. Event counts and Transfer reconciliation are unchanged.
