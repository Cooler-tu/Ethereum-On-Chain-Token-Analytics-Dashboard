# 项目工作交接（HandOver）

> 状态更新时间：2026-09-01
>
> 本轮文档修正前的主分支基线：`c4503ce`，当时 `main` 与 `origin/main` 同步
>
> 自动化测试基线：151 passed、1 skipped
>
> 本文后续保留 2026-08-14 Dashboard 口径修复的详细背景；研究阶段的最终状态和交付方向以本页“当前状态”及 `research-notes/cross-case-evidence-synthesis.md` 为准。

## 0. 当前状态（2026-08-30）

- 核心分析流水线、Uniswap V1–V4、Curve、Balancer V2、Dashboard、Parquet 分析表和本地 Studio 已可运行。
- TURBO 30 日案例完成了池级储备、成交量、价格、LP gross/net flow 和异常交易证据检查。
- FTT、CEL、GALA 已完成冻结窗口、稳健性检验和跨案例统一校正。
- 导师审阅用的 `notebooks/liquidity_analysis_visual_review.ipynb` 已执行并保存 5 张图表输出，同时提交了精简作图数据；它用于展示原始点、趋势和不确定性，补足只看相关性数字的不足。
- 公开币种首页现只保留 7 个有核心时间序列的案例。CRV 已用主导的 Uniswap V3 CRV/WETH 池补跑 5,000 区块并生成 17 个小时价格/成交量/储备桶；OM 已补跑事件前 10,000 区块并生成 35 个成交量桶。CREDI、NCR 和单区块 SPX 占位页暂不发布。
- 所有生成后的币种看板顶部现有 `Print / Save PDF`：使用浏览器原生打印/保存 PDF，打印版为 A4 白底、完整展开滚动表格，并在打印前后调整和恢复 Chart.js 图表尺寸。
- 跨案例结果没有发现可迁移的独立价格预测变量。Transfer 净流、净 LP 流、累计 LP 活动和目标库存集中度不再作为独立崩盘预测器。
- LOW / MEDIUM / HIGH Risk Index 仅用于启发式筛查，不是崩盘概率或经过大样本校准的预测模型。
- Dashboard 的高风险歧义文案已完成修正和人工验收；GitHub Actions 已配置为在 push / pull request 时运行回归测试，Pages 只在测试通过后构建和部署，首次远端测试、构建与部署已全部成功。当前工作方向是研究总结、输出存储策略和交付收口。八案例事件面板、Position Manager 全量追踪、深层钱包归属、多链和实时监控均暂缓。
- `python3 -m src.cli studio` 是本地自助入口；GitHub Pages 是预生成案例的静态展示站，不是公网动态分析后端。
- Dune 402/credits 错误现在会立即停止 Dune 查询并交给上层回退 RPC；只有明确的结果过大错误才拆分区块，429 限速仍按退避策略重试。

正式静态站点：<https://cooler-tu.github.io/On-Chain-Token-Crash-Liquidity-Analysis/>

最终跨案例证据：`research-notes/cross-case-evidence-synthesis.md` 和 `output-cross-case-synthesis/summary.md`。

完整中文白话研究过程：`research-notes/data-analysis-research-summary-zh.md`。

可直接查看的图表与保存结果：`notebooks/liquidity_analysis_visual_review.ipynb`。

## 1. 这段时间完成了什么

这轮工作的重点不是增加新的链上数据源，而是修正 Dashboard 中容易被误解的指标口径，让用户能够分清“真实数值”“部分覆盖”和“数据不可得”。

### 1.1 Notable Wallets 改为自适应筛选

原来的固定标准是 `$10,000`、`50 swaps`、`0.1% volume share`，对不同规模的 token 和不同长度的分析窗口不够稳健。

现在默认在当前分析窗口的钱包样本内部计算 P99，分别考察：

- 最大单笔成交额（Trade）；
- 买卖净流量绝对值（Mover）；
- 累计成交额（Volume）；
- swap 次数（Activity）。

任一指标进入窗口内 P99，即可成为 Notable Wallet。显式传入旧阈值时仍支持固定阈值模式。

当前 uPEG 输出中的实际结果：

| 项目 | 当前值 |
|---|---:|
| 参与比较的钱包 | 683 |
| Notable Wallets | 13 |
| Trade P99 | $5,670.04 |
| Mover P99 | $34,990.42 |
| Activity P99 | 61 swaps |
| Volume P99 | $47,464.40 |

主要实现：

