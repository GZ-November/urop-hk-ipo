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
import calendar
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
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from market_fetcher import get_market_fetcher
from run import load_cfg

WS = ROOT.parent
_cfg = load_cfg()
_configured_book = Path(_cfg["workbook"])
BOOK = _configured_book if _configured_book.is_absolute() else WS / _configured_book
CACHE = _cfg["paths"]["data"] / "market" / "aftermarket"
STATUS_OVERRIDES = ROOT / "schema" / "listing_status_overrides.json"
SHEET = _cfg.get("sheet", "NLR")
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


def norm_header(v) -> str:
    return " ".join(str(v or "").replace("\n", " ").split()).strip().lower()



def hk_symbol(code: str) -> str:
    d = "".join(ch for ch in str(code) if ch.isdigit())
    return f"hk{int(d):05d}"


def fetch_bars(
    symbol: str,
    frm: str,
    to: str,
    n: int = 350,
    retries: int = 4,
    provider: str = "auto",
) -> tuple[list[dict], str, list[str]]:
    """调用弹性市场数据抓取引擎拉取规范化日 K 线序列。"""
    fetcher = get_market_fetcher()
    return fetcher.fetch_bars_resilient(
        symbol, frm, to, n_bars=n, preferred_provider=provider
    )


def find_bar_on_or_after(bars: list[dict], target_date: dt.date) -> dict | None:
    for b in bars:
        if b["date"] >= target_date:
            return b if (b["date"] - target_date).days <= 10 else None
    return None


def find_bar_on_or_before(bars: list[dict], target_date: dt.date) -> dict | None:
    matched = None
    for b in bars:
        if b["date"] <= target_date:
            matched = b
        else:
            break
    return matched


