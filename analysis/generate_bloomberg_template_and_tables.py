import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
CSV_PATH = os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_1994_2026.csv")

df = pd.read_csv(CSV_PATH, low_memory=False)

# Clean ticker for Bloomberg: strip leading zeros from numeric part + " HK Equity"
def to_bbg_ticker(code_str):
    raw = str(code_str).replace(".HK", "").strip()
    if raw.isdigit():
        return f"{int(raw)} HK Equity"
    return f"{raw} HK Equity"

df["bbg_ticker"] = df["stock_code"].apply(to_bbg_ticker)

# Identify the 3 pitfalls for each row:
# Pitfall 1: Missing price series (Survivorship / Delisting bias in free APIs)
df["pitfall_missing_price"] = df["ir_close"].isna() | (df["bars_count"].fillna(0) == 0)

# Pitfall 2: Ticker recycling (same stock_code appears multiple times in 1994-2026)
df["pitfall_dup_ticker"] = df.duplicated(subset=["stock_code"], keep=False)

# Pitfall 3: Split-adjusted / reverse-split distortion on Day-1 price
# HKEX tick sizes never have 3 decimal places for stocks >= HK$0.50, or extreme IR > 300% before 2015
def check_split_suspect(row):
    d1 = row.get("d1_close")
    ir = row.get("ir_close")
    if pd.isna(d1) or pd.isna(ir):
        return False
    # Check if d1_close has strange fractional decimals due to split adjustment factor
    # e.g., 18.355 or 189.339 when price > 1.0
    rem = round(abs(d1 * 100 - round(d1 * 100)), 4)
    if d1 >= 1.0 and rem > 0.01:
        return True
    if abs(ir) > 3.0 and row.get("board") == "Main Board":
        return True
    return False

df["pitfall_split_suspect"] = df.apply(check_split_suspect, axis=1)
df["needs_priority_audit"] = (
    df["pitfall_missing_price"] | df["pitfall_dup_ticker"] | df["pitfall_split_suspect"]
)

def pitfall_tags(row):
    tags = []
    if row["pitfall_missing_price"]:
        tags.append("MISSING_DELISTED_PRICE")
    if row["pitfall_dup_ticker"]:
        tags.append("RECYCLED_TICKER")
    if row["pitfall_split_suspect"]:
        tags.append("SPLIT_ADJUSTED_SUSPECT")
    return "|".join(tags) if tags else "CLEAN_CHECK"

df["audit_flag"] = df.apply(pitfall_tags, axis=1)

print("Total IPOs (1994-2026):", len(df))
print("  Main Board:", (df["board"] == "Main Board").sum())
print("  GEM:", (df["board"] == "GEM").sum())
print("Pitfall 1 - Missing/Delisted price:", df["pitfall_missing_price"].sum())
print("Pitfall 2 - Recycled/Duplicate ticker rows:", df["pitfall_dup_ticker"].sum())
print("Pitfall 3 - Split-adjusted Day-1 suspect:", df["pitfall_split_suspect"].sum())
print("Total Priority Audit rows (union):", df["needs_priority_audit"].sum())

# ---------------------------------------------------------
# 1. Build Pitfalls Summary Table by Era & Board
# ---------------------------------------------------------
pitfall_rows = []
for board in ["Main Board", "GEM"]:
    sub = df[df["board"] == board].copy()
    for epoch, g in sub.groupby("epoch", sort=False):
        ir_raw = g["ir_close"].dropna() * 100
        # Trimmed / non-split-suspect IR
        g_clean = g[~g["pitfall_split_suspect"]]
        ir_clean = g_clean["ir_close"].dropna() * 100
        pitfall_rows.append({
            "Board": board,
            "Epoch": epoch,
            "Total_IPOs": len(g),
            "Missing_Delisted_N": int(g["pitfall_missing_price"].sum()),
            "Missing_Delisted_Pct": round(g["pitfall_missing_price"].mean() * 100, 1),
            "Recycled_Ticker_N": int(g["pitfall_dup_ticker"].sum()),
            "Recycled_Ticker_Pct": round(g["pitfall_dup_ticker"].mean() * 100, 1),
            "Split_Suspect_N": int(g["pitfall_split_suspect"].sum()),
            "Naive_Mean_IR_Pct": round(ir_raw.mean(), 2) if len(ir_raw) else np.nan,
            "Corrected_Mean_IR_Pct": round(ir_clean.mean(), 2) if len(ir_clean) else np.nan,
            "Median_IR_Pct": round(ir_raw.median(), 2) if len(ir_raw) else np.nan,
        })

