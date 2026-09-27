# 手工市场数据导入（HIBOR / 银行体系总结余）

工作簿里 **DF `1-month HIBOR before prospectus (%)`** 与
**DG `Banking system aggregate balance before prospectus (HK$)`** 两列，
数据源（HKMA）在当前网络环境下不稳定，改由手工导出后导入。

## 你要做的事

导出 HKMA **Daily Monetary Statistics**（银行体系流动性）在
**2025-11-01 ~ 2026-04-30** 区间的每日数据，存成下面这个文件：

```
prospectus_pipeline/data/manual/hibor_balance.csv
```

只要 Q1 涉及的交易日（约 60–90 行）就够了，**一张表覆盖全部 38 家**。

### CSV 格式（必须有表头，列名照抄）

```csv
date,hibor_1m_pct,aggregate_balance_hkd_mn
2026-01-02,2.88387,54023
2026-01-05,2.90123,54110
2026-01-06,2.87654,53950
```

| 列 | 含义 | 单位 |
|---|---|---|
| `date` | 观察日 | `YYYY-MM-DD` 或 `DD/MM/YYYY` 都接受 |
| `hibor_1m_pct` | 1 个月 HIBOR 定盘价 | **百分数原值**（HKMA 页面写 `2.88387` 就填 `2.88387`） |
| `aggregate_balance_hkd_mn` | 银行体系总结余 | **百万港元**（HKMA 写 `54023` 就填 `54023`） |

导入时会自动换算成表格要求的单位：
- HIBOR → 小数（`2.88387` → `0.0288387`，单元格格式 `0.0%` 显示为 `2.9%`）
- 总结余 → 基本单位（`54023` → `54023000000`）

### 方式一：官方 API 直接取（推荐，✅ 已跑通）

```bash
python3 prospectus_pipeline/tools_fetch_hkma.py                 # 默认 2025-11-01 ~ 2026-04-30
python3 prospectus_pipeline/tools_fetch_hkma.py --from 2025-11-01 --to 2026-04-30
```

脚本一次大页取回（`pagesize=1000`）、**本地按日期过滤**，直接写出本文件要求的
`hibor_balance.csv`。实测 120 行，2025-11-03 ~ 2026-04-30。

#### ⚠️ 两个坑（已实测确认）

1. **`from` / `to` 参数被这个 API 忽略**。
   传 `?from=2026-01-01&to=2026-03-31` 仍然返回**最新 100 条**（2026-09-09 起）。
   正确做法：用 **大 `pagesize` 一次取回**，或 **`offset` 一步步往回翻**，然后**本地过滤**。
   - `pagesize=100` → 覆盖约 4 个月
   - `pagesize=500` → 覆盖约 1.5 年
   - `pagesize=1000` → 覆盖约 4 年
   - `pagesize=5000` → 回到 2006 年
2. **偶发 502 / 读超时**。网关（Kong）会间歇性抽风：
   根路径 `https://api.hkma.gov.hk/` 返回 `{"message":"no Route matched with those values"}` 说明网关可达；
   真正接口 502 时重试即可（脚本已带指数退避）。

验证网关是否可达（浏览器可直接打开）：

```
https://api.hkma.gov.hk/public/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity?pagesize=5
```

API 参数（来自官方 swagger）：
`pagesize` / `offset` / `fields` / `column` / `filter` / `choose` / `from` / `to` / `sortby` / `sortorder`
文档：<https://apidocs.hkma.gov.hk/documentation/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity/>

### 方式二：手工导出

- HKMA「Daily Monetary Statistics」页面 → Interbank Liquidity（Daily Figures）
- 或 Wind / Choice / Bloomberg 等终端导出

字段对应：`end_of_date` → `date`，`hibor_fixing_1m` → `hibor_1m_pct`，
`closing_balance` → `aggregate_balance_hkd_mn`。

### 取值口径

对每家公司：取**观察日严格早于招股书日期**的**最后一条**记录
（即"招股书刊发前公开可得的最新观察值"），与手册 §4.6 一致。

## 导入

```bash
cd "Data Collecting Templates/News"
python3 prospectus_pipeline/tools_import_market_csv.py --dry-run   # 先看会填什么
python3 prospectus_pipeline/tools_import_market_csv.py             # 确认后写回
```

写回前会自动备份；只改 DF / DG 两列的值，不动任何格式；其它列一律不碰。
