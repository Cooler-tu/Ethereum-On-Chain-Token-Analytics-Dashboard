# Correlation robustness audit / 相关性稳健性审计

Date / 日期: 2026-08-24

Cases / 案例:

- uPEG matched V3 pool: 169 hourly buckets
- TURBO main V3 pool: 31 daily buckets

Local outputs / 本地结果:

- `output-upeg-v3-7d/research-correlation-robustness/`
- `output-turbo-30d-25580851/research-correlation-robustness/`

## Method / 方法

The audit adds three defenses that were absent from the exploratory pilot:

1. Paired moving-block bootstrap confidence intervals, preserving short-range
   time dependence better than iid resampling.
2. Two-sided block-permutation null tests followed by Benjamini-Hochberg false
   discovery rate control.
3. Multi-bucket sensitivity: uPEG at 1/2/4/6/12/24 hours; TURBO at 1/2/3 days.

Multiple testing is reported in three ways:

- a pre-specified zero-lag family;
- an exploratory non-zero lead-lag family;
- the most conservative global family across every feature, method, lag, and
  bucket variant.

本次审计增加三层防护：移动区块 bootstrap 置信区间、区块置换零假设检验加
Benjamini-Hochberg 假发现率控制，以及不同时间桶敏感性。同期关系、探索性
lead-lag 和全部检验分别报告，避免用数百个 lag 搜索稀释预先定义的同期问题，
同时仍保留最保守的全局校正结果。

## Results / 结果

| Case | Test family | Valid tests | BH-FDR passes | Interpretation |
|---|---|---:|---:|---|
| uPEG | Pre-specified zero lag | 36 | 9 | Price return vs reserve change survives at useful intraday buckets |
| uPEG | Exploratory lead-lag | 576 | 0 | No predictive lag survives correction |
| uPEG | Global | 612 | 0 | Strongest global q = 0.0765; no universal claim |
| TURBO | Pre-specified zero lag | 60 | 2 | Only the mechanical reserve-change vs net-LP-flow check survives |
| TURBO | Exploratory lead-lag | 200 | 0 | No predictive lag survives correction |
| TURBO | Global | 260 | 0 | No global pass |

### uPEG: robust contemporaneous inventory relationship

At one hour, price return versus target-token reserve change is:

| Method | Correlation | Moving-block 95% CI | Block p | Zero-lag family q |
|---|---:|---:|---:|---:|
| Pearson | -0.6791 | [-0.8207, -0.5553] | 0.001 | 0.0045 |
| Spearman | -0.7757 | [-0.8625, -0.6693] | 0.001 | 0.0045 |

The sign remains negative for both methods at every 1/2/4/6/12/24-hour
variant. Both methods pass the zero-lag family at 1/2/4/6 hours; 12 hours is
already low power and only Pearson passes, while 24 hours has only six aligned
changes and cannot support inference. No non-zero lag candidate passes the
exploratory lead-lag correction.

This supports a within-case AMM inventory relationship: when WETH-per-uPEG
price rises, the pool tends to hold fewer target tokens, and vice versa. It is
not evidence that reserve change predicts price, nor an externally validated
market law. The global q of 0.0765 also prevents a claim that survives the most
conservative all-tests family.

uPEG 的“价格收益与目标代币储备变化同期反向”在 1/2/4/6 小时桶中同时通过
Pearson、Spearman 的同期家族校正，在所有时间桶中方向均为负。12 小时开始
样本不足，24 小时只有 6 个变化样本。所有非零 lag 均未通过校正。因此它支持
单个 AMM 池内的库存机制，但不能解释为储备变化能够预测价格，也尚未通过独立
案例验证。

### TURBO: exploratory lead-lag candidates do not survive

The one-day mechanical check remains strong:

| Relationship | Method | Correlation | 95% CI | Family q |
|---|---|---:|---:|---:|
| Reserve change vs net LP-flow ratio | Pearson | 0.9653 | [0.9334, 0.9939] | 0.0300 |
| Reserve change vs net LP-flow ratio | Spearman | 0.9658 | [0.8582, 0.9816] | 0.0300 |