def add_calendar_months(value: dt.date, months: int) -> dt.date:
    """Advance a date by whole calendar months, clipping to month end."""
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


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
    if (after_bars[0]["date"] - ld).days > 10:
        return {"error": f"首个股价样本 {after_bars[0]['date']} 晚于上市日 {ld}；历史 K 线截断"}
    
    # 若缺失 day1_close，用首个有效 bar 的 close 补齐
    p1 = day1_close if (day1_close is not None and day1_close > 0) else after_bars[0]["close"]
    p0 = offer_price if (offer_price is not None and offer_price > 0) else p1
    d0 = after_bars[0]["date"]
    benchmark_dates = [b["date"] for b in hsi_bars + hstech_bars]
    market_as_of = max(benchmark_dates) if benchmark_dates else after_bars[-1]["date"]
    last_stock_date = after_bars[-1]["date"]
    status_override = company_info.get("status_override") or {}
    if status_override.get("status"):
        listing_status = str(status_override["status"])
        listing_status_source = status_override.get("source_url")
    elif (market_as_of - last_stock_date).days > 30:
        listing_status = "No recent trading (verify status)"
        listing_status_source = None
    else:
        listing_status = "Active"
        listing_status_source = None
    
    # 指数上市首日基准收盘价
    hsi_d0_bar = find_bar_on_or_after(hsi_bars, d0)
    hstech_d0_bar = find_bar_on_or_after(hstech_bars, d0)
    if hsi_d0_bar is None or hstech_d0_bar is None:
        return {"error": f"上市日 {d0} 附近缺少恒指/恒科样本；历史 K 线截断"}
    hsi_p0 = hsi_d0_bar["close"] if hsi_d0_bar else None
    hstech_p0 = hstech_d0_bar["close"] if hstech_d0_bar else None
    
    # ==================== 1 个月指标 (T+20 交易日) ====================
    # 少于 20 个真实交易日时保持缺失，禁止用“当前最新日”冒充 1M。
    one_month_matured = len(after_bars) >= 20
    bar_1m = after_bars[19] if one_month_matured else None
    p_1m = bar_1m["close"] if bar_1m else None
    d_1m = bar_1m["date"] if bar_1m else None

    bhr_1m = (p_1m / p1) - 1.0 if (p_1m is not None and p1) else None
    total_ret_1m = (p_1m / p0) - 1.0 if (p_1m is not None and p0) else None

    # 同期指数收益
    hsi_1m_bar = find_bar_on_or_after(hsi_bars, d_1m) if d_1m else None
    hstech_1m_bar = find_bar_on_or_after(hstech_bars, d_1m) if d_1m else None

    hsi_ret_1m = (hsi_1m_bar["close"] / hsi_p0 - 1.0) if (hsi_1m_bar and hsi_p0) else None
    hstech_ret_1m = (hstech_1m_bar["close"] / hstech_p0 - 1.0) if (hstech_1m_bar and hstech_p0) else None

    wr_hsi_1m = ((1.0 + bhr_1m) / (1.0 + hsi_ret_1m)) if (bhr_1m is not None and hsi_ret_1m is not None) else None
    wr_hstech_1m = ((1.0 + bhr_1m) / (1.0 + hstech_ret_1m)) if (bhr_1m is not None and hstech_ret_1m is not None) else None

    # 首月日均成交额 (前 20 个交易日)
    turnover_list_1m = [b["turnover"] for b in after_bars[:20] if b.get("turnover") is not None] if one_month_matured else []
    avg_turnover_1m = (sum(turnover_list_1m) / len(turnover_list_1m)) if turnover_list_1m else None

    # ==================== 6 个月指标 (基石解禁日或 T+126 交易日) ====================
    target_6m_date = unlock_date if (unlock_date and unlock_date >= ld) else add_calendar_months(ld, 6)
    # 只有样本真实覆盖目标日后的首个交易日，6M 窗口才成熟。
    bar_6m = find_bar_on_or_after(after_bars, target_6m_date)
    six_month_matured = bar_6m is not None

    idx_6m = after_bars.index(bar_6m) if bar_6m else None
    p_6m = bar_6m["close"] if bar_6m else None
    d_6m = bar_6m["date"] if bar_6m else None

    bhr_6m = (p_6m / p1) - 1.0 if (p_6m is not None and p1) else None
    total_ret_6m = (p_6m / p0) - 1.0 if (p_6m is not None and p0) else None
    
    hsi_6m_bar = find_bar_on_or_after(hsi_bars, d_6m) if d_6m else None
    hstech_6m_bar = find_bar_on_or_after(hstech_bars, d_6m) if d_6m else None
    
    hsi_ret_6m = (hsi_6m_bar["close"] / hsi_p0 - 1.0) if (hsi_6m_bar and hsi_p0) else None
    hstech_ret_6m = (hstech_6m_bar["close"] / hstech_p0 - 1.0) if (hstech_6m_bar and hstech_p0) else None
    
    wr_hsi_6m = ((1.0 + bhr_6m) / (1.0 + hsi_ret_6m)) if (bhr_6m is not None and hsi_ret_6m is not None) else None
    wr_hstech_6m = ((1.0 + bhr_6m) / (1.0 + hstech_ret_6m)) if (bhr_6m is not None and hstech_ret_6m is not None) else None
    
    # 第 6 个月（取 6M 节点前 20 个交易日）日均成交额
    start_idx_m6 = max(0, idx_6m - 19) if idx_6m is not None else None
    turnover_list_6m = (
        [b["turnover"] for b in after_bars[start_idx_m6 : idx_6m + 1] if b.get("turnover") is not None]
        if start_idx_m6 is not None else []
    )
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
        "observation_meta": {
            "data_as_of": market_as_of.isoformat(),
            "last_stock_trading_date": last_stock_date.isoformat(),
            "listing_status": listing_status,
            "listing_status_source": listing_status_source,
            "one_month_target": "20th trading day",
            "one_month_actual_date": d_1m.isoformat() if d_1m else None,
            "one_month_matured": one_month_matured,
            "six_month_target_date": target_6m_date.isoformat(),
            "six_month_actual_date": d_6m.isoformat() if d_6m else None,
            "six_month_matured": six_month_matured,
        },
        139: listing_status,
        140: round(p_1m, 3) if p_1m is not None else None,
        141: round(bhr_1m, 6) if bhr_1m is not None else None,
        142: round(total_ret_1m, 6) if total_ret_1m is not None else None,
        143: round(hsi_ret_1m, 6) if hsi_ret_1m is not None else None,
        144: round(hstech_ret_1m, 6) if hstech_ret_1m is not None else None,
        145: round(wr_hsi_1m, 4) if wr_hsi_1m is not None else None,
        146: round(wr_hstech_1m, 4) if wr_hstech_1m is not None else None,
        147: round(avg_turnover_1m, 2) if avg_turnover_1m is not None else None,
        148: round(p_6m, 3) if p_6m is not None else None,
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
    ap.add_argument(
        "--provider",
        choices=["auto", "tencent", "yahoo"],
        default="auto",
        help="市场行情数据提供商偏好 (auto=腾讯优先并自动降级至雅虎财经, tencent, yahoo)",
    )
    args = ap.parse_args()

    book = Path(args.book)
    if not book.exists():
        sys.stderr.write(f"错误: 目标工作簿不存在: {book}\n")
        return 1

    CACHE.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.load_workbook(book, data_only=True)
    ws = wb[SHEET]

    header_to_idx: dict[str, int] = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v:
            header_to_idx[norm_header(v)] = c

    def find_col_idx(*patterns: str, default: int | None = None) -> int:
        for p in patterns:
            p_low = norm_header(p)
            for h, c in header_to_idx.items():
                if p_low in h:
                    return c
        if default is not None:
            return default
        raise KeyError(f"Required header pattern not found in workbook: {patterns}")

    col_code = find_col_idx("stock code", default=2)
    col_name = find_col_idx("company name at time of listing", default=3)
    col_listing_date = find_col_idx("date of listing", default=5)
    col_offer_price = find_col_idx("ipo subscription price", default=11)
    col_day1_close = find_col_idx("first trading day closing price", default=127)
    col_day1_turnover = find_col_idx("first trading day turnover", default=135)
    col_unlock_date = find_col_idx("earliest cornerstone unlock date", default=104)
    col_18a = find_col_idx("chapter 18a flag", default=77)
    col_18c = find_col_idx("chapter 18c flag", default=78)

    companies = []
    status_overrides = {}
    if STATUS_OVERRIDES.exists():
        status_overrides = json.loads(STATUS_OVERRIDES.read_text(encoding="utf-8"))
    for r in range(2, ws.max_row + 1):
        code_val = ws.cell(r, col_code).value
        if not code_val:
            continue
        code = str(code_val).strip()
        ld = to_date(ws.cell(r, col_listing_date).value)
        if not ld:
            continue
        
        # 读取必要参数
        offer_price = ws.cell(r, col_offer_price).value
        day1_close = ws.cell(r, col_day1_close).value
        day1_turnover = ws.cell(r, col_day1_turnover).value
        unlock_date = to_date(ws.cell(r, col_unlock_date).value)
        is_18a = ws.cell(r, col_18a).value == 1
        is_18c = ws.cell(r, col_18c).value == 1
        name = str(ws.cell(r, col_name).value or "").strip()

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
            "status_override": status_overrides.get(code, {}),
        })
    wb.close()


    if args.only:
        targets = set()
        for x in args.only:
            s = str(x).strip().upper()
            targets.add(s)
            targets.add(s.replace(".HK", ""))
            d = "".join(ch for ch in s if ch.isdigit())
            if d:
                targets.add(f"{int(d):04d}.HK")
                targets.add(f"{int(d):05d}")
                targets.add(str(int(d)))
        companies = [c for c in companies if c["code"].upper() in targets or c["code"].upper().replace(".HK", "") in targets]

    print(f"📊 准备处理 {len(companies)} 家公司二级市场跨期数据 (策略: {args.provider})...")

    # 1. 抓取指数日 K 线
    min_date = min(c["listing_date"] for c in companies) - dt.timedelta(days=10)
    max_date = dt.date.today() + dt.timedelta(days=2)
    frm_str = min_date.strftime("%Y-%m-%d")
    to_str = max_date.strftime("%Y-%m-%d")

    print(f"📈 正在拉取宏观基准指数 ({frm_str} ~ {to_str})...")
    index_n = max(350, (max_date - min_date).days + 10)
    hsi_bars, prov_hsi, errs_hsi = fetch_bars("hkHSI", frm_str, to_str, n=index_n, provider=args.provider)
    (CACHE / "hsi_bars.json").write_text(json.dumps(hsi_bars, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"   ✓ 恒生指数 (hkHSI via {prov_hsi}): {len(hsi_bars)} 条 K 线")

    try:
        hstech_bars, prov_hstech, errs_hstech = fetch_bars("hkHSTECH", frm_str, to_str, n=index_n, provider=args.provider)
        (CACHE / "hstech_bars.json").write_text(json.dumps(hstech_bars, default=str, ensure_ascii=False), encoding="utf-8")
        print(f"   ✓ 恒生科技指数 (hkHSTECH via {prov_hstech}): {len(hstech_bars)} 条 K 线")
    except Exception as exc:
        hstech_bars, prov_hstech, errs_hstech = [], "unavailable", [str(exc)]
        print(f"   ⚠ 恒生科技指数拉取受阻 ({args.provider}): {exc}")

    # 2. 逐一拉取个股日 K 线并计算指标
    computed_rows = []
    print("\n🔍 正在拉取样本公司行情并计算跨期收益与流动性指标...")
    for idx, c in enumerate(companies, 1):
        sym = hk_symbol(c["code"])
        frm_c = c["listing_date"].strftime("%Y-%m-%d")
        try:
            stock_n = max(300, (max_date - c["listing_date"]).days + 10)
            bars, prov_stock, errs_stock = fetch_bars(sym, frm_c, to_str, n=stock_n, provider=args.provider)
            (CACHE / f"{sym}.json").write_text(json.dumps(bars, default=str, ensure_ascii=False), encoding="utf-8")
            metrics = calculate_metrics(c, bars, hsi_bars, hstech_bars)
            if metrics.get("error"):
                raise ValueError(metrics["error"])
            metrics["row"] = c["row"]
            metrics["code"] = c["code"]
            
            # 记录数据来源与降级血统 (Observation Provenance)
            obs_meta = metrics.get("observation_meta", {})
            obs_meta["stock_provider"] = prov_stock
            obs_meta["hsi_provider"] = prov_hsi
            obs_meta["hstech_provider"] = prov_hstech
            if errs_stock:
                obs_meta["stock_fallback_errors"] = errs_stock
            if errs_hsi:
                obs_meta["hsi_fallback_errors"] = errs_hsi
            if errs_hstech:
                obs_meta["hstech_fallback_errors"] = errs_hstech
            metrics["observation_meta"] = obs_meta

            computed_rows.append(metrics)
            def pct(value):
                return f"{value * 100:+.2f}%" if value is not None else "未成熟"

            def ratio(value):
                return f"{value:.3f}" if value is not None else "未成熟"

            print(f"   [{idx:02d}/{len(companies):02d}] {c['code']:7s} ({prov_stock}): "
                  f"1M BHR={pct(metrics[141])}, 6M BHR={pct(metrics[149])}, "
                  f"WR_HSI(6M)={ratio(metrics[153])}, 换手衰减={pct(metrics[156])}")
        except Exception as exc:
            print(f"   [{idx:02d}/{len(companies):02d}] {c['code']:7s}: 抓取/计算异常: {exc}")
        time.sleep(0.15)

    print(f"\n✅ 成功计算 {len(computed_rows)} / {len(companies)} 家公司指标")

    observation_manifest = {
        row["code"]: row.get("observation_meta", {}) for row in computed_rows
    }
    (CACHE / "observation_manifest.json").write_text(
        json.dumps(observation_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if len(computed_rows) < len(companies):
        sys.stderr.write(
            f"错误: 仅成功计算 {len(computed_rows)} / {len(companies)} 家公司指标，"
            "存在外部数据拉取失败；为保证数据完整性，终止写回。\n"
        )
        return 1

    if args.dry_run:
        print("\n[DRY RUN] 演练模式结束，未向工作簿写入数据。")
        return 0

    sys.path.insert(0, str(ROOT / "src"))
    from workbook_transaction import workbook_transaction

    with workbook_transaction(book, operation="aftermarket") as wb:
        ws = wb[SHEET]
        # 动态定位或创建目标列，防止列位移
        field_col_map = {}
        header_positions = {}
        for c in range(1, ws.max_column + 1):
            hv = ws.cell(1, c).value
            if hv:
                header_positions[norm_header(hv)] = c

        for default_idx, header, num_format, desc in AFTERMARKET_FIELDS:
            nh = norm_header(header)
            target_col = header_positions.get(nh, default_idx)
            field_col_map[default_idx] = target_col

        # 设置表头
        for default_idx, header, num_format, desc in AFTERMARKET_FIELDS:
            target_col = field_col_map[default_idx]
            cell = ws.cell(1, target_col)
            cell.value = header
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = HEADER_ALIGN
            col_letter = get_column_letter(target_col)
            ws.column_dimensions[col_letter].width = max(18, len(header) // 2 + 4)

        # 写入数据
        for row_data in computed_rows:
            r = row_data["row"]
            for default_idx, header, num_format, desc in AFTERMARKET_FIELDS:
                target_col = field_col_map[default_idx]
                cell = ws.cell(r, target_col)
                val = row_data.get(default_idx)
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
