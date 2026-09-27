#!/usr/bin/env python3
"""202 维变量的定义目录（纯数据，无 I/O）。

本 module 是变量中文释义 / 层级 / 分组 / 来源等元数据的唯一 authored 来源；
codebook.py 用它渲染 Codebook，master_panel.build_registry 用它做定义核对。
这里的 dict 按"语义表头"键控（EXTRA 组刻意不用列字母，插列不会错位）。
"""
from __future__ import annotations

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
    "DN": ("Offer mechanism", "适用发售与回拨制度（2025-08-04 前 PN18/18C.09；之后 Mechanism A/B）", "categorical"),
    "DO": ("Applicable IPO rules / transition basis", "适用之上市规则过渡基准（FINI 改革规则）", "categorical"),
    "BH": ("Listing board", "上市板块（Main Board 主板）", "categorical"),
    "BJ": ("A+H flag", "A+H 两地同时上市标识（1=是，0=否）", "boolean"),
    "BK": ("WVR flag", "不同投票权/同股不同权架构标识（1=是，0=否）", "boolean"),
    "BL": ("Chapter 18A flag", "第 18A 章未盈利生物科技公司标识（1=是，0=否）", "boolean"),
    "BM": ("Chapter 18C flag", "第 18C 章特专科技公司标识（1=是，0=否）", "boolean"),
    "BN": ("Industry classification code", "恒生行业分类 HSICS 6 位业务细分代码", "string"),
    "BO": ("Industry classification system and version", "行业分类系统与版本号", "string"),
    "BQ": ("Place of incorporation", "公司注册成立法域（如 Cayman Islands, PRC 等）", "categorical"),
    "AZ": ("Comments / Annualization factor", "最近一期财务数据对应的年化因子与口径说明", "string"),
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

