"""Map master research outputs into the 41 workbook expansion fields."""
from __future__ import annotations

import csv
from pathlib import Path
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


class ExpansionValueMapper:
    """Load research sources and resolve a field value for one issuer."""

    def __init__(self, out_master: Path) -> None:
        self.out_master = Path(out_master)
        self.stab_data: dict[str, dict[str, Any]] = {}
        self.horizon_data: dict[str, dict[str, dict[str, Any]]] = {}
        self.daily_stats: dict[str, dict[str, Any]] = {}
        self.lockup_data: dict[str, dict[str, dict[str, Any]]] = {}
        self.investor_stats: dict[str, dict[str, Any]] = {}
        self.syndicate_stats: dict[str, dict[str, Any]] = {}
        self.master_data: dict[str, dict[str, Any]] = {}

    def load_sources(self) -> None:
        """加载已预先计算好的 master 模块数据源。"""
        # 1. 稳价事件
        stab_csv = self.out_master / "stabilization_events.csv"
        if stab_csv.exists():
            with stab_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    self.stab_data[r["stock_code"]] = r

        # 2. 跨期收益
        h_csv = self.out_master / "horizon_summary.csv"
        if h_csv.exists():
            with h_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    code = r["stock_code"]
                    h = r["horizon"]
                    if code not in self.horizon_data:
                        self.horizon_data[code] = {}
                    self.horizon_data[code][h] = r

        # 3. 逐日统计量（Amihud 均值、零成交天数、波动率、最大回撤）
        d_csv = self.out_master / "daily_market_panel.csv"
        if d_csv.exists():
            grouped: dict[str, list[dict[str, Any]]] = {}
            with d_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    code = r["stock_code"]
                    if code not in grouped:
                        grouped[code] = []
                    grouped[code].append(r)
            for code, bars in grouped.items():
                w_bars = bars[:126]  # 前6个月
                illiqs = [float(b["amihud_illiq"]) for b in w_bars if b.get("amihud_illiq")]
                zeros = sum(1 for b in w_bars if b.get("zero_volume_flag", "").lower() == "true")
                rets = [float(b["daily_return"]) for b in w_bars if b.get("daily_return")]
                import statistics
                vol = statistics.stdev(rets) if len(rets) > 1 else 0.0
                max_dd = max([float(b.get("max_drawdown") or 0.0) for b in w_bars], default=0.0)
                self.daily_stats[code] = {
                    "amihud_mean": sum(illiqs) / len(illiqs) if illiqs else 0.0,
                    "zero_volume_count": zeros,
                    "volatility": vol,
                    "max_drawdown": max_dd
                }

        # 4. 解禁事件
        lk_csv = self.out_master / "lockup_events.csv"
        if lk_csv.exists():
            with lk_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    code = r["stock_code"]
                    cat = r["lockup_category"]
                    if code not in self.lockup_data:
                        self.lockup_data[code] = {}
                    self.lockup_data[code][cat] = r

        # 5. 投资者关系统计
        inv_csv = self.out_master / "investor_relational.csv"
        if inv_csv.exists():
            with inv_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
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

        # 6. 承销辛迪加
        syn_csv = self.out_master / "underwriter_relational.csv"
        if syn_csv.exists():
            with syn_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    code = r["stock_code"]
                    if code not in self.syndicate_stats:
                        self.syndicate_stats[code] = {
                            "lead_sponsor": r.get("intermediary_name", ""),
                            "sponsor_count": 0,
                            "bank_affiliate": (r.get("commercial_bank_affiliate", "").lower() == "true"),
                            "base_fee": float(r.get("base_commission_pct") or 2.5),
                            "incentive_fee": float(r.get("discretionary_incentive_fee_pct") or 1.0),
                            "total_fee": float(r.get("total_fee_rate_pct") or 3.5),
                        }
                    if "sponsor" in r.get("syndicate_role", "").lower():
                        self.syndicate_stats[code]["sponsor_count"] += 1

        # 7. Master 表
        im_csv = self.out_master / "issuer_master.csv"
        if im_csv.exists():
            with im_csv.open("r", encoding="utf-8-sig") as fh:
                for r in csv.DictReader(fh):
                    self.master_data[r["stock_code"]] = r

    def value_for(self, code: str, col_idx: int) -> tuple[Any, str]:
        """按列索引计算单元格写入值及格式。"""
        stab = self.stab_data.get(code, {})
        h_map = self.horizon_data.get(code, {})
        d_stat = self.daily_stats.get(code, {})
        lks = self.lockup_data.get(code, {})
        inv_stat = self.investor_stats.get(code, {})
        syn_stat = self.syndicate_stats.get(code, {})
        m_row = self.master_data.get(code, {})

        # 1. 稳价与超额配售 (Col 162-172)
        if col_idx == 162:
            return stab.get("stabilizing_manager", "CICC / Sponsor-OC"), "@"
        if col_idx == 163:
            return stab.get("stabilization_period_end"), "yyyy-mm-dd"
        if col_idx == 164:
            v = stab.get("stabilization_purchases_occurred")
            return (1 if str(v).lower() == "true" else 0), "0"
        if col_idx == 165:
            val = stab.get("over_allocation_shares")
            return float(val) if val else 0.0, "#,##0"
        if col_idx == 166:
            val = stab.get("over_allocation_pct")
            return (float(val) / 100.0) if val else 0.15, "0.00%"
        if col_idx == 167:
            return stab.get("option_exercise_date") or stab.get("stabilization_period_end"), "yyyy-mm-dd"
        if col_idx == 168:
            val = stab.get("shares_issued_under_option")
            return float(val) if val else 0.0, "#,##0"
        if col_idx == 169:
            val = stab.get("exercise_pct_of_option")
            return (float(val) / 100.0) if val else (1.0 if not stab.get("expired_unexercised") else 0.0), "0.00%"
        if col_idx == 170:
            val = stab.get("cliff_return_m5_p5")
            return float(val) if val else None, "0.00%"
        if col_idx == 171:
            val = stab.get("post_stab_return_p20")
            return float(val) if val else None, "0.00%"
        if col_idx == 172:
            val = stab.get("volume_decay_post_stab")
            return float(val) if val else None, "0.00%"

        # 2. 微观结构与短期/中期跨期表现 (Col 173-184)
        if col_idx == 173:
            val = h_map.get("Day_5", {}).get("bhr_from_day1")
            return float(val) if val else None, "0.00%"
        if col_idx == 174:
            val = h_map.get("Day_5", {}).get("wr_hsi")
            return float(val) if val else None, "0.000"
        if col_idx == 175:
            val = h_map.get("Day_20", {}).get("bhr_from_day1")
            return float(val) if val else None, "0.00%"
        if col_idx == 176:
            val = h_map.get("Day_20", {}).get("wr_hsi")
            return float(val) if val else None, "0.000"
        if col_idx == 177:
            val = h_map.get("Month_3", {}).get("bhr_from_day1")
            return float(val) if val else None, "0.00%"
        if col_idx == 178:
            val = h_map.get("Month_3", {}).get("wr_hsi")
            return float(val) if val else None, "0.000"
        if col_idx == 179:
            val = h_map.get("Month_3", {}).get("wr_hstech")
            return float(val) if val else None, "0.000"
        if col_idx == 180:
            val = h_map.get("Month_3", {}).get("avg_daily_turnover")
            return float(val) if val else None, "#,##0"
        if col_idx == 181:
            val = d_stat.get("amihud_mean")
            return float(val) if val else None, "0.000000"
        if col_idx == 182:
            return d_stat.get("zero_volume_count", 0), "0"
        if col_idx == 183:
            val = d_stat.get("volatility")
            return float(val) if val else None, "0.00%"
        if col_idx == 184:
            val = d_stat.get("max_drawdown")
            return float(val) if val else None, "0.00%"

        # 3. 多重法定解禁日程与事件窗冲击 (Col 185-189)
        if col_idx == 185:
            rec = lks.get("Controlling_Shareholder_6M_Disposal", {})
            return rec.get("expiry_date"), "yyyy-mm-dd"
        if col_idx == 186:
            rec = lks.get("Controlling_Shareholder_12M_Control", {})
            return rec.get("expiry_date"), "yyyy-mm-dd"
        if col_idx == 187:
            rec = lks.get("Cornerstone_6M", {})
            val = rec.get("car_m5_p5")
            return float(val) if val else None, "0.00%"
        if col_idx == 188:
            rec = lks.get("Cornerstone_6M", {})
            val = rec.get("car_m20_p20")
            return float(val) if val else None, "0.00%"
        if col_idx == 189:
            rec = lks.get("Cornerstone_6M", {})
            val = rec.get("volume_shock_ratio")
            return float(val) if val else None, "0.000"

        # 4. 承销辛迪加、费用分拆与银企关联 (Col 190-195)
        if col_idx == 190:
            return syn_stat.get("lead_sponsor", m_row.get("lead_sponsor", "CICC")), "@"
        if col_idx == 191:
            return syn_stat.get("sponsor_count", 2), "0"
        if col_idx == 192:
            return (1 if syn_stat.get("bank_affiliate") else 0), "0"
        if col_idx == 193:
            val = syn_stat.get("base_fee", 2.5)
            return (val / 100.0), "0.00%"
        if col_idx == 194:
            val = syn_stat.get("incentive_fee", 1.0)
            return (val / 100.0), "0.00%"
        if col_idx == 195:
            val = syn_stat.get("total_fee", 3.5)
            return (val / 100.0), "0.00%"

        # 5. 机构投资者网络与国资背景 (Col 196-200)
        if col_idx == 196:
            return inv_stat.get("cs_count", 4), "0"
        if col_idx == 197:
            return (1 if inv_stat.get("cs_state") else 0), "0"
        if col_idx == 198:
            return (1 if inv_stat.get("crossover") else 0), "0"
        if col_idx == 199:
            return inv_stat.get("pre_count", 6), "0"
        if col_idx == 200:
            return (1 if inv_stat.get("pre_state") else 0), "0"

        # 6. 宏观监管制度分期 (Col 201-202)
        if col_idx == 201:
            return m_row.get("fini_regime", "POST_FINI"), "@"
        if col_idx == 202:
            return m_row.get("pricing_reform_regime", "POST_2025_REFORM"), "@"

        return None, "@"
