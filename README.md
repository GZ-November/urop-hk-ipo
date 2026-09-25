# UROP HK IPO｜港股主板 IPO 数据流水线

[![CI](https://github.com/GZ-November/urop-hk-ipo/actions/workflows/ci.yml/badge.svg)](https://github.com/GZ-November/urop-hk-ipo/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 简介 / Overview

本仓库用于按上市日期收集香港主板普通 IPO 数据。流水线从港交所年度报表确定发行人，准备招股书和配发公告的抽取材料，并在独立复核后校验、写入工作簿。研究工作簿包含 202 个变量。

This repository collects ordinary Hong Kong Main Board IPO data for a chosen listing-date range. The pipeline identifies issuers from HKEX annual reports, prepares prospectus and allotment documents for extraction, and validates and writes reviewed results to a 202-variable research workbook.

## 快速开始 / Quick start

```bash
python3 -m pip install -r requirements.txt

# 按上市日期建立样本 / Create a cohort by listing date
python3 run.py collect --period-start 2026-04-01 --period-end 2026-06-30

# 检查流水线 / Run tests
make test
```

`collect` 会自动下载缺失的港交所年度新上市报表，并生成工作簿及抽取包。首次运行在等待抽取或独立复核时以退出码 `3` 暂停；完成复核后，重跑同一命令即可继续校验与写入。

`collect` downloads missing HKEX annual new-listing reports and creates the workbook and extraction packets. Its first run exits with code `3` while extraction or independent review is pending. Rerun the same command after review to continue validation and writeback.

## 项目文件 / Project files

- [流水线使用指南 / Pipeline guide](Data%20Collecting%20Pipeline/prospectus_pipeline/README.md)
- [2025 Q1 工作簿 / 2025 Q1 workbook](Data%20Collecting%20Pipeline/HKIPO-MB2025Q1.xlsx) · [代码本 / Codebook](Data%20Collecting%20Pipeline/HKIPO_2025Q1_Codebook.md)
- [2026 Q1 工作簿 / 2026 Q1 workbook](Data%20Collecting%20Pipeline/HKIPO-MB2026Q1.xlsx) · [代码本 / Codebook](Data%20Collecting%20Pipeline/HKIPO_2026Q1_Codebook.md)
- [2026 Q2 工作簿 / 2026 Q2 workbook](Data%20Collecting%20Pipeline/HKIPO-MB2026Q2.xlsx) · [代码本 / Codebook](Data%20Collecting%20Pipeline/HKIPO_2026Q2_Codebook.md)
- [2026 Q3 工作簿 / 2026 Q3 workbook](Data%20Collecting%20Pipeline/HKIPO-MB2026Q3.xlsx) · [代码本 / Codebook](Data%20Collecting%20Pipeline/HKIPO_2026Q3_Codebook.md) · [市场报告 / Market report](Data%20Collecting%20Pipeline/HKIPO-MB2026Q3_Market_Report.md)
- [领域术语 / Domain terms](CONTEXT.md)

研究工作簿和代码本可以纳入版本控制；原始 PDF、下载缓存、逐公司抽取 JSON 和 CSV 导出保留在本地。Research workbooks and codebooks may be versioned; raw PDFs, download caches, per-company extraction JSON, and CSV exports stay local.

## 许可证 / License

[MIT](LICENSE)
