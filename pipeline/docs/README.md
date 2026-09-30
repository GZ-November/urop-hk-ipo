# 项目文档索引 (Documentation Index)

本目录保留原始构建规范、采集指南与历史阶段记录。当前工作簿为 202 列；早期 120 列手册需结合 variable_catalog.py 和现行 registry 阅读。所有当前统计和回归限定为 2026 年上市数据。

---

## 目录分类导航

### 1. 权威规范与业务字段口径 (`specs/`)
收纳原始 120 列模板的数据口径、来源划分及导师要求；新增列参照现行注册表：
- [数据规则确认表.md](./specs/数据规则确认表.md)：★ 权威字段口径确认表、三色分区划分及与老师模板的差异说明。
- [数据收集说明.md](./specs/数据收集说明.md)：全景字段采集说明、数据结构与逻辑关联。
- [深蓝字段采集方案.md](./specs/深蓝字段采集方案.md)：配发结果（CK, CM–DC）与外部行情/规则字段（DD–DO, DF/DG）专项方案。
- [Data Construction Manual_students.docx](./specs/Data%20Construction%20Manual_students.docx)：导师原始数据构建手册（口径与颜色来源）。
- [Hang_Seng_Industry_Classification_System_2026.pdf](./specs/Hang_Seng_Industry_Classification_System_2026.pdf)：恒生行业分类系统（HSICS 2026）官方权威编制与细分定义手册。

### 2. 团队作业与采集指引 (`guides/`)
收纳多人协作采集规范与阶段性操作记录：
- [队友采集指示_全列手册.md](./guides/队友采集指示_全列手册.md)：团队协作采集手册与各字段操作规范。
- [Q1_浅绿字段采集记录.md](./guides/Q1_浅绿字段采集记录.md)：港交所新上市报告 A–K 浅绿字段采集操作历史记录。

### 3. 阶段规划与成本台账 (`reports/`)
收纳模型成本分析与抽取开销汇报：
- [Flash低成本采集计划.md](./reports/Flash低成本采集计划.md)：低成本模型抽取方案与 token 控制策略。
- [HKIPO_Flash成本汇报.xlsx](./reports/HKIPO_Flash成本汇报.xlsx)：模型调用成本统计明细台账。
