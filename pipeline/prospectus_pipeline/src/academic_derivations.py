"""学术衍生变量计算引擎 (Academic Empirical Derivation Engine)

本模块严格依据 Michelle Lowry, Roni Michaely, and Ekaterina Volkova (2017)
《Initial Public Offerings: A Synthesis of the Literature and Directions for Future Research》
以及实证金融经典文献，提供第一阶段 8 个核心学术衍生指标的标准化数学推导逻辑。

涵盖模型与文献：
  1. Rock (1986) / Ritter (1984): 首日抑价率 (Initial Return / Underpricing)
  2. Benveniste & Spindt (1989) / Hanley (1993): 询价区间动态信息提取 (Partial Adjustment / Filing Price Revision)
  3. Beatty & Ritter (1986): 事前估值不确定性 (Ex-Ante Valuation Uncertainty / Filing Range Width)
  4. Lowry et al. (2017) Table 3.3: 定价落点分类体系 (Pricing Position in Filing Range)
  5. Lowry et al. (2017) Table 3.4: 企业成立至上市生命周期年龄 (Firm Age at IPO)
  6. Aggarwal (2003): 机构短线翻转抛售率 (Day-1 Flipping Velocity / Trading Turnover)
  7. Loughran & Ritter (2002): 行为金融学财富流失 (Money Left on the Table)
  8. Ellis, Michaely, & O'Hara (2000): 绿鞋机制与超额配售执行率 (Greenshoe Exercise Rate)
"""
from __future__ import annotations

import datetime as dt
from typing import Any, Optional


def derive_firm_age(
    listing_date: Optional[dt.date | dt.datetime | str],
    incorporation_date: Optional[dt.date | dt.datetime | str],
) -> Optional[float]:
    """计算公司成立至上市的年限 (Firm Age at IPO)。
    
    公式: (Listing Date - Incorporation Date) / 365.25
    
    参数:
        listing_date: 正式挂牌上市交易日期 (col_E)
        incorporation_date: 公司法定注册成立日期 (col_BZ)
        
    返回:
        保留 2 位小数的年限浮点数。若任一日期间隔缺失或无效则返回 None。
    """
    def _parse(d: Any) -> Optional[dt.date]:
        if d is None or d in ("", "NA", "NaN", "N/A"):
            return None
        if isinstance(d, dt.datetime):
            return d.date()
        if isinstance(d, dt.date):
            return d
        s = str(d).strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%Y/%m/%d"):
            try:
                return dt.datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    ld = _parse(listing_date)
    id_ = _parse(incorporation_date)
    if ld is None or id_ is None or ld < id_:
        return None
    days = (ld - id_).days
    return round(days / 365.25, 2)


def derive_pricing_dynamics(
    offer_price: Optional[float | int | str],
    max_offer_price: Optional[float | int | str],
    min_offer_price: Optional[float | int | str],
) -> tuple[Optional[float], Optional[float], str]:
    """计算询价区间价格修正幅度、相对宽度及定价落点分类。
    
    模型基础:
      - Hanley (1993): Delta P = (P_offer - P_mid) / P_mid
      - Beatty & Ritter (1986): Range Width = (P_max - P_min) / P_mid
      - Lowry et al. (2017) Table 3.3 分类
      
    参数:
        offer_price: 最终发售价 (HK$)
        max_offer_price: 最高发售价 (HK$)
        min_offer_price: 最低发售价 (HK$) (若固定价格发行则为 None / NA)
        
    返回:
        (price_revision, range_width, pricing_position)
        - price_revision: 偏离区间中点比例 (如 +0.0710 代表上浮 7.10%)
        - range_width: 区间相对宽度 (如 0.1421 代表 14.21%)
        - pricing_position: 取值之一:
            'Fixed price'   (固定发售价，无下限)
            'Above range'   (突破发售价区间上限，P_offer > P_max)
            'At high'       (区间顶限定价，P_offer == P_max)
            'Midpoint'      (中点定价，P_offer == P_mid)
            'Within range'  (区间内其他位置定价)
            'At low'        (区间底限定价，P_offer == P_min)
            'Below range'   (跌破发售价区间下限，P_offer < P_min)
    """
    def _to_float(v: Any) -> Optional[float]:
        if v is None or str(v).strip() in ("", "NA", "NaN", "N/A"):
            return None
        try:
            return float(str(v).replace(",", "").strip())
        except ValueError:
            return None

    p_off = _to_float(offer_price)
    p_max = _to_float(max_offer_price)
    p_min = _to_float(min_offer_price)

    if p_off is None or p_max is None:
        return None, None, "Unknown"

    # 固定发售价情形 (Fixed price: 无最低价或最低价等于最高价)
    if p_min is None or abs(p_max - p_min) < 1e-6:
        return 0.0, 0.0, "Fixed price"

    p_mid = (p_min + p_max) / 2.0
    if p_mid <= 0:
        return None, None, "Unknown"

    revision = round((p_off - p_mid) / p_mid, 6)
    width = round((p_max - p_min) / p_mid, 6)

    eps = 1e-4
    if p_off > p_max + eps:
        pos = "Above range"
    elif abs(p_off - p_max) <= eps:
        pos = "At high"
    elif abs(p_off - p_mid) <= eps:
        pos = "Midpoint"
    elif abs(p_off - p_min) <= eps:
        pos = "At low"
    elif p_off < p_min - eps:
        pos = "Below range"
    else:
        pos = "Within range"

    return revision, width, pos