pitfall_df = pd.DataFrame(pitfall_rows)
pitfall_df.to_csv(os.path.join(OUT_DIR, "table_pitfalls_audit_1994_2026.csv"), index=False)
print("\nSaved table_pitfalls_audit_1994_2026.csv")
print(pitfall_df.to_string(index=False))

# ---------------------------------------------------------
# 2. Build Excel Workbook with Ready-to-Use Bloomberg Formulas
# ---------------------------------------------------------
wb = openpyxl.Workbook()
# Sheet 0: ReadMe
ws0 = wb.active
ws0.title = "0_ReadMe_操作说明"

header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
sub_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
bold_font = Font(name="Calibri", size=11, bold=True)
norm_font = Font(name="Calibri", size=10)

readme_lines = [
    ["港股 IPO 三十三年 (1994–2026) 学校 Bloomberg 终端数据采集模板 (0 Token 方案)"],
    [""],
    ["一、 为什么你在自己电脑上看不到 Bloomberg 插件？如何在学校机器上启用？"],
    ["1. Bloomberg Excel 插件 (Bloomberg UI / BDP / BDH 公式) 必须在安装了 Bloomberg Terminal 客户端并登录账号的【学校实验室电脑】上运行。"],
    ["2. 如果你在学校 Bloomberg 电脑上打开 Excel 没看到顶部有 'Bloomberg' 菜单栏，请按以下方法花 10 秒钟开启："],
    ["   - 方法 A：点击电脑左下角 Windows 开始菜单 -> 所有程序 -> 找到【Bloomberg】文件夹 -> 点击【Install Office Add-Ins】-> 点击 Install，然后重启 Excel 即可。"],
    ["   - 方法 B：打开 Excel -> 文件 (File) -> 选项 (Options) -> 加载项 (Add-ins) -> 底部管理选择【COM 加载项】点转到 -> 勾选 'Bloomberg Excel Tools'。"],
    [""],
    ["二、 最省力的双保险采集法（强烈建议先做 Step 1，再做 Step 2）"],
    ["【Step 1：在 Bloomberg 终端界面直接用 ECDR <GO> 批量导出（无需任何插件，15 分钟搞定全部历史 IPO）】"],
    ["   1) 在 Bloomberg 黑色终端命令行输入：ECDR <GO> 回车（进入 Equity Offerings 新股发行数据库）。"],
    ["   2) 顶部筛选条件设置："],
    ["      - Offer Type: 勾选 IPO"],
    ["      - Exchange / Country: 选择 Hong Kong (HKEX，包含主板与创业板 GEM)"],
    ["      - Date Range: 01/01/1994 To 12/31/2026"],
    ["      - Offer Stage: 先选 Trading（导出成功上市的新股）；导出后再改选 Withdrawn / Postponed / Pending（导出撤回和失败的新股，用于论文第 5 节）。"],
    ["   3) 点击右上角 Edit Columns 添加以下列："],
    ["      Ticker, Issuer Name, Deal ID, ISIN, Announcement Date, Pricing Date, First Trade Date, Initial Price Range Low, Initial Price Range High,"],
    ["      Offer Price, Offer Size (M), Total Offer Size Inc Over-Allotment, Greenshoe Exercised, Gross Spread (%), Retail Subscription Multiple,"],
    ["      Offer to 1st Day Open (%), Offer to 1st Day Close (%), Offer to 1M (%), Offer to 3M (%), Offer to 6M (%), Offer to 1Y (%), Lead Bookrunners."],
    ["   4) 点击右上角 Output -> Excel 导出保存！ECDR 里的 'Offer to 1st Day Close (%)' 是 Bloomberg 按当年真实未复权价格算好的，不受后来合股或代码重用影响！"],
    [""],
    ["【Step 2：使用本工作簿的自动公式表（Sheet 1 / Sheet 2 / Sheet 3）】"],
    ["   - Sheet '1_Priority_Audit_600'：精选出需要修复的 600 家重点样本（含 254 家退市缺行情、代码重用、及 15 家合股复权失真股）。如果学校机器有每月下载配额限制，只刷新这一张表即可解决全部三大测量陷阱！"],
    ["   - Sheet '2_Full_2865_IPOs'：1994–2026 全部 2,865 家主板+GEM 普通 IPO 的完整自动公式表。"],
    ["   - Sheet '3_Macro_Benchmarks'：恒生指数 (HSI)、恒生综指 (HSCI)、恒生小型股指数 (HSHKSI)、AH溢价指数 (HSAHP)、1个月港元 HIBOR (HIHD01M) 的历史序列公式。"],
    [""],
    ["三、 如何让本表中的公式在学校 Bloomberg 电脑上开始拉数？"],
    ["   1) 为了防止你在自己电脑上打开时满屏报错，表中的公式默认在最前面加了一个单引号（例如 '=BDP(...)）或者放在了可以直接激活的列里。"],
    ["   2) 在学校登录 Bloomberg 后打开本表，选中公式区域（J列至V列），按 Ctrl+H（查找和替换）："],
    ["      【查找内容】输入：'=      【替换为】输入：=      然后点击【全部替换 (Replace All)】，Bloomberg 就会自动开始批量拉取数据！"],
    ["   3) 等待右上角状态栏从 'Requesting Data...' 变为完成，全选表格 -> 复制 -> 右键【粘贴为数值 (Paste Values)】并另存为新文件带回即可！"]
]

