# TURBO anomaly evidence bundle / TURBO 异常窗口证据包

Date / 日期: 2026-08-22

Pool / 主池: `0x7baecE5d47f1BC5E1953FBE0E9931D54DAB6D810`

UTC window / 时间窗口: `2026-08-05` through `2026-08-09`

Blocks / 区块: `25684865–25720864`

Local evidence / 本地证据: `output-turbo-30d-25580851/research-anomaly-evidence/`

## Question / 研究问题

The 31-day pilot found a moderate candidate in which high turnover preceded
later price returns and gross withdrawal activity by two to three days. This
bundle tests whether that pattern represents permanent liquidity exit, routine
V3 position recreation, or trading-driven pool inventory movement.

31 日试验发现了一个中等强度的候选关系：高周转率可能领先 2–3 天的价格收益和
累计撤资活动。本证据包进一步判断它是真实流动性退出、常规 V3 头寸重建，还是
交易造成的池库存变化。

## Four-ledger result / 四本账结果

| UTC date | Swap sell / buy | Actual Transfer net to pool | LP add / remove | Matched remove→mint | +1d | +2d | +3d |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-08-05 | 5.825M / 4.487M | -4.261M | 96.225M / 101.815M | 10 / 89.4% | -1.85% | -2.43% | +2.59% |
| 2026-08-06 | 6.698M / 4.689M | +5.145M | 52.339M / 49.186M | 2 / 43.4% | -0.59% | +4.53% | +10.13% |
| 2026-08-07 | 1.039M / 2.166M | -4.845M | 0 / 3.719M | 0 / 0% | +5.15% | +10.78% | +6.93% |
| 2026-08-08 | 0.079M / 0.669M | +9.902M | 152.113M / 141.621M | 11 / 81.9% | +5.36% | +1.70% | -2.25% |
| 2026-08-09 | 2.494M / 3.374M | -10.456M | 98.437M / 108.013M | 6 / 55.8% | -3.47% | -7.23% | -8.02% |

Positive Transfer net means TURBO entered the pool; negative means it left.
Forward returns use the daily WETH-per-TURBO close and are not USD returns.

Transfer 净流为正表示 TURBO 进入池，负值表示离开池。未来收益按每日
WETH/TURBO 收盘价计算，不是美元收益。

## Findings / 结论

1. **The cash-flow ledger reconciles exactly.** Across the five-day window,
   192 Swap events produced `+0.750167M TURBO` signed net flow into the pool,
   while actual ERC-20 Transfers and historical `balanceOf` both show
   `-4.515015M TURBO`. The `-5.265183M` difference is non-Swap movement. At the
   daily level, signed Swap net plus raw Mint/Burn principal net explains the
   actual Transfer net with only about `-0.025764M TURBO` residual, consistent
   with fees/other pool movements.

2. **Gross removal is dominated by rapid cycling candidates.** The window has
   `404.354M TURBO` gross removals. A strict one-to-one rule—same raw V3 pool
   owner and tick range, later Mint within 300 blocks, and liquidity within
   15%—matches 29 cycles covering `288.656M TURBO`, or **71.4%** of gross
   removal.

3. **The clearest counterexample is 2026-08-08.** Although gross removal was
   `141.621M TURBO` and the withdrawal ratio exceeded 2, LP net flow was
   **+10.492M TURBO** and actual Transfer net was **+9.902M TURBO** into the
   pool. Calling that day a permanent exit would reverse the actual direction.

4. **Some genuine net exit remains.** August 5 and August 9 show LP net outflow
   of about `-5.590M` and `-9.576M TURBO`; actual pool Transfer net was
   `-4.261M` and `-10.456M`. The result is therefore not “all withdrawals are
   harmless,” but “gross withdrawal must be decomposed before interpretation.”

5. **The lead-lag story is not uniform.** August 6 is followed by positive
   +2/+3-day WETH-relative returns, but August 5 is negative at +1/+2 days and
   only positive at +3 days. The transaction evidence weakens a simple
   “turnover predicts exit” narrative and instead points to a mixture of
   position cycling, trading flow, and smaller net inventory changes.

1. **资金流账本精确闭合。** 五天内 192 个 Swap 的带符号净流量为
   `+0.750167M TURBO` 进入池，但 ERC-20 Transfer 与历史 `balanceOf` 都显示
   池余额净减少 `4.515015M TURBO`，两者相差的 `-5.265183M` 来自非 Swap
   资金移动。逐日看，“Swap 净流 + Mint/Burn 本金净流”与真实 Transfer 净流
   只剩约 `-0.025764M TURBO` 残差，符合手续费或其他池内移动的量级。

2. **累计撤资主要受短时循环候选支配。** 窗口累计撤出 `404.354M TURBO`；
   在“同一池 owner + 相同 tick、300 区块内重新 Mint、liquidity 差异不超过
   15%”的严格一对一规则下，共匹配 29 组，覆盖 `288.656M TURBO`，即
   **71.4%** 的累计撤资。

3. **2026-08-08 是最清楚的反例。** 当天累计撤出 `141.621M TURBO`，撤资比
   超过 2，但 LP 净流量反而为 **+10.492M TURBO**，真实 Transfer 净流也为
   **+9.902M TURBO** 进入池。把这一天解释成“永久退出”会直接看反方向。

4. **仍然存在较小但真实的净流出。** 8 月 5 日、9 日 LP 净流分别约为
   `-5.590M`、`-9.576M TURBO`，真实池 Transfer 净流为 `-4.261M`、
   `-10.456M`。结论不是“所有撤资都无害”，而是“必须拆解累计撤资后才能解释”。

5. **领先关系并不一致。** 8 月 6 日之后 +2/+3 天收益为正，但 8 月 5 日之后
   +1/+2 天仍为负，直到 +3 天才转正。交易证据削弱了“高周转预测退出”的简单
   叙事，更符合头寸循环、交易流和较小净库存变化共同作用。

## Identity guardrail / 身份边界

All 29 matched cycles use pool owner
`0xC36442b4a4522E871399CD717aBDD847Ab11FE88`, the shared Uniswap V3
NonfungiblePositionManager. Matching `owner + tickLower + tickUpper` proves
reuse of a pool-level position key, not that the same wallet or NFT performed
both transactions. Beneficial-owner attribution still requires a targeted
Position Manager/NFT trace.

29 组匹配的池 owner 都是共享的 Uniswap V3 NonfungiblePositionManager
`0xC364...FE88`。因此，相同 `owner + tickLower + tickUpper` 只能证明池级
position key 被再次使用，不能证明前后交易属于同一钱包或同一个 NFT。若要确认
受益所有人，仍需定向追踪 Position Manager/NFT。

## Reproduction / 复现

```bash
python3 scripts/directional_swap_flow.py \
  --output-dir output-turbo-30d-25580851 \
  --pool 0x7baecE5d47f1BC5E1953FBE0E9931D54DAB6D810 \
  --from-block 25684865 --to-block 25720864 \
  --start-balance-block 25684864 \
  --skip-tx-from \
  --out-dir output-turbo-30d-25580851/research-anomaly-evidence/directional

python3 scripts/anomaly_evidence.py \
  --output-dir output-turbo-30d-25580851 \
  --directional-dir output-turbo-30d-25580851/research-anomaly-evidence/directional \
  --pool 0x7baecE5d47f1BC5E1953FBE0E9931D54DAB6D810 \
  --from-block 25684865 --to-block 25720864 \
  --start-date 2026-08-05 --end-date 2026-08-09 \
  --out-dir output-turbo-30d-25580851/research-anomaly-evidence
```
