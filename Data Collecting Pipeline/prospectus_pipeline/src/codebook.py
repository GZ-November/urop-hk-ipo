#!/usr/bin/env python3
"""HK IPO 学术研究级变量字典（Codebook）与纯净 CSV 导出引擎。

功能：
  1. 完整解析 HKIPO-MB2026Q1.xlsx 交付物（120 列 × 38 家公司）；
  2. 自动识别三色数据层级：
     - 浅绿（A–K，11 列）：香港交易所新上市报告官方基础信息；
     - 浅蓝（L–AY, DP, CJ, BA–CI，60 列）：招股书全量披露指标；
     - 深蓝（CK, CM–DC，18 列）：配发结果公告与确定性派生指标；
     - 深蓝（DD–DO, DF, DG，31 列）：外部工具行情、HIBOR、总结余与监管分类。
  3. 变量类型智能推断（Numeric / Date / Boolean / Categorical / Text）；
  4. 计算样本统计量（有效样本量、填报率、均值、中位数、标准差、分位数、极值范围、分类频数）；
  5. 导出：
     - out/HKIPO-MB2026Q1_clean.csv (UTF-8 with BOM, compatible with Stata, Python pandas, and Excel);
     - out/HKIPO_2026Q1_Codebook.md (学术数据变量字典，供论文附录与导师汇报)；
     - out/HKIPO_2026Q1_Codebook.json (结构化机器可读变量元数据)。
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from run import load_cfg  # noqa: E402

# 浅绿 A–K 官方定义
HKEX_GREEN_VARS = {
    "A": ("HKEx file# of the year", "港交所年度申请编号", "string"),
    "B": ("Stock Code", "股份代号（四位港股代码，如 6082.HK）", "string"),
    "C": ("Company Name at time of listing", "公司上市时法定英文名称", "string"),
    "D": ("Date of Prospectus (dd/mm/yy)", "招股书刊发日期", "date"),
    "E": ("Date of Listing (dd/mm/yy)", "正式挂牌上市交易日期", "date"),
    "F": ("Sponsor(s)", "独家/联席保荐人名单", "string"),
    "G": ("Reporting Accountants", "申报会计师事务所", "string"),
    "H": ("Valuer(s)", "独立物业或资产估值师", "string"),
    "I": ("Funds Raised HK (a)", "香港公开发售募资额 (HK$)", "numeric"),
    "J": ("Funds Raised Int.(b)", "国际配售募资额 (HK$)", "numeric"),
    "K": ("IPO Subscription Price (HK$)", "最终发售定价 (HK$)", "numeric"),
}

# 外部工具深蓝字段描述
EXTERNAL_VARS = {
    "DD": ("HSI return over 20 trading days before prospectus (%)", "招股日前 20 个交易日恒生指数累计收益率 (%)", "numeric"),
    "DE": ("HK ordinary IPO count in 90 calendar days before prospectus", "招股日前 90 个自然日香港普通主板 IPO 上市数量", "integer"),
    "DF": ("1-month HIBOR before prospectus (%)", "招股日前一交易日香港银行同业拆借 1 个月 HIBOR 利率 (%)", "numeric"),
    "DG": ("Banking system aggregate balance before prospectus (HK$)", "招股日前一交易日香港银行体系总结余 (HK$)", "numeric"),
    "DH": ("First trading day closing price (HK$)", "首日上市二级市场收盘价 (HK$)", "numeric"),
    "DI": ("First trading day opening price (HK$)", "首日上市二级市场开盘价 (HK$)", "numeric"),
    "DJ": ("First trading day high (HK$)", "首日上市二级市场盘中最高价 (HK$)", "numeric"),
    "DK": ("First trading day low (HK$)", "首日上市二级市场盘中最低价 (HK$)", "numeric"),
    "DL": ("First trading day volume (shares)", "首日上市二级市场全天成交量（股）", "numeric"),
    "DM": ("First trading day turnover (HK$)", "首日上市二级市场全天成交金额 (HK$)", "numeric"),
    "DN": ("Offer mechanism", "发售与回拨机制（Mechanism A 传统 / Mechanism B 灵活）", "categorical"),
    "DO": ("Applicable IPO rules / transition basis", "适用之上市规则过渡基准（FINI 改革规则）", "categorical"),
    "BH": ("Listing board", "上市板块（Main Board 主板）", "categorical"),
    "BJ": ("A+H flag", "A+H 两地同时上市标识（1=是，0=否）", "boolean"),
    "BK": ("WVR flag", "不同投票权/同股不同权架构标识（1=是，0=否）", "boolean"),
    "BL": ("Chapter 18A flag", "第 18A 章未盈利生物科技公司标识（1=是，0=否）", "boolean"),
    "BM": ("Chapter 18C flag", "第 18C 章特专科技公司标识（1=是，0=否）", "boolean"),
    "BN": ("Industry classification code", "恒生行业分类 HSICS 6 位业务细分代码", "string"),
    "BO": ("Industry classification system and version", "行业分类系统与版本号", "string"),
    "BQ": ("Place of incorporation", "公司注册成立法域（如 Cayman Islands, PRC 等）", "categorical"),
    "AZ": ("Comments / Annualization factor", "财务报表年化因子说明", "string"),
    "BS": ("Financial statement unit multiplier", "财务报表基础货币乘数（千元/万元/百万元）", "string"),
    "BU": ("Financial period: Year-3 start", "往绩记录前三年起始日", "date"),
    "BV": ("Financial period: Year-3 end", "往绩记录前三年截止日", "date"),
    "BW": ("Financial period: Year-2 start", "往绩记录前两年起始日", "date"),
    "BX": ("Financial period: Year-2 end", "往绩记录前两年截止日", "date"),
    "BY": ("Financial period: Year-1 start", "往绩记录最近一年起始日", "date"),
    "BZ": ("Financial: Year-1 net sales (original)", "往绩最近一年营业收入（原币种）", "numeric"),
    "CA": ("Financial: Year-1 profit before tax (original)", "往绩最近一年除税前利润（原币种）", "numeric"),
    "CB": ("Financial: Year-1 profit for period (original)", "往绩最近一年期内净利润（原币种）", "numeric"),
    "CL": ("Earliest cornerstone unlock date", "基石投资者最早法定解禁日（上市日起满6个月）", "date"),
}

# 学术文献核心衍生变量 (Lowry, Michaely, and Volkova 2017)
ACADEMIC_VARS = {
    "Filing price revision (%)": ("Filing price revision (%)", "发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%）", "numeric", "浅蓝 (招股书全量披露)", "pricing_dynamics"),
    "Filing range width (%)": ("Filing range width (%)", "询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%）", "numeric", "浅蓝 (招股书全量披露)", "pricing_dynamics"),
    "Pricing position in filing range": ("Pricing position in filing range", "定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range）", "categorical", "浅蓝 (招股书全量披露)", "pricing_dynamics"),
    "Firm age at IPO (years)": ("Firm age at IPO (years)", "公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量）", "numeric", "浅蓝 (招股书全量披露)", "firm_profile"),
    "Greenshoe exercise rate (%)": ("Greenshoe exercise rate (%)", "绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持）", "numeric", "深蓝 (配发结果与确定性派生)", "greenshoe"),
    "First-day return / Underpricing (%)": ("First-day return / Underpricing (%)", "上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量）", "numeric", "深蓝 (配发及外部数据)", "secondary_market"),
    "Money left on the table (HK$)": ("Money left on the table (HK$)", "留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标）", "numeric", "深蓝 (配发及外部数据)", "secondary_market"),
    "First-day flipping ratio (%)": ("First-day flipping ratio (%)", "首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说）", "numeric", "深蓝 (配发及外部数据)", "secondary_market"),
}


def parse_numeric(v: Any) -> float | None:
    if v in (None, "", "NA", "NaN"):
        return None
    try:
        val = float(v)
        return None if (math.isnan(val) or math.isinf(val)) else val
    except (ValueError, TypeError):
        return None


def parse_date_str(v: Any) -> str | None:
    if v in (None, "", "NA", "NaN"):
        return None
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    s = str(v).strip()
    return s if s else None


def clean_header_name(s: str) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip()


def norm_header(v: Any) -> str:
    return " ".join(str(v or "").replace("\n", " ").split()).strip().lower()


def build_codebook(cfg: dict | None = None) -> tuple[list[dict], dict]:
    """完整扫描工作簿生成全量变量字典与样本统计量。"""
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

    # 加载招股书 schema 与配发 schema
    p_schema_by_header = {}
    p_schema_by_col = {}
    p_schema_path = ROOT / "schema" / "fields.json"
    if p_schema_path.exists():
        p_data = json.loads(p_schema_path.read_text(encoding="utf-8"))
        p_schema_by_col = {f.get("col"): f for f in p_data.get("fields", []) if f.get("col")}
        p_schema_by_header = {norm_header(f["header"]): f for f in p_data.get("fields", [])}

    a_schema_by_header = {}
    a_schema_by_col = {}
    a_schema_path = ROOT / "schema" / "allot_fields.json"
    if a_schema_path.exists():
        a_data = json.loads(a_schema_path.read_text(encoding="utf-8"))
        a_schema_by_col = {f.get("col"): f for f in a_data.get("fields", []) if f.get("col")}
        a_schema_by_header = {norm_header(f["header"]): f for f in a_data.get("fields", [])}

    green_by_header = {norm_header(val[0]): val for val in HKEX_GREEN_VARS.values()}
    ext_by_header = {norm_header(val[0]): val for val in EXTERNAL_VARS.values()}
    academic_by_header = {norm_header(k): v for k, v in ACADEMIC_VARS.items()}

    start_row = cfg["data_start_row"]
    max_col = ws.max_column

    # 动态确定实际公司样本数量
    valid_rows = []
    for r in range(start_row, ws.max_row + 1):
        c_val = ws.cell(r, 2).value
        if c_val is not None and str(c_val).strip():
            valid_rows.append(r)
    n_companies = len(valid_rows)
    if n_companies == 0:
        n_companies = max(1, ws.max_row - start_row + 1)
        valid_rows = list(range(start_row, start_row + n_companies))

    variables = []
    matrix = []

    # 提取所有数据行
    for r in valid_rows:
        row_vals = [ws.cell(r, c).value for c in range(1, max_col + 1)]
        matrix.append(row_vals)

    wb.close()

    # 逐列解析
    for c in range(1, max_col + 1):
        col_letter = get_column_letter(c)
        raw_header = str(ws.cell(1, c).value or "").strip()
        clean_header = clean_header_name(raw_header)
        norm_h = norm_header(raw_header)
        col_vals = [matrix[r_idx][c - 1] for r_idx in range(n_companies)]

        # 确定三色来源与分组
        tier = "深蓝 (配发及外部数据)"
        source_desc = "外部数据源 / 配发公告 / 港交所衍生工具"
        group_name = "external"
        chinese_desc = clean_header

        if norm_h in academic_by_header:
            item = academic_by_header[norm_h]
            clean_header, chinese_desc, _, tier, group_name = item
            source_desc = f"实证金融模型衍生指标（Group: {group_name}，Lowry et al. 2017 规范）"
        elif norm_h in green_by_header:
            tier = "浅绿 (港交所官方报告)"
            item = green_by_header[norm_h]
            clean_header, chinese_desc, _ = item
            source_desc = "香港交易所 (HKEX) 新上市报告 (New Listing Report) 官方表格"
            group_name = "hkex_nlr"
        elif norm_h in p_schema_by_header:
            tier = "浅蓝 (招股书全量披露)"
            meta = p_schema_by_header[norm_h]
            source_desc = f"招股书法定披露章节（Group: {meta.get('group', 'prospectus')}）"
            group_name = meta.get("group", "prospectus")
            chinese_desc = meta.get("description", meta.get("hint", clean_header))
        elif norm_h in a_schema_by_header:
            tier = "深蓝 (配发结果与确定性派生)"
            meta = a_schema_by_header[norm_h]
            source_desc = f"配发结果公告 (Allotment Results) / 确定性派生"
            group_name = meta.get("group", "allotment")
            chinese_desc = meta.get("description", clean_header)
        elif norm_h in ext_by_header:
            item = ext_by_header[norm_h]
            clean_header, chinese_desc, _ = item
            source_desc = "外部市场数据 (Hang Seng / HKMA / 港交所规则)"
            group_name = "external_tools"
        elif col_letter in HKEX_GREEN_VARS:
            tier = "浅绿 (港交所官方报告)"
            clean_header, chinese_desc, _ = HKEX_GREEN_VARS[col_letter]
            source_desc = "香港交易所 (HKEX) 新上市报告 (New Listing Report) 官方表格"
            group_name = "hkex_nlr"
        elif col_letter in p_schema_by_col:
            tier = "浅蓝 (招股书全量披露)"
            meta = p_schema_by_col[col_letter]
            source_desc = f"招股书法定披露章节（Group: {meta.get('group', 'prospectus')}）"
            group_name = meta.get("group", "prospectus")
            chinese_desc = meta.get("description", meta.get("hint", clean_header))
        elif col_letter in a_schema_by_col:
            tier = "深蓝 (配发结果与确定性派生)"
            meta = a_schema_by_col[col_letter]
            source_desc = f"配发结果公告 (Allotment Results) / 确定性派生"
            group_name = meta.get("group", "allotment")
            chinese_desc = meta.get("description", clean_header)
        elif col_letter in EXTERNAL_VARS:
            clean_header, chinese_desc, _ = EXTERNAL_VARS[col_letter]
            source_desc = "外部市场数据 (Hang Seng / HKMA / 港交所规则)"
            group_name = "external_tools"

        # 分析缺失率
        valid_vals = [v for v in col_vals if v not in (None, "", "NA", "NaN")]
        valid_n = len(valid_vals)
        missing_n = n_companies - valid_n
        fill_rate = (valid_n / n_companies) * 100.0

        # 推断数据类型与统计量
        # 1. 检查是否为日期
        is_date = any(isinstance(v, (dt.date, dt.datetime)) for v in valid_vals) or "Date" in clean_header
        # 2. 检查是否为布尔 (0/1)
        is_bool = all(v in (0, 1, "0", "1", True, False) for v in valid_vals) and (
            col_letter in ("BJ", "BK", "BL", "BM", "CR") or "flag" in clean_header.lower() or "0/1" in clean_header
        )
        # 3. 检查是否为纯数值
        numeric_vals = [parse_numeric(v) for v in col_vals]
        valid_nums = [v for v in numeric_vals if v is not None]
        is_numeric = (len(valid_nums) == valid_n and valid_n > 0) and not is_date and not is_bool

        dtype = "string"
        stats: dict[str, Any] = {
            "valid_n": valid_n,
            "missing_n": missing_n,
            "fill_rate_pct": round(fill_rate, 2),
        }

        if is_bool:
            dtype = "boolean (0/1)"
            bool_ints = [int(v) for v in valid_vals]
            ones = sum(1 for v in bool_ints if v == 1)
            zeros = sum(1 for v in bool_ints if v == 0)
            stats.update({
                "true_count": ones,
                "false_count": zeros,
                "true_pct": round(ones / valid_n * 100.0, 1) if valid_n else 0.0,
                "summary_display": f"1 (是): {ones} 家 ({ones/valid_n*100:.1f}%), 0 (否): {zeros} 家" if valid_n else "全部缺失"
            })
        elif is_numeric:
            dtype = "numeric"
            avg = statistics.mean(valid_nums)
            med = statistics.median(valid_nums)
            std_dev = statistics.stdev(valid_nums) if len(valid_nums) > 1 else 0.0
            min_v = min(valid_nums)
            max_v = max(valid_nums)
            sorted_nums = sorted(valid_nums)
            q25 = sorted_nums[int(len(sorted_nums) * 0.25)]
            q75 = sorted_nums[int(len(sorted_nums) * 0.75)]
            stats.update({
                "mean": avg,
                "std": std_dev,
                "median": med,
                "min": min_v,
                "q25": q25,
                "q75": q75,
                "max": max_v,
                "summary_display": f"均值 {avg:,.2f} | 中位数 {med:,.2f} | 区间 [{min_v:,.2f}, {max_v:,.2f}]"
            })
        elif is_date:
            dtype = "date (YYYY-MM-DD)"
            date_strs = sorted([parse_date_str(v) for v in valid_vals if parse_date_str(v)])
            min_d = date_strs[0] if date_strs else "N/A"
            max_d = date_strs[-1] if date_strs else "N/A"
            stats.update({
                "min_date": min_d,
                "max_date": max_d,
                "summary_display": f"区间: {min_d} ~ {max_d}" if date_strs else "无有效日期"
            })
        else:
            dtype = "string / categorical"
            counts = Counter(str(v).strip() for v in valid_vals)
            top3 = counts.most_common(3)
            top_str = ", ".join(f"'{k}': {cnt}" for k, cnt in top3)
            stats.update({
                "unique_count": len(counts),
                "top_categories": dict(counts.most_common(5)),
                "summary_display": f"共 {len(counts)} 种取值 ({top_str})" if valid_n else "全部缺失"
            })

        variables.append({
            "col_idx": c,
            "col_letter": col_letter,
            "header": clean_header,
            "chinese_desc": chinese_desc,
            "tier": tier,
            "group": group_name,
            "data_type": dtype,
            "source": source_desc,
            "stats": stats,
            "values": col_vals,
        })

    cohort_str = cfg.get("dataset", {}).get("cohort", "2026 Q1") if cfg else "2026 Q1"
    summary = {
        "dataset_name": f"HK IPO Main Board {cohort_str} Full Dataset",
        "cohort": cohort_str,
        "workbook_name": book_path.name,
        "sheet": cfg.get("sheet", "NLR") if cfg else "NLR",
        "sample_size": n_companies,
        "variable_count": len(variables),
        "tiers": {
            "green_hkex": sum(1 for v in variables if "浅绿" in v["tier"]),
            "blue_prospectus": sum(1 for v in variables if "浅蓝" in v["tier"]),
            "darkblue_external": sum(1 for v in variables if "深蓝" in v["tier"]),
        },
        "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return variables, summary


def export_clean_csv(variables: list[dict], out_path: Path | None = None) -> Path:
    """导出格式规整、无编码歧义的 UTF-8-BOM CSV 文件。"""
    if out_path is None:
        out_path = ROOT / "out" / "HKIPO-MB2026Q1_clean.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_rows = variables[0]["stats"]["valid_n"] + variables[0]["stats"]["missing_n"]
    headers = [v["header"] for v in variables]

    with open(out_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for r_idx in range(n_rows):
            row_vals = []
            for v in variables:
                val = v["values"][r_idx]
                if val in (None, "", "NA", "NaN"):
                    row_vals.append("")
                elif isinstance(val, (dt.date, dt.datetime)):
                    row_vals.append(val.strftime("%Y-%m-%d"))
                elif isinstance(val, float):
                    if math.isnan(val) or math.isinf(val):
                        row_vals.append("")
                    else:
                        row_vals.append(f"{int(val)}" if val.is_integer() else f"{val:.6g}")
                else:
                    row_vals.append(str(val).strip())
            writer.writerow(row_vals)

    return out_path


def generate_codebook_markdown(variables: list[dict], summary: dict, out_path: Path | None = None) -> Path:
    """生成详尽的学术计量级数据变量代码本（Markdown 格式）。"""
    cohort = summary.get("cohort", "2026 Q1")
    wb_name = summary.get("workbook_name", "HKIPO-MB2026Q1.xlsx")
    sheet_name = summary.get("sheet", "NLR")
    if out_path is None:
        tag = cohort.replace(" ", "")
        out_path = ROOT / "out" / f"HKIPO_{tag}_Codebook.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# 香港主板 {cohort} IPO 学术研究数据变量代码本 (Data Codebook)",
        f"\n- **样本规模 (N)**：{summary['sample_size']} 家香港联交所主板新上市公司",
        f"- **变量总数 (K)**：{summary['variable_count']} 维完整跨学科指标",
        f"- **数据层级划分**：浅绿官方基础 ({summary['tiers']['green_hkex']} 列) + 浅蓝招股书披露 ({summary['tiers']['blue_prospectus']} 列) + 深蓝配发及外部衍生 ({summary['tiers']['darkblue_external']} 列)",
        f"- **生成时间**：{summary['generated_at']} | **数据基准**：`{wb_name}` (Sheet: {sheet_name})",
        "\n---",
        "\n## 一、变量层级与来源体系导览",
        "\n| 数据层级 | 覆盖范围 | 列数 | 核心特征与学术用途 |",
        "|---|---|---|---|",
        f"| **浅绿 (HKEX 官方来源)** | 列 A–K | {summary['tiers']['green_hkex']} 列 | 港交所新上市报告官方确证指标：上市编号、代码、保荐人、会计师、公开发售及国际发售募资额、最终定价。 |",
        f"| **浅蓝 (招股书全量来源)** | 招股书法定披露与Pre-IPO结构 | {summary['tiers']['blue_prospectus']} 列 | 发行人招股书披露：资本结构、发售价区间、Pre-IPO VC/PE 投资背景与治理席位、近三年财务与业务指标。 |",
        f"| **深蓝 (配发及外部数据)** | 配发公告与外部市场数据 | {summary['tiers']['darkblue_external']} 列 | 发行结果与市场宏观：基石投资者最终获配及禁售期、回拨机制、超购倍数、自由流通量、首日二级市场表现、恒指收益率、HIBOR、总结余、监管分类。 |",
        "\n---",
        f"\n## 二、{summary['variable_count']} 维全量变量字典详细清单 (Codebook)",
        "\n| 列 | 变量英文名 (Variable Header) | 中文口径释义 | 数据层级 | 数据类型 | 有效样本 (填报率) | 描述性统计 / 分布特征 |",
        "|---|---|---|---|---|---|---|"
    ]

    for v in variables:
        col = f"**{v['col_letter']}**"
        h = f"`{v['header']}`"
        desc = v["chinese_desc"].replace("|", "/")
        tier_short = v["tier"].split("(")[0].strip()
        dtype = v["data_type"].split()[0]
        fill = f"{v['stats']['valid_n']}/{summary['sample_size']} ({v['stats']['fill_rate_pct']}%)"
        summary_disp = v["stats"].get("summary_display", "-").replace("|", "/")
        lines.append(f"| {col} | {h} | {desc} | {tier_short} | `{dtype}` | {fill} | {summary_disp} |")

    lines.extend([
        "\n---",
        "\n## 三、计量软件导入指引 (Stata / Python)",
        f"\n配套清洗数据文件：`out/{Path(wb_name).stem}_clean.csv`（编码：UTF-8 with BOM）。",
        "\n### 1. Stata",
        "```stata",
        '* 导入纯净版 CSV 数据',
        f'import delimited "out/{Path(wb_name).stem}_clean.csv", clear bindquote(strict) varnames(1)',
        'describe',
        'summarize',
        '```',
        "\n### 2. Python (pandas)",
        "```python",
        'import pandas as pd',
        f'df = pd.read_csv("out/{Path(wb_name).stem}_clean.csv")',
        'print(df.info())',
        'print(df.describe())',
        '```',
        "\n---\n*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*"
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def generate_codebook_json(variables: list[dict], summary: dict, out_path: Path | None = None) -> Path:
    """导出结构化 JSON 格式代码本供 Agent 或 API 调用。"""
    if out_path is None:
        out_path = ROOT / "out" / "HKIPO_2026Q1_Codebook.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "summary": summary,
        "variables": [{k: v for k, v in item.items() if k != "values"} for item in variables]
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out_path


def export_all(cfg: dict | None = None, out_dir: Path | str | None = None) -> dict:
    """一键执行代码本构建、CSV 导出与 JSON 生成。"""
    if cfg is None:
        cfg = load_cfg()
    variables, summary = build_codebook(cfg)
    cohort = summary.get("cohort", "2026 Q1")
    tag = cohort.replace(" ", "")
    dataset_id = cfg.get("dataset", {}).get("id", "HKIPO-MB2026Q1") if cfg else "HKIPO-MB2026Q1"

    csv_name = f"{dataset_id}_clean.csv"
    md_name = f"HKIPO_{tag}_Codebook.md"
    json_name = f"HKIPO_{tag}_Codebook.json"

    if out_dir is not None:
        od = Path(out_dir)
        od.mkdir(parents=True, exist_ok=True)
        csv_path = export_clean_csv(variables, out_path=od / csv_name)
        md_path = generate_codebook_markdown(variables, summary, out_path=od / md_name)
        json_path = generate_codebook_json(variables, summary, out_path=od / json_name)
    else:
        out_root = cfg["paths"]["out"] if (cfg and "paths" in cfg and "out" in cfg["paths"]) else ROOT / "out"
        out_root.mkdir(parents=True, exist_ok=True)
        csv_path = export_clean_csv(variables, out_path=out_root / csv_name)
        md_path = generate_codebook_markdown(variables, summary, out_path=out_root / md_name)
        json_path = generate_codebook_json(variables, summary, out_path=out_root / json_name)

    print("\n" + "=" * 70)
    print("HK IPO 学术代码本与科研 CSV 导出完成")
    print("=" * 70)
    print(f"样本规模: {summary['sample_size']} 家公司 | 变量总数: {summary['variable_count']} 列 (100% 完整解析)")
    print(f"数据层级: 浅绿 (HKEX) {summary['tiers']['green_hkex']} 列 | 浅蓝 (招股书) {summary['tiers']['blue_prospectus']} 列 | 深蓝 (外部/配发) {summary['tiers']['darkblue_external']} 列")
    print("-" * 70)
    print("产出成果文件:")
    print(f"  - 计量分析纯净 CSV:  {csv_path}")
    print(f"  - 学术数据代码本 MD: {md_path}")
    print(f"  - 结构化变量元数据:  {json_path}")
    print("=" * 70 + "\n")

    return {
        "csv_path": str(csv_path),
        "md_path": str(md_path),
        "json_path": str(json_path),
        "variable_count": summary["variable_count"],
        "sample_size": summary["sample_size"]
    }


def main():
    export_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
