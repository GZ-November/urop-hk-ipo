"""Descriptive offering/company facts for 113 IPOs through 2026-09-30.

No aftermarket observations or hypothesis tests. Source fields are inventoried
even when unsuitable for a headline statistic. All money aggregates use HKD;
financial statement amounts are summarized within reporting currency only.
"""
from __future__ import annotations

import hashlib
import json
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from research_inputs import C, MASTER, ROOT, load_panel, select_2026

OUT = ROOT / "analysis/out/offer_facts"
CUTOFF = pd.Timestamp("2026-09-30")
SECTORS = {
    "051": "Materials and mining", "052": "Materials and mining", "053": "Materials and mining",
    "101": "Industrials and equipment", "103": "Industrials and equipment", "231": "Consumer discretionary",
    "232": "Consumer discretionary", "235": "Consumer discretionary", "237": "Consumer discretionary",
    "251": "Consumer staples", "252": "Consumer staples", "281": "Biotech and pharma",
    "282": "Medical devices and services", "502": "Other", "601": "Other",
    "701": "Hardware and robotics", "702": "Software and AI", "703": "Semiconductors",
}
# These producer fields have known provenance problems or concentrated values
# requiring source review; retain their coverage, but do not headline them.
REVIEW_FIELDS = {
    "Lead sponsor name": "Known field error; parse participation from Sponsor(s)",
    "Joint sponsor count": "Parse Sponsor(s); original derived count needs review",
    "Sponsor commercial bank affiliate flag": "Derived institution classification requires review",
    "Underwriting base commission rate (%)": "Use original disclosed HK/international commission fields",
    "Underwriting discretionary incentive fee rate (%)": "Highly concentrated and incomplete; not actual payments",
    "Total underwriting fee rate (%)": "Known derived-definition problem; not total fees",
    "Pre-IPO investor board seat (1=yes; 0=no)": "Fourteen Q2 zeros lack supporting evidence",
    "Cornerstone investor count": "Partial coverage; value 4 repeated 26 times; review required",
    "Pre-IPO institutional investor count": "Value 6 repeated in 71 of 106 rows; review required",
    "Cornerstone state-owned presence flag": "Derived classification not independently source-reviewed",
    "Crossover fund presence flag": "Derived classification not independently source-reviewed",
    "Pre-IPO state-owned backing flag": "Use original State/Gov backing; review derived field",
}


def ratio(a: pd.Series, b: pd.Series) -> pd.Series:
    """Require a finite numerator and strictly positive finite denominator."""
    a = a.replace([np.inf, -np.inf], np.nan)
    b = b.replace([np.inf, -np.inf], np.nan)
    return (a / b.where(b > 0)).replace([np.inf, -np.inf], np.nan)


def flag(s: pd.Series, predicate) -> pd.Series:
    return predicate(s).astype(float).where(s.notna())


def normalized_text(s: pd.Series) -> pd.Series:
    return s.astype("string").str.replace(r"\s+", " ", regex=True).str.strip()


