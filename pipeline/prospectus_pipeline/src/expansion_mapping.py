"""Map master research outputs into the 41 workbook expansion fields."""
from __future__ import annotations

import csv

import master_contracts  # noqa: E402
from pathlib import Path
from regimes import fini_regime, pricing_reform_regime
from typing import Any

# 41 个新增学术字段定义清单 (Col 162 - Col 202)
EXPANSION_COLUMNS = [
    # 1. 稳价与超额配售 (Col 162-172)
    (162, "Stabilizing manager", "@", "官方指定价格稳定经理人名称"),
    (163, "Stabilization period end date", "yyyy-mm-dd", "法定30天稳价期结束日期"),
    (164, "Stabilization purchases occurred", "0", "稳价期内是否发生二级市场托单购买 (1=是, 0=否)"),
    (165, "Over-allocation shares", "#,##0", "国际配售超额配售股份数量（股）"),
    (166, "Over-allocation (% of base offer)", "0.00%", "超额配售股数占基础发售股份比例 (%)"),
    (167, "Over-allotment option exercise date", "yyyy-mm-dd", "超额配售权实际行使公告日期"),
    (168, "Shares issued under over-allotment option", "#,##0", "超额配售权最终发行股份数量（股）"),
    (169, "Over-allotment exercise percentage (%)", "0.00%", "超额配售权行使比例 (行使股数/超额配售上限, %)"),
    (170, "Post-stabilization cliff return [-5, +5] (%)", "0.00%", "稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试）"),
    (171, "Post-stabilization 20-day return [0, +20] (%)", "0.00%", "稳价期结束后20个交易日累计收益率 (%)"),
    (172, "Post-stabilization volume decay ratio (%)", "0.00%", "稳价结束后20日均成交额相对稳价期内之比 (%)"),

    # 2. 微观结构与短期/中期跨期表现 (Col 173-184)
    (173, "Day-5 BHR from Day-1 close (%)", "0.00%", "挂牌首周 (T+5交易日) 二级买入持有收益率 (%)"),
    (174, "Day-5 wealth relative vs HSI", "0.000", "挂牌首周对标恒指财富相对比 (WR_HSI)"),
    (175, "Day-20 BHR from Day-1 close (%)", "0.00%", "首月 (T+20交易日) 二级买入持有收益率 (%)"),
    (176, "Day-20 wealth relative vs HSI", "0.000", "首月对标恒指财富相对比 (WR_HSI)"),
    (177, "3-month BHR from Day-1 close (%)", "0.00%", "首季 (T+63交易日) 二级买入持有收益率 (%)"),
    (178, "3-month wealth relative vs HSI", "0.000", "首季对标恒指财富相对比 (WR_HSI)"),
    (179, "3-month wealth relative vs HSTECH", "0.000", "首季对标恒科财富相对比 (WR_HSTECH)"),
    (180, "3-month average daily turnover (HK$)", "#,##0", "首季度日均成交金额 (港元)"),
    (181, "Amihud illiquidity (6M mean)", "0.000000", "上市前6个月日均 Amihud (2002) 非流动性指标"),
    (182, "Zero-volume days count (first 6M)", "0", "上市前6个月零成交量交易日天数"),
    (183, "Return volatility (first 6M daily std dev, %)", "0.00%", "上市前6个月日度收益率标准差 (波动率, %)"),
    (184, "Maximum drawdown (first 6M, %)", "0.00%", "上市前6个月二级市场最大回撤幅度 (%)"),

    # 3. 多重法定解禁日程与事件窗冲击 (Col 185-189)
    (185, "Controlling shareholder 6-month disposal lockup expiry date", "yyyy-mm-dd", "控股股东首阶段6个月绝对禁售期满日"),
    (186, "Controlling shareholder 12-month cessation of control expiry date", "yyyy-mm-dd", "控股股东次阶段12个月控制权锁定到期日"),
    (187, "Cornerstone unlock CAR [-5, +5] (%)", "0.00%", "基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI)"),
    (188, "Cornerstone unlock CAR [-20, +20] (%)", "0.00%", "基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI)"),
    (189, "Cornerstone unlock volume shock ratio", "0.000", "基石解禁后20日均换手额相对解禁前20日换手额之比"),

    # 4. 承销辛迪加、费用分拆与银企关联 (Col 190-195)
    (190, "Lead sponsor name", "@", "独家/联席牵头保荐人英文全称"),
    (191, "Joint sponsor count", "0", "保荐人总家数 (独家=1, 联席=2+)"),
    (192, "Sponsor commercial bank affiliate flag", "0", "保荐人是否属于商业银行系金融机构 (1=是, 0=否)"),
    (193, "Underwriting base commission rate (%)", "0.00%", "承销基础佣金费率 (%)"),
    (194, "Underwriting discretionary incentive fee rate (%)", "0.00%", "承销酌情奖励费率估算 (%)"),
    (195, "Total underwriting fee rate (%)", "0.00%", "承销总费率估算 (基础+奖励, %)"),

    # 5. 机构投资者网络与国资背景 (Col 196-200)
    (196, "Cornerstone investor count", "0", "基石投资者机构总家数"),
    (197, "Cornerstone state-owned presence flag", "0", "基石投资者中是否包含国资/地方政府基金 (1=是, 0=否)"),
    (198, "Crossover fund presence flag", "0", "是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否)"),
    (199, "Pre-IPO institutional investor count", "0", "主要 Pre-IPO 投资机构总数"),
    (200, "Pre-IPO state-owned backing flag", "0", "Pre-IPO 股东中是否包含国资机构 (1=是, 0=否)"),

    # 6. 宏观监管制度分期 (Col 201-202)
    (201, "FINI digital settlement regime", "@", "结算监管体制 (POST_FINI / PRE_FINI)"),
    (202, "2025 pricing reform regime", "@", "发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM)"),
]