def derive_day1_trading(
    day1_close_price: Optional[float | int | str],
    offer_price: Optional[float | int | str],
    day1_volume_shares: Optional[float | int | str],
    offer_shares: Optional[float | int | str],
) -> tuple[Optional[float], Optional[float], Optional[float]]:
    """计算首日抑价率、首日换手翻转率以及留在桌面上的财富。
    
    文献支撑:
      - Ritter (1984): Underpricing / Initial Return = (P_close - P_offer) / P_offer
      - Aggarwal (2003): Flipping Ratio = Day 1 Volume / Offer Shares
      - Loughran & Ritter (2002): Money Left on the Table = (P_close - P_offer) * Offer Shares
      
    参数:
        day1_close_price: 首日上市二级市场收盘价 (HK$)
        offer_price: 最终发售价 (HK$)
        day1_volume_shares: 首日成交股数 (股)
        offer_shares: 全球发售股份总数 (不含超额配售) (股)
        
    返回:
        (underpricing_ratio, money_left_on_table, flipping_ratio)
    """
    def _to_float(v: Any) -> Optional[float]:
        if v is None or str(v).strip() in ("", "NA", "NaN", "N/A"):
            return None
        try:
            return float(str(v).replace(",", "").strip())
        except ValueError:
            return None

    p_close = _to_float(day1_close_price)
    p_off = _to_float(offer_price)
    vol = _to_float(day1_volume_shares)
    shares = _to_float(offer_shares)

    if p_close is None or p_off is None or p_off <= 0:
        ir = None
        money_left = None
    else:
        ir = round((p_close - p_off) / p_off, 6)
        if shares is not None and shares > 0:
            money_left = round((p_close - p_off) * shares, 2)
        else:
            money_left = None

    if vol is not None and shares is not None and shares > 0:
        flipping = round(vol / shares, 6)
    else:
        flipping = None

    return ir, money_left, flipping


def derive_greenshoe_rate(
    overallotment_shares_issued: Optional[float | int | str],
    base_offer_shares: Optional[float | int | str],
    overallotment_option_pct: Optional[float | int | str],
) -> Optional[float]:
    """计算绿鞋实际行使比例 (Greenshoe Exercise Rate)。
    
    文献支撑:
      - Ellis, Michaely, & O'Hara (2000): 绿鞋机制与承销商二级市场价格稳定
      
    公式:
      实际超额配售股数 / (基础发售股数 * 超额配售选择权比例)
      
    参数:
        overallotment_shares_issued: 实际发行的超额配售股份数量 (股)
        base_offer_shares: 基础全球发售股份数 (股)
        overallotment_option_pct: 招股书披露的最大超额配售比例 (如 0.15 代表 15%)
        
    返回:
        实际行使率浮点数 (0.0 ~ 1.0)。若无绿鞋或实际发行 0 股则返回 0.0。
    """
    def _to_float(v: Any) -> Optional[float]:
        if v is None or str(v).strip() in ("", "NA", "NaN", "N/A"):
            return None
        try:
            return float(str(v).replace(",", "").strip())
        except ValueError:
            return None

    issued = _to_float(overallotment_shares_issued) or 0.0
    base = _to_float(base_offer_shares)
    opt = _to_float(overallotment_option_pct) or 0.0

    if base is None or base <= 0 or opt <= 0:
        return 0.0

    max_greenshoe_shares = base * opt
    if max_greenshoe_shares <= 0:
        return 0.0

    rate = round(issued / max_greenshoe_shares, 6)
    # 浮点微小误差修正：如 0.999996 归一化为 1.0000
    if abs(rate - 1.0) < 1e-4:
        return 1.0
    return rate
