# 图表审阅材料

`liquidity_analysis_visual_review.ipynb` 是给导师查看的数据分析图表版。Notebook 已经执行，图和表格结果保存在文件中，在 GitHub 直接打开即可阅读。

它重点展示：

- uPEG 价格与池库存的实际时间曲线；
- TURBO 累计撤出、快速重建、净 LP 流和真实 Transfer 的区别；
- FTT、CEL、GALA 相同变量在不同案例中的结果和不确定范围；
- 净 LP 流与未来 24 小时收益的原始小时散点；
- GALA 对“目标代币库存占比”解释的独立验证。

## 数据文件

- `data/visual_review_time_series.csv`：从 uPEG、TURBO、FTT、CEL、GALA 已完成分析的 `analysis_series.parquet` 中抽取作图所需列；FTT/CEL/GALA 使用事件前窗口的 token-total 小时序列。
- `data/turbo_anomaly_daily.csv`：TURBO 2026-08-05 至 2026-08-09 的逐日异常证据摘要，与原 `daily_ledger.csv` 一致。
- Notebook 还直接读取已提交的 `output-cross-case-synthesis/association_ledger.csv` 和 `output-gala-inventory-validation/hourly_features.csv`。

这些是便于公开复核的精简结果，不替代本地保存的原始 Swap、Transfer 和 LP 事件表。

## 本地重新运行

```bash
python3 -m pip install -r notebooks/requirements.txt
jupyter lab notebooks/liquidity_analysis_visual_review.ipynb
```

重新运行后应得到 5 张图。图中的价格统一使用 WETH 计价；相关关系只用于描述和核验，不代表因果或已经验证的崩盘预测能力。