# 基石解禁事件窗字段 (Col 187-189)：无基石发行人不存在该事件，必须留空。
CORNERSTONE_EVENT_COLS = frozenset({187, 188, 189})
CORNERSTONE_UNLOCK_HEADER = "Earliest cornerstone unlock date (dd/mm/yy)"
CORNERSTONE_ALLOCATION_HEADER = "Final cornerstone allocation (% of base offer)"


def is_no_cornerstone(unlock_date: Any, allocation: Any) -> bool:
    """与 tools/external/flags.py 一致：解禁日为 NA 或最终基石配售为 0 即确认无基石。"""
    if isinstance(unlock_date, str) and unlock_date.strip().upper() == "NA":
        return True
    if allocation is None or isinstance(allocation, bool):
        return False
    try:
        return float(str(allocation).strip().rstrip("%")) == 0
    except ValueError:
        return False


# 缺来源一律返回 None：不得以行业惯例值、默认券商名或其他列代填。
def _present(val: Any) -> bool:
    return val is not None and str(val).strip() != ""


def _text(val: Any) -> str | None:
    return str(val).strip() if _present(val) else None


def _num(val: Any, divisor: float = 1.0) -> float | None:
    return float(val) / divisor if _present(val) else None


def _pct(val: float | None) -> float | None:
    return None if val is None else val / 100.0


def _flag(val: Any) -> int | None:
    """"true"/"false"（不区分大小写）→ 1/0；空值或无法识别 → None。"""
    text = str(val).strip().lower() if _present(val) else ""
    return {"true": 1, "false": 0}.get(text)


def _bool01(val: bool | None) -> int | None:
    return None if val is None else int(bool(val))


