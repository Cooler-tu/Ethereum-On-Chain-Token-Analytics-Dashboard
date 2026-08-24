# FTT crash/control validation

- Confirmatory primary tests: **0/3**.
- Primary design: hourly predictors vs observed-endpoint future 24h return; Spearman correlation.
- Dependence handling: 24-paired-observation moving-block bootstrap and block permutation.
- Multiplicity: BH-FDR across the three crash-window primary tests at q < 0.05.
- Minimum paired observations: 80 per window.

## Data quality

| Window | Hourly rows | Observed price rows | Reserve coverage | Quantified Mint/Burn |
|---|---:|---:|---:|---:|
| Control | 716 | 314 | 100.0% | 19/19 (100.0%) |
| Crash | 717 | 336 | 100.0% | 162/162 (100.0%) |

All return pairs require an actual trade in both endpoint buckets; carried-forward-only prices are excluded.

## Primary tests

| Predictor | Expected | Control ρ [95% CI] | Crash ρ [95% CI] | Crash p / BH q | Crash−control [95% CI] | Verdict | N control/crash |
|---|---|---:|---:|---:|---:|---|---:|
| actual_transfer_net_ratio | negative | -0.0085 [-0.1768, 0.2508] | -0.1279 [-0.2280, 0.0460] | 0.1128 / 0.1618 | -0.1194 [-0.3911, 0.1305] | not confirmed | 142/171 |
| net_lp_flow_ratio | positive | -0.0280 [-0.2169, 0.1136] | -0.2979 [-0.4744, -0.0018] | 0.0026 / 0.0078 | -0.2699 [-0.5090, 0.0863] | not confirmed | 142/171 |
| gross_lp_activity_ratio | positive | 0.0996 [-0.0026, 0.1837] | 0.1564 [-0.1882, 0.3993] | 0.1618 / 0.1618 | 0.0569 [-0.2936, 0.3122] | not confirmed | 142/171 |

## Interpretation

A primary hypothesis is confirmed only when the crash association has the frozen direction, its bootstrap CI excludes zero, its crash permutation p-value survives the three-test BH correction, and the crash-minus-control bootstrap CI excludes zero.

This is an Ethereum Uniswap study of three pre-selected FTT/WETH pools. It does not observe the complete centralized-exchange order flow and does not establish causality. Secondary horizons, Pearson results, and coarser buckets are saved separately and must not be promoted to confirmatory findings.
