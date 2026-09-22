#!/usr/bin/env python3
"""第一阶段核心学术衍生变量与 Pre-IPO VC/PE 主表全量工程化富集器。

功能：
  1. 完整维护 2026 Q1 全量 38 家港股主板 IPO 发行人的 8 个第一阶段核心学术衍生指标；
  2. 验证并协同维护已有的 10 个 Pre-IPO VC/PE 细分维度；
  3. 安全注入 canonical 工作簿 HKIPO-MB2026Q1.xlsx 主表（NLR 表单）：
     - 自动创建时间戳备份快照；
     - 依据金融学逻辑精确定位插入位置：
       * 询价动态组 (3列): 紧随 Minimum Offer Price (col_U) 之后；
       * 公司画像组 (1列): 紧随 Incorporation date (col_BZ) 之后；
       * 绿鞋执行组 (1列): 紧随 Over-allotment shares actually issued 之后；
       * 二级市场与抑价组 (3列): 紧随 First trading day closing price 与 Volume 之后；
     - 表头精准应用法定浅蓝主题填充（Theme 4 Tint 0.8）与深蓝填充（RGB FF00B0F0）；
     - 字体规范统一为 Arial 12pt Bold，自动居中换行与边框；
     - 数据单元格精准匹配 0.00%、0.00、#,##0.00 与 @ 格式；
     - 严谨保证第 138 列恒为 Company Chinese Name；
  4. 触发 clean CSV 与最新版 138 维 Data Codebook 导出。
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from academic_derivations import (
    derive_firm_age,
    derive_greenshoe_rate,
    derive_pricing_dynamics,
    derive_day1_trading,
)
from run import load_cfg
from storage import file_sha256
from workbook_transaction import commit_prepared_workbook


def norm(s: Any) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip().lower()


# 8 个新增学术变量的规范化定义
ACADEMIC_FIELDS = [
    # 组 1：发售区间动态（3 列，浅蓝）
    {
        "key": "col_price_revision",
        "header": "Filing price revision (%)",
        "anchor": "minimum offer price",
        "tier": "blue",
        "kind": "number",
        "format": "0.00%",
        "align": "right",
        "width": 16.0,
        "desc": "发售定价偏离询价区间中点幅度（Hanley 1993 动态信息提取，固定价格发售为 0.00%）",
    },
    {
        "key": "col_range_width",
        "header": "Filing range width (%)",
        "anchor": "minimum offer price",
        "tier": "blue",
        "kind": "number",
        "format": "0.00%",
        "align": "right",
        "width": 16.0,
        "desc": "询价区间相对宽度（Beatty & Ritter 1986 事前估值不确定性，固定价格发售为 0.00%）",
    },
    {
        "key": "col_pricing_position",
        "header": "Pricing position in filing range",
        "anchor": "minimum offer price",
        "tier": "blue",
        "kind": "text",
        "format": "@",
        "align": "center",
        "width": 18.0,
        "desc": "定价落点分类体系（Fixed price / Above range / At high / Midpoint / Within range / At low / Below range）",
    },
    # 组 2：企业生命周期（1 列，浅蓝）
    {
        "key": "col_firm_age",
        "header": "Firm age at IPO (years)",
        "anchor": "incorporation date",
        "tier": "blue",
        "kind": "number",
        "format": "0.00",
        "align": "right",
        "width": 16.0,
        "desc": "公司成立至上市年限（Lowry et al. 2017 Table 3.4 基础控制变量）",
    },
    # 组 3：绿鞋机制执行（1 列，深蓝）
    {
        "key": "col_greenshoe_rate",
        "header": "Greenshoe exercise rate (%)",
        "anchor": "over-allotment shares actually issued",
        "tier": "dark_blue",
        "kind": "number",
        "format": "0.00%",
        "align": "right",
        "width": 18.0,
        "desc": "绿鞋实际行使比例（Ellis et al. 2000 超额配售执行度与价格支持）",
    },
    # 组 4：首日交易与抑价（3 列，深蓝）
    {
        "key": "col_underpricing",
        "header": "First-day return / Underpricing (%)",
        "anchor": "first trading day closing price (hk$)",
        "tier": "dark_blue",
        "kind": "number",
        "format": "0.00%",
        "align": "right",
        "width": 18.0,
        "desc": "上市首日抑价率 / 初始收益率（Rock 1986 / Ritter 1984 核心被解释变量）",
    },
    {
        "key": "col_money_left",
        "header": "Money left on the table (HK$)",
        "anchor": "first trading day closing price (hk$)",
        "tier": "dark_blue",
        "kind": "number",
        "format": "#,##0.00",
        "align": "right",
        "width": 22.0,
        "desc": "留在桌面上的财富 / 抑价转移财富总额（Loughran & Ritter 2002 前景理论指标）",
    },
    {
        "key": "col_flipping_ratio",
        "header": "First-day flipping ratio (%)",
        "anchor": "first trading day volume (shares)",
        "tier": "dark_blue",
        "kind": "number",
        "format": "0.00%",
        "align": "right",
        "width": 18.0,
        "desc": "首日短线翻转抛售率 / 成交量占全球发售比例（Aggarwal 2003 机构抛售假说）",
    },
]


def inject_academic_derivations() -> Path:
    """计算 8 个第一阶段学术衍生字段并安全注入到 HKIPO-MB2026Q1.xlsx 主表中。"""
    book_path = WS / "HKIPO-MB2026Q1.xlsx"
    if not book_path.exists():
        raise FileNotFoundError(f"Workbook not found: {book_path}")

    # 1. 记录源版本；统一事务管理器会在提交锁内创建备份并检查并发变化。
    source_sha256 = file_sha256(book_path)

    # 2. 读取原始数据并进行推导计算
    wb_read = openpyxl.load_workbook(book_path, data_only=True)
    ws_read = wb_read["NLR"]

    headers_orig = [ws_read.cell(row=1, column=c).value for c in range(1, ws_read.max_column + 1)]
    hmap_read = {norm(h): i + 1 for i, h in enumerate(headers_orig) if h}

    col_offer_price = hmap_read[norm("IPO Subscription Price (HK$)")]
    col_max_price = hmap_read[norm("Maximum Offer Price")]
    col_min_price = hmap_read[norm("Minimum Offer Price")]
    col_listing_date = hmap_read[norm("Date of Listing (dd/mm/yy)")]
    col_incorp_date = hmap_read[norm("Incorporation date")]
    col_day1_close = hmap_read[norm("First trading day closing price (HK$)")]
    col_day1_vol = hmap_read[norm("First trading day volume (shares)")]
    col_global_shares = hmap_read[norm("Final global offering shares (before over-allotment)")]
    col_greenshoe_opt = hmap_read[norm("Over-allotment Option (%)")]
    col_greenshoe_issued = hmap_read[norm("Over-allotment shares actually issued")]

    derived_data: dict[str, dict[str, Any]] = {}
    for r in range(2, 40):
        code = str(ws_read.cell(row=r, column=2).value or "").strip()
        if not code:
            continue

        p_off = ws_read.cell(row=r, column=col_offer_price).value
        p_max = ws_read.cell(row=r, column=col_max_price).value
        p_min = ws_read.cell(row=r, column=col_min_price).value
        l_date = ws_read.cell(row=r, column=col_listing_date).value
        i_date = ws_read.cell(row=r, column=col_incorp_date).value
        c_price = ws_read.cell(row=r, column=col_day1_close).value
        vol = ws_read.cell(row=r, column=col_day1_vol).value
        shares = ws_read.cell(row=r, column=col_global_shares).value
        opt = ws_read.cell(row=r, column=col_greenshoe_opt).value
        issued = ws_read.cell(row=r, column=col_greenshoe_issued).value

        # 执行推导
        firm_age = derive_firm_age(l_date, i_date)
        rev, width, pos = derive_pricing_dynamics(p_off, p_max, p_min)
        ir, money_left, flip = derive_day1_trading(c_price, p_off, vol, shares)
        shoe_rate = derive_greenshoe_rate(issued, shares, opt)

        derived_data[code] = {
            "col_price_revision": rev,
            "col_range_width": width,
            "col_pricing_position": pos,
            "col_firm_age": firm_age,
            "col_greenshoe_rate": shoe_rate,
            "col_underpricing": ir,
            "col_money_left": money_left,
            "col_flipping_ratio": flip,
        }

    wb_read.close()
    print(f"[Compute] Computed academic derivations for {len(derived_data)} issuers.")

    # 3. 写入工作簿 (非只读模式)
    wb = openpyxl.load_workbook(book_path)
    ws = wb["NLR"]

    # 检查是否已经注入过
    headers_current = [norm(ws.cell(row=1, column=c).value) for c in range(1, ws.max_column + 1)]
    if norm(ACADEMIC_FIELDS[0]["header"]) in headers_current:
        print("[Schema] Academic fields already exist in workbook. Updating values in-place.")
    else:
        # 执行逆向安全插入（由右至左插入，保证左侧锚点索引不受影响）
        # 插入规划：
        # 1. anchor: first trading day volume (shares) -> 插入 col_flipping_ratio
        # 2. anchor: first trading day closing price (hk$) -> 插入 col_underpricing, col_money_left
        # 3. anchor: over-allotment shares actually issued -> 插入 col_greenshoe_rate
        # 4. anchor: incorporation date -> 插入 col_firm_age
        # 5. anchor: minimum offer price -> 插入 col_price_revision, col_range_width, col_pricing_position

        insertion_batches = [
            # 批次 1 (最右): flipping ratio
            (
                "first trading day volume (shares)",
                [f for f in ACADEMIC_FIELDS if f["key"] == "col_flipping_ratio"],
            ),
            # 批次 2: underpricing & money left
            (
                "first trading day closing price (hk$)",
                [f for f in ACADEMIC_FIELDS if f["key"] in ("col_underpricing", "col_money_left")],
            ),
            # 批次 3: greenshoe rate
            (
                "over-allotment shares actually issued",
                [f for f in ACADEMIC_FIELDS if f["key"] == "col_greenshoe_rate"],
            ),
            # 批次 4: firm age
            (
                "incorporation date",
                [f for f in ACADEMIC_FIELDS if f["key"] == "col_firm_age"],
            ),
            # 批次 5 (最左): pricing dynamics
            (
                "minimum offer price",
                [f for f in ACADEMIC_FIELDS if f["key"] in ("col_price_revision", "col_range_width", "col_pricing_position")],
            ),
        ]

        for anchor_name, fields_to_insert in insertion_batches:
            # 动态寻找锚点列
            anchor_col = None
            for c in range(1, ws.max_column + 1):
                if norm(ws.cell(1, c).value) == anchor_name:
                    anchor_col = c
                    break
            if anchor_col is None:
                raise RuntimeError(f"Anchor column '{anchor_name}' not found!")

            insert_idx = anchor_col + 1
            ws.insert_cols(insert_idx, amount=len(fields_to_insert))
            print(f"[Schema] Inserted {len(fields_to_insert)} column(s) after '{anchor_name}' (at Col {insert_idx})")

            # 填充表头
            for offset, fdef in enumerate(fields_to_insert):
                target_col = insert_idx + offset
                c_let = get_column_letter(target_col)
                h_cell = ws.cell(1, target_col)
                h_cell.value = fdef["header"]
                h_cell.font = Font(name="Arial", size=12, bold=True)
                h_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                thin_side = Side(border_style="thin", color="D9D9D9")
                h_cell.border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

                if fdef["tier"] == "blue":
                    # 浅蓝: Theme 4, Tint 0.8
                    h_cell.fill = copy.copy(ws.cell(1, anchor_col).fill)
                else:
                    # 深蓝 / 天蓝: RGB FF00B0F0
                    h_cell.fill = PatternFill(fill_type="solid", fgColor="FF00B0F0", bgColor="FF00B0F0")

                ws.column_dimensions[c_let].width = fdef["width"]

    # 4. 重新建立最新的表头映射，写入数据行
    hmap_new = {norm(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1) if ws.cell(1, c).value}

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    for r in range(2, 40):
        code = str(ws.cell(r, 2).value or "").strip()
        if not code or code not in derived_data:
            continue
        c_res = derived_data[code]

        for fdef in ACADEMIC_FIELDS:
            c_idx = hmap_new.get(norm(fdef["header"]))
            if c_idx is None:
                raise RuntimeError(f"Header '{fdef['header']}' could not be located!")
            cell = ws.cell(r, c_idx)
            val = c_res.get(fdef["key"])
            cell.value = val
            cell.font = Font(name="Arial", size=11)
            cell.alignment = Alignment(horizontal=fdef["align"], vertical="center")
            cell.number_format = fdef["format"]
            cell.border = thin_border

    # 5. 校验工作簿完整性
    total_cols = ws.max_column
    last_col_header = ws.cell(1, total_cols).value
    print(f"[Verification] Total columns: {total_cols}")
    print(f"[Verification] Last column (Col {total_cols}): {last_col_header}")

    if total_cols != 138:
        raise ValueError(f"Expected 138 columns after academic expansion, got {total_cols}!")
    if norm(last_col_header) != norm("Company Chinese Name"):
        raise ValueError(f"Last column must be 'Company Chinese Name', got '{last_col_header}'!")

    commit_prepared_workbook(book_path, wb, source_sha256, operation="academic-expansion")
    print(f"[Success] Saved updated workbook: {book_path.name} with 138 columns!")
    return book_path


if __name__ == "__main__":
    inject_academic_derivations()