class ExpansionValueMapper:
    """Load research sources and resolve a field value for one issuer."""

    def __init__(self, out_master: Path, no_cornerstone: set[str] | None = None) -> None:
        self.out_master = Path(out_master)
        # Issuers confirmed to have no cornerstone investors (see cornerstone.confirmed_absent);
        # the writer also adds workbook-derived ones. Cols 187-189 are blank for them.
        self.no_cornerstone = set(no_cornerstone or ())
        self.stab_data: dict[str, dict[str, Any]] = {}
        self.horizon_data: dict[str, dict[str, dict[str, Any]]] = {}
        self.daily_stats: dict[str, dict[str, Any]] = {}
        self.lockup_data: dict[str, dict[str, dict[str, Any]]] = {}
        self.investor_stats: dict[str, dict[str, Any]] = {}
        self.syndicate_stats: dict[str, dict[str, Any]] = {}
        self.master_data: dict[str, dict[str, Any]] = {}

    def load_sources(self) -> None:
        """加载已预先计算好的 master 模块数据源。"""
        # 1. 稳价事件（fail-closed：缺文件/缺列在加载时报错，而非静默空格）
        for r in master_contracts.load_rows(
                self.out_master / master_contracts.STABILIZATION_EVENTS,
                master_contracts.STABILIZATION_EVENTS_COLS):
            self.stab_data[r["stock_code"]] = r

        # 2. 跨期收益
        for r in master_contracts.load_rows(
                self.out_master / master_contracts.HORIZON_SUMMARY,
                master_contracts.HORIZON_SUMMARY_COLS):
            self.horizon_data.setdefault(r["stock_code"], {})[r["horizon"]] = r

        # 3. 逐日统计量（Amihud 均值、零成交天数、波动率、最大回撤）
        #    无可用观测时记 None，不以 0 充数。
        import statistics
        for code, bars in master_contracts.load_grouped(
                self.out_master / master_contracts.DAILY_MARKET_PANEL,
                master_contracts.DAILY_MARKET_PANEL_COLS).items():
            w_bars = bars[:126]  # 前6个月
            illiqs = [float(b["amihud_illiq"]) for b in w_bars if _present(b.get("amihud_illiq"))]
            zero_flags = [_flag(b.get("zero_volume_flag")) for b in w_bars]
            zero_flags = [f for f in zero_flags if f is not None]
            rets = [float(b["daily_return"]) for b in w_bars if _present(b.get("daily_return"))]
            drawdowns = [float(b["max_drawdown"]) for b in w_bars if _present(b.get("max_drawdown"))]
            self.daily_stats[code] = {
                "amihud_mean": sum(illiqs) / len(illiqs) if illiqs else None,
                "zero_volume_count": sum(zero_flags) if zero_flags else None,
                "volatility": statistics.stdev(rets) if len(rets) > 1 else None,
                "max_drawdown": max(drawdowns) if drawdowns else None,
            }

        # 4. 解禁事件
        for r in master_contracts.load_rows(
                self.out_master / master_contracts.LOCKUP_EVENTS,
                master_contracts.LOCKUP_EVENTS_COLS):
            self.lockup_data.setdefault(r["stock_code"], {})[r["lockup_category"]] = r

        # 5. 投资者关系统计（可选交付物：缺文件跳过，缺契约列报错）
        for r in master_contracts.load_rows_if_present(
                self.out_master / master_contracts.INVESTOR_RELATIONAL,
                master_contracts.INVESTOR_RELATIONAL_COLS):
                    code = r["stock_code"]
                    if code not in self.investor_stats:
                        self.investor_stats[code] = {
                            "cs_count": 0, "cs_state": False, "crossover": False,
                            "pre_count": 0, "pre_state": False
                        }
                    st = self.investor_stats[code]
                    if r.get("cornerstone_flag", "").lower() == "true":
                        st["cs_count"] += 1
                        if r.get("state_owned_flag", "").lower() == "true":
                            st["cs_state"] = True
                        if r.get("crossover_flag", "").lower() == "true":
                            st["crossover"] = True
                    if r.get("pre_ipo_flag", "").lower() == "true":
                        st["pre_count"] += 1
                        if r.get("state_owned_flag", "").lower() == "true":
                            st["pre_state"] = True

        # 6. 承销辛迪加（可选交付物）
        #    保荐人字段只取 syndicate_role 含 "sponsor" 的行（稳价经理人不是保荐人）；
        #    费率取该发行人首个非空值；均无来源时保持 None。
        for r in master_contracts.load_rows_if_present(
                self.out_master / master_contracts.UNDERWRITER_RELATIONAL,
                master_contracts.UNDERWRITER_RELATIONAL_COLS):
                    code = r["stock_code"]
                    st = self.syndicate_stats.setdefault(code, {
                        "lead_sponsor": None, "sponsor_count": 0, "bank_affiliate": None,
                        "base_fee": None, "incentive_fee": None, "total_fee": None,
                    })
                    for key, field in (("base_fee", "base_commission_pct"),
                                       ("incentive_fee", "discretionary_incentive_fee_pct"),
                                       ("total_fee", "total_fee_rate_pct")):
                        if st[key] is None:
                            st[key] = _num(r.get(field))
                    if "sponsor" not in (r.get("syndicate_role") or "").lower():
                        continue
                    st["sponsor_count"] += 1
                    if st["lead_sponsor"] is None:
                        st["lead_sponsor"] = _text(r.get("intermediary_name"))
                    bank = _flag(r.get("commercial_bank_affiliate"))
                    if bank is not None:
                        st["bank_affiliate"] = max(st["bank_affiliate"] or 0, bank)

        # 7. Master 表
        im_csv = self.out_master / "issuer_master.csv"
        if im_csv.exists():
            with im_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    self.master_data[r["stock_code"]] = r

    def value_for(self, code: str, col_idx: int, listing_date: Any = None) -> tuple[Any, str]:
        """按列索引计算单元格写入值及格式。

        listing_date 为工作簿「Date of Listing」列的值；缺失时回退到 issuer_master
        的 listing_date。制度分期列 (201-202) 只由上市日期推导，两者皆缺则报错。
        """
        stab = self.stab_data.get(code, {})
        h_map = self.horizon_data.get(code, {})
        d_stat = self.daily_stats.get(code, {})
        lks = self.lockup_data.get(code, {})
        inv_stat = self.investor_stats.get(code, {})
        syn_stat = self.syndicate_stats.get(code, {})
        m_row = self.master_data.get(code, {})

        # 1. 稳价与超额配售 (Col 162-172)
        if col_idx == 162:
            return _text(stab.get("stabilizing_manager")), "@"
        if col_idx == 163:
            return _text(stab.get("stabilization_period_end")), "yyyy-mm-dd"
        if col_idx == 164:
            return _flag(stab.get("stabilization_purchases_occurred")), "0"
        if col_idx == 165:
            return _num(stab.get("over_allocation_shares")), "#,##0"
        if col_idx == 166:
            return _num(stab.get("over_allocation_pct"), 100.0), "0.00%"
        if col_idx == 167:
            # 不以稳价期结束日代填：行使日缺失即为缺失。
            return _text(stab.get("option_exercise_date")), "yyyy-mm-dd"
        if col_idx == 168:
            return _num(stab.get("shares_issued_under_option")), "#,##0"
        if col_idx == 169:
            pct = _num(stab.get("exercise_pct_of_option"), 100.0)
            if pct is None and _flag(stab.get("expired_unexercised")) == 1:
                pct = 0.0
            return pct, "0.00%"
        if col_idx == 170:
            return _num(stab.get("cliff_return_m5_p5")), "0.00%"
        if col_idx == 171:
            return _num(stab.get("post_stab_return_p20")), "0.00%"
        if col_idx == 172:
            return _num(stab.get("volume_decay_post_stab")), "0.00%"

        # 2. 微观结构与短期/中期跨期表现 (Col 173-184)
        if col_idx == 173:
            return _num(h_map.get("Day_5", {}).get("bhr_from_day1")), "0.00%"
        if col_idx == 174:
            return _num(h_map.get("Day_5", {}).get("wr_hsi")), "0.000"
        if col_idx == 175:
            return _num(h_map.get("Day_20", {}).get("bhr_from_day1")), "0.00%"
        if col_idx == 176:
            return _num(h_map.get("Day_20", {}).get("wr_hsi")), "0.000"
        if col_idx == 177:
            return _num(h_map.get("Month_3", {}).get("bhr_from_day1")), "0.00%"
        if col_idx == 178:
            return _num(h_map.get("Month_3", {}).get("wr_hsi")), "0.000"
        if col_idx == 179:
            return _num(h_map.get("Month_3", {}).get("wr_hstech")), "0.000"
        if col_idx == 180:
            return _num(h_map.get("Month_3", {}).get("avg_daily_turnover")), "#,##0"
        if col_idx == 181:
            return d_stat.get("amihud_mean"), "0.000000"
        if col_idx == 182:
            return d_stat.get("zero_volume_count"), "0"
        if col_idx == 183:
            return d_stat.get("volatility"), "0.00%"
        if col_idx == 184:
            return d_stat.get("max_drawdown"), "0.00%"

        # 3. 多重法定解禁日程与事件窗冲击 (Col 185-189)
        if col_idx in CORNERSTONE_EVENT_COLS and code in self.no_cornerstone:
            return None, "0.000" if col_idx == 189 else "0.00%"
        if col_idx == 185:
            rec = lks.get("Controlling_Shareholder_6M_Disposal", {})
            return _text(rec.get("expiry_date")), "yyyy-mm-dd"
        if col_idx == 186:
            rec = lks.get("Controlling_Shareholder_12M_Control", {})
            return _text(rec.get("expiry_date")), "yyyy-mm-dd"
        if col_idx == 187:
            return _num(lks.get("Cornerstone_6M", {}).get("car_m5_p5")), "0.00%"
        if col_idx == 188:
            return _num(lks.get("Cornerstone_6M", {}).get("car_m20_p20")), "0.00%"
        if col_idx == 189:
            return _num(lks.get("Cornerstone_6M", {}).get("volume_shock_ratio")), "0.000"

        # 4. 承销辛迪加、费用分拆与银企关联 (Col 190-195)
        if col_idx == 190:
            return syn_stat.get("lead_sponsor") or _text(m_row.get("lead_sponsor")), "@"
        if col_idx == 191:
            return syn_stat.get("sponsor_count") or None, "0"
        if col_idx == 192:
            return syn_stat.get("bank_affiliate"), "0"
        if col_idx == 193:
            return _pct(syn_stat.get("base_fee")), "0.00%"
        if col_idx == 194:
            return _pct(syn_stat.get("incentive_fee")), "0.00%"
        if col_idx == 195:
            return _pct(syn_stat.get("total_fee")), "0.00%"

        # 5. 机构投资者网络与国资背景 (Col 196-200)
        #    该发行人无投资者关系行时全部为 None；有行时计数/旗标基于真实行。
        if col_idx == 196:
            # Never invent a count: investor_relational.csv is the only source of
            # names, so an issuer missing from it is 0 only when confirmed to have
            # no cornerstones, otherwise unknown (blank).
            if "cs_count" in inv_stat:
                return inv_stat["cs_count"], "0"
            return (0 if code in self.no_cornerstone else None), "0"
        if col_idx == 197:
            return _bool01(inv_stat.get("cs_state")), "0"
        if col_idx == 198:
            return _bool01(inv_stat.get("crossover")), "0"
        if col_idx == 199:
            return inv_stat.get("pre_count"), "0"
        if col_idx == 200:
            return _bool01(inv_stat.get("pre_state")), "0"

        # 6. 宏观监管制度分期 (Col 201-202)：按上市日期推导，缺日期 fail-closed
        if col_idx in (201, 202):
            l_date = listing_date or m_row.get("listing_date")
            if col_idx == 201:
                return fini_regime(l_date, code), "@"
            return pricing_reform_regime(l_date, code), "@"

        return None, "@"
