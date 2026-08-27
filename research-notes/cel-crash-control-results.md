# CEL crash/control replication results

Date: 2026-08-27

This is the first independent replication of the FTT same-token crash/control
design.  The corrected event cutoff, adjacent 30-day windows, two active
CEL/WETH pools, variables, directions, 24-hour horizon, inference, seed, and
stop rules were committed in `a78cabd` before any CEL outcome correlation was
calculated; see `research-notes/cel-crash-control-preregistration.md`.

## Result

**None of the three original directional hypotheses was confirmed (0/3).**
However, the opposite-direction net-LP-flow anomaly first seen in FTT appears
again in CEL.

| Predictor at hour t | Frozen expectation | Control Spearman ρ | Crash Spearman ρ | Crash p / BH q | Crash − control, 95% block-bootstrap CI | Verdict |
|---|---|---:|---:|---:|---:|---|
| Actual CEL Transfer net flow into pools / prior reserve | Negative future 24h return | 0.0915 | -0.0048 | 0.9024 / 0.9024 | -0.0963 [-0.2113, 0.0086] | Not confirmed |
| Net CEL Mint/Burn LP flow / prior reserve | Positive future 24h return | 0.1107 | **-0.0856** | **0.0166 / 0.0498** | **-0.1962 [-0.2847, -0.0780]** | Significant but opposite direction; not confirmed |
| Gross CEL LP activity / prior reserve | Positive future absolute 24h return | -0.0317 | 0.0191 | 0.6940 / 0.9024 | 0.0507 [-0.0694, 0.1716] | Not confirmed |

For net LP flow, the crash-window 95% moving-block interval is
`[-0.1531, -0.0003]`.  It only narrowly excludes zero, and the BH q-value
`0.0498` is just below the frozen 0.05 threshold.  The crash-minus-control
interval is entirely negative, unlike FTT's wider interval.  Because the sign
is opposite the registered positive hypothesis, this remains a replicated
anomaly—not a confirmatory success and not a causal warning rule.

## Cross-case comparison

| Case | Crash net-LP-flow ρ | BH q | Crash − control ρ | Difference 95% CI | Original positive hypothesis |
|---|---:|---:|---:|---:|---|
| FTT | -0.2979 | 0.0078 | -0.2699 | [-0.5090, 0.0863] | Not confirmed; difference uncertain |
| CEL | -0.0856 | 0.0498 | -0.1962 | [-0.2847, -0.0780] | Not confirmed; opposite-direction difference |

The repeated sign supports a new transaction-level question: during a collapse,
does positive target-token LP flow represent market makers absorbing or adding
falling inventory, asymmetric liquidity provision, adverse selection, or
rapid remove/re-add behavior rather than bullish capital support?  That
mechanism was not pre-registered, so it must be investigated as a new phase and
tested prospectively on a later case before becoming a predictive claim.

## Data quality

| Window | Hourly token-total rows | Observed-price rows | Primary pairs | Reserve coverage | Quantified Mint/Burn |
|---|---:|---:|---:|---:|---:|
| Control | 721 | 622 | 522 | 100% | 34/34 (100%) |
| Crash | 721 | 612 | 504 | 100% | 53/53 (100%) |

- Control collection: 4,076 Swaps, 51 liquidity rows, 3,998 pool-endpoint
  Transfers.
- Crash collection: 4,972 Swaps, 78 liquidity rows, 4,841 pool-endpoint
  Transfers.
- Every pool/window Transfer sum exactly matches its historical CEL balance
  change:
  - Control V3: `-4804295489` raw; V2: `+488513690` raw.
  - Crash V3: `-441322596` raw; V2: `+464524306` raw.
- Position Manager identity was intentionally skipped.  Mint/Burn amounts are
  pool-level evidence; LP beneficial-owner identity remains unavailable.
- The legacy static risk scores (`0.0855` control, `0.3738` crash, both labelled
  LOW) are not the registered outcome and must not replace the time-series test.

## Interpretation boundaries

- CEL's primary q-value and crash CI are borderline; small design changes could
  change threshold classification.  The frozen analysis is reported unchanged.
- LP predictors contain many zero hours (18 unique control values and 28 crash
  values among the paired rows), so rank ties remain important.
- Future 24-hour returns overlap; 24-paired-observation moving blocks were used
  to reduce iid overconfidence.
- The study covers two pre-selected Ethereum Uniswap CEL/WETH pools.  It does
  not observe Celsius's centralized platform ledger or complete market flow.
- Association does not determine whether LP behavior leads, reacts to, or is
  jointly driven by falling prices and volatility.

## Reproduction

```bash
python3 scripts/crash_control_validation.py \
  --control-dir output-cel-control-30d \
  --crash-dir output-cel-crash-30d \
  --study-label CEL \
  --out-dir output-cel-crash-30d/research-crash-control
```

## 中文结论

CEL 的三项原始方向性假设仍然是 `0/3` 确认，但 FTT 中出现的反常方向获得了
第一次独立复现：崩盘期净 LP 流与未来 24 小时收益呈负相关（Spearman
`-0.0856`，BH `q=0.0498`），崩盘减对照的区间也完全低于 0。由于预注册方向
原本是正相关，因此不能把它写成“原假设验证成功”；更准确的结论是，FTT 与
CEL 都提示危机期间的目标代币 LP 净流入可能代表吸收下跌库存、非对称做市、
逆向选择或撤出后重建，而不是价格支撑。下一阶段应比较两个案例的具体小时与
交易行为，再将新机制预注册到第三个独立案例。