def build_frame() -> tuple[pd.DataFrame, dict[str, tuple[str, str]]]:
    """Return the fixed issuer sample and display/source definitions."""
    d = select_2026(load_panel())
    d = d.loc[d.listing_date <= CUTOFF].copy()
    if len(d) != 113:
        raise ValueError(f"Expected the user's 113-IPO snapshot, observed {len(d)}")
    d["sector"] = d["Industry classification code"].map(
        lambda x: SECTORS.get(str(int(x)).zfill(6)[:3], "Unmapped") if pd.notna(x) else "Unknown")
    metrics: dict[str, tuple[str, str]] = {}

    def add(key, label, unit, values):
        d[key] = values
        metrics[key] = (label, unit)

    def source(key, label, unit, column):
        add(key, label, unit, d[column])

    source("age", "上市时公司年龄", "年", C["age"])
    add("base_bn", "基础发售募资（价格×最终基础股数）", "十亿港元", d.base_proceeds / 1e9)
    add("reported_bn", "原记录香港+国际募资（口径可能含超配）", "十亿港元", d.gross_proceeds / 1e9)
    source("offer_price", "发行价格", "港元", C["offer"])
    add("net_bn", "发行人净所得款（原披露）", "十亿港元", d["Net IPO proceeds to issuer (HK$)"] / 1e9)
    add("expense_m", "上市开支（原披露）", "百万港元", d["Listing expenses (HK$)"] / 1e6)
    add("expense_share", "上市开支/基础募资", "%", 100 * ratio(d["Listing expenses (HK$)"], d.base_proceeds))
    source("fee_hk", "香港承销佣金率", "%", "Underwriting Commission (% of fund raised HK (a)")
    d["fee_hk"] *= 100
    source("fee_int", "国际承销佣金率", "%", "Underwriting Commission (% of fund raised Int.(b)")
    d["fee_int"] *= 100
    add("sale_share", "旧股出售/初始全球发售", "%", 100 * ratio(d["Sale Shares"], d["Global Offering (without option)"]))
    add("initial_public", "初始公开发售/初始全球发售", "%", 100 * ratio(d["Public Offer shares"], d["Global Offering (without option)"]))
    add("final_public", "最终公开发售/最终基础发售", "%", 100 * ratio(d["Final public offer shares"], d[C["base_shares"]]))
    add("public_increase", "最终与初始公开发售份额差", "百分点", d.final_public - d.initial_public)
    add("allocation", "最终公开股数/有效申请股数", "%", 100 * ratio(d["Final public offer shares"], d["Public valid applied shares"]))
    source("subscription", "公开认购倍数（原披露口径）", "倍", C["sub"])
    source("applicants", "公开申请人数", "人次", "Public applicants")
    add("applied_bn", "有效申请股数×发行价（名义金额）", "十亿港元", d["Public valid applied shares"] * d[C["offer"]] / 1e9)
    add("application_k", "名义申请金额/申请人数", "千港元", ratio(d.applied_bn * 1e9, d.applicants) / 1e3)
    for key, label, column in [
        ("corner", "基石份额（基础发售）", C["corner"]),
        ("public_float", "公众持股占公司股本", "Public shareholding at listing (%)"),
        ("free_float", "非受限公众持股占公司股本", C["float"]),
        ("institutional", "Pre-IPO机构持股", "Pre-IPO institutional shareholding (%)"),
        ("controller_econ", "控制人经济权益", "Controller economic interest at listing (%)"),
        ("controller_vote", "控制人投票权益", "Controller voting rights at listing (%)"),
        ("customers", "前五大客户收入占比", "Top 5 customers (% of year-1 revenue)"),
        ("repayment", "计划净募资用于偿债", "Debt repayment (% of planned net IPO proceeds)"),
    ]:
        add(key, label, "%", 100 * d[column].where(d[column].between(0, 1)))
    same_base = np.isclose(d["Share base used for both public shareholding ratios"],
                           d["Free float denominator shares"], equal_nan=False)
    add("locked_gap", "公众持股与非受限公众持股差（同股本分母）", "百分点",
        (d.public_float - d.free_float).where(same_base))
    add("voting_wedge", "投票权益减经济权益", "百分点", d.controller_vote - d.controller_econ)
    source("holding", "Pre-IPO持有期", "年", "Pre-IPO holding duration (years)")
    for key, label, col in [
        ("vcpe", "VC/PE-backed背景", C["vc"]),
        ("vc", "有VC背景", "Pre-IPO VC backing (1=yes; 0=no)"),
        ("pe", "有PE背景", "Pre-IPO PE backing (1=yes; 0=no)"),
        ("cvc", "有CVC背景", "Pre-IPO CVC backing (1=yes; 0=no)"),
        ("state", "有国家/政府Pre-IPO背景", "Pre-IPO State/Gov backing (1=yes; 0=no)"),
        ("top_vc", "有顶级VC/PE背景（现行分类）", "Top-tier VC/PE backing (1=yes; 0=no)"),
        ("ah", "独立A+H标记", "ah_true"), ("wvr", "WVR标记", C["wvr"]),
    ]:
        add(key, label, "0/1", d[col].where(d[col].isin([0, 1])))
    source("loss", "最近一期亏损", "0/1", "loss_y1")
    add("negative_ocf", "最近一期经营现金流为负", "0/1", flag(d["Operating cash flow in year-1 (before annualization)"], lambda s: s < 0))
    add("negative_equity", "最近期权益为负", "0/1", flag(d["total equity in year-1"], lambda s: s < 0))
    original_sales = d["Year-1 net sales (original, pre-annualization)"]
    original_profit = d["Year-1 profit for period (original)"]
    for key, label, a, b in [
        ("leverage", "负债/资产", d["total liability in year-1"], d["total assets in year-1"]),
        ("cash_assets", "现金/资产", d["Cash and cash equivalents at year-1 end"], d["total assets in year-1"]),
        ("debt_assets", "有息债/资产", d["Interest-bearing debt at year-1 end"], d["total assets in year-1"]),
        ("net_margin", "净利润率（同一期未年化原值）", original_profit, original_sales),
        ("ocf_margin", "经营现金流/收入（同一期原值）", d["Operating cash flow in year-1 (before annualization)"], original_sales),
        ("rd_sales", "费用化研发/收入（同一期原值）", d["R&D expensed in year-1 (before annualization)"], original_sales),
        ("capdev_sales", "资本化研发新增/收入（同一期原值）", d["Development costs capitalized in year-1 (additions, before annualization)"], original_sales),
    ]:
        add(key, label, "%", 100 * ratio(a, b))
    add("sales_growth", "现行年化营收同比增长", "%", 100 * (ratio(d["Net sales in year-1"], d["Net sales in year-2"]) - 1))
    add("roa", "年化净利润/期末资产", "%", 100 * ratio(d["Profit for the year in year-1"], d["total assets in year-1"]))
    add("fixed", "定价分类为固定价", "0/1", flag(d[C["pricing"]], lambda s: s == "Fixed price"))
    ranged = d[C["pricing"]].ne("Fixed price") & d[C["pricing"]].notna()
    valid_range = ranged & (d["Maximum Offer Price"] > d["Minimum Offer Price"])
    mid = (d["Maximum Offer Price"] + d["Minimum Offer Price"]) / 2
    add("revision", "区间发行价相对中点调整", "%", (100 * (ratio(d[C["offer"]], mid) - 1)).where(valid_range))
    add("range_width", "招股区间宽度/中点", "%", (100 * ratio(d["Maximum Offer Price"] - d["Minimum Offer Price"], mid)).where(valid_range))
    add("range_position", "发行价格区间位置", "%", (100 * ratio(d[C["offer"]] - d["Minimum Offer Price"], d["Maximum Offer Price"] - d["Minimum Offer Price"])).where(valid_range))
    for key, label, start, end in [
        ("offer_days", "申购开日至截止日", "Subscription opening date", "Subscription closing date"),
        ("close_listing", "申购截止日至上市", "Subscription closing date", C["list_date"]),
        ("prospectus_listing", "招股书日至上市", "Date of Prospectus (dd/mm/yy)", C["list_date"]),
        ("pricing_listing", "定价日至上市", "Pricing date", C["list_date"]),
        ("allot_listing", "配发公告日至上市", "Allotment announcement date", C["list_date"]),
    ]:
        delta = (pd.to_datetime(d[end], errors="coerce") - pd.to_datetime(d[start], errors="coerce")).dt.days
        add(key, label, "日历日", delta.where(delta >= 0))
    add("fiscal_months", "最近期财务时长（记录年化因子×12）", "月", 12 * d["Comments / Annualization factor"])
    sponsors = normalized_text(d["Sponsor(s)"])
    d["sponsor_tokens"] = sponsors.map(lambda s: list(dict.fromkeys(p.strip() for p in str(s).split("/") if p.strip())) if pd.notna(s) else None)
    add("sponsor_n", "Sponsor(s)解析参与机构数", "家", d.sponsor_tokens.map(lambda s: len(s) if s is not None else np.nan))
    d["size_group"] = pd.cut(d.base_bn, [0, 1, 5, 10, np.inf], labels=["Below HKD1bn", "HKD1–5bn", "HKD5–10bn", "HKD10bn or more"], right=False)
    d["backing_group"] = d.vcpe.map({1: "VC/PE-backed", 0: "Not VC/PE-backed"}).fillna("Unknown")
    d["corner_group"] = pd.cut(d.corner, [-0.001, 0.001, 25, 50, 100], labels=["No cornerstones", "Cornerstone below25%", "Cornerstone25–50%", "Cornerstone50% or more"], right=False)
    english_labels = {'age': 'Firm age at listing', 'base_bn': 'Base offering proceeds', 'reported_bn': 'Recorded HK plus international proceeds (mixed overallotment scope)', 'offer_price': 'Offer price', 'net_bn': 'Issuer net proceeds (as disclosed)', 'expense_m': 'Listing expenses (as disclosed)', 'expense_share': 'Listing expenses/base offering proceeds', 'fee_hk': 'Disclosed HK underwriting commission', 'fee_int': 'Disclosed international underwriting commission', 'sale_share': 'Sale shares/initial global offer', 'initial_public': 'Initial retail share of initial offer', 'final_public': 'Final retail share of final base offer', 'public_increase': 'Final minus initial retail share', 'allocation': 'Final retail shares/valid applied shares', 'subscription': 'Reported retail subscription multiple', 'applicants': 'Public applicants', 'applied_bn': 'Nominal valid application value', 'application_k': 'Nominal application value per applicant', 'corner': 'Cornerstone share of base offer', 'public_float': 'Public ownership at listing', 'free_float': 'Unrestricted public ownership at listing', 'institutional': 'Pre-IPO institutional ownership', 'controller_econ': 'Controller economic interest', 'controller_vote': 'Controller voting interest', 'customers': 'Top-five customer revenue share', 'repayment': 'Planned debt repayment share of net proceeds', 'locked_gap': 'Public minus unrestricted public ownership (matched denominator)', 'voting_wedge': 'Voting minus economic interest', 'holding': 'Pre-IPO holding duration', 'vcpe': 'VC/PE-backed', 'vc': 'VC-backed', 'pe': 'PE-backed', 'cvc': 'CVC-backed', 'state': 'State/government pre-IPO backing', 'top_vc': 'Top-tier VC/PE backing (current classification)', 'ah': 'Independent A+H flag', 'wvr': 'WVR flag', 'loss': 'Loss-making in latest period', 'negative_ocf': 'Negative latest-period operating cash flow', 'negative_equity': 'Negative latest-period equity', 'leverage': 'Liabilities/assets', 'cash_assets': 'Cash/assets', 'debt_assets': 'Interest-bearing debt/assets', 'net_margin': 'Net profit margin (same-period originals)', 'ocf_margin': 'Operating cash flow/revenue (same-period originals)', 'rd_sales': 'Expensed R&D/revenue (same-period originals)', 'capdev_sales': 'Capitalized development additions/revenue (same-period originals)', 'sales_growth': 'Revenue growth using current annualization convention', 'roa': 'Annualized net profit/closing assets', 'fixed': 'Fixed-price classification', 'revision': 'Range offer-price revision versus midpoint', 'range_width': 'Filing range width/midpoint', 'range_position': 'Offer-price position in range', 'offer_days': 'Subscription opening to close', 'close_listing': 'Subscription close to listing', 'prospectus_listing': 'Prospectus to listing', 'pricing_listing': 'Pricing to listing', 'allot_listing': 'Allotment announcement to listing', 'fiscal_months': 'Latest financial-period length (annualization factor×12)', 'sponsor_n': 'Sponsor participants parsed from Sponsor(s)'}
    english_units = {'年': 'Years', '十亿港元': 'HKD billion', '港元': 'HKD', '百万港元': 'HKD million', '倍': 'Times', '人次': 'Applications', '千港元': 'HKD thousand', '百分点': 'Percentage points', '日历日': 'Calendar days', '月': 'Months', '家': 'Institutions'}
    metrics = {k: (english_labels[k], english_units.get(v[1], v[1])) for k, v in metrics.items()}
    return d, metrics


