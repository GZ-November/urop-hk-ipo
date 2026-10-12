# 采集请求模板 · Collection request template

复制一个模板，改掉 `{}` 里的内容，发给 agent。只有时间段是必填的，其余都有默认值。

## 最简（一句话）

```text
收集 {2025 年第四季度} 的港股 IPO。
```

## 完整（可选项写清楚）

```text
用 https://github.com/GZ-November/urop-hk-ipo 收集港股 IPO 数据。

时间段（按实际上市日期，含首尾）：{2025 年第四季度}
板块：{主板和 GEM（默认） / 只要主板 / 只要 GEM}
观察截止日：{默认今天（香港时间）}
仓库里已有的季度：{复用并审计（默认） / 重新采集}
交付：一个 ZIP，并告诉我每个季度的公司数、上市日期范围、Excel/CSV 路径、
缺失字段、待复核项和数据源限制。
```

## English

```text
Collect Hong Kong IPOs listed in {2025 Q4}.
```

```text
Use https://github.com/GZ-November/urop-hk-ipo to collect Hong Kong IPO data.

Period (actual listing date, inclusive): {2025 Q4}
Boards: {Main Board and GEM (default) / Main Board only / GEM only}
Observation cutoff: {today in Hong Kong (default)}
Quarters already stored in the repository: {reuse and audit (default) / re-collect}
Delivery: one ZIP, plus issuer counts, listing-date ranges, Excel/CSV paths,
missing fields, pending reviews and source limitations for each quarter.
```

## 时间段写法 · Period forms

| 中文 | English | Plan term |
|---|---|---|
| 2025 年全年 | year 2025 | `2025` |
| 2025 年下半年 | 2025 second half | `2025H2` |
| 2025 年第四季度 | 2025 Q4 | `2025Q4` |
| 2025 年 11 月 | November 2025 | `2025-11` |
| 2024 年第三季度到 2025 年第二季度 | 2024 Q3 through 2025 Q2 | `2024Q3..2025Q2` |
| 2025 年 11 月 15 日到 2026 年 2 月 10 日 | 15 Nov 2025 to 10 Feb 2026 | `2025-11-15..2026-02-10` |
| 上个季度 | last completed quarter | `latest` |

To preview the jobs without collecting anything, run `python3 run.py plan <term>`.
