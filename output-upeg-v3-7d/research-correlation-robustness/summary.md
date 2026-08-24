# Correlation robustness audit

- Scope: `0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775`
- Base bucket seconds: `3600`
- Bucket factors: `1, 2, 4, 6, 12, 24`
- Features: `price_return, tvl_change, volume_turnover`
- Valid lag tests: `612`
- Global BH-FDR threshold: `0.05`
- Tests surviving global BH-FDR: `0`
- Zero-lag family BH-FDR: `9/36`
- Exploratory lead-lag family BH-FDR: `0/576`
- Null test: two-sided block permutation; CI: paired moving-block bootstrap.

## Best lag per bucket / feature pair

| Bucket | X | Y | Method | Lag | Correlation | 95% CI | Block p | Family q | Global q | Verdict | N |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 14400s | price_return | tvl_change | pearson | 0 | -0.8166 | [-0.9133, -0.6148] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 41 |
| 7200s | price_return | tvl_change | pearson | 0 | -0.8027 | [-0.9031, -0.6242] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 83 |
| 7200s | price_return | tvl_change | spearman | 0 | -0.7932 | [-0.8971, -0.6427] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 83 |
| 3600s | price_return | tvl_change | spearman | 0 | -0.7757 | [-0.8625, -0.6693] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 168 |
| 14400s | price_return | tvl_change | spearman | 0 | -0.7575 | [-0.8965, -0.5558] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 41 |
| 21600s | price_return | tvl_change | spearman | 0 | -0.7534 | [-0.9097, -0.4563] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 27 |
| 21600s | price_return | tvl_change | pearson | 0 | -0.7410 | [-0.9171, -0.5013] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 27 |
| 3600s | price_return | tvl_change | pearson | 0 | -0.6791 | [-0.8207, -0.5553] | 0.0010 | 0.0045 | 0.0765 | CI excludes 0, family FDR pass | 168 |
| 43200s | price_return | tvl_change | pearson | 0 | -0.7638 | [-0.9644, -0.3152] | 0.0080 | 0.0320 | 0.2720 | CI excludes 0, family FDR pass, low power | 13 |
| 21600s | price_return | volume_turnover | pearson | 2 | 0.5402 | [0.0027, 0.7637] | 0.0040 | 0.5120 | 0.2720 | CI excludes 0 | 25 |
| 14400s | tvl_change | volume_turnover | spearman | -3 | -0.4080 | [-0.6823, -0.0150] | 0.0060 | 0.5120 | 0.2720 | CI excludes 0 | 38 |
| 7200s | price_return | volume_turnover | spearman | 5 | 0.3087 | [0.0871, 0.5025] | 0.0070 | 0.5120 | 0.2720 | CI excludes 0 | 78 |
| 7200s | tvl_change | volume_turnover | spearman | 5 | -0.2785 | [-0.4465, -0.1101] | 0.0080 | 0.5120 | 0.2720 | CI excludes 0 | 78 |
| 3600s | tvl_change | volume_turnover | spearman | -16 | -0.2394 | [-0.3929, -0.0832] | 0.0050 | 0.5120 | 0.2720 | CI excludes 0 | 152 |
| 3600s | price_return | volume_turnover | spearman | 12 | 0.1842 | [0.0350, 0.3252] | 0.0070 | 0.5120 | 0.2720 | CI excludes 0 | 156 |
| 3600s | price_return | volume_turnover | pearson | 12 | 0.1888 | [0.0625, 0.2877] | 0.0120 | 0.5760 | 0.3497 | CI excludes 0 | 156 |
| 43200s | price_return | volume_turnover | pearson | 1 | 0.5326 | [0.3069, 0.8843] | 0.0150 | 0.5760 | 0.3825 | CI excludes 0, low power | 12 |
| 43200s | price_return | tvl_change | spearman | 0 | -0.6648 | [-1.0000, -0.2091] | 0.0160 | 0.0576 | 0.3917 | CI excludes 0, low power | 13 |
| 3600s | tvl_change | volume_turnover | pearson | 0 | 0.2027 | [-0.1560, 0.4611] | 0.0300 | 0.0982 | 0.5923 | exploratory | 168 |
| 43200s | price_return | volume_turnover | spearman | 1 | 0.6224 | [0.2274, 0.9140] | 0.0370 | 0.7680 | 0.6120 | CI excludes 0, low power | 12 |
| 7200s | price_return | volume_turnover | pearson | 5 | 0.2398 | [0.0313, 0.4015] | 0.0350 | 0.7680 | 0.6120 | CI excludes 0 | 78 |
| 7200s | tvl_change | volume_turnover | pearson | -6 | -0.2371 | [-0.4347, 0.0321] | 0.0360 | 0.7680 | 0.6120 | exploratory | 77 |
| 21600s | tvl_change | volume_turnover | spearman | 2 | -0.3754 | [-0.6538, 0.0548] | 0.0400 | 0.7680 | 0.6250 | exploratory | 25 |
| 21600s | price_return | volume_turnover | spearman | 2 | 0.3577 | [-0.1143, 0.6958] | 0.0650 | 0.8576 | 0.7322 | exploratory | 25 |
| 14400s | tvl_change | volume_turnover | pearson | -3 | -0.3138 | [-0.5095, 0.0914] | 0.0740 | 0.8640 | 0.7548 | exploratory | 38 |
| 21600s | tvl_change | volume_turnover | pearson | -3 | -0.4105 | [-0.5950, 0.0149] | 0.0760 | 0.8640 | 0.7625 | exploratory | 24 |
| 14400s | price_return | volume_turnover | spearman | -3 | 0.2794 | [-0.0616, 0.5551] | 0.0920 | 0.8640 | 0.7691 | exploratory | 38 |
| 14400s | price_return | volume_turnover | pearson | 2 | 0.2564 | [0.0450, 0.4814] | 0.0890 | 0.8640 | 0.7691 | CI excludes 0 | 39 |
| 43200s | tvl_change | volume_turnover | spearman | 1 | -0.5524 | [-0.8512, -0.0960] | 0.1100 | 0.9183 | 0.8284 | CI excludes 0, low power | 12 |
| 43200s | tvl_change | volume_turnover | pearson | 0 | 0.5535 | [-0.6428, 0.9028] | 0.1430 | 0.3432 | 0.9022 | low power | 13 |
| 86400s | price_return | tvl_change | spearman | 0 | -0.9429 | [-1.0000, -0.8000] | 0.3330 | 0.6347 | 0.9463 | CI excludes 0, low power | 6 |
| 86400s | price_return | tvl_change | pearson | 0 | -0.8462 | [-1.0000, -0.7009] | 0.3350 | 0.6347 | 0.9463 | CI excludes 0, low power | 6 |
| 86400s | tvl_change | volume_turnover | spearman | 0 | -0.3143 | [-1.0000, 0.8000] | 0.4920 | 0.7701 | 0.9922 | low power | 6 |
| 86400s | price_return | volume_turnover | pearson | 0 | -0.4250 | [-0.9711, 0.9545] | 0.8310 | 0.9065 | 0.9975 | low power | 6 |
| 86400s | price_return | volume_turnover | spearman | 0 | 0.0857 | [-0.8000, 1.0000] | 0.8140 | 0.9065 | 0.9975 | low power | 6 |
| 86400s | tvl_change | volume_turnover | pearson | 0 | 0.0306 | [-0.9980, 0.9880] | 1.0000 | 1.0000 | 1.0000 | low power | 6 |

## Interpretation guardrails

- Selecting the largest absolute lag is exploratory; the global BH correction covers all tested feature pairs, lags, methods, and bucket variants in this run.
- Block permutation and moving-block bootstrap retain short-range dependence better than iid resampling. Neither corrects unmeasured confounding.
- Coarse variants with fewer than 20 aligned observations are labelled low power even if their point estimate is large.
- Stability requires direction and plausible horizon to persist across bucket sizes, not merely one significant cell.
