# FTT + CEL opposite-direction LP-flow forensics

Date: 2026-08-27

The pre-registered FTT test and unchanged CEL replication both found a
negative, rather than registered-positive, association between hourly target-token
net LP flow and the future 24-hour return. This transaction-level phase asks
what those positive LP-flow hours actually contain. It does not change either
primary result and is explicitly exploratory.

## Deterministic selection

For each crash window:

1. require an observed price at hour `t` and `t+24h`;
2. retain `net_lp_flow_ratio > 0` and future 24-hour log return `< 0`;
3. rank descending by net LP flow divided by prior target-token reserve;
4. decompose the top five hours into pool, transaction, target/WETH inventory,
   signed Swap, actual Transfer, V3 tick, NFT tokenId, transaction sender, and
   owner-at-block evidence.

This produces 11 FTT and 10 CEL candidate hours. The rule is transparent and
reproducible, but it was created after the correlation result and is not a new
confirmatory test.

## Hour-level result

| Case | Candidate hours | Top-five venue | Target side of added WETH-equivalent value | Fully target-only share of tokens added | Largest hour: net LP / prior reserve | Largest hour: future 24h |
|---|---:|---|---:|---:|---:|---:|
| FTT | 11 | All V3 | 81.57% | 79.56% | +225.77% | -2.79% |
| CEL | 10 | All V3 | 67.32% | 0.00% | +1.98% | -13.67% |

All ten selected hours are V3-driven, and a single add transaction contributes
75.3%–100% of target tokens added in every selected hour. Positive target-token
LP flow is therefore highly event-concentrated; it is not a broad vote by many
independent LPs.

### FTT: an extreme one-sided inventory placement

The largest FTT hour is `2022-11-06 02:00 UTC`. NFT `354342`, controlled at the
transaction block by `0x74f53ed1175715d126c0c95d3b1b20f67c8a1273`, minted
`23,862.8321 FTT` and `0 WETH` into the 0.30% V3 pool. Its narrow tick range
`[-42240, -42180]` sat above the hour-close WETH/FTT price, so the position was
entirely FTT inventory below range. The hour also burned `657.6302 FTT` from a
different NFT, leaving `+23,205.2019 FTT` net LP flow. Dividing that amount by
the small prior attributable reserve (`10,278.2600 FTT`) creates the exceptional
`+225.77%` ratio. It is a concentrated limit-order-like placement, not evidence
that 225.77% of equivalent external capital entered the market.

### FTT: one verified short-lived position cycle

In the second-ranked hour, NFT `355173` was minted at block `15915923`
(`05:01:47 UTC`) and burned at block `15916002` (`05:17:35 UTC`): 79 blocks /
948 seconds later. Both actions have the same owner, transaction sender, and
tick range `[-48800, -35800]`, with essentially the same `101.3173 FTT` and
`1.2666 WETH`. This is direct evidence of short-gap liquidity cycling. It does
not explain the whole hour: a separate new NFT `355198` added `4,125.7364 FTT`
and `70 WETH`, dominating the positive net flow.

### CEL: in-range but often target-heavy

CEL has no fully target-only Mint among its selected top five. Its largest hour,
`2022-05-14 13:00 UTC`, is NFT `239116`: `24,238.2095 CEL` plus `2.1281 WETH`
in tick range `[243780, 245820]`, controlled by
`0x376731891c47fab75ccf690ad9afc6d3fa4a46c8`. The position was in range at the
hour close, but CEL still represented about 81.79% of its added value at that
price. Across the five CEL hours, the target side represents 67.32% of added
WETH-equivalent value. CEL therefore supports a target-inventory interpretation
without reproducing FTT's exact one-sided strategy.

## Position Manager trace quality

- 18 selected transactions and 18 pool Mint/Burn events were decoded.
- 17/18 pool events matched an Increase/DecreaseLiquidity event by exact
  `amount0` and `amount1`; the unmatched row is a zero-amount CEL Burn/poke.
- The matches expose 14 NFT tokenIds and 10 distinct transaction senders.
- Two events are below-range target-only positions; 16 are in-range at the
  hour-close price; none is WETH-only.
- One same-NFT opposite-action pair is verified in the selected set (FTT
  `355173`).

Historical `ownerOf` and same-receipt NFT Transfers identify the owner at the
transaction block where available. Hour-close price is used to classify range
shape and can differ from the exact intra-block execution price. Contract-facing
NonfungiblePositionManager ownership is never treated as beneficial LP identity.

## Interpretation

The repeated negative correlation is better described as **target-token
inventory provision during falling prices** than as generic capital inflow.
FTT and CEL share V3 dominance, target-side inventory weight, and high
single-transaction concentration. They do not yet share one exact strategy:
FTT includes an extreme target-only placement and verified rapid cycling,
whereas CEL's selected Mints are in range.

This suggests a prospective third-case hypothesis family, to be frozen before
outcome inspection:

- positive target-token LP-flow hours during a crash are disproportionately V3;
- added liquidity is concentrated in one transaction and weighted toward the
  target-token side by contemporaneous WETH value;
- target-side inventory share, not raw target-token net LP flow alone, is the
  candidate predictor of negative future return.

The thresholds, case, window, pool universe, event-time price, treatment of zero
LP hours, and statistical family still need pre-registration. No predictive or
causal claim should be made until that prospective test is complete.

## Reproduction

```bash
python3 scripts/cross_case_lp_forensics.py \
  --case FTT=output-ftt-crash-30d \
  --case CEL=output-cel-crash-30d \
  --top-n 5 --horizon-hours 24 \
  --out-dir output-cross-case-lp-forensics

python3 scripts/trace_v3_positions.py \
  --transactions output-cross-case-lp-forensics/top_hour_transactions.csv \
  --ranked-hours output-cross-case-lp-forensics/ranked_hours.csv \
  --case FTT=output-ftt-crash-30d \
  --case CEL=output-cel-crash-30d \
  --out-dir output-cross-case-lp-forensics
```

## 中文结论

FTT 与 CEL 的反向净 LP 流相关性，不能简单理解成“资金进入池子后价格反而下跌”。
交易拆解显示，两组案例前五名异常小时全部由 V3 主导，而且新增价值明显偏向目标
代币库存：FTT 为 81.57%，CEL 为 67.32%。FTT 最极端小时是一笔只加入
23,862.8321 FTT、完全不加入 WETH 的区间外单边仓位；CEL 最大小时虽然是区间内
双边仓位，但按当时价格计算仍有 81.79% 的新增价值来自 CEL 侧。

Position Manager 定向追踪还确认了一个 FTT NFT 在 15 分 48 秒内由同一钱包、
同一 tick 区间先加后撤。这说明净 LP 流同时可能包含单边库存挂单、正常双边做市和
短期仓位循环。当前更准确的机制描述是“下跌中的目标代币库存配置”，而不是笼统的
外部资本流入。下一步应把 V3 占比、目标侧价值占比和单笔交易集中度写入第三个案例
的预注册设计，再做真正的前瞻验证。
