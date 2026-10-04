# 来源与修正材料索引

本目录保存 2026-09-30 集成复核的证据记录。研究说明见 [集成报告](../../../docs/archive/README.md)，当前估计见 [A+H 输出](../../../analysis/out/ah_anchor/ah_anchor.md) 与 [孖展输出](../../../analysis/out/margin/margin.md)。

| 文件 | 状态与用途 |
|---|---|
| [first_day_price_corrections.csv](first_day_price_corrections.csv) | 26 家原始首日收盘价修正的前后明细 |
| [market_source_manifest.json](market_source_manifest.json) | 当次 A/H 行情、来源 ledger 与导出的 hash 快照；更新数据后旧 hash 不代表新工件 |
| [audit_2026q1.txt](audit_2026q1.txt)、[audit_2026q2.txt](audit_2026q2.txt)、[audit_2026q3.txt](audit_2026q3.txt) | 按 cohort 保存的存储对账；Q2 有 14 个 BL 字段缺 JSON，不能替代语义复核 |
| [source_exclusions.json](source_exclusions.json) | 来源 ledger 内不属于存储研究样本的观测排除记录 |
| [agy_candidates_UNVERIFIED.csv](agy_candidates_UNVERIFIED.csv) | 原始 42 条候选记录，保留追溯；未核实，不供分析读取 |

正式孖展来源为 [reported_snapshots.json](../../prospectus_pipeline/data/margin/reported_snapshots.json)，导出为 [HKIPO-2026-margin-daily.csv](../../exports/HKIPO-2026-margin-daily.csv)。来源日期、调查范围和计量单位应从 ledger 查证，不能用候选文件或零售认购结果代填。
