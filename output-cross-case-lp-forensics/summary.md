# FTT + CEL opposite-direction LP-flow forensics

The deterministic candidate rule is: positive hourly net LP flow, negative observed future 24-hour log return, ranked by net LP flow divided by prior target-token reserve. The first `5` hours per case receive transaction-level decomposition.

## Ranked hours

| Case | Rank | UTC hour | Net LP / prior reserve | Future 24h | LP add / remove | WETH add / remove | Target value share | Target-only add | Largest add tx | Pool version |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| FTT | 1 | 2022-11-06T02:00:00Z | +225.77% | -2.79% | 23.863K / 657.630 | 0.0000 / 0.0000 | +100.00% | +100.00% | +100.00% | v3 |
| FTT | 2 | 2022-11-07T05:00:00Z | +42.41% | -23.22% | 4.328K / 101.317 | 72.6013 / 1.2666 | +45.19% | +0.00% | +95.32% | v3 |
| FTT | 3 | 2022-10-31T13:00:00Z | +7.50% | -0.68% | 589.991 / 0.000 | 7.0939 / 0.0000 | +57.68% | +0.00% | +100.00% | v3 |
| FTT | 4 | 2022-11-07T06:00:00Z | +6.01% | -16.29% | 869.967 / 0.000 | 16.7615 / 0.0000 | +41.99% | +0.00% | +75.26% | v3 |
| FTT | 5 | 2022-10-26T08:00:00Z | +4.45% | -1.71% | 343.232 / 0.000 | 1.7427 / 0.0000 | +75.91% | +0.00% | +100.00% | v3 |
| CEL | 1 | 2022-05-14T13:00:00Z | +1.98% | -13.67% | 24.238K / 0.000 | 2.1281 / 0.0000 | +81.79% | +0.00% | +100.00% | v3 |
| CEL | 2 | 2022-05-19T03:00:00Z | +0.79% | -1.90% | 9.816K / 0.000 | 4.2939 / 0.0000 | +48.84% | +0.00% | +100.00% | v3 |
| CEL | 3 | 2022-05-27T23:00:00Z | +0.21% | -6.12% | 2.687K / 0.000 | 0.2548 / 0.0000 | +77.37% | +0.00% | +100.00% | v3 |
| CEL | 4 | 2022-05-29T20:00:00Z | +0.18% | -4.31% | 2.330K / 0.000 | 0.9997 / 0.0000 | +44.91% | +0.00% | +100.00% | v3 |
| CEL | 5 | 2022-05-21T08:00:00Z | +0.11% | -6.73% | 1.436K / 0.000 | 0.0509 / 0.0000 | +91.81% | +0.00% | +100.00% | v3 |

## What the decomposition establishes

- **CEL:** 10 candidate hours; top 5 are all V3. Target inventory represents +67.32% of added WETH-equivalent value at each hour close; fully target-only deposits are +0.00% of target tokens added.
- **FTT:** 11 candidate hours; top 5 are all V3. Target inventory represents +81.57% of added WETH-equivalent value at each hour close; fully target-only deposits are +79.56% of target tokens added.
- A positive target-token LP flow is not automatically equivalent to fresh quote capital or price support. A V3 Mint can be target-only, balanced, or quote-only depending on its range and the current price.
- `actual Transfer net − signed Swap net − Mint/Burn net` is a reconciliation diagnostic, not unexplained profit: V3 Burn and Collect can occur at different times, and fees or other pool movements can enter the residual.
- Same-transaction add/remove is measured directly. Cross-transaction range repositioning is deliberately not inferred from the shared NonfungiblePositionManager address.

## Current mechanism boundary

The repeated negative correlation is now better described as **target-token inventory provision during falling prices**, not generic capital inflow. FTT includes an extreme one-sided V3 inventory placement, while CEL's largest hour is a two-sided V3 Mint. This heterogeneity means the cross-case correlation does not yet identify one common wallet strategy. Targeted V3 owner/tick/NFT tracing is the next evidentiary step before pre-registering a third case.

## 中文结论

筛选规则固定为：小时净 LP 流为正、未来 24 小时价格为负，并按净 LP 流占前一小时目标代币储备的比例排序。FTT 与 CEL 的前五名异常小时都由 V3 事件主导，但两者机制并不完全相同。FTT 最大异常小时主要是单边加入 FTT、没有同步加入 WETH；CEL 最大异常小时则是双边加入。因此，原先的“净 LP 流入”更准确地说是下跌期间向池中配置目标代币库存，不能直接解释成外部资金托价。下一步需要针对这些交易追踪 V3 tick 区间、Position Manager NFT 和真实控制钱包，区分单边挂单、正常做市与撤出后重建。