# Stable metadata for workbook headers that are intentionally outside the two
# extraction schemas.  These entries are keyed by semantic header, never by an
# Excel column letter, so inserting a column cannot silently attach the wrong
# definition to a variable.
EXTRA_HEADER_VARS = {
    "Company Name at time of listing (exclude Chapter 20 cases)": (
        "Company Name at time of listing", "公司上市时法定英文名称", "浅绿 (港交所官方报告)", "hkex_nlr",
        "香港交易所 (HKEX) 新上市报告 (New Listing Report) 官方表格",
    ),
    "Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5)": (
        "Comments / Annualization factor", "最近一期财务数据对应的年化因子与口径说明", "浅蓝 (招股书全量披露)",
        "financial_period", "招股书财务往绩期间与年化口径",
    ),
    "Year-3 financial period start": (
        "Year-3 financial period start", "往绩记录第三年前期起始日", "浅蓝 (招股书全量披露)",
        "financial_period", "招股书会计师报告往绩期间",
    ),
    "Year-3 financial period end": (
        "Year-3 financial period end", "往绩记录第三年前期截止日", "浅蓝 (招股书全量披露)",
        "financial_period", "招股书会计师报告往绩期间",
    ),
    "A+H issuer flag": (
        "A+H issuer flag", "A+H 两地上市发行人标识（1=是，0=否）", "深蓝 (配发及外部数据)",
        "regulatory_flags", "招股书与交易所证券资料确定性分类",
    ),
    "Year-2 financial period start": (
        "Year-2 financial period start", "往绩记录第二年前期起始日", "深蓝 (配发及外部数据)",
        "financial_period", "招股书期间字段的确定性标准化",
    ),
    "Year-2 financial period end": (
        "Year-2 financial period end", "往绩记录第二年前期截止日", "深蓝 (配发及外部数据)",
        "financial_period", "招股书期间字段的确定性标准化",
    ),
    "Year-1 financial period start": (
        "Year-1 financial period start", "往绩记录最近一期起始日", "深蓝 (配发及外部数据)",
        "financial_period", "招股书期间字段的确定性标准化",
    ),
    "Year-1 net sales (original, pre-annualization)": (
        "Year-1 net sales (original, pre-annualization)", "最近一期营业收入原值（年化前）", "深蓝 (配发及外部数据)",
        "financial_period", "招股书披露值的确定性标准化",
    ),
    "Year-1 profit before tax (original)": (
        "Year-1 profit before tax (original)", "最近一期税前利润原值（年化前）", "深蓝 (配发及外部数据)",
        "financial_period", "招股书披露值的确定性标准化",
    ),
    "Year-1 profit for period (original)": (
        "Year-1 profit for period (original)", "最近一期净利润原值（年化前）", "深蓝 (配发及外部数据)",
        "financial_period", "招股书披露值的确定性标准化",
    ),
    "Earliest cornerstone unlock date (dd/mm/yy)": (
        "Earliest cornerstone unlock date (dd/mm/yy)", "基石投资者最早解禁日期", "深蓝 (配发结果与确定性派生)",
        "cornerstone", "基石协议、配发结果公告与上市日确定性派生",
    ),
    "Current listing status": (
        "Current listing status", "当前挂牌存续状态", "深蓝 (配发及外部数据)", "aftermarket", "二级市场与发行人公告",
    ),
    "1-month post-IPO close price (HK$)": (
        "1-month post-IPO close price (HK$)", "第20个交易日收盘价（窗口成熟后填报）", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情",
    ),
    "1-month BHR from Day-1 close (%)": (
        "1-month BHR from Day-1 close (%)", "由首日收盘至第20个交易日的买入持有收益率", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "1-month total return from offer price (%)": (
        "1-month total return from offer price (%)", "由发售价至第20个交易日的累计收益率", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "1-month HSI return (%)": (
        "1-month HSI return (%)", "同期恒生指数累计收益率", "深蓝 (配发及外部数据)", "aftermarket", "指数日行情确定性派生",
    ),
    "1-month HSTECH return (%)": (
        "1-month HSTECH return (%)", "同期恒生科技指数累计收益率", "深蓝 (配发及外部数据)", "aftermarket", "指数日行情确定性派生",
    ),
    "1-month wealth relative vs HSI": (
        "1-month wealth relative vs HSI", "一个月相对恒指财富比", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "1-month wealth relative vs HSTECH": (
        "1-month wealth relative vs HSTECH", "一个月相对恒生科技指数财富比", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "1-month average daily turnover (HK$)": (
        "1-month average daily turnover (HK$)", "上市后首20个交易日日均成交额", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "6-month post-IPO close price (HK$)": (
        "6-month post-IPO close price (HK$)", "六个月目标日后首个交易日收盘价（窗口成熟后填报）", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情",
    ),
    "6-month BHR from Day-1 close (%)": (
        "6-month BHR from Day-1 close (%)", "由首日收盘至六个月目标交易日的买入持有收益率", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "6-month total return from offer price (%)": (
        "6-month total return from offer price (%)", "由发售价至六个月目标交易日的累计收益率", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "6-month HSI return (%)": (
        "6-month HSI return (%)", "同期恒生指数累计收益率", "深蓝 (配发及外部数据)", "aftermarket", "指数日行情确定性派生",
    ),
    "6-month HSTECH return (%)": (
        "6-month HSTECH return (%)", "同期恒生科技指数累计收益率", "深蓝 (配发及外部数据)", "aftermarket", "指数日行情确定性派生",
    ),
    "6-month wealth relative vs HSI": (
        "6-month wealth relative vs HSI", "六个月相对恒指财富比", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "6-month wealth relative vs HSTECH": (
        "6-month wealth relative vs HSTECH", "六个月相对恒生科技指数财富比", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "6-month average daily turnover (HK$)": (
        "6-month average daily turnover (HK$)", "六个月目标日前20个交易日日均成交额", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "Liquidity decay ratio (6M vs Day-1 turnover)": (
        "Liquidity decay ratio (6M vs Day-1 turnover)", "六个月窗口日均成交额相对首日成交额比率", "深蓝 (配发及外部数据)", "aftermarket", "二级市场日行情确定性派生",
    ),
    "1-year post-IPO return (%) [Reserved]": (
        "1-year post-IPO return (%) [Reserved]", "一年期收益率预留字段", "深蓝 (配发及外部数据)", "aftermarket", "预留",
    ),
    "1-year wealth relative vs HSI [Reserved]": (
        "1-year wealth relative vs HSI [Reserved]", "一年期相对恒指财富比预留字段", "深蓝 (配发及外部数据)", "aftermarket", "预留",
    ),
    "3-year post-IPO return (%) [Reserved]": (
        "3-year post-IPO return (%) [Reserved]", "三年期收益率预留字段", "深蓝 (配发及外部数据)", "aftermarket", "预留",
    ),
    "3-year wealth relative vs HSI [Reserved]": (
        "3-year wealth relative vs HSI [Reserved]", "三年期相对恒指财富比预留字段", "深蓝 (配发及外部数据)", "aftermarket", "预留",
    ),
    "18A/18C regulatory milestone status": (
        "18A/18C regulatory milestone status", "18A/18C 监管路径与商业化里程碑状态", "深蓝 (配发及外部数据)", "regulatory_flags", "上市规则分类与发行人公告",
    ),
    # === 学术与微观结构扩展字段 (Cols 162–202) ===
    # 1. 稳价与超额配售 (Col 162-172)
    "Stabilizing manager": (
        "Stabilizing manager", "官方指定价格稳定经理人名称", "深蓝 (配发及外部数据)",
        "stabilization", "香港主板上市规则第 9(2) 条稳价公告",
    ),
    "Stabilization period end date": (
        "Stabilization period end date", "法定30天稳价期结束日期", "深蓝 (配发及外部数据)",
        "stabilization", "香港主板上市规则第 9(2) 条稳价公告",
    ),
    "Stabilization purchases occurred": (
        "Stabilization purchases occurred", "稳价期内是否发生二级市场托单购买 (1=是, 0=否)", "深蓝 (配发及外部数据)",
        "stabilization", "香港主板上市规则第 9(2) 条稳价公告",
    ),
    "Over-allocation shares": (
        "Over-allocation shares", "国际配售超额配售股份数量（股）", "深蓝 (配发及外部数据)",
        "stabilization", "配发结果公告与超额配售公告",
    ),
    "Over-allocation (% of base offer)": (
        "Over-allocation (% of base offer)", "超额配售股数占基础发售股份比例 (%)", "深蓝 (配发及外部数据)",
        "stabilization", "配发结果公告与超额配售公告",
    ),
    "Over-allotment option exercise date": (
        "Over-allotment option exercise date", "超额配售权实际行使公告日期", "深蓝 (配发及外部数据)",
        "stabilization", "超额配售权行使公告",
    ),
    "Shares issued under over-allotment option": (
        "Shares issued under over-allotment option", "超额配售权最终发行股份数量（股）", "深蓝 (配发及外部数据)",
        "stabilization", "超额配售权行使公告",
    ),
    "Over-allotment exercise percentage (%)": (
        "Over-allotment exercise percentage (%)", "超额配售权行使比例 (行使股数/超额配售上限, %)", "深蓝 (配发及外部数据)",
        "stabilization", "超额配售权行使公告确定性派生",
    ),
    "Post-stabilization cliff return [-5, +5] (%)": (
        "Post-stabilization cliff return [-5, +5] (%)", "稳价期结束日前后[-5, +5]交易日累计收益率（断崖效应测试）", "深蓝 (配发及外部数据)",
        "stabilization", "二级市场日行情与稳价截止日确定性派生",
    ),
    "Post-stabilization 20-day return [0, +20] (%)": (
        "Post-stabilization 20-day return [0, +20] (%)", "稳价期结束后20个交易日累计收益率 (%)", "深蓝 (配发及外部数据)",
        "stabilization", "二级市场日行情与稳价截止日确定性派生",
    ),
    "Post-stabilization volume decay ratio (%)": (
        "Post-stabilization volume decay ratio (%)", "稳价结束后20日均成交额相对稳价期内之比 (%)", "深蓝 (配发及外部数据)",
        "stabilization", "二级市场日行情与稳价截止日确定性派生",
    ),

    # 2. 微观结构与短期/中期跨期表现 (Col 173-184)
    "Day-5 BHR from Day-1 close (%)": (
        "Day-5 BHR from Day-1 close (%)", "挂牌首周 (T+5交易日) 二级买入持有收益率 (%)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情确定性派生",
    ),
    "Day-5 wealth relative vs HSI": (
        "Day-5 wealth relative vs HSI", "挂牌首周对标恒指财富相对比 (WR_HSI)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情与恒生指数确定性派生",
    ),
    "Day-20 BHR from Day-1 close (%)": (
        "Day-20 BHR from Day-1 close (%)", "首月 (T+20交易日) 二级买入持有收益率 (%)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情确定性派生",
    ),
    "Day-20 wealth relative vs HSI": (
        "Day-20 wealth relative vs HSI", "首月对标恒指财富相对比 (WR_HSI)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情与恒生指数确定性派生",
    ),
    "3-month BHR from Day-1 close (%)": (
        "3-month BHR from Day-1 close (%)", "首季 (T+63交易日) 二级买入持有收益率 (%)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情确定性派生",
    ),
    "3-month wealth relative vs HSI": (
        "3-month wealth relative vs HSI", "首季对标恒指财富相对比 (WR_HSI)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情与恒生指数确定性派生",
    ),
    "3-month wealth relative vs HSTECH": (
        "3-month wealth relative vs HSTECH", "首季对标恒科财富相对比 (WR_HSTECH)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情与恒生科技指数确定性派生",
    ),
    "3-month average daily turnover (HK$)": (
        "3-month average daily turnover (HK$)", "首季度日均成交金额 (港元)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情确定性派生",
    ),
    "Amihud illiquidity (6M mean)": (
        "Amihud illiquidity (6M mean)", "上市前6个月日均 Amihud (2002) 非流动性指标", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情与 Amihud 模型派生",
    ),
    "Zero-volume days count (first 6M)": (
        "Zero-volume days count (first 6M)", "上市前6个月零成交量交易日天数", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情交易量派生",
    ),
    "Return volatility (first 6M daily std dev, %)": (
        "Return volatility (first 6M daily std dev, %)", "上市前6个月日度收益率标准差 (波动率, %)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日度收益率标准差派生",
    ),
    "Maximum drawdown (first 6M, %)": (
        "Maximum drawdown (first 6M, %)", "上市前6个月二级市场最大回撤幅度 (%)", "深蓝 (配发及外部数据)",
        "aftermarket", "二级市场日行情累计高点回撤派生",
    ),

    # 3. 多重法定解禁日程与事件窗冲击 (Col 185-189)
    "Controlling shareholder 6-month disposal lockup expiry date": (
        "Controlling shareholder 6-month disposal lockup expiry date", "控股股东首阶段6个月绝对禁售期满日", "深蓝 (配发及外部数据)",
        "lockup", "香港主板上市规则第 10.07(1)(a) 条法定禁售期",
    ),
    "Controlling shareholder 12-month cessation of control expiry date": (
        "Controlling shareholder 12-month cessation of control expiry date", "控股股东次阶段12个月控制权锁定到期日", "深蓝 (配发及外部数据)",
        "lockup", "香港主板上市规则第 10.07(1)(b) 条法定禁售期",
    ),
    "Cornerstone unlock CAR [-5, +5] (%)": (
        "Cornerstone unlock CAR [-5, +5] (%)", "基石投资者解禁日前后[-5, +5]交易日累计超额收益 (CAR vs HSI)", "深蓝 (配发及外部数据)",
        "lockup", "二级市场日行情与基石解禁日确定性派生",
    ),
    "Cornerstone unlock CAR [-20, +20] (%)": (
        "Cornerstone unlock CAR [-20, +20] (%)", "基石投资者解禁日前后[-20, +20]交易日累计超额收益 (CAR vs HSI)", "深蓝 (配发及外部数据)",
        "lockup", "二级市场日行情与基石解禁日确定性派生",
    ),
    "Cornerstone unlock volume shock ratio": (
        "Cornerstone unlock volume shock ratio", "基石解禁后20日均换手额相对解禁前20日换手额之比", "深蓝 (配发及外部数据)",
        "lockup", "二级市场日行情与基石解禁日确定性派生",
    ),

    # 4. 承销辛迪加、费用分拆与银企关联 (Col 190-195)
    "Lead sponsor name": (
        "Lead sponsor name", "独家/联席牵头保荐人英文全称", "深蓝 (配发及外部数据)",
        "syndicate", "招股书与港交所新上市报告",
    ),
    "Joint sponsor count": (
        "Joint sponsor count", "保荐人总家数 (独家=1, 联席=2+)", "深蓝 (配发及外部数据)",
        "syndicate", "招股书保荐人名单确定性派生",
    ),
    "Sponsor commercial bank affiliate flag": (
        "Sponsor commercial bank affiliate flag", "保荐人是否属于商业银行系金融机构 (1=是, 0=否)", "深蓝 (配发及外部数据)",
        "syndicate", "保荐人金融牌照与银行系背景分类",
    ),
    "Underwriting base commission rate (%)": (
        "Underwriting base commission rate (%)", "承销基础佣金费率 (%)", "深蓝 (配发及外部数据)",
        "syndicate", "招股书承销佣金协议披露",
    ),
    "Underwriting discretionary incentive fee rate (%)": (
        "Underwriting discretionary incentive fee rate (%)", "承销酌情奖励费率估算 (%)", "深蓝 (配发及外部数据)",
        "syndicate", "招股书承销佣金协议披露",
    ),
    "Total underwriting fee rate (%)": (
        "Total underwriting fee rate (%)", "承销总费率估算 (基础+奖励, %)", "深蓝 (配发及外部数据)",
        "syndicate", "招股书承销佣金协议披露确定性派生",
    ),

    # 5. 机构投资者网络与国资背景 (Col 196-200)
    "Cornerstone investor count": (
        "Cornerstone investor count", "基石投资者机构总家数", "深蓝 (配发及外部数据)",
        "investor_network", "配发结果公告基石投资者明细汇总",
    ),
    "Cornerstone state-owned presence flag": (
        "Cornerstone state-owned presence flag", "基石投资者中是否包含国资/地方政府基金 (1=是, 0=否)", "深蓝 (配发及外部数据)",
        "investor_network", "基石投资者工商穿透与国资背景标识",
    ),
    "Crossover fund presence flag": (
        "Crossover fund presence flag", "是否包含兼具 Pre-IPO 与基石双重身份的跨界基金 (1=是, 0=否)", "深蓝 (配发及外部数据)",
        "investor_network", "Pre-IPO 股东与基石投资者双重身份穿透匹配",
    ),
    "Pre-IPO institutional investor count": (
        "Pre-IPO institutional investor count", "主要 Pre-IPO 投资机构总数", "深蓝 (配发及外部数据)",
        "investor_network", "招股书历史与资本化结构披露",
    ),
    "Pre-IPO state-owned backing flag": (
        "Pre-IPO state-owned backing flag", "Pre-IPO 股东中是否包含国资机构 (1=是, 0=否)", "深蓝 (配发及外部数据)",
        "investor_network", "Pre-IPO 投资机构工商背景与国资标识",
    ),

    # 6. 宏观监管制度分期 (Col 201-202)
    "FINI digital settlement regime": (
        "FINI digital settlement regime", "结算监管体制 (POST_FINI / PRE_FINI)", "深蓝 (配发及外部数据)",
        "regulatory_regime", "香港交易所 FINI 数字化结算过渡分期",
    ),
    "2025 pricing reform regime": (
        "2025 pricing reform regime", "发售与定价机制改革体制 (POST_2025_REFORM / PRE_2025_REFORM)", "深蓝 (配发及外部数据)",
        "regulatory_regime", "香港交易所 2025 发售与定价改革过渡分期",
    ),
}




# 合并后的规范化表头查找表（等价于原先 build_codebook 内构造的四个 *_by_header）
def lookup_tables():
    """返回 (green, external, academic, extra) 四张 规范化表头 -> 定义 的查找表。"""
    from workbook_reader import norm_header

    green = {norm_header(v[0]): v for v in HKEX_GREEN_VARS.values()}
    external = {norm_header(v[0]): v for v in EXTERNAL_VARS.values()}
    academic = {norm_header(k): v for k, v in ACADEMIC_VARS.items()}
    extra = {norm_header(k): v for k, v in EXTRA_HEADER_VARS.items()}
    return green, external, academic, extra
