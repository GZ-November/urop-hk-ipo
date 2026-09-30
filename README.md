# UROP HK IPO · 港股主板 IPO 研究流水线

[![CI](https://github.com/GZ-November/urop-hk-ipo/actions/workflows/ci.yml/badge.svg)](https://github.com/GZ-November/urop-hk-ipo/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

从港交所披露文件构建可追溯的香港主板普通 IPO 数据集，并开展 **仅限 2026 年上市发行人** 的统计和计量分析。研究工作簿包含 202 个变量，覆盖发行结构、财务、Pre-IPO 投资者、基石、承销、首日表现与上市后事件窗口。

An evidence-linked research pipeline for ordinary Hong Kong Main Board IPOs: document collection, deterministic validation, reviewed Excel delivery, and statistical and econometric analysis restricted to 2026 listings.

## 项目能做什么

- **建立发行人 cohort**：按上市日期从港交所官方报表筛选；剔除 GEM 转板、SPAC/de-SPAC 与介绍上市。
- **抽取与复核**：准备招股书和配发公告材料；校验字段、来源引用及会计/股数关系。写回前验证抽取与复核状态及对应 SHA-256。
- **安全写回**：事务保存、写入前快照、保留工作簿样式；缺来源或未成熟窗口保持缺失。
- **研究交付**：季度工作簿、代码本、变量注册表、master 面板、样本排除记录和漂移报告。
- **2026 年分析**：Module A 描述统计；Module B 首日收益回归、HC3/月聚类推断及 bootstrap；季度、月份和收益分解。

哈希验证用于确认被复核的文件版本；数据含义仍须根据原始披露进行独立复核。历史 cohort 可用于流水线验证，但不会进入当前研究分析。

## 安装与检查

Python 3.9+；建议使用独立虚拟环境。在仓库根目录运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[analysis,dev]'
make check-code
python run.py --help
```

这是从源码 checkout 运行的 CLI；`pip install -e` 安装依赖配置和项目元数据。请保留仓库目录、schema、配置及研究工件。

`make check-code` 与 CI 和 pre-push hook 共用检查入口：语法、静态检查、流水线测试、分析测试及注册表一致性。已有工作簿与抽取状态可另用 `make check` 做数据审计。

## 数据收集与分析

```bash
# 以明确上市日期区间建立 cohort
python run.py collect --period-start 2026-04-01 --period-end 2026-06-30

# 指定现有 cohort；配置路径相对 pipeline/
python run.py status --config prospectus_pipeline/config_2026q3.yaml
python run.py audit --target all --config prospectus_pipeline/config_2026q3.yaml

# 从季度导出建立研究面板
python run.py registry --check
python run.py master --derive

# 重新生成全部分析表格与图片：只使用 2026 年上市数据
make analysis
```

`collect` 在等待抽取或独立复核时以退出码 `3` 暂停；完成复核后重跑同一命令。已有季度 CSV 位于 `pipeline/exports/`；如需从工作簿更新，逐 cohort 执行 `python run.py export --config ...`，再生成 master。

2026 样本按实际上市年份筛选，并拒绝 cohort/日期冲突与重复股票代码。Module A 的季度、路径、定价和 VC/PE 比较全部在 2026 样本内；Module B 使用共同完整样本、4–6 月控制项，最多 10 个解释变量。各模块报告样本量及缺失情况；当前结果属于探索性研究。

## 目录与文档

| 路径 | 用途 |
|---|---|
| `pipeline/cohorts/` | 规范研究工作簿 |
| `pipeline/exports/` | 季度 clean CSV 与 master 面板 |
| `pipeline/codebooks/`、`pipeline/registry/` | 代码本与变量注册表 |
| `pipeline/reports/` | 审计、样本筛选、漂移与市场报告 |
| `pipeline/prospectus_pipeline/` | 核心代码、schema、cohort 配置与测试 |
| `analysis/`、`analysis/out/` | 2026 年分析脚本与生成结果 |

- [流水线指南](pipeline/prospectus_pipeline/README.md) · [内部架构与维护](pipeline/SYSTEM_MANAGEMENT.md)
- [2026 研究计划](docs/RESEARCH_PLAN_2026.md) · [分析使用说明](analysis/README.md)
- [领域术语](CONTEXT.md) · [变量注册表](pipeline/registry/HKIPO_Variable_Registry.yaml)
- [2026Q1 代码本](pipeline/codebooks/HKIPO_2026Q1_Codebook.md) · [2026Q2 代码本](pipeline/codebooks/HKIPO_2026Q2_Codebook.md) · [2026Q3 代码本](pipeline/codebooks/HKIPO_2026Q3_Codebook.md)
- [贡献指南](CONTRIBUTING.md) · [数据与安全政策](SECURITY.md)

版本控制包含公开披露形成的研究工作簿、CSV、抽取证据和报告。原始招股书 PDF、全文切片、隔离采集缓存、快照、临时脚本及模型运行日志保留在本地；以 `.gitignore` 和贡献指南为准。

[MIT License](LICENSE)
