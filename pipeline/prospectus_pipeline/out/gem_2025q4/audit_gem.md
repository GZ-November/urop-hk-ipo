# HK IPO Excel vs JSON 逐格对账与数据质量审计报告

> **生成时间**：2026-10-15 10:59:37  
> **目标工作簿**：`cohorts/HKIPO-GEM2025Q4.xlsx` (Sheet: `GEM_details`)  
> **审计范围**：1 家公司 × (0 招股书字段 + 0 配发字段 = 0 字段，共 15 个单元格) + 14 个外部工具字段  

## 一、核心审计结论汇总

| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **合计 (0 字段)** | 0 | 0 | 0 | 0 | 0 | 0 | **0%** |

### 关键发现点：
1. **总单元格数**：0 个，匹配格数：0（匹配率：0%）；
2. **差异统计**：Excel 缺失 0 项，JSON 缺失 0 项，数值不匹配 0 项；
   其中匹配格内有 0 格两边均缺失，不是已核实的证据，不能计入证据覆盖率；
3. **外部/工具衍生字段**：共 14 列；全量填报 9 列，部分填报 0 列，未填报或仅有缺失占位 5 列。此统计与上方 88 字段逐格对账是不同范围。

## 二、差异明细清单 (Discrepancies)

✅ **未发现任何字段差异，所有单元格均完全一致！**

## 三、14 个外部/工具衍生字段填报审计

| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |
|---|---|---|---:|---:|---|
| `L` | GEM eligibility R&D / operatin | `Other external / manual` | 0/1 | 0.0% | `—` |
| `M` | GEM disclosed minimum market c | `Other external / manual` | 0/1 | 0.0% | `—` |
| `N` | GEM disclosed minimum public f | `Other external / manual` | 1/1 | 100.0% | `0.25` |
| `O` | GEM public float waiver / exem | `Other external / manual` | 0/1 | 0.0% | `—` |
| `P` | GEM disclosed controller locku | `Other external / manual` | 1/1 | 100.0% | `6` |
| `Q` | GEM compliance adviser | `Other external / manual` | 1/1 | 100.0% | `Alliance Capital Partners` |
| `R` | GEM compliance adviser appoint | `Other external / manual` | 0/1 | 0.0% | `—` |
| `S` | GEM offering structure | `Other external / manual` | 1/1 | 100.0% | `Combined share offer: Hon` |
| `T` | GEM board lot (shares) | `Other external / manual` | 1/1 | 100.0% | `5000` |
| `U` | Official GEM funds raised (HK$ | `Other external / manual` | 1/1 | 100.0% | `50000000` |
| `V` | Official GEM shares at listing | `Other external / manual` | 1/1 | 100.0% | `400000000` |
| `W` | Official GEM market capitalisa | `Other external / manual` | 1/1 | 100.0% | `200000000` |
| `X` | Official GEM source report | `Other external / manual` | 1/1 | 100.0% | `/Users/kate/Documents/URO` |
| `Y` | GEM prospectus date source | `Other external / manual` | 0/1 | 0.0% | `—` |

## 四、1 家公司流水线门禁状态 (Pipeline State)

| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `8549.HK` | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⏳ legacy-untracked |
