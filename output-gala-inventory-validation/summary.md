# GALA inventory mechanism validation

This is the frozen third and final hand-selected case. Two-sided 24-hour block-permutation p-values are BH-adjusted across H1–H3; confidence intervals use 24-hour calendar moving blocks.

| Test | Control n | Event n | Control | Event | Effect | 95% block CI | p | BH q | Confirmed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| H1 | — | 78 | — | -0.0915 | -0.0915 | [-0.2725, 0.0880] | 0.4646 | 0.6969 | no |
| H2 | 65 | 79 | 0.4700 | 0.5120 | 0.0420 | [-0.0401, 0.2382] | 0.1938 | 0.5814 | no |
| H3 | 65 | 79 | 1.0000 | 1.0000 | 0.0000 | [0.0000, 0.0000] | 1.0000 | 1.0000 | no |

## Coverage

- Control: 72 Mint rows, 65 eligible add hours, 100.0% quantified, 100.0% priced.
- Event: 128 Mint rows, 79 eligible add hours, 100.0% quantified, 100.0% priced.
- Frozen coverage gate: PASS.

## Decision

`close_hand_selected_mechanism_line_as_unconfirmed`

A non-confirmation means this hand-selected mechanism line stops; it does not prove LP inventory behavior never matters. Confirmation advances to a broad batch validation rather than a fourth selected case.

## 中文结论

这是第三个、也是最后一个人工挑选案例。H1–H3 使用 24 小时日历区块 bootstrap 与双侧区块置换检验，并对三个主检验做 BH 校正。若没有主假设同时满足预设方向、q < 0.05 且置信区间不跨 0，则按预注册规则停止继续挑案例；若有确认，则下一步转向批量样本验证。
