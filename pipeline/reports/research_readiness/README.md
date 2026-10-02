# 研究数据修复与剩余限制 · 2026-10-02

本页已同步PR #23、#25及#27；行情与分析观测截止日仍为2026-09-30。当前master包含113家2026普通IPO：Q1 38、Q2 45、Q3 30。旧106家基准已被季度扩展取代。文档同步不代表重新运行流水线或全面语义核验。

## 1. Q2董事席位：已完成字段级修复

原先14个未经支持零值已通过独立原披露复核写回，当前master为8个“有”、1个“无”、5个“未知”。未知保留缺失，不再补0；董事席位研究不再因这14项修复而整体暂停，仍须检查实际有效N、组别支持和选择内生性。

修复来源与范围见 [review_provenance.csv](../repair_handoff/review_provenance.csv)。这些review针对指定字段，不表示整个payload已独立复核。[旧reconciliation](q2_board_seat_reconciliation.csv)、[旧定位queue](q2_board_review_queue.csv)、[before audit](q2_audit_before.json)及[local candidate audit](q2_audit_local_candidate.json)保留为历史证据，不描述当前canonical值。未知之间匹配不能计作已核实值。

## 2. 6228.HK：已处理HDR/股份单位

PR #23已确认每份HDR代表10股，并在 [offer_units.json](../../prospectus_pipeline/data/manual/offer_units.json)记录原披露与计量规则；复核材料见 [6228_units_review.json](../repair_handoff/6228_units_review.json)。报价和发售数量使用HDR口径，与股本比较时应用10倍转换，不能把所有数量机械乘10。

当前 [retail_sample.csv](../../../analysis/out/research_frontier/retail_sample.csv)已重新纳入6228.HK，配售率约0.226175，旧异常排除已撤销。当前研究输入和生成结果按修复后的口径使用，不再列作待修复。

## 3. 契约解禁证据已合并，行情窗口仍受日期约束

PR #23完成原106家契约证据，PR #25补齐7家新增发行人；[lockup_contracts.json](../../prospectus_pipeline/data/manual/lockup_contracts.json)现覆盖113家，候选、独立review及assembly记录位于 [lockup_contracts/](../repair_handoff/lockup_contracts/)。事件panel消费该文件，缺契约证据时显式报告，不以“上市日加固定月数”补日期。契约核验不意味着真实卖出行为可观察，也不意味着事件具有外生性。

当前 [event_readiness.csv](../../../analysis/out/research_frontier/event_readiness.csv)有113家；六日历月端点37家已观测、1家成熟但缺行情、75家未成熟。其工作簿日期覆盖标签为：完整29家、事件后行情缺失1家、窗口不完整6家、事件未成熟73家、缺事件日期4家。这是单一工作簿事件日期的覆盖诊断，不是完整多事件契约panel的计数。

该CSV仍保留“workbook date; contract not independently reverified in this run”标签；它表示该脚本运行未重新执行合同review，不能据此推断PR #23/#25的契约核验未完成。合同证据状态查正式文件及review，窗口覆盖查实际行情。显式as-of继续截断未来bar，缺基准不前向填成0。Q2完整窗口按发行人实际契约日期从10月起陆续成熟。

## 4. 孖展：时点元数据已补，覆盖与识别限制仍在

当前覆盖25家/93条；截止日规格N=15、G=4。PR #23已加入发布时间、截止日期、调查范围及可用性元数据和覆盖选择诊断；当前截止前可用快照规格N=25、G=6。93条中78条发表于截止日前、13条明确晚于截止时点、2条截止日时刻未知。订购截止前可用不能代替定价前可用。

来源见 [ledger](../../prospectus_pipeline/data/margin/reported_snapshots.json)，输入见 [CSV](../../exports/HKIPO-2026-margin-daily.csv)，当前估计及限制见 [margin.md](../../../analysis/out/margin/margin.md)。7656.HK的报道/金额冲突继续保留未解决，不为扩样挑选数值。稀疏快照和券商调查覆盖不能识别个体杠杆、需求加速或羊群因果效应。

## 5. 剩余研究工作与解释边界

- 选定主线，固定主要因变量、共同样本、事件日期、排除规则和推断方法；已有结果仍为探索性。
- 零售收益方向优先补官方申请档位配售表；A+H方向补首次发行公告日期和同行匹配。A+H当前子样本38家，实际各horizon另报N。
- 机制支持表中19家18C均为A；非18C只有6家A，另有机制未知记录。缺共同支持及发行人自选择不能由matching或bootstrap消除。
- 基石与需求仍内生，需求控制可能条件化于通道或碰撞点；OVB敏感性不是因果识别。
- 成熟后刷新解禁窗口，区分契约、供给暴露、实际交易及重叠公告；预测模型应在Q4检验前冻结。

[2026-10-01 evidence coverage](../repair_handoff/evidence_coverage_summary.md)与[market audit](../repair_handoff/market_data_audit_summary.md)是106家阶段快照，不能作113家全量审计结论。PR #27补齐113/113逐股表目录，也不等于所有字段已全面核实。本次仅同步文档，未重跑旧检查或改写历史审计数值。

正式字段后续新增/修正继续遵守 [hk-ipo-pipeline skill](../../../.agents/skills/hk-ipo-pipeline/SKILL.md) 的证据、验证及独立review门禁。研究设计见 [RESEARCH_DESIGN_2026.md](../../../docs/RESEARCH_DESIGN_2026.md)，当前待办见 [RESEARCH_PLAN_2026.md](../../../docs/RESEARCH_PLAN_2026.md)。
