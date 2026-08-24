# FTT crash/control validation results

Date: 2026-08-24

This note reports the first independent same-token validation of the project's
liquidity/price hypotheses.  The design, windows, pools, directions, 24-hour
horizon, observed-price endpoint rule, multiplicity family, and data-quality
thresholds were frozen before the outcome correlations were calculated; see
`research-notes/ftt-crash-control-preregistration.md`.

## Result

**None of the three primary hypotheses was confirmed.**  Both windows passed
the data-quality gates: target-token reserve coverage was 100%, all 181
Mint/Burn rows had quantified token amounts, and every primary comparison had
142 control pairs and 171 crash pairs (minimum required: 80).

| Predictor at hour t | Frozen expectation | Control Spearman ρ | Crash Spearman ρ | Crash p / BH q | Crash − control, 95% block-bootstrap CI | Verdict |
|---|---|---:|---:|---:|---:|---|
| Actual FTT Transfer net flow into pools / prior reserve | Negative future 24h return | -0.0085 | -0.1279 | 0.1128 / 0.1618 | -0.1194 [-0.3911, 0.1305] | Not confirmed |
| Net FTT Mint/Burn LP flow / prior reserve | Positive future 24h return | -0.0280 | **-0.2979** | **0.0026 / 0.0078** | -0.2699 [-0.5090, 0.0863] | Significant but opposite direction; not confirmed |
| Gross FTT LP activity / prior reserve | Positive future absolute 24h return | 0.0996 | 0.1564 | 0.1618 / 0.1618 | 0.0569 [-0.2936, 0.3122] | Not confirmed |

The net-LP-flow result is the useful anomaly.  During the crash window, more
net FTT added through Mint/Burn evidence was associated with a lower price over
the following 24 hours, not the pre-registered stabilizing direction.  Its
crash-window bootstrap interval narrowly excludes zero
(`[-0.4744, -0.0018]`) and its q-value passes the three-test FDR threshold.
However, it fails two confirmatory requirements: the sign is opposite the
frozen hypothesis, and the crash-minus-control interval crosses zero.  It is
therefore a transaction-forensics candidate rather than a validated warning
signal.

## Interpretation boundaries

- Positive target-token LP flow need not mean bullish capital.  An LP can add
  FTT while inventory is repriced downward, add asymmetric inventory, or react
  to volatility instead of predicting it.
- The control period had only 19 Mint/Burn events versus 162 during the crash
  period.  Correlation pair counts are adequate, but the control predictor has
  many tied zero values, which weakens the regime-difference estimate.
- The 24-hour returns overlap, so inference used 24-paired-observation moving
  blocks rather than iid errors.  This reduces, but cannot remove, dependence
  and confounding.
- The evidence covers three pre-selected Ethereum Uniswap FTT/WETH pools.  It
  does not include the centralized FTX order book and cannot reconstruct the
  complete cause of the crisis.
- Secondary 48/72-hour, Pearson, and 6/12/24-hour bucket outputs are exploratory
  and are not promoted to findings.

## Reproduction

```bash
python3 scripts/crash_control_validation.py \
  --control-dir output-ftt-control-30d \
  --crash-dir output-ftt-crash-30d \
  --out-dir output-ftt-crash-30d/research-crash-control
```

Machine-readable results are in
`output-ftt-crash-30d/research-crash-control/results.json`; the compact human
report is `output-ftt-crash-30d/research-crash-control/summary.md`.

## 中文结论

三项主要假设均未被确认。最值得继续调查的反常结果是：崩盘期净 LP 流入与
未来 24 小时价格收益呈负相关（Spearman `-0.2979`，BH `q=0.0078`），而不是
预注册的正方向。但它与对照期的相关系数差值区间仍跨过 0，且方向与原假设相反，
所以不能称为已验证的预警指标。更合适的表述是：崩盘期间 LP 添加 FTT 可能是
对下跌和波动的被动响应、库存再平衡或非对称建仓，下一步应回到具体交易证据，
或者用 CEL 独立复验该反常方向。
