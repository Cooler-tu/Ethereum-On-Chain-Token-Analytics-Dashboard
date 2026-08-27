# CEL crash/control validation

- Confirmatory primary tests: **0/3**.
- Primary design: hourly predictors vs observed-endpoint future 24h return; Spearman correlation.
- Dependence handling: 24-paired-observation moving-block bootstrap and block permutation.
- Multiplicity: BH-FDR across the three crash-window primary tests at q < 0.05.
- Minimum paired observations: 80 per window.

## Data quality

| Window | Hourly rows | Observed price rows | Reserve coverage | Quantified Mint/Burn |
|---|---:|---:|---:|---:|
| Control | 721 | 622 | 100.0% | 34/34 (100.0%) |
| Crash | 721 | 612 | 100.0% | 53/53 (100.0%) |

All return pairs require an actual trade in both endpoint buckets; carried-forward-only prices are excluded.

## Primary tests

| Predictor | Expected | Control ρ [95% CI] | Crash ρ [95% CI] | Crash p / BH q | Crash−control [95% CI] | Verdict | N control/crash |
|---|---|---:|---:|---:|---:|---|---:|
| actual_transfer_net_ratio | negative | 0.0915 [0.0323, 0.1725] | -0.0048 [-0.0791, 0.0829] | 0.9024 / 0.9024 | -0.0963 [-0.2113, 0.0086] | not confirmed | 522/504 |
| net_lp_flow_ratio | positive | 0.1107 [0.0316, 0.1780] | -0.0856 [-0.1531, -0.0003] | 0.0166 / 0.0498 | -0.1962 [-0.2847, -0.0780] | not confirmed | 522/504 |
| gross_lp_activity_ratio | positive | -0.0317 [-0.1315, 0.0626] | 0.0191 [-0.0489, 0.0797] | 0.6940 / 0.9024 | 0.0507 [-0.0694, 0.1716] | not confirmed | 522/504 |

## Interpretation

A primary hypothesis is confirmed only when the crash association has the frozen direction, its bootstrap CI excludes zero, its crash permutation p-value survives the three-test BH correction, and the crash-minus-control bootstrap CI excludes zero.

This is an Ethereum Uniswap study of 2 pre-selected CEL/WETH pool(s). It does not observe complete centralized-venue order flow and does not establish causality. Secondary horizons, Pearson results, and coarser buckets are saved separately and must not be promoted to confirmatory findings.
