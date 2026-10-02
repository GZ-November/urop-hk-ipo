# 继续研究的入口

文档同步于2026-10-02；行情与事件观测截止日仍为2026-09-30。当前研究基准为113家2026 IPO（Q1 38、Q2 45、Q3 30），已包含PR #23的证据修复及PR #25的季度扩展。先读 [当前计划](RESEARCH_PLAN_2026.md) 与 [修复及剩余限制](../pipeline/reports/research_readiness/README.md)，再选择一个研究问题。[9月30日来源复核](AGY_INTEGRATION_2026-09-30.md)保留为阶段性记录。所有旧价格数值写稿已放进 [归档](archive/README.md)。

## 用新 skill 开始

本仓库自带 [ipo-empirical-research](../.agents/skills/ipo-empirical-research/SKILL.md)，适合研究设计、IPO 变量、回归与推断；[hk-ipo-pipeline](../.agents/skills/hk-ipo-pipeline/SKILL.md) 负责采集、核验、刷新和导出。仓库的字段定义、样本计划和日期合同优先于 skill 的通用默认值。

可以把下面的提示交给 agent，并填入研究问题：

```text
使用本仓库的 ipo-empirical-research skill 研究【研究问题】。
先读 docs/RESEARCH_START.md、docs/RESEARCH_PLAN_2026.md 和对应的 skill reference。
只用 2026 上市样本，从当前 master 与来源记录确认变量、单位、时点和覆盖。
先写假说、主要因变量、共同样本和推断方案；列出无法识别的部分。
复用已有 analysis 脚本和 skill helper，保存代码、样本筛选和生成输出。
所有报告数值从输出引用，说明探索性、多重检验和缺失原因。
```

## 数据到结果的路径

| 层 | 位置 | 使用约定 |
|---|---|---|
| 工作簿 | [pipeline/cohorts/](../pipeline/cohorts/) | 规范采集交付；通过验证与事务写回更新 |
| 字段定义 | [registry](../pipeline/registry/HKIPO_Variable_Registry.yaml)、[codebooks](../pipeline/codebooks/) | 单位、缺失、定义；authoring 入口见 ADR |
| 证据与行情 | [prospectus_pipeline/data/](../pipeline/prospectus_pipeline/data/)、[out/](../pipeline/prospectus_pipeline/out/) | 来源、提取/复核状态与行情缓存；部分原始材料仅在本地 |
| 研究输入 | [HKIPO-MB-MASTER_clean.csv](../pipeline/exports/HKIPO-MB-MASTER_clean.csv) | 合并各 cohort 后按实际上市年选择 2026 |
| A+H 输入 | [2026 reference](../pipeline/exports/HKIPO-2026-AH-reference.csv)、[跨年 reference](../pipeline/exports/HKIPO-MASTER-AH-reference.csv) | 当前回归使用 2026 文件；跨年采集不扩大估计样本 |
| 孖展来源与输入 | [来源 ledger](../pipeline/prospectus_pipeline/data/margin/reported_snapshots.json)、[margin CSV](../pipeline/exports/HKIPO-2026-margin-daily.csv) | 每条保留来源、日期与范围；缺失日不插值 |
| 分析代码 | [analysis/README.md](../analysis/README.md) | 脚本、模型及各输出目录 |
| 生成结果 | [analysis/out/](../analysis/out/) | 可复现表格、图、样本筛选与 horizon 覆盖 |
| 复核材料 | [margin_review/](../pipeline/reports/margin_review/) | 修正明细、审计和 hash；UNVERIFIED 候选不进入研究输入 |

## 复现与刷新

从仓库根目录执行。已有环境时直接使用其 Python；首次安装见 [根 README](../README.md)。

```bash
# 代码与字段合同检查
make check-code

# 使用已存储的季度导出，重建派生 master 和全部分析
python run.py master --derive
make analysis

# ledger 更新后重建孖展输入与该模块
make margin-reference
python analysis/margin_financing_2026.py
```

`master --derive` 不会自动从工作簿导出。工作簿变化后，先按实际变化的 cohort 执行 `python run.py export --config prospectus_pipeline/config_2026qN.yaml`（把 N 换成实际季度），再重建 master 和分析。

`make refresh-2026` 会联网刷新原始首日行情、academic/aftermarket 字段和 A 股参考，并重写工作簿、导出及分析结果。完整事件窗口成熟或确需更新行情时运行；普通研究整理只使用现有工件。多 cohort 写入共享报告路径时顺序运行，分别保留审计结果。

单项研究可直接运行 [分析索引](../analysis/README.md) 中的对应脚本。新环境首次使用 skill helper 时执行 `python .agents/skills/ipo-empirical-research/scripts/selftest.py`，它检验 helper，不能代替研究数据核验。

## 目前仍需解决

- Q2的14个董事席位已完成字段级独立复核和写回：8个有、1个无、5个未知。6228.HK的HDR/股份单位也已处理；两项均不再列作待修复。未知仍保留缺失，不能把字段级复核扩大为整份数据已核实。
- 孖展覆盖113家中的25家／93条，截止日规格15家、4个上市月；已有发布时间/截止时点元数据与选择覆盖诊断。截止前可用快照规格25家、6个上市月；仍需核实相对定价的可用时点与调查范围。
- 113家已纳入契约解禁证据文件；按实际契约日期及行情覆盖进入事件样本。Q2窗口随日期成熟更新，未成熟窗口不补估计。
- 机制选择、基石份额和需求具有内生性；相关结果需明确识别限制。已有探索发现不能直接升级为预注册检验。

现有 [学术设计与16项 brainstorm](RESEARCH_DESIGN_2026.md)、[生成结果](../analysis/out/research_frontier/research.md) 和 [证据修复状态](../pipeline/reports/research_readiness/README.md)。

新研究文档、输入与输出的归属规则见 [仓库组织指南](REPOSITORY_GUIDE.md)。
