# 研究数据问题的处置 · 2026-09-30

这份报告区分已修正的错误与仍受数据/识别限制的问题。新版 skill 不能使尚未发生的窗口成熟，也不能凭一项统计方法消除内生性。

## 1. Q2 董事席位

实际字段为 `Pre-IPO investor board seat (1=yes; 0=no)`，不是另一张旧位置映射中的 Chapter 18A flag。14 家的正式 JSON 为未知，而工作簿原为0。现行 schema 明确“没有证据不等于0”。

Q2 源数据修复由用户在 Zcode 中继续进行，本研究分支不修改 Q2 工作簿、正式 JSON、codebook 或 master 导出。当前基线仍包含这14个未经证据支持的0；涉及董事席位的回归暂停。

曾在本地测试撤销14个零值的候选方案，随后从交付中撤回以避免并行写入。候选明细见 [reconciliation](q2_board_seat_reconciliation.csv)，复核候选页和原文 hash 见 [queue](q2_board_review_queue.csv)。关键词命中只是定位线索，包含公司法等无关段落，不能作为席位证据。

[before audit](q2_audit_before.json) 与 [local candidate audit](q2_audit_local_candidate.json) 仅记录该候选试验，后者不描述当前 canonical 数据。候选方案的14个差异变成“两边未知”，审计会将两边缺失计作匹配，因此3150匹配格不能写成3150个已验证值。master 的布尔缺失提示改为“未知保留缺失”，避免诱导补0；该提示修正独立于 Q2 源数据修复。

## 2. 孖展扩展及实际推断

新增七篇日期明确的智通报道，共26条候选金额；24条进入存储样本，2条样本外观测留在来源ledger并记入排除表。导出从23家/69条提升至25家/93条，截止日从9家升至15家。新增报道保留发布时刻；报道时刻不等于贷款计量时刻，也不能证明投资者在定价前已知。

当前截止日规格 N15、上市月份 G4、最大杠杆0.586；HC3已可计算，p=0.473。最新观察的简单秩相关 rho=0.46、p=0.020，但加入时间窗口和规模后 HC3 p=0.265、restricted wild p=0.219。不能将简单相关解释为融资导致抑价。共同嵌套规格的样本已固定，并输出 rank、杠杆与估计状态。

完整来源见 [ledger](../../prospectus_pipeline/data/margin/reported_snapshots.json)，输入见 [CSV](../../exports/HKIPO-2026-margin-daily.csv)，结果见 [margin.md](../../../analysis/out/margin/margin.md)。瑞为技术的7月3日报道与7月2日调查金额/公开认购表述明显冲突，本轮没有采入该报道；保留日期/调查范围问题，不能为了增加截止日N挑选金额。

## 3. 日期成熟与行情覆盖

固定截至日2026-09-30，新 [event_readiness.csv](../../../analysis/out/research_frontier/event_readiness.csv) 为106家逐项记录工作簿事件日期、实际交易日期、缓存末日和缺失原因。Q1的六日历月端点37家已观测，1家端点行情缺失；Q2/Q3共68家日历窗口未成熟。解禁[-5,+5]窗口Q1完整29家、窗口不完整8家、事件后行情缺失1家；Q2/Q3事件未成熟。

事件frame现在接受显式as-of，截断未来个股/指数bar；缺基准回报不会通过pct_change前向填补成0。工作簿事件日期没有在本轮完成逐份合同核验，因此“窗口完整”不代表契约日期已独立验证，不能升级因果结论。

## 4. 新发现：6228.HK股数单位

该发行人正式提取的 final base/public/placing 值，与自身引用中的89,668,600 / 8,966,900 / 80,701,700存在十倍差异。当前公开配售股数/申请股数=2.261753，不能当作分配率并截为1。

本轮新零售分析排除该行，并将它从新的基石焦点规格隔离；排除原因保存在 [retail_sample.csv](../../../analysis/out/research_frontier/retail_sample.csv)。尚未改写正式JSON或工作簿数值；需要用原始配发文件确认HDR/股份计量，再通过验证与独立审核门禁修正。旧模块的相关股数、财富分配与自由流通数值也须在该修正后重算，不能宣称本轮全表已核实。

## 5. 内生性与研究状态

机制×18C支持表显示17家18C全选A，而非18C只有6家A；此格子缺少对照，matching/IV不能凭空提供识别。基石与需求的内生性继续通过估计对象说明、共同样本、少聚类推断与点估计OVB敏感性处理。已有数据和结果已看过，本轮所有分析均是探索，不是预注册检验。

复现检查：287个流水线测试（2个本地PDF依赖测试跳过）和47个分析测试通过，含未来bar截断、缺基准不补0、经济分母与OVB代数的新增回归测试；lint/registry通过。安装版skill核心检查与22个边界测试通过；未安装的linearmodels/pyfixest明确跳过。来源manifest更新并保留旧hash快照；哈希不证明语义真实。

本轮16项brainstorm和执行设计见 [RESEARCH_DESIGN_2026.md](../../../docs/RESEARCH_DESIGN_2026.md)。

正式源字段新增/修正仍须遵守 [hk-ipo-pipeline skill](../../../.agents/skills/hk-ipo-pipeline/SKILL.md) 的要求：“Writeback requires passing extracted, validated and reviewed records bound to the same payload hash.” 本分支没有改写这些正式字段或合成review通过记录；董事席位由 Zcode 继续修复，6228的原披露核验尚未完成。
