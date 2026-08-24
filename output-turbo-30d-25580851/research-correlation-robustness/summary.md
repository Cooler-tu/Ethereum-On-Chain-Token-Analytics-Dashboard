# Correlation robustness audit

- Scope: `0x7baece5d47f1bc5e1953fbe0e9931d54dab6d810`
- Base bucket seconds: `86400`
- Bucket factors: `1, 2, 3`
- Features: `price_return, tvl_change, volume_turnover, net_lp_flow_ratio, withdrawal_ratio`
- Valid lag tests: `260`
- Global BH-FDR threshold: `0.05`
- Tests surviving global BH-FDR: `0`
- Zero-lag family BH-FDR: `2/60`
- Exploratory lead-lag family BH-FDR: `0/200`
- Null test: two-sided block permutation; CI: paired moving-block bootstrap.

## Best lag per bucket / feature pair

| Bucket | X | Y | Method | Lag | Correlation | 95% CI | Block p | Family q | Global q | Verdict | N |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 86400s | tvl_change | net_lp_flow_ratio | spearman | 0 | 0.9658 | [0.8582, 0.9816] | 0.0010 | 0.0300 | 0.0520 | CI excludes 0, family FDR pass | 30 |
| 86400s | tvl_change | net_lp_flow_ratio | pearson | 0 | 0.9653 | [0.9334, 0.9939] | 0.0010 | 0.0300 | 0.0520 | CI excludes 0, family FDR pass | 30 |
| 172800s | volume_turnover | net_lp_flow_ratio | pearson | -1 | -0.7403 | [-0.9544, -0.2883] | 0.0020 | 0.0800 | 0.0743 | CI excludes 0, low power | 13 |
| 86400s | volume_turnover | withdrawal_ratio | pearson | 3 | 0.4094 | [0.0732, 0.6812] | 0.0040 | 0.1333 | 0.1300 | CI excludes 0 | 27 |
| 172800s | volume_turnover | net_lp_flow_ratio | spearman | -1 | -0.7127 | [-0.9678, -0.2328] | 0.0060 | 0.1714 | 0.1733 | CI excludes 0, low power | 13 |
| 259200s | tvl_change | net_lp_flow_ratio | pearson | 0 | 0.9310 | [0.7731, 0.9967] | 0.0090 | 0.1800 | 0.2340 | CI excludes 0, low power | 9 |
| 259200s | tvl_change | net_lp_flow_ratio | spearman | 0 | 0.8954 | [0.6121, 1.0000] | 0.0150 | 0.1800 | 0.2786 | CI excludes 0, low power | 9 |
| 172800s | tvl_change | net_lp_flow_ratio | pearson | 0 | 0.8114 | [-0.2936, 0.9806] | 0.0140 | 0.1800 | 0.2786 | low power | 14 |
| 86400s | price_return | volume_turnover | spearman | -2 | 0.4702 | [0.0985, 0.7147] | 0.0120 | 0.3000 | 0.2786 | CI excludes 0 | 28 |
| 86400s | price_return | withdrawal_ratio | spearman | 2 | 0.4286 | [0.0557, 0.6944] | 0.0150 | 0.3333 | 0.2786 | CI excludes 0 | 28 |
| 259200s | volume_turnover | net_lp_flow_ratio | pearson | 1 | 0.7362 | [0.1981, 0.9599] | 0.0290 | 0.4000 | 0.3968 | CI excludes 0, low power | 8 |
| 172800s | tvl_change | volume_turnover | pearson | 1 | -0.6560 | [-0.9033, 0.1682] | 0.0250 | 0.4000 | 0.3968 | low power | 13 |
| 259200s | price_return | net_lp_flow_ratio | pearson | 1 | -0.8585 | [-0.9939, -0.5965] | 0.0360 | 0.4000 | 0.4070 | CI excludes 0, low power | 8 |
| 86400s | price_return | withdrawal_ratio | pearson | 1 | 0.4169 | [-0.0224, 0.7284] | 0.0360 | 0.4000 | 0.4070 | exploratory | 29 |
| 86400s | price_return | volume_turnover | pearson | -2 | 0.4127 | [0.1718, 0.6389] | 0.0320 | 0.4000 | 0.4070 | CI excludes 0 | 28 |
| 86400s | volume_turnover | withdrawal_ratio | spearman | 3 | 0.3471 | [-0.0076, 0.6280] | 0.0340 | 0.4000 | 0.4070 | exploratory | 27 |
| 259200s | price_return | net_lp_flow_ratio | spearman | 1 | -0.7904 | [-1.0000, -0.2531] | 0.0420 | 0.4273 | 0.4073 | CI excludes 0, low power | 8 |
| 259200s | tvl_change | volume_turnover | pearson | -1 | 0.6961 | [0.1574, 0.9418] | 0.0440 | 0.4273 | 0.4073 | CI excludes 0, low power | 8 |
| 172800s | price_return | tvl_change | spearman | 0 | -0.5165 | [-0.8779, 0.0000] | 0.0470 | 0.3525 | 0.4073 | low power | 14 |
| 172800s | price_return | withdrawal_ratio | pearson | 0 | 0.5031 | [0.0991, 0.8732] | 0.0380 | 0.3429 | 0.4073 | CI excludes 0, low power | 14 |
| 259200s | price_return | withdrawal_ratio | pearson | 0 | 0.5819 | [0.1371, 0.8834] | 0.0630 | 0.3780 | 0.5119 | CI excludes 0, low power | 9 |
| 172800s | net_lp_flow_ratio | withdrawal_ratio | spearman | 0 | 0.5146 | [-0.5027, 0.8976] | 0.0620 | 0.3780 | 0.5119 | low power | 14 |
| 259200s | tvl_change | volume_turnover | spearman | -1 | 0.6667 | [0.0732, 0.9747] | 0.0730 | 0.6083 | 0.5582 | CI excludes 0, low power | 8 |
| 172800s | price_return | volume_turnover | pearson | -1 | 0.4887 | [-0.1003, 0.7995] | 0.0710 | 0.6083 | 0.5582 | low power | 13 |
| 259200s | volume_turnover | net_lp_flow_ratio | spearman | 1 | 0.7186 | [0.3094, 0.9747] | 0.0840 | 0.6720 | 0.6240 | CI excludes 0, low power | 8 |
| 259200s | price_return | tvl_change | pearson | 1 | -0.7925 | [-0.9693, -0.4169] | 0.0950 | 0.7185 | 0.6816 | CI excludes 0, low power | 8 |
| 172800s | price_return | net_lp_flow_ratio | spearman | 1 | -0.4931 | [-0.8776, 0.1193] | 0.0970 | 0.7185 | 0.6816 | low power | 13 |
| 172800s | tvl_change | net_lp_flow_ratio | spearman | 0 | 0.4689 | [-0.3146, 0.9552] | 0.1090 | 0.5500 | 0.7333 | low power | 14 |
| 172800s | net_lp_flow_ratio | withdrawal_ratio | pearson | 0 | 0.4633 | [-0.3433, 0.9070] | 0.1100 | 0.5500 | 0.7333 | low power | 14 |
| 259200s | price_return | tvl_change | spearman | 1 | -0.7619 | [-1.0000, 0.0380] | 0.1160 | 0.8286 | 0.7540 | low power | 8 |
| 259200s | volume_turnover | withdrawal_ratio | spearman | 1 | 0.6228 | [-0.2722, 0.8228] | 0.1310 | 0.8645 | 0.7916 | low power | 8 |
| 259200s | price_return | withdrawal_ratio | spearman | 0 | 0.5188 | [-0.1357, 1.0000] | 0.1250 | 0.5769 | 0.7916 | low power | 9 |
| 172800s | tvl_change | volume_turnover | spearman | 0 | -0.4110 | [-0.7047, 0.1179] | 0.1370 | 0.5871 | 0.7916 | low power | 14 |
| 86400s | tvl_change | withdrawal_ratio | pearson | 3 | 0.2445 | [-0.1234, 0.4735] | 0.1410 | 0.8718 | 0.7970 | exploratory | 27 |
| 172800s | price_return | volume_turnover | spearman | -1 | 0.3791 | [-0.2204, 0.7994] | 0.1700 | 0.8718 | 0.8340 | low power | 13 |
| 172800s | price_return | net_lp_flow_ratio | pearson | 1 | -0.3766 | [-0.7625, 0.1183] | 0.1690 | 0.8718 | 0.8340 | low power | 13 |
| 86400s | volume_turnover | net_lp_flow_ratio | pearson | 2 | 0.2906 | [-0.2733, 0.6462] | 0.1650 | 0.8718 | 0.8340 | exploratory | 28 |
| 259200s | price_return | volume_turnover | pearson | 1 | 0.5581 | [0.3037, 0.9036] | 0.1830 | 0.8927 | 0.8651 | CI excludes 0, low power | 8 |
| 259200s | price_return | volume_turnover | spearman | 1 | 0.6190 | [-0.0380, 0.9737] | 0.1970 | 0.8980 | 0.8656 | low power | 8 |
| 259200s | net_lp_flow_ratio | withdrawal_ratio | spearman | 0 | 0.4454 | [-0.3520, 0.9450] | 0.2230 | 0.7260 | 0.8656 | low power | 9 |
| 259200s | net_lp_flow_ratio | withdrawal_ratio | pearson | 0 | 0.4394 | [-0.3323, 0.8435] | 0.2320 | 0.7260 | 0.8656 | low power | 9 |
| 172800s | volume_turnover | withdrawal_ratio | spearman | 1 | 0.4179 | [-0.1254, 0.7773] | 0.2570 | 0.9018 | 0.8656 | low power | 13 |
| 172800s | price_return | tvl_change | pearson | 1 | -0.3530 | [-0.7384, 0.1128] | 0.1950 | 0.8980 | 0.8656 | low power | 13 |
| 172800s | price_return | withdrawal_ratio | spearman | 0 | 0.3178 | [-0.1296, 0.7729] | 0.2380 | 0.7260 | 0.8656 | low power | 14 |
| 86400s | price_return | tvl_change | pearson | 0 | -0.2422 | [-0.4785, 0.0361] | 0.1980 | 0.7260 | 0.8656 | exploratory | 30 |
| 86400s | price_return | tvl_change | spearman | 0 | -0.2320 | [-0.5320, 0.0733] | 0.2050 | 0.7260 | 0.8656 | exploratory | 30 |
| 86400s | price_return | net_lp_flow_ratio | pearson | 1 | 0.2185 | [-0.2626, 0.5237] | 0.2630 | 0.9069 | 0.8656 | exploratory | 29 |
| 86400s | price_return | net_lp_flow_ratio | spearman | 3 | -0.2171 | [-0.4413, 0.0355] | 0.2510 | 0.9018 | 0.8656 | exploratory | 27 |
| 86400s | tvl_change | withdrawal_ratio | spearman | 3 | 0.1543 | [-0.1477, 0.3977] | 0.2440 | 0.9018 | 0.8656 | exploratory | 27 |
| 172800s | tvl_change | withdrawal_ratio | pearson | 1 | 0.3562 | [-0.0847, 0.6475] | 0.2860 | 0.9079 | 0.8748 | low power | 13 |
| 259200s | tvl_change | withdrawal_ratio | pearson | 0 | 0.3335 | [-0.4806, 0.8207] | 0.2860 | 0.7716 | 0.8748 | low power | 9 |
| 172800s | volume_turnover | withdrawal_ratio | pearson | 1 | 0.3693 | [-0.0921, 0.7255] | 0.2970 | 0.9121 | 0.8893 | low power | 13 |
| 86400s | net_lp_flow_ratio | withdrawal_ratio | pearson | 3 | 0.1599 | [-0.1754, 0.4038] | 0.3010 | 0.9121 | 0.8893 | exploratory | 27 |
| 259200s | volume_turnover | withdrawal_ratio | pearson | 1 | 0.4429 | [-0.1566, 0.8929] | 0.3560 | 0.9547 | 0.9131 | low power | 8 |
| 259200s | tvl_change | withdrawal_ratio | spearman | 0 | 0.2929 | [-0.6136, 0.8589] | 0.3770 | 0.7716 | 0.9131 | low power | 9 |
| 86400s | tvl_change | volume_turnover | pearson | -2 | 0.1914 | [-0.3344, 0.5463] | 0.3900 | 0.9593 | 0.9131 | exploratory | 28 |
| 172800s | tvl_change | withdrawal_ratio | spearman | 1 | 0.1866 | [-0.3873, 0.7977] | 0.5660 | 0.9593 | 0.9131 | low power | 13 |
| 86400s | volume_turnover | net_lp_flow_ratio | spearman | -2 | -0.1677 | [-0.6074, 0.3227] | 0.4580 | 0.9593 | 0.9131 | exploratory | 28 |
| 86400s | tvl_change | volume_turnover | spearman | 3 | 0.1618 | [-0.2580, 0.5244] | 0.3940 | 0.9593 | 0.9131 | exploratory | 27 |
| 86400s | net_lp_flow_ratio | withdrawal_ratio | spearman | -3 | -0.1338 | [-0.5104, 0.2763] | 0.4040 | 0.9593 | 0.9131 | exploratory | 27 |

## Interpretation guardrails

- Selecting the largest absolute lag is exploratory; the global BH correction covers all tested feature pairs, lags, methods, and bucket variants in this run.
- Block permutation and moving-block bootstrap retain short-range dependence better than iid resampling. Neither corrects unmeasured confounding.
- Coarse variants with fewer than 20 aligned observations are labelled low power even if their point estimate is large.
- Stability requires direction and plausible horizon to persist across bucket sizes, not merely one significant cell.
