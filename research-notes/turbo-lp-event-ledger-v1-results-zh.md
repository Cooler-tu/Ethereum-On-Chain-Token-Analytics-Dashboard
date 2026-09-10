# TURBO LP 事件账本 v1：事实层结果

## 这一步做了什么

把既有的 90 天 TURBO LP 候选 Burn 固定为研究样本，再追踪到区块 `25944714`（冻结时的 finalized 区块）。事实被严格拆成三层：原始 Mint/Burn、每条 Mint 只使用一次的 Burn→Mint 链接、以及不重复计算资金的连续 campaign。

## 冻结结果

- Factory 动态发现并核验 2 个 TURBO/WETH V3 池：1% 主池和 0.3% 池；
- 918 条原始 Mint/Burn，其中候选 Burn 仍为 447 条；
- 448 条 Burn→Mint 链接，涉及 446 个候选 Burn；Mint 重复使用数为 0；
- 连续净流归并后得到 159 个 campaign；
- 157 个 campaign 在30天内达到 90% 净恢复；
- 1 个 campaign 观察已满30天，但在已扫描 TURBO/WETH 池中没有 Mint；
- 1 个 campaign 只观察约8天，必须标记为截断，不能算30天未回归。

447 个 Burn 与 159 个 campaign 回答不同问题：前者保留每次链上动作，后者防止连续 Burn/Mint 反复搬动同一笔资金时被重复累计为多次独立撤离。

## 口径边界

- 钱包按同一地址追踪，只是控制主体的下限；
- 同钱包后续 Mint 不等于已经证明使用了同一笔本金；
- “没有回归”只限于 Factory 找到并扫描的 TURBO/WETH V3 池；
- 本层不判断自动/人工动机，不声称永久退出，也不下滑点结论；
- 净恢复率使用最初 Burn 价格下的 WETH 等价值，允许低于 0 或高于 100%，不截断。

## 复现

```bash
set -a
source .env
set +a

.venv/bin/python scripts/fetch_factory_pools.py \
  --token-a 0xA35923162C49cF95e6BF26623385eb431ad920D3 \
  --token-b 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 \
  --to-block 25944714 \
  --output notebooks/data/turbo_lp_event_ledger_v1/factory_pools.json

.venv/bin/python scripts/build_turbo_lp_event_ledger.py \
  --factory-pools notebooks/data/turbo_lp_event_ledger_v1/factory_pools.json \
  --output-dir notebooks/data/turbo_lp_event_ledger_v1 \
  --followup-to-block 25944714

.venv/bin/python scripts/create_turbo_lp_event_ledger_notebook.py
.venv/bin/jupyter execute notebooks/turbo_lp_event_ledger.ipynb --inplace --timeout 300
```

主审阅文件：`notebooks/turbo_lp_event_ledger.ipynb`。冻结元数据与文件哈希：`notebooks/data/turbo_lp_event_ledger_v1/manifest.json`。
