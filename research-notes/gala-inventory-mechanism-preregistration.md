# GALA third-case inventory mechanism — pre-registration

Date frozen: 2026-08-29

This note freezes the only planned prospective test of the V3 target-inventory
mechanism suggested by the completed FTT/CEL forensics. It is written before
GALA target-side value shares, transaction concentration, future-return
correlations, or event/control differences are calculated. Regardless of the
answer, no fourth hand-selected forensic case will be added.

## Incident anchor

Gala's official report says a compromised address with a minter role created
five billion unauthorized GALA tokens on May 20, 2024; see the
[official incident report](https://news.gala.com/gala-games/incident-report-unauthorized-token-minting-blockchain-game-partners-inc/).
The mint is Ethereum transaction
[`0xa6d90a…77fe`](https://etherscan.io/tx/0xa6d90abe17d17743a9cecab84bcefb0fd0bbfa0c61bba60fd2f680b0a2f077fe)
in block `19913232`, timestamped exactly `2024-05-20 19:32:11 UTC`. The event
window begins at that block so the unauthorized mint and subsequent Uniswap
selling are not incorrectly placed in the control window.

## Frozen windows

The windows are adjacent exact 30-day UTC intervals and do not overlap.

| Window | UTC | Blocks (inclusive) | Role |
|---|---|---:|---|
| Control | 2024-04-20 19:32:11 → 2024-05-20 19:32:11 | `19698731–19913231` | Same token and pools immediately before the mint |
| Event | 2024-05-20 19:32:11 → 2024-06-19 19:32:11 | `19913232–20127891` | Begins with the unauthorized mint and covers the aftermath |

Block `19698731` and the incident block are timestamped exactly at their UTC
boundaries. Block `20127892`, excluded from the event window, is timestamped
exactly `2024-06-19 19:32:11 UTC`.

## Frozen pool universe

`research-inputs/gala-primary-pools.json` fixes two GALA/WETH pools:

| Pool | Version | Fee | Control early/late Swaps | Event early/late Swaps |
|---|---|---:|---:|---:|
| `0x72B1…579A` | V2 | — | 93 / 52 | 409 / 59 |
| `0x465E…3719` | V3 | 0.30% | 245 / 218 | 1,730 / 143 |

Each sample covers 10,000 blocks. These are feasibility counts only. The V3 1%
pool `0xF1Dd…1597` is excluded because its pre-event samples contain only 4/11
Swaps and its GALA reserve is below 0.35% of the main V3 pool. Stablecoin and
non-Uniswap pools are excluded to keep the quote unit and architecture aligned
with the FTT/CEL WETH study. Pool selection will not change after outcomes are
visible.

## Frozen feature construction

The unit is an hourly token-total bucket across the two selected pools.

Only quantified pool `Mint` additions form LP-add value. The five-billion-token
contract mint, ordinary Swaps, Transfers, Burns, and Collects are not counted as
LP additions.

For every pool Mint:

1. use the most recent same-pool Swap price at or before the Mint within one
   hour, respecting block and log order;
2. if unavailable, use the pool's end-of-block on-chain price (`slot0` for V3,
   reserve ratio for V2);
3. if neither is available, mark the Mint unpriced and exclude its value from
   the primary feature while reporting coverage.

Within each hour:

- `target_inventory_share` = added GALA valued in WETH / total added
  GALA-plus-WETH value;
- `largest_add_tx_share` = the largest transaction's added WETH-equivalent value
  / total added value;
- `v3_add_value_share` = V3 added value / all selected-pool added value.

Hours with no quantified, priced LP addition are missing for these features and
are **not** encoded as zero. Price outcomes use token-total WETH per GALA close;
both `t` and `t+24h` must contain observed trades, not carried-only prices.

## Frozen primary hypotheses

| ID | Test | Frozen direction |
|---|---|---|
| H1 | Event-window Spearman correlation: `target_inventory_share[t]` vs future 24h GALA/WETH log return | Negative |
| H2 | Event minus control difference in median `target_inventory_share` across eligible LP-add hours | Positive |
| H3 | Event minus control difference in median `largest_add_tx_share` across eligible LP-add hours | Positive |

`v3_add_value_share`, actual pool Transfer net, raw target-token LP flow, and
one-sided-range classification are secondary descriptive evidence. They cannot
replace a failed primary test. No non-zero lag search is allowed.

## Frozen inference and stop rules

- Hourly base grid; 24-hour future return only.
- Calendar-time moving-block bootstrap with 24-hour blocks, 1,999 repetitions.
- Block permutation null, 4,999 repetitions.
- BH-FDR across H1–H3, `q < 0.05`.
- Seed `20260829`.
- Confirmation requires the frozen direction, BH `q < 0.05`, and a 95% block
  bootstrap interval excluding zero.
- H1 requires at least 30 eligible event-window price/feature pairs.
- H2/H3 require at least 30 eligible hours in each window.
- At least 90% of Mint rows must have quantified token amounts, and at least 80%
  of added WETH-equivalent value must be priced by the frozen hierarchy.
- Underpowered or low-coverage tests are reported as such; thresholds, pools,
  bucket size, outcome horizon, and missing-value handling will not be changed.
- Position Manager identity remains skipped during full collection. Targeted
  receipt/NFT tracing is allowed only if at least one primary test confirms and
  is then supporting evidence, not a new test.
- This is the final hand-selected case. Failure closes this mechanism as an
  unconfirmed descriptive pattern; success moves it to batch-screen validation,
  not another hand-picked case.

## Frozen collection commands

```bash
set -a
source .env
set +a
export ETH_LOG_CHUNK_SIZE=10000
export ETH_BLOCK_BATCH_SIZE=20

python3 -m src.cli analyze 0xd1d2Eb1B1e90B638588728b4130137D262C87cae \
  --from-block 19698731 --to-block 19913231 \
  --pools-file research-inputs/gala-primary-pools.json \
  --index-source rpc --holdings-source rpc \
  --skip-position-manager --pool-transfers-only --artifact-format both \
  --output-dir output-gala-control-30d

python3 -m src.cli analyze 0xd1d2Eb1B1e90B638588728b4130137D262C87cae \
  --from-block 19913232 --to-block 20127891 \
  --incident-block 19913232 \
  --pools-file research-inputs/gala-primary-pools.json \
  --index-source rpc --holdings-source rpc \
  --skip-position-manager --pool-transfers-only --artifact-format both \
  --output-dir output-gala-event-30d
```

After collection, both outputs will be rebuilt as hourly research series with
historical reserve snapshots. A dedicated validation script will implement the
frozen features and inference. It will not be run until this pre-registration
is committed and pushed.

## 中文摘要

第三案例选择 GALA，是因为未经授权增发有精确链上交易和时间边界，攻击者随后直接
通过 Uniswap 抛售，而且主 V3 池在事件前后均有充足 Swap 与 Mint/Burn。控制期固定
为事件前 30 天，事件期固定为事件后 30 天。主要检验只包含三项：目标代币新增价值
占比与未来 24 小时收益的负相关、事件期相对控制期的目标侧价值占比上升、以及单笔
交易集中度上升。没有 LP Add 的小时视为缺失而不是零，不搜索其他 lag，也不会在
看到结果后更换池、阈值或窗口。这是最后一个人工挑选案例：失败就结束这条机制研究，
成功也只进入批量扫描验证，不再继续挑第四个案例。