- `src/analysis/metrics.py`：计算 P99、percentile rank、notability score 和自适应标签；
- `src/analysis/dashboard.py`：显示本次实际阈值、Volume Share 和入选原因；
- `src/cli.py`：支持从本地 swap artifacts 刷新钱包指标，不重新请求 Dune/RPC。

### 1.2 多池曲线增加视觉区分

TVL、Price 等多池曲线原来只有少量颜色，池数量增加后会出现重复。

现在采用更大的深色主题调色板，并叠加实线、长虚线、短虚线等线型。即使颜色接近，也能通过线型继续区分。

### 1.3 DEX custody reserve 改为饼图并增加限制说明

原来的 `DEX Pool Contracts` 表容易把 V2/V3 pool contract、V4 poolId 和 V4 共享 PoolManager 混为一谈。

现在该区域使用饼图展示“已识别 DEX 托管地址持有的目标 token 余额分布”，并明确：

- 它不是 LP 数量；
- 它不是完整的双边 USD TVL；
- V4 PoolManager 是共享托管，一个扇区可能对应多个 V4 poolId。

表格入口现已使用 `Pool Identifier`，避免把 V4 poolId 直接称作合约地址。进一步拆分 `Contract Address` 和 `V4 Pool ID` 属于延后设计项，只有在研究需要逐池 V4 归属时再做。

### 1.4 Pool TVL Share 改为“已测池范围内的份额”

Dashboard 不再把缺少 per-pool TVL 的池显示为 `0%`。

当前页面明确显示：

- 14 个 verified pools 中只有 3 个成功测量；
- 覆盖率为 21.4%；
- 份额分母只包含这 3 个 measured pools；
- 11 个未可靠拆分的 V4 pools 显示 `Not measured`；
- `99.41%` 只能解释为“占 3 个已测池总量的 99.41%”，不能解释为占全部 14 个池。

当前 TVL timeline 来源为 `event_accumulate_fallback`，因此图表会标注为 event-reconstructed proxy，而不是精确链上余额快照。

### 1.5 Non-Pool Holders 排名语义明确化

Dashboard 现在明确执行以下规则：

1. 排除 pool/custody 地址；
2. 排除 `zero_fill` 和非正期末余额；
3. 按 end balance 从高到低排序；
4. 图表最多显示 Top 10，表格最多显示 Top 20。

当前 uPEG 数据覆盖情况：

| 项目 | 当前值 |
|---|---:|
| Transfer 中出现的地址 | 1,134 |
| 成功取得余额的地址 | 80 |
| 未覆盖、以 zero-fill 占位的地址 | 1,054 |
| 正余额 Non-Pool Holders | 38 |
| 正余额 Pool/Custody 地址 | 4 |

因此 Top 20 只是“余额查询已覆盖地址中的 Top 20”，不是全量持有人排行榜。EOA 和普通合约都可能出现在 Non-Pool 列表中。

### 1.6 Liquidity Withdrawals 区分真实 0 与金额缺失

本轮最重要的语义修复之一，是不再把 V4 `ModifyLiquidity` 中 token0/token1 的零占位解释为真实撤出 0。

数据层现在使用三种状态：

- `quantified`：token amount 已知，可以计算 token、USD 和 TVL share；
- `liquidity_delta_only`：负 liquidity delta 已确认撤池动作，但没有 token amount；
- `unmapped`：事件无法可靠映射到目标 token 一侧。

当前 uPEG 看板显示：

| 项目 | 当前值 |
|---|---:|
| Removal actions detected | 114 |
| Amount known | 0 |
| Amount missing | 114 |
| Pool mapping failed | 0 |

页面中的表达已经改为：

- `Raw Liquidity Change`：保留原始负 liquidity delta；
- `Token amount not returned`：查询没有返回 token0/token1 amount；
- `Cannot calculate`：因此不能计算 USD 和 TVL share；
- 真正经过量化的 0 仍然显示为 0。

需要特别注意：这 114 次操作证明发生了 removal activity，但不能说明“撤出了 0 uPEG”，也不能仅凭 liquidity delta 换算出 token 或 USD 数量。

为了兼容旧分析目录，Dashboard 重建时会从 canonical `liquidity_events` 在内存中重新计算上述三态。当前旧 run 的 `output/metrics.json` 不一定包含新增的三态计数字段；直接研究该 JSON 时不要把缺失字段或零占位当结论。新跑的完整 pipeline 会写入新字段。

## 2. 关键文件及职责

