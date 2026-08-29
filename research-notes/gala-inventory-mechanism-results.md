# GALA inventory-mechanism validation results

Date completed: 2026-08-29

This is the outcome of the design frozen in
`gala-inventory-mechanism-preregistration.md`. It is the third and final
hand-selected case; no pool, window, feature, lag, or threshold was changed
after the outcome became visible.

## Data and coverage

The adjacent 30-day control/event windows cover the fixed GALA/WETH V2 and V3
0.30% pools. The control run indexed 5,879 Swaps, 252 liquidity events, and
5,998 pool Transfers; the event run indexed 7,022 Swaps, 398 liquidity events,
and 7,170 pool Transfers. Each hourly research table contains 721 token-total
buckets.

All 72 control Mints and all 128 event Mints have quantified token amounts.
Every Mint has a same-pool Swap at or before it within one hour, so all 200
Mints use the frozen primary price source and none requires a fallback price.
This yields 65 control and 79 event hours with priced LP additions. The amount,
pricing, and minimum-sample gates all pass.

## Primary results

Inference uses 1,999 24-hour calendar moving-block bootstrap repetitions,
4,999 two-sided block permutations, seed `20260829`, and BH correction across
H1–H3.

| Test | Frozen direction | Control | Event/effect | 95% block CI | p | BH q | Confirmed |
|---|---|---:|---:|---:|---:|---:|---|
| H1: target share vs future 24h return | Negative | — | Spearman `ρ=-0.0915` (N=78) | `[-0.2725, 0.0880]` | `0.4646` | `0.6969` | No |
| H2: event − control median target share | Positive | `0.4700` (N=65) | `+0.0420`; event `0.5120` (N=79) | `[-0.0401, 0.2382]` | `0.1938` | `0.5814` | No |
| H3: event − control median largest-tx share | Positive | `1.0000` (N=65) | `0.0000`; event `1.0000` (N=79) | `[0.0000, 0.0000]` | `1.0000` | `1.0000` | No |

H1 has the frozen negative sign, but its effect is small and its interval
crosses zero. H2 also has the frozen positive sign, but its interval crosses
zero after calendar dependence is retained. H3 is exactly unchanged: the
median add hour is dominated by one transaction in both windows, so this
concentration statistic does not distinguish the incident period.

## Decision

Zero of three primary hypotheses confirms. Under the pre-registered stop rule,
the concentrated target-inventory mechanism remains an unconfirmed descriptive
pattern and the hand-selected case line closes. We will not select a fourth
token to rescue it. The negative result does not prove LP inventory never
matters; it shows that the FTT/CEL forensic pattern did not generalize strongly
enough to this prospective GALA incident under the frozen design.

The highest-value next step is a direction reset and cross-case synthesis, not
more detailed GALA wallet/NFT tracing. Position Manager identity was explicitly
conditional on a confirmed primary test, and that condition was not met.

## Reproduction

```bash
python3 scripts/gala_inventory_validation.py \
  --control-dir output-gala-control-30d \
  --event-dir output-gala-event-30d \
  --pools-file research-inputs/gala-primary-pools.json \
  --output-dir output-gala-inventory-validation
```

Machine-readable results are in
`output-gala-inventory-validation/primary_tests.json`; Mint-level valuations
and eligible hourly features are also exported as CSV.

## 中文结论

GALA 是第三个、也是最后一个人工挑选案例。控制期与事件期分别抓取 5,879 / 7,022
笔 Swap；72 / 128 条 Mint 全部有可量化金额，而且 200 条 Mint 都能使用同池、发生
在其之前一小时内的真实 Swap 价格，因此覆盖门槛全部通过。

三项主假设均未确认。H1 的方向虽为负，但相关性只有 `-0.0915`，置信区间跨 0；
H2 的事件期目标侧占比中位数比控制期高 `0.0420`，但区间同样跨 0；H3 在两个窗口
的中位数都为 `1.0000`，没有上升。按照预注册停止规则，不再挑第四个代币，也不继续
追踪 GALA Position Manager 身份。这条“集中目标库存配置可解释未来下跌”的机制目前
只能保留为未确认的描述性线索。下一步应转向跨案例总结和重新选择研究问题，而不是
继续在单个案例中深挖。