for r_idx, line in enumerate(readme_lines, start=1):
    cell = ws0.cell(row=r_idx, column=1, value=line[0])
    if r_idx == 1:
        cell.font = Font(name="Calibri", size=14, bold=True, color="1F4E78")
    elif line[0].startswith(("一、", "二、", "三、", "【Step")):
        cell.font = bold_font
        cell.fill = sub_fill
    else:
        cell.font = norm_font
ws0.column_dimensions["A"].width = 135

def populate_ipo_sheet(ws, sub_df):
    headers = [
        "row_id", "cohort_year", "board", "stock_code", "bbg_ticker",
        "company_name_hkex", "listing_date", "offer_price_hkd", "funds_raised_hkd_m",
        "existing_ir_close", "audit_flag",
        "date_1y", "date_3y", "date_5y",
        "BBG_Current_Name (BDP)", "BBG_Recorded_IPO_Date (Check Recycling)",
        "BBG_Recorded_IPO_Price", "BBG_Market_Status (ACTV/DLST)", "BBG_Inactive_Delist_Date",
        "BBG_Day1_Open_Unadj (CapChg=N)", "BBG_Day1_Close_Unadj (CapChg=N)",
        "BBG_Day1_Volume_Unadj", "BBG_Day1_MktCap_HKD_M",
        "BBG_TRI_Day1", "BBG_TRI_1Y", "BBG_TRI_3Y", "BBG_TRI_5Y"
    ]
    ws.append(headers)
    for col_idx in range(1, len(headers) + 1):
        c = ws.cell(row=1, column=col_idx)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for idx, (_, row) in enumerate(sub_df.iterrows(), start=2):
        ld = str(row["listing_date"])[:10]
        # Compute +1Y, +3Y, +5Y dates safely
        try:
            dt = pd.to_datetime(ld)
            d1y = (dt + pd.DateOffset(years=1)).strftime("%Y-%m-%d")
            d3y = (dt + pd.DateOffset(years=3)).strftime("%Y-%m-%d")
            d5y = (dt + pd.DateOffset(years=5)).strftime("%Y-%m-%d")
        except Exception:
            d1y, d3y, d5y = "", "", ""

        funds_m = round(float(row["funds_raised_total_hkd"]) / 1e6, 2) if pd.notna(row["funds_raised_total_hkd"]) else ""
        ir_val = round(float(row["ir_close"]), 4) if pd.notna(row["ir_close"]) else ""

        # Columns:
        # E is bbg_ticker (col 5), G is listing_date (col 7), L is date_1y (col 12), M is date_3y (col 13), N is date_5y (col 14)
        # Prefix with '= so it doesn't error before opening on Bloomberg machine, or replace '= with = in 1 click
        r = idx
        row_vals = [
            r - 1,
            int(row["cohort_year"]),
            str(row["board"]),
            str(row["stock_code"]),
            str(row["bbg_ticker"]),
            str(row["company_name"]),
            ld,
            float(row["offer_price_hkd"]) if pd.notna(row["offer_price_hkd"]) else "",
            funds_m,
            ir_val,
            str(row["audit_flag"]),
            d1y,
            d3y,
            d5y,
            f"'=BDP(E{r},\"NAME\")",
            f"'=BDP(E{r},\"EQY_INIT_PO_DT\")",
            f"'=BDP(E{r},\"EQY_INIT_PO_SH_PX\")",
            f"'=BDP(E{r},\"MARKET_STATUS\")",
            f"'=BDP(E{r},\"INACTIVE_DATE\")",
            f"'=BDH(E{r},\"PX_OPEN\",G{r},G{r},\"Dates=H\",\"Days=A\",\"Fill=P\",\"CshAdjNormal=N\",\"CshAdjAbnormal=N\",\"CapChg=N\")",
            f"'=BDH(E{r},\"PX_LAST\",G{r},G{r},\"Dates=H\",\"Days=A\",\"Fill=P\",\"CshAdjNormal=N\",\"CshAdjAbnormal=N\",\"CapChg=N\")",
            f"'=BDH(E{r},\"PX_VOLUME\",G{r},G{r},\"Dates=H\",\"Days=A\",\"Fill=P\",\"CshAdjNormal=N\",\"CshAdjAbnormal=N\",\"CapChg=N\")",
            f"'=BDH(E{r},\"CUR_MKT_CAP\",G{r},G{r},\"Dates=H\",\"Days=A\",\"Fill=P\")",
            f"'=BDH(E{r},\"TOT_RETURN_INDEX_GROSS_DVDS\",G{r},G{r},\"Dates=H\",\"Days=A\",\"Fill=P\")",
            f"'=BDH(E{r},\"TOT_RETURN_INDEX_GROSS_DVDS\",L{r},L{r},\"Dates=H\",\"Days=A\",\"Fill=P\")",
            f"'=BDH(E{r},\"TOT_RETURN_INDEX_GROSS_DVDS\",M{r},M{r},\"Dates=H\",\"Days=A\",\"Fill=P\")",
            f"'=BDH(E{r},\"TOT_RETURN_INDEX_GROSS_DVDS\",N{r},N{r},\"Dates=H\",\"Days=A\",\"Fill=P\")",
        ]
        ws.append(row_vals)

    ws.freeze_panes = "F2"
    widths = [8, 10, 12, 12, 16, 36, 13, 14, 16, 14, 28, 12, 12, 12] + [24] * 13
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