| 文件 | 本轮相关职责 |
|---|---|
| `src/analysis/metrics.py` | 自适应钱包阈值；withdrawal 三态、金额归一和覆盖计数 |
| `src/analysis/dashboard.py` | 看板文案、表格、饼图、Holder 排名、曲线颜色/线型、本地兼容刷新 |
| `src/indexer/dune_index.py` | 标记 liquidity event 是否具备 token amounts |
| `src/data/artifacts.py` | Parquet liquidity schema 增加 `amounts_available` 和 `quantification_status` |
| `src/cli.py` | 本地刷新 adaptive wallet activity 的 CLI 参数 |
| `tests/test_metrics.py` | P99 钱包筛选和 withdrawal 真 0/未知值回归测试 |
| `tests/test_dashboard.py` | Holder、TVL coverage、withdrawal 文案与多池曲线测试 |
| `tests/test_artifacts.py` | liquidity Parquet 新字段与原始大整数保存测试 |
| `docs/DATA_FLOW.md` | 当前 pipeline 和 Dashboard 口径 |
| `docs/METHODOLOGY_DEFENSE.md` | 方法、公式、限制和答辩边界 |
| `plan.md` | 已完成事项与优先级 backlog |

## 3. 本地验收方式

进入项目：

```bash
cd /Users/jelly/Desktop/On-Chain-Token-Crash-Liquidity-Analysis-main
```

只使用已有数据重建 Dashboard，不会请求 Dune/RPC：

```bash
python3 -m src.cli dashboard --output-dir output
open output/dashboard.html
```

如果页面已经打开，重建后按 `⌘R` 刷新。

从本地 artifacts 重新计算 adaptive Notable Wallets：

```bash
python3 -m src.cli dashboard \
  --output-dir output \
  --refresh-wallet-activity
```

运行回归测试：

```bash
python3 -m unittest discover -s tests -q
```

当前测试结果（2026-08-30）：151 项通过，1 项因可选依赖条件按设计跳过。

如果需要把最新版同步到 public site：

```bash
python3 scripts/publish_site.py
```

该命令现在把历史 `output-*` 当作只读输入，只在 `site/` 中生成发布页面。

然后检查 `site/` 首页和 token 页面，再提交并推送。推送到 `main` 后，`.github/workflows/deploy-pages.yml` 会重新生成并部署静态站点；它不会在服务器上运行任意 token 分析。

## 4. API Key 与安全

Dune API Key 只应放在本地环境变量或 `.env` 中，不能提交到 GitHub。

```bash
export DUNE_API_KEY="YOUR_DUNE_API_KEY"
```

当前主提交已检查，没有上传真实 Key。完整分析前还要确认 `ETH_RPC_URL` 已配置。

## 5. 汇报时不要混淆的结论

| 不准确说法 | 应该怎么说 |
|---|---|
| “我们已经做了完整的钱包聚类” | 已有 `wallet_clustering.py` 原型，但尚未接入主 Dashboard；当前完成的是按钱包聚合 swap activity 与自适应筛选 |
| “Top 20 是全量 Holder 排名” | 是余额查询已覆盖地址中的正余额 Non-Pool Top 20；当前覆盖 80/1,134 |
| “99.41% 表示占全部池 TVL” | 只表示占 3 个 measured pools 总量的 99.41%；verified pools 共 14 个 |
| “114 次撤池金额都是 0” | 检测到 114 次动作，但 114 次都缺少 token amount，因此金额未知 |
| “Raw Liquidity Change 可以直接换算 uPEG” | 不可以；V4 liquidity delta 与 amount0/amount1 不是同一单位 |
| “DEX custody 饼图代表每个 V4 池 TVL” | 不代表；V4 PoolManager 是多个 poolId 的共享托管地址 |
| “TVL timeline 是精确余额快照” | 当前是 `event_accumulate_fallback`，应称为 activity-based reconstructed proxy |

## 6. 下一步建议（按优先级）

1. **导师人工审阅**：一起检查 `research-notes/data-analysis-research-summary-zh.md` 和 `notebooks/liquidity_analysis_visual_review.ipynb`，先根据反馈改展示，不急着增加案例。
2. **收口输出存储策略**：Git 保留摘要、报告、精简作图数据和展示文件，大型原始事件表继续留在本地或外部存储。
3. **暂缓低价值扩展**：不继续选择第四个手工相关性案例；八案例事件面板、Position Manager 全量追踪、beneficial owner、多链和实时告警只在出现新机制或明确外部需求时恢复。

## 7. Git 交接状态

- 分支：`main`
- 本轮 Markdown 修正前的基线提交：`c4503ce`
- 远程：`origin/main`
- 基线检查时本地与远端同步；本轮 Markdown 修正完成后仍需重新提交和推送。
- 当前仓库已包含 TURBO、FTT、CEL、GALA、稳健性检验、跨案例综合、Dashboard、测试和公开站点文件。