This is a pipeline consistency result because both variables share pool-flow
mechanics and a prior-reserve denominator. It is not a predictive law.

The prior lead-lag candidates weaken under correction and bucket changes:

| Candidate | One-day estimate | 95% CI | Lead-lag family q | Multi-bucket result |
|---|---:|---:|---:|---|
| Turnover leads price by 2d, Pearson | 0.4127 | [0.1718, 0.6389] | 0.4000 | Direction of the selected lag flips at the 3-day bucket |
| Turnover leads price by 2d, Spearman | 0.4702 | [0.0985, 0.7147] | 0.3000 | Coarse buckets are low power; no FDR pass |
| Turnover leads gross withdrawal by 3d, Pearson | 0.4094 | [0.0732, 0.6812] | 0.1333 | Horizon stays around 2–3d, but coarse CIs are unstable |
| Turnover leads gross withdrawal by 3d, Spearman | 0.3471 | [-0.0076, 0.6280] | 0.4000 | CI already includes zero at one day |
| Price leads gross withdrawal by 1–2d | 0.4169–0.4286 | mixed | 0.3333–0.4000 | Becomes contemporaneous at coarser buckets |

No TURBO non-zero lag survives the 200-test lead-lag family. This agrees with
the transaction audit: gross withdrawal is heavily contaminated by rapid
remove→mint cycling and should not be treated as permanent exit.

TURBO 唯一通过同期校正的是“储备变化 vs 净 LP 流”，但这是机械性的自洽
检查。此前三个 lead-lag 候选都没有通过 200 次非零 lag 的 FDR 校正；有些单格
置信区间不跨零，但换成 2/3 日桶后 lag 方向改变、退化为同期关系或因样本过少而
不稳定。结合交易证据，当前不能声称成交量能够预测未来价格或 LP 永久退出。

## Research decision / 研究决策

1. Retain uPEG price/reserve inverse movement as a **within-pool structural
   finding**, not a predictive signal.
2. Downgrade every TURBO predictive lead-lag candidate to **unconfirmed**.
3. Treat gross withdrawal as an activity/cycling feature; use net LP flow and
   actual pool Transfer net for exit hypotheses.
4. Do not search more lags on the same 31-day TURBO sample. The next valid test
   is a pre-registered independent crash/control case with fixed metrics and
   horizons.

1. 保留 uPEG 价格与储备反向变化作为“池内结构关系”，不称为预测信号。
2. TURBO 所有预测性 lead-lag 候选降级为“尚未确认”。
3. 累计撤资只作为活动/循环指标；资金退出假设使用净 LP 流和池地址真实 Transfer。
4. 不再对同一组 31 日 TURBO 数据继续搜索更多 lag；下一步应预先固定指标和时间
   范围，在独立崩盘案例与正常对照窗口上验证。

## Reproduction / 复现

```bash
python3 scripts/correlation_robustness.py \
  --output-dir output-upeg-v3-7d --scope pool \
  --pool 0xdc893995d488e5be8ec8ca1db92cbec2a1ab0775 \
  --features price_return,tvl_change,volume_turnover \
  --bucket-factors 1,2,4,6,12,24 --max-horizon-base-buckets 24 \
  --min-pairs 6 --bootstrap-repetitions 1000 --permutation-repetitions 999 \
  --out-dir output-upeg-v3-7d/research-correlation-robustness

python3 scripts/correlation_robustness.py \
  --output-dir output-turbo-30d-25580851 --scope pool \
  --pool 0x7baecE5d47f1BC5E1953FBE0E9931D54DAB6D810 \
  --features price_return,tvl_change,volume_turnover,net_lp_flow_ratio,withdrawal_ratio \
  --bucket-factors 1,2,3 --max-horizon-base-buckets 3 \
  --min-pairs 8 --bootstrap-repetitions 1000 --permutation-repetitions 999 \
  --out-dir output-turbo-30d-25580851/research-correlation-robustness
```
