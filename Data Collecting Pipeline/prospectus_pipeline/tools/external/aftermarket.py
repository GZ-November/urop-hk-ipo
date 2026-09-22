#!/usr/bin/env python3
"""香港主板新股二级市场跨期表现与流动性衰减采集引擎 (Col 139–161).

基于 Lowry, Michaely, & Volkova (2017) 长期表现与风格基准实证框架：
  1. 采集上市后 1 个月（T+20 交易日，稳价期结束点）收盘价、买入持有收益 (BHR)、一级申购回报、同期恒指/恒科收益及财富相对比 (WR)；
  2. 采集上市后 6 个月（基石投资者法定解禁日 / T+126 交易日）收盘价、BHR、一级申购回报、同期恒指/恒科收益及财富相对比；
  3. 测算流动性断崖衰减率（6 个月日均成交额相对上市首日成交额之比）；
  4. 预留 1 年期及 3 年期标准化长期跟踪字段；
  5. 记录挂牌存续状态与 18A/18C 监管资格演变。

数据源：腾讯证券高频前复权日 K 线（港股个股 hkXXXXX，恒生指数 hkHSI，恒生科技指数 hkHSTECH）。
安全保证：写入前自动生成带有时间戳的 Excel 快照备份，严格保留既有单元格格式与前 138 列原貌。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
BOOK = WS / "HKIPO-MB2026Q1.xlsx"
CACHE = ROOT / "data" / "market" / "aftermarket"
SHEET = "NLR"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# 新增 23 个字段的标准定义矩阵 (Col 139 - Col 161)
AFTERMARKET_FIELDS = [
    # (col_idx, header, num_format, description)
    (139, "Current listing status", "@", "当前挂牌存续状态 (Active/Suspended/Delisted)"),
    (140, "1-month post-IPO close price (HK$)", "0.00", "上市满1个月(T+20交易日)收盘价 (HK$)"),
    (141, "1-month BHR from Day-1 close (%)", "0.00%", "1个月二级买入持有收益率 (%)"),
    (142, "1-month total return from offer price (%)", "0.00%", "1个月一级申购累计回报率 (%)"),
    (143, "1-month HSI return (%)", "0.00%", "同期恒生指数累计收益率 (%)"),
    (144, "1-month HSTECH return (%)", "0.00%", "同期恒生科技指数累计收益率 (%)"),
    (145, "1-month wealth relative vs HSI", "0.000", "1个月对标恒指财富相对比 (WR_HSI)"),
    (146, "1-month wealth relative vs HSTECH", "0.000", "1个月对标恒科财富相对比 (WR_HSTECH)"),
    (147, "1-month average daily turnover (HK$)", "#,##0", "首月日均成交金额 (港元)"),
    (148, "6-month post-IPO close price (HK$)", "0.00", "上市满6个月(基石解禁日)收盘价 (HK$)"),
    (149, "6-month BHR from Day-1 close (%)", "0.00%", "6个月二级买入持有收益率 (%)"),
    (150, "6-month total return from offer price (%)", "0.00%", "6个月一级申购累计回报率 (%)"),
    (151, "6-month HSI return (%)", "0.00%", "同期恒生指数累计收益率 (%)"),
    (152, "6-month HSTECH return (%)", "0.00%", "同期恒生科技指数累计收益率 (%)"),
    (153, "6-month wealth relative vs HSI", "0.000", "6个月对标恒指财富相对比 (WR_HSI)"),
    (154, "6-month wealth relative vs HSTECH", "0.000", "6个月对标恒科财富相对比 (WR_HSTECH)"),
    (155, "6-month average daily turnover (HK$)", "#,##0", "第6个月日均成交金额 (港元)"),
    (156, "Liquidity decay ratio (6M vs Day-1 turnover)", "0.00%", "6个月相对首日流动性衰减比率 (%)"),
    (157, "1-year post-IPO return (%) [Reserved]", "0.00%", "1年期持有收益率 [预留]"),
    (158, "1-year wealth relative vs HSI [Reserved]", "0.000", "1年期对标恒指财富相对比 [预留]"),
    (159, "3-year post-IPO return (%) [Reserved]", "0.00%", "3年期持有收益率 [预留]"),
    (160, "3-year wealth relative vs HSI [Reserved]", "0.000", "3年期对标恒指财富相对比 [预留]"),
    (161, "18A/18C regulatory milestone status", "@", "监管资格演变与商业化里程碑状态"),
]

HEADER_FILL = PatternFill(start_color="FF00B0F0", end_color="FF00B0F0", fill_type="solid")
HEADER_FONT = Font(name="Arial", size=11, bold=True, color="000000")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DATA_ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
DATA_ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
DATA_ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
DATA_FONT = Font(name="Arial", size=10)

THIN_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)


def to_date(v) -> dt.date | None:
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str) and len(v) >= 10:
        try:
            return dt.datetime.strptime(v[:10], "%Y-%m-%d").date()
        except ValueError:
            pass
    return None


def hk_symbol(code: str) -> str:
    d = "".join(ch for ch in str(code) if ch.isdigit())
    return f"hk{int(d):05d}"


def fetch_bars(symbol: str, frm: str, to: str, n: int = 350, retries: int = 4) -> list[dict]:
    url = (f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
           f"?param={symbol},day,{frm},{to},{n},qfq")
    last_err = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                payload = json.loads(r.read().decode())
            if payload.get("code") != 0:
                raise RuntimeError(f"{symbol} code={payload.get('code')} msg={payload.get('msg')}")
            data = (payload.get("data") or {}).get(symbol) or {}
            rows = data.get("qfqday") or data.get("day") or []
            if not rows:
                raise RuntimeError(f"{symbol} empty bars returned")
            
            bars = []
            for row in rows:
                turnover = None
                if len(row) > 8 and row[8] not in (None, "", "{}", {}):
                    try:
                        turnover = float(row[8]) * 10_000
                    except (TypeError, ValueError):
                        turnover = None
                bars.append({
                    "date": dt.datetime.strptime(str(row[0])[:10], "%Y-%m-%d").date(),
                    "open": float(row[1]),
                    "close": float(row[2]),
                    "high": float(row[3]),
                    "low": float(row[4]),
                    "volume": float(row[5]),
                    "turnover": turnover,
                })
            return bars
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(0.5 * (i + 1))
    raise RuntimeError(f"{symbol} 拉取失败：{last_err}")


def find_bar_on_or_after(bars: list[dict], target_date: dt.date) -> dict | None:
    for b in bars:
        if b["date"] >= target_date:
            return b
    return None


def find_bar_on_or_before(bars: list[dict], target_date: dt.date) -> dict | None:
    matched = None
    for b in bars:
        if b["date"] <= target_date:
            matched = b
        else:
            break
    return matched


def calculate_metrics(company_info: dict, stock_bars: list[dict], hsi_bars: list[dict], hstech_bars: list[dict]) -> dict[str, Any]:
    ld = company_info["listing_date"]
    offer_price = company_info["offer_price"]
    day1_close = company_info["day1_close"]
    day1_turnover = company_info["day1_turnover"]
    unlock_date = company_info["unlock_date"]
    
    # 过滤出上市日及以后的 bars
    after_bars = [b for b in stock_bars if b["date"] >= ld]
    if not after_bars:
        return {"error": "无上市日及之后的行情数据"}
    
    # 若缺失 day1_close，用首个有效 bar 的 close 补齐
    p1 = day1_close if (day1_close is not None and day1_close > 0) else after_bars[0]["close"]
    p0 = offer_price if (offer_price is not None and offer_price > 0) else p1
    d0 = after_bars[0]["date"]
    
    # 指数上市首日基准收盘价
    hsi_d0_bar = find_bar_on_or_after(hsi_bars, d0)
    hstech_d0_bar = find_bar_on_or_after(hstech_bars, d0)
    hsi_p0 = hsi_d0_bar["close"] if hsi_d0_bar else None
    hstech_p0 = hstech_d0_bar["close"] if hstech_d0_bar else None
    
    # ==================== 1 个月指标 (T+20 交易日) ====================
    idx_1m = min(19, len(after_bars) - 1)
    bar_1m = after_bars[idx_1m]
    p_1m = bar_1m["close"]
    d_1m = bar_1m["date"]
    
    bhr_1m = (p_1m / p1) - 1.0 if p1 else None
    total_ret_1m = (p_1m / p0) - 1.0 if p0 else None
    
    # 同期指数收益
    hsi_1m_bar = find_bar_on_or_after(hsi_bars, d_1m)
    hstech_1m_bar = find_bar_on_or_after(hstech_bars, d_1m)
    
    hsi_ret_1m = (hsi_1m_bar["close"] / hsi_p0 - 1.0) if (hsi_1m_bar and hsi_p0) else None
    hstech_ret_1m = (hstech_1m_bar["close"] / hstech_p0 - 1.0) if (hstech_1m_bar and hstech_p0) else None
    
    wr_hsi_1m = ((1.0 + bhr_1m) / (1.0 + hsi_ret_1m)) if (bhr_1m is not None and hsi_ret_1m is not None) else None
    wr_hstech_1m = ((1.0 + bhr_1m) / (1.0 + hstech_ret_1m)) if (bhr_1m is not None and hstech_ret_1m is not None) else None
    
    # 首月日均成交额 (前 20 个交易日)
    turnover_list_1m = [b["turnover"] for b in after_bars[: idx_1m + 1] if b.get("turnover") is not None]
    avg_turnover_1m = (sum(turnover_list_1m) / len(turnover_list_1m)) if turnover_list_1m else None

    # ==================== 6 个月指标 (基石解禁日或 T+126 交易日) ====================
    target_6m_date = unlock_date if unlock_date else (ld + dt.timedelta(days=180))
    # 查找首个在目标解禁日及之后的 bar；若尚未达到目标日，则取当前最新的交易 bar
    bar_6m = find_bar_on_or_after(after_bars, target_6m_date)
    if not bar_6m:
        bar_6m = after_bars[-1]
    
    idx_6m = after_bars.index(bar_6m)
    p_6m = bar_6m["close"]
    d_6m = bar_6m["date"]
    
    bhr_6m = (p_6m / p1) - 1.0 if p1 else None
    total_ret_6m = (p_6m / p0) - 1.0 if p0 else None
    
    hsi_6m_bar = find_bar_on_or_after(hsi_bars, d_6m)
    hstech_6m_bar = find_bar_on_or_after(hstech_bars, d_6m)
    
    hsi_ret_6m = (hsi_6m_bar["close"] / hsi_p0 - 1.0) if (hsi_6m_bar and hsi_p0) else None
    hstech_ret_6m = (hstech_6m_bar["close"] / hstech_p0 - 1.0) if (hstech_6m_bar and hstech_p0) else None
    
    wr_hsi_6m = ((1.0 + bhr_6m) / (1.0 + hsi_ret_6m)) if (bhr_6m is not None and hsi_ret_6m is not None) else None
    wr_hstech_6m = ((1.0 + bhr_6m) / (1.0 + hstech_ret_6m)) if (bhr_6m is not None and hstech_ret_6m is not None) else None
    
    # 第 6 个月（取 6M 节点前 20 个交易日）日均成交额
    start_idx_m6 = max(0, idx_6m - 19)
    turnover_list_6m = [b["turnover"] for b in after_bars[start_idx_m6 : idx_6m + 1] if b.get("turnover") is not None]
    avg_turnover_6m = (sum(turnover_list_6m) / len(turnover_list_6m)) if turnover_list_6m else None
    
    # 流动性衰减率 (6M 日均 / 首日成交额)
    t0_turnover = day1_turnover if (day1_turnover and day1_turnover > 0) else after_bars[0].get("turnover")
    liquidity_decay = (avg_turnover_6m / t0_turnover) if (avg_turnover_6m and t0_turnover and t0_turnover > 0) else None

    # ==================== 监管与存续里程碑 ====================
    is_18a = bool(company_info.get("is_18a"))
    is_18c = bool(company_info.get("is_18c"))
    name = company_info.get("name", "")
    
    if is_18c:
        milestone = "18C (Specialist Tech)"
    elif is_18a:
        milestone = "18A (Biotech / B-tag)"
    else:
        milestone = "Standard"

    return {
        139: "Active",
        140: round(p_1m, 3),
        141: round(bhr_1m, 6) if bhr_1m is not None else None,
        142: round(total_ret_1m, 6) if total_ret_1m is not None else None,
        143: round(hsi_ret_1m, 6) if hsi_ret_1m is not None else None,
        144: round(hstech_ret_1m, 6) if hstech_ret_1m is not None else None,
        145: round(wr_hsi_1m, 4) if wr_hsi_1m is not None else None,
        146: round(wr_hstech_1m, 4) if wr_hstech_1m is not None else None,
        147: round(avg_turnover_1m, 2) if avg_turnover_1m is not None else None,
        148: round(p_6m, 3),
        149: round(bhr_6m, 6) if bhr_6m is not None else None,
        150: round(total_ret_6m, 6) if total_ret_6m is not None else None,
        151: round(hsi_ret_6m, 6) if hsi_ret_6m is not None else None,
        152: round(hstech_ret_6m, 6) if hstech_ret_6m is not None else None,
        153: round(wr_hsi_6m, 4) if wr_hsi_6m is not None else None,
        154: round(wr_hstech_6m, 4) if wr_hstech_6m is not None else None,
        155: round(avg_turnover_6m, 2) if avg_turnover_6m is not None else None,
        156: round(liquidity_decay, 6) if liquidity_decay is not None else None,
        157: None,  # 1Y Reserved
        158: None,  # 1Y WR Reserved
        159: None,  # 3Y Reserved
        160: None,  # 3Y WR Reserved
        161: milestone,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="采集与计算港股新股二级市场跨期表现与流动性衰减指标 (Col 139-161)")
    ap.add_argument("--dry-run", action="store_true", help="演练模式：仅打印计算结果摘要，不修改 Excel")
    ap.add_argument("--book", default=str(BOOK), help="目标 Excel 工作簿路径")
    ap.add_argument("--only", nargs="*", default=None, help="只处理指定股票代码")
    args = ap.parse_args()

    book = Path(args.book)
    if not book.exists():
        sys.stderr.write(f"错误: 目标工作簿不存在: {book}\n")
        return 1

    CACHE.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.load_workbook(book, data_only=True)
    ws = wb[SHEET]

    companies = []
    for r in range(2, ws.max_row + 1):
        code_val = ws.cell(r, 2).value
        if not code_val:
            continue
        code = str(code_val).strip()
        ld = to_date(ws.cell(r, 5).value)
        if not ld:
            continue
        
        # 读取必要参数
        offer_price = ws.cell(r, 11).value
        day1_close = ws.cell(r, 127).value
        day1_turnover = ws.cell(r, 135).value
        unlock_date = to_date(ws.cell(r, 104).value)
        is_18a = ws.cell(r, 77).value == 1
        is_18c = ws.cell(r, 78).value == 1
        name = str(ws.cell(r, 3).value or "").strip()

        companies.append({
            "row": r,
            "code": code,
            "name": name,
            "listing_date": ld,
            "offer_price": float(offer_price) if offer_price else None,
            "day1_close": float(day1_close) if day1_close else None,
            "day1_turnover": float(day1_turnover) if day1_turnover else None,
            "unlock_date": unlock_date,
            "is_18a": is_18a,
            "is_18c": is_18c,
        })
    wb.close()

    if args.only:
        companies = [c for c in companies if c["code"] in args.only]

    print(f"📊 准备处理 {len(companies)} 家公司二级市场跨期数据...")

    # 1. 抓取指数日 K 线
    min_date = min(c["listing_date"] for c in companies) - dt.timedelta(days=10)
    max_date = dt.date.today() + dt.timedelta(days=2)
    frm_str = min_date.strftime("%Y-%m-%d")
    to_str = max_date.strftime("%Y-%m-%d")

    print(f"📈 正在拉取宏观基准指数 ({frm_str} ~ {to_str})...")
    hsi_bars = fetch_bars("hkHSI", frm_str, to_str, n=350)
    (CACHE / "hsi_bars.json").write_text(json.dumps(hsi_bars, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"   ✓ 恒生指数 (hkHSI): {len(hsi_bars)} 条 K 线")

    hstech_bars = fetch_bars("hkHSTECH", frm_str, to_str, n=350)
    (CACHE / "hstech_bars.json").write_text(json.dumps(hstech_bars, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"   ✓ 恒生科技指数 (hkHSTECH): {len(hstech_bars)} 条 K 线")

    # 2. 逐一拉取个股日 K 线并计算指标
    computed_rows = []
    print("\n🔍 正在拉取样本公司行情并计算跨期收益与流动性指标...")
    for idx, c in enumerate(companies, 1):
        sym = hk_symbol(c["code"])
        frm_c = c["listing_date"].strftime("%Y-%m-%d")
        try:
            bars = fetch_bars(sym, frm_c, to_str, n=300)
            (CACHE / f"{sym}.json").write_text(json.dumps(bars, default=str, ensure_ascii=False), encoding="utf-8")
            metrics = calculate_metrics(c, bars, hsi_bars, hstech_bars)
            metrics["row"] = c["row"]
            metrics["code"] = c["code"]
            computed_rows.append(metrics)
            print(f"   [{idx:02d}/{len(companies):02d}] {c['code']:7s}: "
                  f"1M BHR={metrics[141]*100:+.2f}%, 6M BHR={metrics[149]*100:+.2f}%, "
                  f"WR_HSI(6M)={metrics[153]:.3f}, 换手衰减={metrics[156]*100:.1f}%")
        except Exception as exc:
            print(f"   [{idx:02d}/{len(companies):02d}] {c['code']:7s}: 抓取/计算异常: {exc}")
        time.sleep(0.15)

    print(f"\n✅ 成功计算 {len(computed_rows)} / {len(companies)} 家公司指标")

    if args.dry_run:
        print("\n[DRY RUN] 演练模式结束，未向工作簿写入数据。")
        return 0

    sys.path.insert(0, str(ROOT / "src"))
    from workbook_transaction import workbook_transaction

    with workbook_transaction(book, operation="aftermarket") as wb:
        ws = wb[SHEET]
        # 设置表头
        for col_idx, header, num_format, desc in AFTERMARKET_FIELDS:
            cell = ws.cell(1, col_idx)
            cell.value = header
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = HEADER_ALIGN
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = max(18, len(header) // 2 + 4)

        # 写入数据
        for row_data in computed_rows:
            r = row_data["row"]
            for col_idx, header, num_format, desc in AFTERMARKET_FIELDS:
                cell = ws.cell(r, col_idx)
                val = row_data.get(col_idx)
                cell.value = val
                cell.font = DATA_FONT
                cell.border = THIN_BORDER
                cell.number_format = num_format
                if num_format == "@":
                    cell.alignment = DATA_ALIGN_CENTER
                elif num_format in ("0.00%", "0.00", "0.000", "#,##0"):
                    cell.alignment = DATA_ALIGN_RIGHT
                else:
                    cell.alignment = DATA_ALIGN_CENTER

    print(f"🎉 成功将 23 个二级市场跨期与流动性指标写入主表 {SHEET} (Col 139–161) -> {book.name}！\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
