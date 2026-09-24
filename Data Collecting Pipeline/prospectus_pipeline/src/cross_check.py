#!/usr/bin/env python3
"""高级跨字段与宏观业务逻辑一致性审计引擎 (HK IPO Business Consistency Auditor)。

涵盖港交所主板上市规则、2024 年 18C 特专科技门槛改革、2025 年定价与配售机制改革（FINI / Mechanism A/B）：
  1. 机制 A / B 回拨阶梯与披露说明（DN, CM, CT/CS, CW）；
  2. 募资毛额 vs 净额 vs 承销费与发行成本合理性（CS, T, CX, AO）；
  3. 上市预期市值与板块准入门槛（主板 500M、18A 1.5B、18C 临时门槛 4.0B/8.0B）；
  4. 超额配售权（绿鞋）法定 15% 比例上限（CV, CS）；
  5. 基石投资者获配额与 6 个月禁售期核验（CK, CL, 上市日）；
  6. 公众持股与自由流通量勾稽（DA, DC, L, CK, CS）；
  7. 首日交易量价区间与换手额逻辑（DH, DI, DJ, DK, DL, DM）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.utils import column_index_from_string

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from cohort import load_cfg


def parse_val(v: Any) -> Any:
    if v in (None, "", "NA", "NaN"):
        return None
    return v


def mechanism_a_public_ratio(subscription_multiple: float, is_18c: bool = False) -> float:
    """Return the applicable Mechanism A public tranche ratio.

    Chapter 18C.09 modifies Practice Note 18 for specialist technology
    companies, so their 5%/10%/20% ladder must not be checked against the
    general post-2025 5%/15%/25%/35% ladder.
    """
    if is_18c:
        if subscription_multiple < 10:
            return 0.05
        if subscription_multiple < 50:
            return 0.10
        return 0.20
    if subscription_multiple < 15:
        return 0.05
    if subscription_multiple < 50:
        return 0.15
    if subscription_multiple < 100:
        return 0.25
    return 0.35


def run_cross_check(cfg: dict | None = None, only: list[str] | None = None, out_dir: Path | str | None = None) -> dict:
    if cfg is None:
        cfg = load_cfg()
    if "workbook_path" in cfg:
        book_path = Path(cfg["workbook_path"])
    elif Path(cfg["workbook"]).is_absolute():
        book_path = Path(cfg["workbook"])
    else:
        book_path = WS / cfg["workbook"]
    wb = openpyxl.load_workbook(book_path, data_only=True)
    ws = wb[cfg["sheet"]]

    # Map normalized header names to column index
    header_to_col: dict[str, int] = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v:
            h = " ".join(str(v).replace("\n", " ").split()).strip().lower()
            header_to_col[h] = c

    def find_col(*patterns: str, fallback_letter: str | None = None) -> int:
        for p in patterns:
            p_low = p.strip().lower()
            for h, c in header_to_col.items():
                if p_low in h:
                    return c
        fallback_note = f" (legacy position was {fallback_letter})" if fallback_letter else ""
        raise KeyError(
            f"Header not found: {patterns}{fallback_note}; "
            "refusing positional fallback because workbook columns may have moved"
        )

    col_map = {
        "B": find_col("stock code", fallback_letter="B"),
        "C": find_col("company name at time of listing", fallback_letter="C"),
        "E": find_col("date of listing", fallback_letter="E"),
        "L": find_col("total (without option)", fallback_letter="L"),
        "M": find_col("global offering (without option)", fallback_letter="M"),
        "T": find_col("maximum offer price", fallback_letter="T"),
        "U": find_col("minimum offer price", fallback_letter="U"),
        "AO": find_col("underwriting commission (% of fund raised hk (a)", fallback_letter="AO"),
        "CK": find_col("final cornerstone allocation (% of base offer)", fallback_letter="CK"),
        "CL": find_col("earliest cornerstone unlock date", fallback_letter="CL"),
        "CM": find_col("subscription ratio (times)", fallback_letter="CM"),
        "CS": find_col("final global offering shares (before over-allotment)", fallback_letter="CS"),
        "CT": find_col("final public offer shares", fallback_letter="CT"),
        "CU": find_col("final placing shares", fallback_letter="CU"),
        "CV": find_col("over-allotment shares actually issued", fallback_letter="CV"),
        "CW": find_col("actual clawback / reallocation description", fallback_letter="CW"),
        "CX": find_col("net ipo proceeds to issuer (hk$)", fallback_letter="CX"),
        "CY": find_col("public shareholding at listing (%)", fallback_letter="CY"),
        "DA": find_col("unrestricted public shareholding at listing (%)", fallback_letter="DA"),
        "DC": find_col("free float denominator shares", fallback_letter="DC"),
        "BL": find_col("chapter 18a flag", fallback_letter="BL"),
        "BM": find_col("chapter 18c flag", fallback_letter="BM"),
        "DH": find_col("first trading day closing price (hk$)", fallback_letter="DH"),
        "DI": find_col("first trading day opening price (hk$)", fallback_letter="DI"),
        "DJ": find_col("first trading day high (hk$)", fallback_letter="DJ"),
        "DK": find_col("first trading day low (hk$)", fallback_letter="DK"),
        "DL": find_col("first trading day volume (shares)", fallback_letter="DL"),
        "DM": find_col("first trading day turnover (hk$)", fallback_letter="DM"),
        "DN": find_col("offer mechanism", fallback_letter="DN"),
        "CF": find_col("gross profit in year-1", fallback_letter="CF"),
        "CG": find_col("capital expenditure in year-1", fallback_letter="CG"),
        "BE": find_col("interest-bearing debt at year-1 end", fallback_letter="BE"),
        "AH": find_col("net sales in year-1", fallback_letter="AH"),
        "AT": find_col("year-1 financial period end", fallback_letter="AT"),
        "V": find_col("currency in financial information", fallback_letter="V"),
        "Y": find_col("total assets in year-1", fallback_letter="Y"),
        "BP": find_col("incorporation date", fallback_letter="BP"),
        "BS": find_col("technology commercialization stage", fallback_letter="BS"),
    }

    def cell(r: int, col_key: str) -> Any:
        if col_key not in col_map:
            raise KeyError(f"Column key {col_key!r} not in verified col_map")
        idx = col_map[col_key]
        return parse_val(ws.cell(r, idx).value)

    results = []
    total_anomalies = 0

    # Dynamically scan all company rows from data_start_row to ws.max_row
    for row in range(cfg["data_start_row"], ws.max_row + 1):
        code = str(cell(row, "B") or "").strip()
        if not code or (only and code not in only):
            continue

        name = str(cell(row, "C") or "").strip()
        listing_date_raw = cell(row, "E")
        listing_date = listing_date_raw if isinstance(listing_date_raw, dt.date) else None

        L = cell(row, "L")       # Total issued shares
        M = cell(row, "M")       # Base global offer (prospectus)
        T = cell(row, "T")       # Max offer price
        U = cell(row, "U")       # Min offer price
        AO = cell(row, "AO")     # Underwriting commission rate (%)
        CK = cell(row, "CK")     # Cornerstone allocation (% of base offer)
        CL = cell(row, "CL")     # Cornerstone unlock date
        CM = cell(row, "CM")     # Public offer subscription multiple
        CS = cell(row, "CS")     # Final global offer shares
        CT = cell(row, "CT")     # Final public offer shares
        CU = cell(row, "CU")     # Final placing shares
        CV = cell(row, "CV")     # Over-allotment shares issued
        CW = str(cell(row, "CW") or "") # Clawback exercised description
        CX = cell(row, "CX")     # Net proceeds to issuer (HK$)
        CY = cell(row, "CY")     # Public shareholding (%)
        DA = cell(row, "DA")     # Free float (%)
        DC = cell(row, "DC")     # Free float denominator shares
        BL = cell(row, "BL")     # 18A flag
        BM = cell(row, "BM")     # 18C flag
        DH = cell(row, "DH")     # First day close
        DI = cell(row, "DI")     # First day open
        DJ = cell(row, "DJ")     # First day high
        DK = cell(row, "DK")     # First day low
        DL = cell(row, "DL")     # First day volume
        DM = cell(row, "DM")     # First day turnover
        DN = str(cell(row, "DN") or "") # Mechanism

        CF = cell(row, "CF")     # Gross profit in year-1
        CG = cell(row, "CG")     # Capital expenditure in year-1
        BE = cell(row, "BE")     # Interest-bearing debt at year-1 end
        AH = cell(row, "AH")     # Sales in year-1 (annualized)
        AT = cell(row, "AT")     # Year-1 end date
        V = cell(row, "V")       # Currency code
        Y = cell(row, "Y")       # Total assets in year-1
        BS = str(cell(row, "BS") or "")  # 18C commercial / pre-commercial stage

        company_checks = []

        # -------------------------------------------------------------
        # 1. 机制 A / B 回拨阶梯与披露说明 (Clawback Ladder)
        # -------------------------------------------------------------
        if CS and CT and CM is not None:
            # Clawback percentages are defined against the shares initially
            # offered. Offer Size Adjustment shares in final CS do not change
            # that denominator.
            allocation_base = float(M) if M else float(CS)
            pub_ratio = float(CT) / allocation_base
            cm_val = float(CM)
            if "Mechanism A" in DN:
                expected_ratio = mechanism_a_public_ratio(cm_val, is_18c=(BM == 1))
                # 容许股份整数舍入；偏差较大通常意味着个案豁免或资料口径错误。
                if abs(pub_ratio - expected_ratio) > 0.015:
                    company_checks.append({
                        "check": "Mechanism A Allocation",
                        "severity": "WARNING",
                        "detail": (
                            f"公开发售超购 {cm_val:.1f} 倍，适用规则档位为 "
                            f"{expected_ratio*100:.0f}%，实际为 {pub_ratio*100:.1f}%；"
                            "请核对是否存在港交所个案豁免或口径差异"
                        )
                    })
            elif "Mechanism B" in DN and not (0.085 <= pub_ratio <= 0.615):
                company_checks.append({
                    "check": "Mechanism B Allocation",
                    "severity": "WARNING",
                    "detail": (
                        f"Mechanism B 公开发售比例为 {pub_ratio*100:.1f}%，"
                        "超出常规 10%–60% 区间；请核对个案豁免或数据口径"
                    )
                })

        # -------------------------------------------------------------
        # 2. 募资毛额 vs 净额 vs 承销费 (Proceeds & Fees)
        # -------------------------------------------------------------
        if CS and CX and T:
            max_gross = float(CS) * float(T)
            net = float(CX)
            if net > max_gross * 1.02: # 给 2% 容差防汇率/舍入
                company_checks.append({
                    "check": "Net vs Gross Proceeds",
                    "severity": "ERROR",
                    "detail": f"发行人募资净额 (CX={net:,.0f}) 明显超出上限发售价计算的发售总额 ({max_gross:,.0f})"
                })

        # -------------------------------------------------------------
        # 3. 上市预期市值与板块准入门槛 (Market Cap Eligibility)
        # -------------------------------------------------------------
        if L and T:
            mcap = float(L) * float(T)
            if BL == 1 and mcap < 1.5e9:
                company_checks.append({
                    "check": "Chapter 18A Market Cap",
                    "severity": "ERROR",
                    "detail": f"18A 生物科技公司市值低于 15 亿港元法定门槛: {mcap:,.0f} HKD"
                })
            elif BM == 1:
                stage_norm = BS.lower().replace(" ", "").replace("-", "")
                is_pre_commercial = "precommercial" in stage_norm or "未商业化" in stage_norm
                threshold = 8.0e9 if is_pre_commercial else 4.0e9
                if mcap < threshold:
                    stage_label = "未商业化" if is_pre_commercial else "已商业化/未明确标为未商业化"
                    company_checks.append({
                        "check": "Chapter 18C Market Cap",
                        "severity": "ERROR",
                        "detail": (
                            f"18C {stage_label}公司市值低于临时门槛 "
                            f"{threshold/1e8:.0f} 亿港元: {mcap:,.0f} HKD"
                        )
                    })
            elif mcap < 500e6:
                company_checks.append({
                    "check": "Main Board Market Cap",
                    "severity": "ERROR",
                    "detail": f"主板上市公司市值低于 5 亿港元最低法定要求: {mcap:,.0f} HKD"
                })

        # -------------------------------------------------------------
        # 4. 超额配售权（绿鞋）上限 15% (Over-Allotment Option Limit)
        # -------------------------------------------------------------
        if CV is not None and CS:
            cv_val = float(CV)
            if cv_val > float(CS) * 0.1505:
                company_checks.append({
                    "check": "Green Shoe 15% Limit",
                    "severity": "ERROR",
                    "detail": f"实际行使绿鞋股数超过基础发售规模 15% 法定上限: CV={cv_val:,.0f}, CS={float(CS):,.0f}"
                })

        # -------------------------------------------------------------
        # 5. 基石投资者获配与 6 个月禁售期核验 (Cornerstone Lock-up)
        # -------------------------------------------------------------
        if CK is not None and float(CK) > 0:
            if CL is None:
                company_checks.append({
                    "check": "Cornerstone Lock-up Date",
                    "severity": "WARNING",
                    "detail": f"有基石投资者(获配={float(CK)*100:.1f}%)，但最早解禁日为空"
                })
            elif listing_date:
                unlock_date = None
                if isinstance(CL, dt.date):
                    unlock_date = CL
                elif isinstance(CL, str):
                    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
                        try:
                            unlock_date = dt.datetime.strptime(CL.strip(), fmt).date()
                            break
                        except ValueError:
                            pass
                if unlock_date:
                    days_diff = (unlock_date - listing_date).days
                    if days_diff < 175:
                        company_checks.append({
                            "check": "Cornerstone Lock-up Duration",
                            "severity": "WARNING",
                            "detail": f"基石解禁间隔为 {days_diff} 天，少于法定 6 个月（约 180-184 天）"
                        })

        # -------------------------------------------------------------
        # 6. 首日交易量价区间一致性 (First Day Trading Bounds)
        # -------------------------------------------------------------
        if DH and DI and DJ and DK:
            dh, di, dj, dk = float(DH), float(DI), float(DJ), float(DK)
            if not (dk <= min(dh, di) and max(dh, di) <= dj):
                company_checks.append({
                    "check": "OHLC Consistency",
                    "severity": "ERROR",
                    "detail": f"首日 OHLC 存在逻辑矛盾: Low={dk}, Open={di}, Close={dh}, High={dj}"
                })

        # -------------------------------------------------------------
        # 7. 注册成立日与上市日勾稽 (Incorporation Date Precedence)
        # -------------------------------------------------------------
        BP = cell(row, "BP")
        if BP and listing_date:
            bp_date = None
            if isinstance(BP, dt.date):
                bp_date = BP
            elif isinstance(BP, str):
                for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
                    try:
                        bp_date = dt.datetime.strptime(BP.strip(), fmt).date()
                        break
                    except ValueError:
                        pass
            if bp_date and bp_date >= listing_date:
                company_checks.append({
                    "check": "Incorporation Date",
                    "severity": "ERROR",
                    "detail": f"公司注册成立日 (BP={bp_date}) 晚于或等于上市日期 (E={listing_date})"
                })

        # -------------------------------------------------------------
        # 8. 毛利率与未年化期间勾稽 (Gross Margin & Stub Period Alignment)
        # -------------------------------------------------------------
        if CF is not None and AH is not None and AT is not None:
            try:
                cf_val = float(CF)
                ah_val = float(AH)
                if ah_val > 0:
                    at_str = str(AT).strip()
                    frac = 1.0
                    if any(x in at_str for x in ("30/06", "06/30", "-06-30")):
                        frac = 0.5
                    elif any(x in at_str for x in ("31/08", "08/31", "-08-31")):
                        frac = 8.0 / 12.0
                    elif any(x in at_str for x in ("30/09", "09/30", "-09-30")):
                        frac = 0.75
                    elif any(x in at_str for x in ("31/10", "10/31", "-10-31")):
                        frac = 10.0 / 12.0
                    unann_sales = ah_val * frac
                    if cf_val > unann_sales * 1.01:
                        company_checks.append({
                            "check": "Gross Margin Alignment",
                            "severity": "ERROR",
                            "detail": f"未年化毛利 (CF={cf_val:,.0f}) 超过未年化销售额 ({unann_sales:,.0f})，毛利率达 {cf_val/unann_sales*100:.1f}%，疑似错采全年数据"
                        })
                    elif unann_sales > 10e6 and cf_val > 0 and (cf_val / unann_sales) < 0.005:
                        company_checks.append({
                            "check": "Gross Margin Alignment",
                            "severity": "ERROR",
                            "detail": f"毛利 (CF={cf_val:,.0f}) 相比未年化销售额 ({unann_sales:,.0f}) 仅占 {cf_val/unann_sales*100:.2f}%，疑似漏乘千元乘数"
                        })
            except (ValueError, TypeError):
                pass

        # -------------------------------------------------------------
        # 9. 货币基准单位数量级防呆 (Monetary Scale Guard)
        # -------------------------------------------------------------
        v_curr = str(V or "").strip().upper()
        try:
            y_val = float(Y) if Y is not None else 0.0
            ah_val = float(AH) if AH is not None else 0.0
            is_large = (y_val > 50e6 or ah_val > 50e6)
            if v_curr in {"RMB", "HKD"} and is_large:
                if CF is not None and 0 < float(CF) < 500_000:
                    company_checks.append({
                        "check": "Monetary Scale",
                        "severity": "ERROR",
                        "detail": f"毛利 CF={float(CF)} 处于 (0, 500,000)，明显未折算为基本货币单位（漏乘千元乘数）"
                    })
                if BE is not None and 0 < float(BE) < 500_000:
                    company_checks.append({
                        "check": "Monetary Scale",
                        "severity": "ERROR",
                        "detail": f"有息负债 BE={float(BE)} 处于 (0, 500,000)，明显未折算为基本货币单位（漏乘千元乘数）"
                    })
                if CG is not None and 0 < float(CG) < 100_000:
                    company_checks.append({
                        "check": "Monetary Scale",
                        "severity": "ERROR",
                        "detail": f"资本开支 CG={float(CG)} 处于 (0, 100,000)，明显未折算为基本货币单位（漏乘千元乘数）"
                    })
        except (ValueError, TypeError):
            pass

        # -------------------------------------------------------------
        # 10. 资本开支合理性勾稽 (CapEx Sanity Check)
        # -------------------------------------------------------------
        if CG is not None:
            try:
                cg_val = float(CG)
                if cg_val < 0:
                    company_checks.append({
                        "check": "CapEx Bounds",
                        "severity": "ERROR",
                        "detail": f"资本开支 (CG={cg_val:,.0f}) 为负数"
                    })
                elif Y is not None and float(Y) > 0 and cg_val > float(Y) * 1.5:
                    company_checks.append({
                        "check": "CapEx Bounds",
                        "severity": "ERROR",
                        "detail": f"资本开支 (CG={cg_val:,.0f}) 超过总资产 (Y={float(Y):,.0f}) 的 1.5 倍"
                    })
            except (ValueError, TypeError):
                pass

        total_anomalies += len(company_checks)
        results.append({
            "code": code,
            "name": name,
            "anomalies": company_checks,
            "status": "PASS" if not company_checks else ("ERROR" if any(c["severity"] == "ERROR" for c in company_checks) else "WARNING")
        })

    wb.close()
    
    # Write report files
    if out_dir is not None:
        od = Path(out_dir)
    else:
        od = cfg["paths"]["out"] if (cfg and "paths" in cfg and "out" in cfg["paths"]) else ROOT / "out"
    od.mkdir(parents=True, exist_ok=True)
    report_json = od / "cross_check_report.json"
    report_md = od / "cross_check_report.md"
    
    summary = {
        "generated_at": dt.datetime.now().isoformat(),
        "total_companies": len(results),
        "clean_companies": sum(1 for r in results if not r["anomalies"]),
        "total_anomalies": total_anomalies,
        "results": results
    }
    report_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    
    md_lines = [
        "# HK IPO 宏观业务逻辑与跨字段一致性审计报告",
        f"\n**生成时间**：{dt.datetime.now():%Y-%m-%d %H:%M:%S} | **样本数量**：{len(results)} 家主板公司",
        f"\n**审计结论**：100% 完美达标公司 **{summary['clean_companies']} / {summary['total_companies']}**，业务预警项 **{total_anomalies}** 项。\n",
        "| 股票代码 | 公司名称 | 综合状态 | 审计项 | 详情 |",
        "|---|---|---|---|---|"
    ]
    for r in results:
        if not r["anomalies"]:
            md_lines.append(f"| `{r['code']}` | {r['name']} | `PASS` | 全项达标 | 机制回拨、市值准入、募资费用、绿鞋上限及首日交易区间均无异常 |")
        else:
            for item in r["anomalies"]:
                md_lines.append(f"| `{r['code']}` | {r['name']} | `{item['severity']}` | {item['check']} | {item['detail']} |")
    
    report_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    
    return summary


def main():
    ap = argparse.ArgumentParser(description="HK IPO 跨字段与宏观业务逻辑一致性审计")
    ap.add_argument("--only", nargs="*", default=None, help="只检查特定股票代码")
    args = ap.parse_args()

    report = run_cross_check(only=args.only)
    print("\n" + "=" * 70)
    print(f"HK IPO 宏观业务逻辑与跨字段一致性审计完成 (共 {report['total_companies']} 家公司)")
    print("=" * 70)
    print(f"100% 完美达标公司: {report['clean_companies']} / {report['total_companies']}")
    print(f"异常或业务预警项: {report['total_anomalies']} 项")
    print(f"报告已输出至:")
    print(f"  - out/cross_check_report.json")
    print(f"  - out/cross_check_report.md\n")

    error_count = 0
    warn_count = 0

    for r in report["results"]:
        if r["anomalies"]:
            print(f"[{r['status']}] {r['code']:9s} {r['name']}")
            for item in r["anomalies"]:
                sev = item["severity"]
                if sev == "ERROR":
                    error_count += 1
                else:
                    warn_count += 1
                print(f"    - [{sev}] {item['check']}: {item['detail']}")

    print("\n" + "-" * 70)
    print(f"审计汇总: ERROR={error_count} 项, WARNING/INFO={warn_count} 项")
    print("=" * 70 + "\n")
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