# Sheet 1: Priority Audit rows
ws1 = wb.create_sheet(title="1_Priority_Audit")
priority_df = df[df["needs_priority_audit"]].copy()
populate_ipo_sheet(ws1, priority_df)

# Sheet 2: Full 2865 IPOs
ws2 = wb.create_sheet(title="2_Full_2865_IPOs")
populate_ipo_sheet(ws2, df)

# Sheet 3: Macro Benchmarks
ws3 = wb.create_sheet(title="3_Macro_Benchmarks")
ws3.append([
    "Benchmark_Ticker", "Description", "Start_Date", "End_Date",
    "Activate_Formula_Below (Ctrl+H replace '= with =)"
])
for col_idx in range(1, 6):
    c = ws3.cell(row=1, column=col_idx)
    c.font = header_font
    c.fill = header_fill

benchmarks = [
    ("HSI Index", "Hang Seng Index (Price, Total Return Index, PE Ratio)", "1994-01-01", "2026-10-30",
     "'=BDH(\"HSI Index\",\"PX_LAST,TOT_RETURN_INDEX_GROSS_DVDS,PE_RATIO\",\"1994-01-01\",\"2026-10-30\",\"Days=T\",\"Fill=P\")"),
    ("HSCI Index", "Hang Seng Composite Index (Price & Total Return)", "2000-01-01", "2026-10-30",
     "'=BDH(\"HSCI Index\",\"PX_LAST,TOT_RETURN_INDEX_GROSS_DVDS\",\"2000-01-01\",\"2026-10-30\",\"Days=T\",\"Fill=P\")"),
    ("HSHKSI Index", "Hang Seng HK SmallCap Index (Small-Cap / Shell Benchmark)", "2000-01-01", "2026-10-30",
     "'=BDH(\"HSHKSI Index\",\"PX_LAST,TOT_RETURN_INDEX_GROSS_DVDS\",\"2000-01-01\",\"2026-10-30\",\"Days=T\",\"Fill=P\")"),
    ("HSAHP Index", "Hang Seng Stock Connect China AH Premium Index", "2006-01-01", "2026-10-30",
     "'=BDH(\"HSAHP Index\",\"PX_LAST\",\"2006-01-01\",\"2026-10-30\",\"Days=T\",\"Fill=P\")"),
    ("HIHD01M Index", "HKD HIBOR 1-Month Fixing Rate (% p.a., Margin Interest Cost)", "1994-01-01", "2026-10-30",
     "'=BDH(\"HIHD01M Index\",\"PX_LAST\",\"1994-01-01\",\"2026-10-30\",\"Days=T\",\"Fill=P\")"),
    ("HIHD01W Index", "HKD HIBOR 1-Week Fixing Rate (% p.a., Short-Term IPO Freeze)", "1994-01-01", "2026-10-30",
     "'=BDH(\"HIHD01W Index\",\"PX_LAST\",\"1994-01-01\",\"2026-10-30\",\"Days=T\",\"Fill=P\")"),
]
for b in benchmarks:
    ws3.append(list(b))
for i, w in enumerate([18, 52, 14, 14, 95], start=1):
    ws3.column_dimensions[get_column_letter(i)].width = w

xlsx_path = os.path.join(OUT_DIR, "bloomberg_collection_template_1994_2026.xlsx")
wb.save(xlsx_path)
print(f"\nSaved Excel template to: {xlsx_path}")