def summary(s: pd.Series) -> dict:
    s = pd.to_numeric(s, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return {"Valid N": len(s), "Mean": s.mean(), "SD": s.std(), "Min": s.min(),
            "P10": s.quantile(.1), "P25": s.quantile(.25), "Median": s.median(),
            "P75": s.quantile(.75), "P90": s.quantile(.9), "Max": s.max()}


def table(frame: pd.DataFrame) -> str:
    """Render Markdown without an optional tabulate dependency."""
    def render(x):
        if pd.isna(x):
            return "—"
        if isinstance(x, (float, np.floating)):
            return f"{x:,.3f}"
        return str(x).replace("|", "/").replace("\n", " ")
    lines = ["| " + " | ".join(map(str, frame.columns)) + " |",
             "| " + " | ".join(["---"] * len(frame.columns)) + " |"]
    lines += ["| " + " | ".join(render(v) for v in row) + " |" for row in frame.itertuples(index=False, name=None)]
    return "\n".join(lines)


def group_table(d: pd.DataFrame, col: str) -> pd.DataFrame:
    rows = []
    for name, g in d.groupby(col, observed=True, dropna=False):
        row = {"Group": str(name), "Issuer N": len(g), "Base proceeds (HKD bn)": g.base_bn.sum(min_count=1),
               "Proceeds share (%)": 100 * g.base_bn.sum() / d.base_bn.sum()}
        for key in ["base_bn", "age", "subscription", "applicants", "corner", "free_float", "allocation", "fee_hk",
                    "expense_share", "leverage", "rd_sales", "customers", "controller_econ", "institutional", "holding", "sales_growth"]:
            row[key + " median"] = g[key].median()
            row[key + " N"] = int(g[key].count())
        for key in ["loss", "negative_ocf", "vcpe", "fixed"]:
            row[key + " (%)"] = 100 * g[key].mean()
            row[key + " N"] = int(g[key].count())
        rows.append(row)
    return pd.DataFrame(rows)


def inventory(d: pd.DataFrame) -> pd.DataFrame:
    variables = yaml.safe_load((ROOT / "pipeline/registry/HKIPO_Variable_Registry.yaml").read_text())["variables"]
    rows = []
    exclusions = re.compile(r"first trading|first.day|money left|post.IPO|BHR|wealth relative|turnover|stabili|greenshoe|over.allocation|over.allotment.*(actually|exercise|date)|shares issued under over.allotment|CAR \[|unlock volume|return volatility|drawdown|zero.volume|illiquidity|cliff|volume decay|liquidity decay|^[136].(month|year).*(return|close)|current listing status", re.I)
    for v in variables:
        c = v["header"]
        if c not in d:
            continue
        s = d[c]
        status = "Excluded: trading/performance/execution" if exclusions.search(c) else "Explored: source observation"
        if c in REVIEW_FIELDS:
            status = "Coverage only: source review required"
        rows.append({"Field": c, "Type": v["dtype"], "Registry unit": v.get("unit", ""),
                     "Valid N": int(s.count()), "Missing N": int(s.isna().sum()), "Distinct observed values": s.nunique(),
                     "Treatment": status, "Note": REVIEW_FIELDS.get(c, "")})
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    d, metrics = build_frame()
    stats = pd.DataFrame([{"Metric": label, "Unit": unit, "Missing N": len(d) - d[key].count(), **summary(d[key])}
                          for key, (label, unit) in metrics.items()])
    stats.to_csv(OUT / "descriptive_statistics.csv", index=False)
    inv = inventory(d)
    inv.to_csv(OUT / "field_inventory.csv", index=False)
    raw_profiles = []
    for row in inv.itertuples(index=False, name=None):
        col, dtype, unit, _, _, _, status, _ = row
        if dtype not in {"numeric", "boolean"} or status != "Explored: source observation":
            continue
        monetary = (unit == "reporting_currency_raw" and "customers" not in col) or col.startswith("Year-1 ") or col == "Interest-bearing debt at year-1 end"
        partitions = d.groupby("currency in financial information", dropna=False) if monetary else [("All", d)]
        for currency, g in partitions:
            raw_profiles.append({"Field": col, "Currency group": currency, "Registry unit": unit,
                                 "Missing N in group": int(g[col].isna().sum()), **summary(g[col])})
    pd.DataFrame(raw_profiles).to_csv(OUT / "source_numeric_profiles.csv", index=False)
    d[["Stock Code", "Company Name at time of listing", "listing_date", "cohort", "route", "sector", *metrics]].to_csv(OUT / "issuer_facts.csv", index=False)
    report = ["# Offering and Company Facts: 113 Hong Kong IPOs through 30 September 2026",
              "This report examines offering terms, issuer fundamentals, investor backing, retail demand, allocation, fees and the issuance timetable. First-day and aftermarket returns, trading activity, stabilization execution and lockup-event performance are excluded. It describes existing master observations; original disclosures were not independently re-audited in this exercise.",
              f"The sample contains {len(d)} unique issuers listed between {d.listing_date.min():%d %B %Y} and {d.listing_date.max():%d %B %Y}. Q1/Q2/Q3 contain 38/45/30 issuers. Each statistic uses its own available observations; missing classifications are not coded as zero. Distributions are not winsorized.",
              "## 1. Main descriptive findings"]
    total = d.base_bn.sum()
    def note(text):
        report.append("- " + text)
    note(f"Base offering proceeds total HKD {total:.2f} billion. The median deal raises HKD {d.base_bn.median():.2f} billion, compared with a mean of HKD {d.base_bn.mean():.2f} billion. The largest five and ten deals account for {100*d.nlargest(5,'base_bn').base_bn.sum()/total:.1f}% and {100*d.nlargest(10,'base_bn').base_bn.sum()/total:.1f}% of proceeds.")
    for name, g in d.groupby("route"):
        note(f"{name}: {len(g)} issuers ({100*len(g)/len(d):.1f}% of the sample), {100*g.base_bn.sum()/total:.1f}% of base proceeds, and median firm age {g.age.median():.1f} years.")
    note(f"The independent A+H flag identifies {int(d.ah.sum())}/{d.ah.count()} issuers; the mutually exclusive route classification identifies {int(d.route.eq('A+H (19A)').sum())}. The classifications use different definitions.")
    for key in ["loss", "negative_ocf", "negative_equity", "vcpe", "vc", "pe", "cvc", "state", "top_vc", "fixed", "wvr"]:
        s = d[key].dropna()
        note(f"{metrics[key][0]}: {int(s.sum())}/{len(s)} ({100*s.mean():.1f}%); {len(d)-len(s)} unknown observations.")
    pair = d[["loss", "negative_ocf"]].dropna()
    note(f"Both losses and negative operating cash flow are recorded for {int(((pair.loss==1)&(pair.negative_ocf==1)).sum())}/{len(pair)} issuers. Negative operating cash flow despite non-negative profits occurs in {int(((pair.loss==0)&(pair.negative_ocf==1)).sum())}/{len(pair)}.")
    note(f"Top-five customers generate at least half of revenue for {int((d.customers>=50).sum())}/{d.customers.count()} issuers. Expensed R&D exceeds same-period revenue for {int((d.rd_sales>100).sum())}/{d.rd_sales.count()}. Median institutional ownership is {d.institutional.median():.1f}% (N={d.institutional.count()}); median pre-IPO holding duration is {d.holding.median():.2f} years (N={d.holding.count()}).")
    note(f"The median reported retail subscription multiple is {d.subscription.median():,.1f}x; {int((d.subscription>=1000).sum())}/{d.subscription.count()} deals reach 1,000x. The median number of applicants is {d.applicants.median():,.0f}. Summed applicant counts ({d.applicants.sum():,.0f}) include repeat applications across IPOs, rather than unique investors.")
    note(f"Positive cornerstone allocation occurs in {int((d.corner>0).sum())}/{d.corner.count()} IPOs. The median cornerstone share is {d.corner.median():.1f}% and the median final retail share is {d.final_public.median():.1f}% of base offer shares. These shares must not be added to public ownership measured against company capital.")
    note(f"Median public ownership is {d.public_float.median():.1f}%, compared with unrestricted public ownership of {d.free_float.median():.1f}%. Unrestricted ownership is below 10% in {int((d.free_float<10).sum())}/{d.free_float.count()} issuers. For paired observations using the same company-capital denominator, the median gap is {d.locked_gap.median():.1f} percentage points (N={d.locked_gap.count()}).")
    note(f"Final retail shares divided by valid applied shares have a median of {d.allocation.median():.4f}%; {int((d.allocation<.1).sum())}/{d.allocation.count()} are below 0.1%. This issuer-level overall allocation ratio is not the probability of obtaining one board lot.")
    note(f"The final retail tranche share exceeds its initial share in {int((d.public_increase>.01).sum())}/{d.public_increase.count()} deals and is smaller in {int((d.public_increase<-.01).sum())}, using a 0.01-percentage-point tolerance. These differences can reflect reallocation or changes in total offering size; they do not establish a particular legal trigger.")
    note(f"Existing-share sales are recorded in {int((d.sale_share>0).sum())}/{d.sale_share.count()} offerings. Positive planned debt-repayment allocations occur in {int((d.repayment>0).sum())}/{d.repayment.count()}; zeros are described as recorded values, rather than freshly verified disclosures.")
    note(f"The median disclosed Hong Kong commission is {d.fee_hk.median():.2f}% (N={d.fee_hk.count()}). Median listing expenses are HKD {d.expense_m.median():.1f} million; the median expense/base-proceeds ratio is {d.expense_share.median():.2f}% (N={d.expense_share.count()}). Listing expenses may include commissions, so these costs cannot be added without checking disclosure scope.")
    note(f"The median subscription-close-to-listing interval is {d.close_listing.median():.0f} calendar days (N={d.close_listing.count()}). Only {d.pricing_listing.count()} pricing dates are available; subscription closing dates are not substituted for them.")
    report += ["## 2. Descriptive distributions", "Percentage variables are displayed after multiplying decimal source shares by 100. Binary means are proportions among observed cases. Extreme financial ratios are retained, including cases with very small revenue denominators.", table(stats)]
    report += ["## 3. Time, Industry and Offering Structure"]
    for col, title in [("cohort", "Listing quarter"), ("month", "Listing month"), ("sector", "Industry"), ("route", "Exclusive listing route"),
                       ("size_group", "Base offering size"), ("backing_group", "VC/PE backing"),
                       (C["pricing"], "Pricing position"), ("Offer mechanism", "Recorded mechanism"), ("corner_group", "Cornerstone allocation")]:
        frame = group_table(d, col)
        filename = 'pricing' if col == C['pricing'] else 'mechanism' if col == 'Offer mechanism' else col
        frame.to_csv(OUT / f"group_{filename}.csv", index=False)
        display = frame[["Group", "Issuer N", "Base proceeds (HKD bn)", "Proceeds share (%)", "base_bn median", "subscription median", "corner median", "loss (%)", "loss N"]]
        report += [f"### {title}", "Full CSV tables report valid N for each metric. The issuer count is not the denominator for every statistic. Metric keys correspond to issuer_facts.csv and the definitions below.", table(display)]
    for left, right, title in [("sector", "cohort", "Industry by quarter"), ("route", "Offer mechanism", "Route by recorded mechanism"),
                               ("backing_group", "route", "Backing by route"), ("loss", "negative_ocf", "Losses and negative operating cash flow")]:
        frame = pd.crosstab(d[left].astype("string").fillna("Unknown"), d[right].astype("string").fillna("Unknown"), dropna=False).reset_index()
        filename = 'mechanism' if right == 'Offer mechanism' else right
        frame.to_csv(OUT / f"crosstab_{left}_{filename}.csv", index=False)
        report += [f"### {title}", table(frame)]
    ranks = d.sort_values("base_bn", ascending=False).copy()
    ranks["Cumulative proceeds share (%)"] = 100*ranks.base_bn.cumsum()/total
    rank_columns = ["Stock Code", "Company Name at time of listing", "cohort", "route", "sector", "base_bn", "Cumulative proceeds share (%)"]
    ranks[rank_columns].to_csv(OUT / "proceeds_ranking.csv", index=False)
    report += ["## 4. Proceeds Concentration", table(ranks.head(15)[rank_columns])]
    report += ["## 5. Financial Statements and Reporting Currency", "Profit, cash-flow and R&D ratios use same-currency, same-period original amounts. Revenue growth and ROA use the existing annualization convention; annualization does not remove seasonality. ROA uses closing assets. Absolute statement amounts are summarized separately by reporting currency and are not multiplied by the unit multiplier again."]
    financial = []
    for currency, g in d.groupby("currency in financial information", dropna=False):
        for c in ["total assets in year-1", "total equity in year-1", "Year-1 net sales (original, pre-annualization)",
                  "Year-1 profit for period (original)", "Operating cash flow in year-1 (before annualization)",
                  "Cash and cash equivalents at year-1 end", "R&D expensed in year-1 (before annualization)", "Capital expenditure in year-1"]:
            financial.append({"Currency": currency, "Field": c, "Unit": "Million reporting-currency units", **summary(g[c]/1e6)})
    fin = pd.DataFrame(financial)
    fin.to_csv(OUT / "financial_by_currency.csv", index=False)
    report += [table(fin[["Currency", "Field", "Valid N", "Median", "P25", "P75"]])]
    patterns = []
    for label, columns in [("Profit", ["Profit for the year in year-3", "Profit for the year in year-2", "Profit for the year in year-1"]),
                           ("Equity", ["total equity in year-3", "total equity in year-2", "total equity in year-1"])]:
        complete = d[columns].dropna()
        signatures = complete.apply(lambda row: " → ".join("Negative" if v<0 else "Non-negative" for v in row), axis=1)
        for pattern, n in signatures.value_counts().items():
            patterns.append({"Measure": label, "Year-3 to year-1": pattern, "N": n, "Three-period complete N": len(complete), "Incomplete N": len(d)-len(complete)})
    history = pd.DataFrame(patterns)
    history.to_csv(OUT / "financial_history_patterns.csv", index=False)
    report += ["### Three-period sign patterns", "Complete observations only. Non-negative includes zero and does not establish financial sustainability.", table(history)]
    thresholds = []
    for key, threshold in [("age",10),("age",20),("free_float",5),("free_float",10),("allocation",.1),
                           ("allocation",1),("holding",5),("customers",50),("expense_share",10),("controller_econ",50)]:
        s=d[key].dropna()
        thresholds.append({"Metric":metrics[key][0],"Unit":metrics[key][1],"Below threshold":threshold,
                           "Count":int((s<threshold).sum()),"Valid N":len(s),"Share (%)":100*(s<threshold).mean(),"Missing N":len(d)-len(s)})
    thresholds=pd.DataFrame(thresholds)
    thresholds.to_csv(OUT / "threshold_facts.csv",index=False)
    report += ["### Illustrative threshold counts", "Thresholds are descriptive and are not treated as regulatory cutoffs or prespecified hypotheses.",table(thresholds)]
    rankings=[]
    for key in ["base_bn","subscription","applicants","corner","age","expense_share","customers","rd_sales"]:
        for _,row in d.nlargest(10,key).iterrows():
            rankings.append({"Metric":metrics[key][0],"Unit":metrics[key][1],"Stock Code":row["Stock Code"],"Company":row["Company Name at time of listing"],"Value":row[key]})
    pd.DataFrame(rankings).to_csv(OUT / "top10_facts.csv",index=False)
    report += ["## 6. Intermediary Participation and Source Categories", "Sponsor(s) is split on slashes, whitespace is normalized, and duplicates within a deal are removed. Each co-sponsored deal counts once for each participant: counts and associated proceeds cannot be summed across firms. No lead role or merger-related name consolidation is inferred. Source-language controller and address categories are preserved verbatim in categorical_frequencies.csv."]
    sponsor_rows=[]
    for _,row in d.iterrows():
        for name in row.sponsor_tokens or []:
            sponsor_rows.append({"Institution":name,"Stock Code":row["Stock Code"],"base_bn":row.base_bn})
    sponsors=pd.DataFrame(sponsor_rows).groupby("Institution").agg(deals=("Stock Code","nunique"),associated_base_proceeds_hkd_bn=("base_bn","sum")).sort_values("deals",ascending=False).reset_index()
    sponsors.to_csv(OUT / "sponsor_participation.csv",index=False)
    report += [table(sponsors.head(15))]
    cats=[]
    for c in ["Reporting Accountants","Place of incorporation","Accounting standard","currency in financial information",
              "Share class","Ultimate controller type","Earliest Pre-IPO investment round","Principal place of business","Technology commercialization stage"]:
        counts=normalized_text(d[c]).value_counts(dropna=False)
        for value,n in counts.items():
            cats.append({"Field":c,"Verbatim source category":str(value),"N":n,"Full-sample share (%)":100*n/len(d)})
        if c in ["Reporting Accountants","Place of incorporation","currency in financial information","Share class"]:
            report += [f"### {c}",table(pd.DataFrame([{"Category":str(v),"N":n} for v,n in counts.items()]))]
    pd.DataFrame(cats).to_csv(OUT / "categorical_frequencies.csv",index=False)
    report += ["## 7. Pairwise Associations", "Pairwise Spearman correlations and valid N are reported without significance screening. Some correlations have mechanical denominator links, especially subscription versus allocation and size versus expense/proceeds."]
    keys=["base_bn","age","subscription","applicants","corner","free_float","fee_hk","expense_share","institutional","rd_sales","leverage","allocation"]
    associations=[]
    for i,a in enumerate(keys):
        for b in keys[i+1:]:
            pair=d[[a,b]].dropna()
            rho=pair[a].corr(pair[b],method="spearman") if len(pair)>=3 and pair[a].nunique()>1 and pair[b].nunique()>1 else np.nan
            associations.append({"Variable A":metrics[a][0],"Variable B":metrics[b][0],"N":len(pair),"Spearman":rho})
    assoc=pd.DataFrame(associations)
    assoc.to_csv(OUT / "spearman_pairs.csv",index=False)
    report += [table(assoc.assign(absolute=assoc.Spearman.abs()).sort_values("absolute",ascending=False).head(12).drop(columns="absolute"))]
    checks=[]
    def check(name,mask,detail):
        for _,r in d.loc[mask.fillna(False)].iterrows():
            checks.append({"Issue":name,"Stock Code":r["Stock Code"],"Note":detail})
    check("Missing segment proceeds",d.gross_proceeds.isna(),"Price × final base shares remains available; recorded HK/international proceeds cover fewer than 113 issuers")
    check("Initial share reconciliation",(d["New shares"]+d["Sale Shares"]-d["Global Offering (without option)"]).abs()>1,"New plus sale shares differ from initial global offer by more than one share")
    check("Final share reconciliation",(d["Final public offer shares"]+d["Final placing shares"]-d[C["base_shares"]]).abs()>1,"Retail plus placing shares differ from final base shares by more than one share")
    check("Allocation ratio above 100%",d.allocation>100,"Not capped; definitions require checking")
    check("Balance-sheet reconciliation",((d["total assets in year-1"]-d["total equity in year-1"]-d["total liability in year-1"]).abs()/d["total assets in year-1"].abs())>.01,"Absolute residual exceeds 1% of assets; source unchanged")
    check("Unrestricted ownership exceeds public ownership",d.locked_gap<-.01,"Matched-denominator gap below -0.01 percentage points")
    check("Fixed-price classification with unequal endpoints",d.fixed.eq(1)&d["Minimum Offer Price"].notna()&d["Minimum Offer Price"].ne(d["Maximum Offer Price"]),"Recorded classification used; excluded from range metrics")
    for start,end in [("Subscription opening date","Subscription closing date"),("Subscription closing date",C["list_date"]),("Pricing date",C["list_date"])]:
        check("Reversed dates",pd.to_datetime(d[end],errors="coerce")<pd.to_datetime(d[start],errors="coerce"),start+" > "+end)
    for c in [C["corner"],C["float"],"Public shareholding at listing (%)","Pre-IPO institutional shareholding (%)","Top 5 customers (% of year-1 revenue)","Debt repayment (% of planned net IPO proceeds)"]:
        check("Share outside [0,1]",d[c].notna()&~d[c].between(0,1),c+"; excluded from derived summary")
    issues=pd.DataFrame(checks,columns=["Issue","Stock Code","Note"])
    issues.to_csv(OUT / "consistency_flags.csv",index=False)
    report += ["## 8. Coverage and Interpretation",f"All {len(inv)} registered source fields are inventoried. Internal consistency checks identify {len(issues)} flagged observations. Neither the workbook nor the master is changed.",table(issues),
               table(pd.DataFrame([{"Field":c,"Treatment":reason,"Valid N":int(d[c].count())} for c,reason in REVIEW_FIELDS.items()])),
               "Recorded HK plus international proceeds may include overallotment or different deal-size updates, so base proceeds are calculated consistently as price × final shares before overallotment. Net proceeds, listing expenses and base proceeds can refer to different disclosed scopes: gross-minus-net is not automatically total issuance costs. Nominal application amounts are requested shares × offer price, not actual net frozen funds. Mechanism labels are descriptive; no inference about legal eligibility is made. Coverage is not proof of independently verified evidence.",
               "## 9. Definitions and Replication",table(pd.DataFrame([{"Key":k,"Metric":v[0],"Unit":v[1]} for k,v in metrics.items()])),
               "Run `python3 analysis/offer_facts_2026.py` or `make offer-facts`. Output includes descriptive_statistics.csv, issuer_facts.csv, group_*.csv, field_inventory.csv, source_numeric_profiles.csv, financial_by_currency.csv, financial_history_patterns.csv, threshold_facts.csv, top10_facts.csv, sponsor_participation.csv, categorical_frequencies.csv, proceeds_ranking.csv, spearman_pairs.csv and consistency_flags.csv. Source profiles retain stored units; currency amounts are separated. run_manifest.json records input hashes and sample scope.",
               "![Offering structure](fig_offer_structure.png)"]
    (OUT / "facts.md").write_text("\n\n".join(report)+"\n",encoding="utf-8")
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    monthly=d.groupby(d.listing_date.dt.strftime("%m")).agg(n=("base_bn","size"),proceeds=("base_bn","sum"))
    axes[0,0].bar(monthly.index,monthly.n,color="#2a78d6")
    axes[0,0].set(title="IPO counts by listing month",ylabel="Issuers",xlabel="2026 month")
    axes[0,1].bar(monthly.index,monthly.proceeds,color="#eb6834")
    axes[0,1].set(title="Base offering proceeds by month",ylabel="HKD billion",xlabel="2026 month")
    ranked=d.base_bn.sort_values(ascending=False).to_numpy()
    axes[1,0].plot(np.arange(1,len(d)+1),100*np.cumsum(ranked)/total,color="#2a78d6")
    axes[1,0].set(title="Concentration: largest offerings first",xlabel="Number of largest offerings",ylabel="Cumulative proceeds (%)")
    route=d.groupby("route").base_bn.agg(["size","sum"])
    route.index=["18A" if "18A" in s else "18C" if "18C" in s else "A+H" if "A+H" in s else s for s in route.index]
    pos=np.arange(len(route))
    axes[1,1].bar(pos-.18,100*route["size"]/len(d),.36,label="Issuer share",color="#2a78d6")
    axes[1,1].bar(pos+.18,100*route["sum"]/total,.36,label="Proceeds share",color="#eb6834")
    axes[1,1].set(xticks=pos,xticklabels=route.index,title="Listing routes: counts vs capital",ylabel="Percent")
    axes[1,1].legend()
    for ax in axes.flat:
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y",alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle("2026 HK IPO offering facts | 113 issuers | through 30 September",fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT / "fig_offer_structure.png",dpi=180)
    plt.close(fig)
    manifest={"cutoff":str(CUTOFF.date()),"n":len(d),"cohorts":d.cohort.value_counts().sort_index().to_dict(),
              "input":str(MASTER.relative_to(ROOT)),"sha256":hashlib.sha256(MASTER.read_bytes()).hexdigest(),
              "registry_sha256":hashlib.sha256((ROOT / "pipeline/registry/HKIPO_Variable_Registry.yaml").read_bytes()).hexdigest(),
              "source_semantic_audit":"not performed; existing export observations","numeric_metrics":len(metrics),
              "fields_inventoried":len(inv),"consistency_flag_rows":len(issues),"report_language":"English"}
    (OUT / "run_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(manifest,indent=2))


if __name__ == "__main__":
    main()
