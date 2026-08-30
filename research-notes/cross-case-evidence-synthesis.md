# Cross-case evidence synthesis and research pivot

Date: 2026-08-30

This synthesis asks a deliberately narrow decision question: after FTT, CEL,
and GALA, is any existing liquidity variable valuable enough to keep as a
standalone 24-hour price predictor? The answer is **no**.

## Uniform evidence ledger

`scripts/cross_case_evidence_ledger.py` applies the same hourly predictor,
future 24-hour outcome, Spearman statistic, 24-observation moving-block
bootstrap, and two-sided block permutation to all six existing windows. All 18
rows share one BH family. This is exploratory because FTT/CEL were already
observed before the family was defined.

| Incident-preceding predictor | FTT ρ | CEL ρ | GALA ρ | Same sign? | Cases passing global BH |
|---|---:|---:|---:|---|---|
| Actual pool Transfer net / reserve | -0.1279 | -0.0048 | +0.0495 | No | None |
| Net LP flow / reserve | -0.2979 | -0.0856 | +0.0527 | No | FTT only |
| Gross LP activity / reserve vs absolute return | +0.1564 | +0.0191 | +0.0386 | Yes | None |

The FTT net-LP association remains real within that selected window (`q=0.0216`
in the global 18-test family), but it is not transportable. CEL weakens to
`q=0.1056`, and GALA changes sign. CEL's baseline net-LP association is positive
and globally significant (`q=0.0378`), another warning that the sign is
regime-dependent rather than a stable crash rule.

GALA's post-incident correlations are also near zero: pool Transfer net
`-0.0048`, net LP flow `-0.0281`, and gross LP activity `+0.0511`. The failed
prospective target-inventory tests therefore agree with the common-metric
ledger rather than hiding a strong alternative signal.

## What is retired

- Pool Transfer net flow is retained as a reserve-ledger reconciliation field,
  not a directional price signal.
- Net LP flow is retained as a description of pool inventory change, not a
  standalone 24-hour predictor.
- Gross Mint/Burn activity is retained as a market-activity measure, not a
  proxy for permanent capital exit or future volatility.
- Target-side Mint value and largest-transaction share remain forensic
  descriptors. GALA did not validate them prospectively.
- Position Manager wallet/NFT tracing, more hand-picked tokens, threshold
  changes, and lag searches are stopped. They cannot rescue transportability.

## Comparability boundary

FTT and CEL incident windows end immediately before their public cutoffs; GALA
has a separate 30-day pre-event window and a 30-day post-event window. The
ledger labels these phases and does not pool them. A true event study requires
identical geometry around every timestamp and cannot reuse the old labels as if
they were interchangeable.

## High-value pivot: incident-centered market response

The next question should be about a **joint market response**, not another LP
single-variable correlation:

> After an externally timestamped token/protocol incident, how do price,
> trading turnover, and target-token pool inventory change together, and which
> early response patterns are associated with recovery versus continued
> decline?

The work proceeds through gates:

1. Build an objective incident registry using public primary sources and exact
   timestamps/blocks. Do not select cases from visible correlation outcomes.
2. Run light feasibility only: token contract, pre-existing WETH venue,
   non-zero pre/post reserve, and Swap counts in fixed samples.
3. Require at least eight eligible incidents before full indexing. If fewer
   than eight pass, stop this design rather than lower the bar.
4. Only then freeze identical event geometry (candidate: seven days before and
   after), fixed horizons, normalization, missing-data rules, and the primary
   family.
5. Keep the primary model small. No machine learning, wallet tracing, lag scan,
   or protocol-specific feature until the broad event panel shows a repeatable
   effect.

The first deliverable is therefore the incident registry and feasibility
screen, not another expensive token analysis.

## Reproduction

```bash
python3 scripts/cross_case_evidence_ledger.py \
  --output-dir output-cross-case-synthesis
```

Detailed results are in `output-cross-case-synthesis/summary.md` and
`association_ledger.csv`.

## 中文结论

统一六个窗口、三个指标并对 18 项检验整体校正后，没有任何单变量具备跨案例迁移
价值。FTT 的净 LP 流负相关仍在该窗口显著，但 CEL 在全局校正后不显著，GALA 事前
窗口更变成正相关；累计 LP 活动虽在三个事前窗口同为正，但全部不显著。因此池
Transfer 净流、净 LP 流、累计 LP 活动、目标侧新增价值和单笔集中度都不再作为独立
价格预测器，只保留为记账或描述字段。

下一阶段改为“事件中心的联合市场响应”：用客观规则建立至少八个具有精确事件时间、
事前已存在 WETH 池且前后有交易的数据案例，再以统一的事件前后窗口研究价格、成交
周转和池库存共同如何变化。案例不足八个就停止，不降低门槛；在出现跨案例效果前，
不做 Position Manager 身份追踪、不搜索 lag、不上机器学习，也不再人工挑有利案例。
