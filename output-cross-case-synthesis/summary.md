# FTT / CEL / GALA cross-case evidence ledger

This exploratory ledger applies the same one-hour predictor and future 24-hour outcome to all existing windows. It uses 24-observation moving-block bootstrap intervals, 4,999 two-sided block permutations, and one BH correction across all 18 rows. It is a synthesis, not a new pre-registered confirmation.

## Incident-preceding comparison

| Predictor | FTT ρ | CEL ρ | GALA ρ | Same sign in all three? | Globally significant cases |
|---|---:|---:|---:|---|---|
| pool_transfer_net | -0.1279 | -0.0048 | 0.0495 | no | none |
| net_lp_flow | -0.2979 | -0.0856 | 0.0527 | no | FTT |
| gross_lp_activity | 0.1564 | 0.0191 | 0.0386 | yes | none |

## Full 18-row ledger

| Case | Phase | Predictor | N | ρ | 95% block CI | p | global BH q |
|---|---|---|---:|---:|---:|---:|---:|
| FTT | baseline | pool_transfer_net | 142 | -0.0085 | [-0.1859, 0.2487] | 0.9336 | 0.9336 |
| FTT | baseline | net_lp_flow | 142 | -0.0280 | [-0.2124, 0.1117] | 0.7078 | 0.8494 |
| FTT | baseline | gross_lp_activity | 142 | 0.0996 | [-0.0036, 0.1837] | 0.2950 | 0.5425 |
| FTT | incident_preceding | pool_transfer_net | 171 | -0.1279 | [-0.2283, 0.0512] | 0.1202 | 0.4284 |
| FTT | incident_preceding | net_lp_flow | 171 | -0.2979 | [-0.4802, -0.0109] | 0.0012 | 0.0216 |
| FTT | incident_preceding | gross_lp_activity | 171 | 0.1564 | [-0.1924, 0.3985] | 0.1764 | 0.4284 |
| CEL | baseline | pool_transfer_net | 522 | 0.0915 | [0.0344, 0.1725] | 0.0256 | 0.1152 |
| CEL | baseline | net_lp_flow | 522 | 0.1107 | [0.0292, 0.1799] | 0.0042 | 0.0378 |
| CEL | baseline | gross_lp_activity | 522 | -0.0317 | [-0.1376, 0.0617] | 0.3918 | 0.5425 |
| CEL | incident_preceding | pool_transfer_net | 504 | -0.0048 | [-0.0764, 0.0836] | 0.9040 | 0.9336 |
| CEL | incident_preceding | net_lp_flow | 504 | -0.0856 | [-0.1496, 0.0016] | 0.0176 | 0.1056 |
| CEL | incident_preceding | gross_lp_activity | 504 | 0.0191 | [-0.0491, 0.0797] | 0.7014 | 0.8494 |
| GALA | incident_preceding | pool_transfer_net | 693 | 0.0495 | [-0.0147, 0.1240] | 0.1904 | 0.4284 |
| GALA | incident_preceding | net_lp_flow | 693 | 0.0527 | [-0.0340, 0.1367] | 0.1814 | 0.4284 |
| GALA | incident_preceding | gross_lp_activity | 693 | 0.0386 | [-0.0470, 0.1194] | 0.3378 | 0.5425 |
| GALA | incident_following | pool_transfer_net | 690 | -0.0048 | [-0.0883, 0.0861] | 0.9080 | 0.9336 |
| GALA | incident_following | net_lp_flow | 690 | -0.0281 | [-0.0921, 0.0329] | 0.3784 | 0.5425 |
| GALA | incident_following | gross_lp_activity | 690 | 0.0511 | [-0.0702, 0.1536] | 0.3784 | 0.5425 |

## Decision

`retire_liquidity_single_variables_as_standalone_predictors`

A feature is not retained merely because one selected case is significant. For incident-preceding transport, it must keep the same sign in FTT, CEL, and GALA and survive the global family in at least two cases. None meets that bar. The project should stop treating pool Transfer net flow, net LP flow, or gross LP activity as standalone 24-hour price predictors.

The remaining high-value direction is an incident-centered market-response study with identical pre/post geometry and objective case inclusion. That study should ask how price, turnover, and pool inventory jointly respond after an external incident—not search for another single LP variable or another favorable token.

## 中文结论

统一 18 项检验后，没有一个单变量在 FTT、CEL、GALA 三个事前窗口中保持同一方向并在至少两个案例通过全局校正。FTT/CEL 的净 LP 流负相关在 GALA 事前窗口变为正值，因此不具备跨案例可迁移性。项目应正式停止把池 Transfer 净流、净 LP 流或累计 LP 活动当作独立的 24 小时价格预测器。下一条值得研究的路线，是使用完全一致的事件前后窗口和客观入样规则，研究价格、成交周转与池库存的联合事件响应，而不是继续寻找另一个“显著”的 LP 指标或代币。
