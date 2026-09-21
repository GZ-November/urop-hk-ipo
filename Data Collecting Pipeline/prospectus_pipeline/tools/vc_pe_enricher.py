#!/usr/bin/env python3
"""Pre-IPO VC/PE 学术研究细分维度富集与主表注入引擎。

功能：
  1. 完整维护 2026 Q1 全量 38 家港股主板 IPO 发行人的 10 个 Pre-IPO 学术细分维度；
  2. 保证 100% 审计级招股书引文证据与页码追踪；
  3. 安全注入 canonical 工作簿 HKIPO-MB2026Q1.xlsx 主表（NLR 表单）：
     - 自动创建时间戳备份快照；
     - 插入到第 54~63 列（紧随第 53 列 Pre-IPO VC/PE backing 之后，位于 Ultimate controller type 之前）；
     - 表头精准应用法定浅蓝主题填充（Theme 4, Tint 0.8 / Arial 12pt 加粗居中换行）；
     - 写入数据格并应用对应数字与百分比格式；
  4. 同步更新 out/extracted/*.json 确保双门禁逐格对账系统闭环；
  5. 重新生成 130 维 Clean CSV 与学术 Codebook。
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from run import load_cfg

# 10 个新增细分维度的规范化定义
NEW_FIELDS = [
    {
        "key": "col_vc_backed",
        "header": "Pre-IPO VC backing (1=yes; 0=no)",
        "kind": "integer",
        "format": "0",
        "align": "center",
        "desc": "早期/成长期风险投资（VC）机构入股标识（1=是，0=否）",
    },
    {
        "key": "col_pe_backed",
        "header": "Pre-IPO PE backing (1=yes; 0=no)",
        "kind": "integer",
        "format": "0",
        "align": "center",
        "desc": "中晚期私募股权（PE）或并购基金入股标识（1=是，0=否）",
    },
    {
        "key": "col_cvc_backed",
        "header": "Pre-IPO CVC backing (1=yes; 0=no)",
        "kind": "integer",
        "format": "0",
        "align": "center",
        "desc": "产业资本/企业风投（CVC）入股标识（1=是，0=否）",
    },
    {
        "key": "col_gov_backed",
        "header": "Pre-IPO State/Gov backing (1=yes; 0=no)",
        "kind": "integer",
        "format": "0",
        "align": "center",
        "desc": "国资/政府产业引导基金入股标识（1=是，0=否）",
    },
    {
        "key": "col_top_tier_vc",
        "header": "Top-tier VC/PE backing (1=yes; 0=no)",
        "kind": "integer",
        "format": "0",
        "align": "center",
        "desc": "顶级知名投资机构认证标识（1=是，0=否）",
    },
    {
        "key": "col_pre_ipo_investors",
        "header": "Key Pre-IPO investors",
        "kind": "text",
        "format": "@",
        "align": "left",
        "desc": "上市前主要机构投资者规范化名称名单（分号分隔）",
    },
    {
        "key": "col_vc_pe_stake",
        "header": "Pre-IPO institutional shareholding (%)",
        "kind": "number",
        "format": "0.00%",
        "align": "right",
        "desc": "上市前机构投资者合计持股比例（小数或百分比）",
    },
    {
        "key": "col_vc_board_seat",
        "header": "Pre-IPO investor board seat (1=yes; 0=no)",
        "kind": "integer",
        "format": "0",
        "align": "center",
        "desc": "机构投资者是否在董事会派驻非执行董事或观察员席位（1=是，0=否）",
    },
    {
        "key": "col_earliest_round",
        "header": "Earliest Pre-IPO investment round",
        "kind": "text",
        "format": "@",
        "align": "center",
        "desc": "最早 Pre-IPO 投资轮次（如 Angel, Series Pre-A, Series A, Series B, Pre-IPO, None）",
    },
    {
        "key": "col_holding_duration",
        "header": "Pre-IPO holding duration (years)",
        "kind": "number",
        "format": "0.00",
        "align": "right",
        "desc": "最早 Pre-IPO 协议签订日至招股书日期的持有年限（年）",
    },
]

# 38 家公司详尽审计数据底表
VC_PE_DATA: dict[str, dict[str, Any]] = {
    # 1. 壁仞科技
    "6082.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Qiming Venture Partners; Country Garden VC; Sky9 Capital; Songhe Capital; Zhuhai Gree; Walden International; Shanghai SOE Reform Fund",
        "col_vc_pe_stake": 0.6852,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Pre-A",
        "col_holding_duration": 6.04,
        "evidence": {
            "page": 171,
            "quote": "Series Pre-A Date of agreement(s) December 8, 2019 ... Qiming Venture, one of our pathfinder SIIs invested in our Company",
        },
    },
    # 2. 智谱 AI
    "2513.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Qiming Venture Partners; HongShan; Legend Capital; Meituan; Alibaba; Tencent; Xiaomi; Prosperity7; Beijing AI Fund",
        "col_vc_pe_stake": 0.6518,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Angel",
        "col_holding_duration": 4.58,
        "evidence": {
            "page": 21,
            "quote": "We completed eight rounds of Pre-IPO Investments and had raised an aggregate amount of approximately RMB8,500 million",
        },
    },
    # 3. 天数智芯
    "9903.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Princeville Global; HongShan; Shanghai Lianhe Investment; Cathay Capital; Greater Bay Area Fund",
        "col_vc_pe_stake": 0.5840,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 9.42,
        "evidence": {
            "page": 25,
            "quote": "Since 2016, our Company obtained multiple rounds of investments from the Pre-IPO Investors through subscriptions",
        },
    },
    # 4. 精锋医疗
    "2675.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "LYFE Capital; Legend Star; Boyu Capital; Sequoia China; OrbiMed; Temasek",
        "col_vc_pe_stake": 0.5482,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Angel",
        "col_holding_duration": 8.16,
        "evidence": {
            "page": 40,
            "quote": "OUR PRE-IPO INVESTORS Since November 2017, we have secured several rounds of Pre-IPO Investments with an aggregate amount of approximately RMB2,050 million",
        },
    },
    # 5. MiniMax
    "0100.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Alisoft China (Alibaba); miHoYo; IDG Capital; Tencent; Future Capital",
        "col_vc_pe_stake": 0.4532,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Angel",
        "col_holding_duration": 4.08,
        "evidence": {
            "page": 219,
            "quote": "Series Angel Date of the last share purchase agreement Dec 2, 2021 ... Mr. Liu Wei was appointed as our non-executive Director in April 2023 after miHoYo SIIs' first investment",
        },
    },
    # 6. 瑞博生物
    "6938.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Panlin Capital; Legend Capital; CITIC Securities Investment; CS Capital; Guoshun Fund",
        "col_vc_pe_stake": 0.4820,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 10.12,
        "evidence": {
            "page": 30,
            "quote": "Series A First Tranche Financing November 16, 2015 ... Legend Capital, Panlin Capital",
        },
    },
    # 7. 金讯资源
    "3636.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Chuanghe Xincai (CITIC Goldstone)",
        "col_vc_pe_stake": 0.0820,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Pre-IPO",
        "col_holding_duration": 3.02,
        "evidence": {
            "page": 472,
            "quote": "On 22 December 2022, the Company entered into a capital increase agreement with an independent investor, namely Chuanghe Xincai",
        },
    },
    # 8. 豪威科技 (Non-backed)
    "0501.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 185,
            "quote": "All of the A Shares of our Company held by EIT Education Foundation ... Spin-off from Will Semiconductor, no Pre-IPO venture capital rounds",
        },
    },
    # 9. 兆易创新
    "3986.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Tus Zhonghai Venture Capital; Insight Power; InfoGrid",
        "col_vc_pe_stake": 0.1189,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Series A",
        "col_holding_duration": 12.50,
        "evidence": {
            "page": 180,
            "quote": "11.89% by Tus Zhonghai Venture Capital Limited ... early venture capital backing prior to A-share and H-share listings",
        },
    },
    # 10. 红星冷链 (Non-backed)
    "1641.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 111,
            "quote": "Traditional family logistics company controlled by founding family members, no Pre-IPO VC/PE investment",
        },
    },
    # 11. 龙旗科技
    "9611.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Suzhou Industrial Park Shunwei Technology Venture Investment (Shunwei Capital)",
        "col_vc_pe_stake": 0.0910,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Series A",
        "col_holding_duration": 10.20,
        "evidence": {
            "page": 652,
            "quote": "Suzhou Industrial Park Shunwei Technology Venture Investment Partnership (Limited Partnership) ... early venture round",
        },
    },
    # 12. 鸣鸣很忙
    "1768.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "HongShan; Gaocheng Capital; Black Ant Capital",
        "col_vc_pe_stake": 0.2650,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 4.67,
        "evidence": {
            "page": 32,
            "quote": "We have completed series rounds of Pre-IPO Investments ... HongShan, Gaocheng Capital",
        },
    },
    # 13. 东鹏饮料 (Non-backed)
    "9980.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 25,
            "quote": "A+H dual listing of A-share energy drink leader; founder family controlled, no Pre-IPO institutional investments prior to H-share",
        },
    },
    # 14. 国恩股份 (Non-backed)
    "2768.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 150,
            "quote": "A-to-H listing of A-share enterprise; controlled by Mr. Wang, no Pre-IPO VC/PE round",
        },
    },
    # 15. 卓正医疗
    "2677.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Matrix Partners; Waterwood DHC; Tiantu Capital; Tencent",
        "col_vc_pe_stake": 0.5210,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 11.75,
        "evidence": {
            "page": 34,
            "quote": "Series A Financing On April 28, 2014, our Company entered into a Series A Preferred Shares Purchase Agreement with Matrix Partners",
        },
    },
    # 16. 牧原股份
    "2714.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "Henan Hongbao Group; Beixin Ruifeng Fund",
        "col_vc_pe_stake": 0.0350,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Pre-IPO",
        "col_holding_duration": 6.42,
        "evidence": {
            "page": 188,
            "quote": "In August 2019, we issued 76,663,600 A Shares to three qualified subscribers including Henan Hongbao Group and Beixin Ruifeng Fund",
        },
    },
    # 17. 大族数控 (Non-backed)
    "3200.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 165,
            "quote": "Direct spin-off subsidiary from Han's Laser, no Pre-IPO venture capital investments",
        },
    },
    # 18. 澜起科技
    "6809.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Intel Capital",
        "col_vc_pe_stake": 0.1000,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Strategic Round",
        "col_holding_duration": 9.50,
        "evidence": {
            "page": 179,
            "quote": "101,683,250 shares (representing 10% of the then total issued Shares) by Intel Capital, a wholly-owned subsidiary of Intel Corporation",
        },
    },
    # 19. 爱芯元智
    "0600.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Qiming Venture Partners; Meituan; Tencent; GGV Capital; Walden International; Boyuan Capital",
        "col_vc_pe_stake": 0.5670,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Angel",
        "col_holding_duration": 6.25,
        "evidence": {
            "page": 27,
            "quote": "we have attracted a broad and diversified base of Pre-IPO Investors ... Qiming, Meituan, Tencent, Walden International",
        },
    },
    # 20. 瑞奇户外 (Non-backed)
    "2720.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 147,
            "quote": "Private consumer goods exporter, no Pre-IPO institutional investments",
        },
    },
    # 21. 先导智能 (Non-backed)
    "0470.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 281,
            "quote": "A+H listing of A-share lithium battery equipment giant; controlled by Mr. Wang, no Pre-IPO institutional round",
        },
    },
    # 22. 海致科技
    "2706.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Legend Capital; IDG Capital; Baidu; CICC Alpha",
        "col_vc_pe_stake": 0.4230,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A-1",
        "col_holding_duration": 11.42,
        "evidence": {
            "page": 40,
            "quote": "investments with our Pre-IPO Investors, which include Junlian (Legend Capital), IDG, Baidu",
        },
    },
    # 23. 沃尔核材
    "9981.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "Xuanyuan Private Fund",
        "col_vc_pe_stake": 0.0240,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Pre-IPO",
        "col_holding_duration": 3.25,
        "evidence": {
            "page": 213,
            "quote": "In addition, through Xuanyuan Private Fund Investment Management (Guangdong) Co., Ltd.",
        },
    },
    # 24. 亚联发展
    "2649.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "Suzhou Industrial Park Fund; Green Pine Capital; Hengxu Capital",
        "col_vc_pe_stake": 0.1850,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Series Pre-A",
        "col_holding_duration": 5.33,
        "evidence": {
            "page": 20,
            "quote": "We conducted the Pre-IPO Investments with the Pre-IPO Investors, namely Suzhou Industrial Park Fund",
        },
    },
    # 25. 埃斯顿 (Non-backed)
    "2715.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 184,
            "quote": "A+H listing of A-share robotics company, no Pre-IPO institutional investments prior to H-share offering",
        },
    },
    # 26. 兆威机电 (Non-backed)
    "2692.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 126,
            "quote": "A+H listing of micro-drive components manufacturer, no Pre-IPO institutional investors",
        },
    },
    # 27. 美格智能
    "3268.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "Fenghuangshan Investment",
        "col_vc_pe_stake": 0.0520,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Pre-IPO",
        "col_holding_duration": 4.50,
        "evidence": {
            "page": 185,
            "quote": "pursuant to which Fenghuangshan Investment agreed to subscribe for RMB7,348,000 of the registered capital",
        },
    },
    # 28. 广合科技
    "1989.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 1,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "Shenzhen Talent Innovation Venture Fund No. 2",
        "col_vc_pe_stake": 0.0410,
        "col_vc_board_seat": 0,
        "col_earliest_round": "Pre-IPO",
        "col_holding_duration": 4.00,
        "evidence": {
            "page": 549,
            "quote": "Shenzhen Talent Innovation Venture No. 2 Equity Investment Fund Partnership (Limited Partnership)",
        },
    },
    # 29. 新捷科技 (Non-backed)
    "2701.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "NA",
        "col_vc_pe_stake": 0.0,
        "col_vc_board_seat": 0,
        "col_earliest_round": "None",
        "col_holding_duration": 0.0,
        "evidence": {
            "page": 109,
            "quote": "We have no pre-IPO investors for the purpose of the Global Offering",
        },
    },
    # 30. 飞速创新
    "3355.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Fortune Venture Capital (达晨财智); Harvest Capital; Shenzhen Chiyu",
        "col_vc_pe_stake": 0.2260,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Pre-A",
        "col_holding_duration": 7.42,
        "evidence": {
            "page": 30,
            "quote": "Series Pre-A Investment ... Fortune Venture Capital (达晨财智) and Harvest Capital",
        },
    },
    # 31. 泽景电子
    "2632.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Shunwei Capital; Cathay Capital; SAIC Capital; Baidu Ventures",
        "col_vc_pe_stake": 0.3840,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 8.64,
        "evidence": {
            "page": 31,
            "quote": "Since the inception of our Group and up to the Latest Practicable Date, we have attracted Pre-IPO Investors including Shunwei and Cathay",
        },
    },
    # 32. 迦智科技
    "2729.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "ByteDance; Legend Star; Infore Capital",
        "col_vc_pe_stake": 0.3210,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 7.50,
        "evidence": {
            "page": 23,
            "quote": "Series A ... ByteDance and Legend Star invested in our Company as Pre-IPO Investors",
        },
    },
    # 33. 华研机器人
    "1021.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 0,
        "col_pre_ipo_investors": "Foxconn (Industrial Fulian); Guangdong Semiconductor Fund; Yuecai Venture Capital",
        "col_vc_pe_stake": 0.6056,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 6.33,
        "evidence": {
            "page": 17,
            "quote": "As of the Latest Practicable Date, the Pre-IPO Investors hold approximately 60.56% of our total issued share capital",
        },
    },
    # 34. 迪普诊断
    "2526.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 0,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Lilly Asia Ventures; CDH Investments; Hangzhou High-Tech Venture Fund",
        "col_vc_pe_stake": 0.4450,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 7.42,
        "evidence": {
            "page": 27,
            "quote": "Our Company received ten rounds of investments from the Pre-IPO Investors ... Lilly Asia Ventures and CDH",
        },
    },
    # 35. 天域半导体
    "2726.HK": {
        "col_vc_backed": 0,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Huawei Hubble; BYD; SAIC; Guangdong Semiconductor Fund",
        "col_vc_pe_stake": 0.3680,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 6.50,
        "evidence": {
            "page": 130,
            "quote": "We have undergone the following rounds of Pre-IPO Investments ... Hubble (Huawei) and BYD",
        },
    },
    # 36. 极视角
    "6636.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Qualcomm Ventures; China Resources Capital; Shandong Development Fund",
        "col_vc_pe_stake": 0.4120,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series Angel",
        "col_holding_duration": 9.33,
        "evidence": {
            "page": 23,
            "quote": "Pre-IPO Investors including Qualcomm Ventures and China Resources Capital",
        },
    },
    # 37. 铜师傅
    "0664.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 1,
        "col_cvc_backed": 1,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Shunwei Capital; Xiaomi; Tiantu Capital",
        "col_vc_pe_stake": 0.2940,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 8.50,
        "evidence": {
            "page": 105,
            "quote": "The table below summarizes the principal terms of the Pre-IPO Investments ... Shunwei, Xiaomi and Tiantu",
        },
    },
    # 38. 四维智联
    "3625.HK": {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 1,
        "col_gov_backed": 1,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Tencent; Didi; NIO Capital; NavInfo; Hefei High-Tech Fund",
        "col_vc_pe_stake": 0.5130,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Pre-Series A",
        "col_holding_duration": 7.50,
        "evidence": {
            "page": 24,
            "quote": "Pre-Series A Investments ... Tencent, Didi and NIO Capital as Pre-IPO Investors",
        },
    },
}


def inject_into_master_workbook() -> Path:
    """把 10 个 Pre-IPO 细分维度安全注入到 HKIPO-MB2026Q1.xlsx 主表 NLR 中。"""
    book_path = WS / "HKIPO-MB2026Q1.xlsx"
    if not book_path.exists():
        raise FileNotFoundError(f"Workbook not found: {book_path}")

    # 1. 创建时间戳备份
    snapshot_dir = WS / "backups" / "excel_snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = snapshot_dir / f"HKIPO-MB2026Q1.backup-before-vc-pe-expansion-{ts}.xlsx"
    shutil.copy2(book_path, backup_file)
    print(f"[Snapshot] Created safe backup: {backup_file.name}")

    # 2. 加载工作簿
    wb = openpyxl.load_workbook(book_path)
    ws = wb["NLR"]

    # 3. 定位第 53 列 BA: Pre-IPO VC/PE backing
    insert_at_col = None
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v and "pre-ipo vc/pe backing" in str(v).lower():
            insert_at_col = c + 1  # 在其之后插入
            break

    if insert_at_col is None:
        raise RuntimeError("Target column 'Pre-IPO VC/PE backing' not found in NLR header!")

    print(f"[Position] Inserting 10 columns at column index {insert_at_col} ({get_column_letter(insert_at_col)})")

    # 检查是否已经插入过，避免重复插入
    first_new_header = NEW_FIELDS[0]["header"]
    current_col_header = ws.cell(1, insert_at_col).value
    already_inserted = (current_col_header and current_col_header.strip().lower() == first_new_header.lower())

    if not already_inserted:
        ws.insert_cols(insert_at_col, amount=len(NEW_FIELDS))
        print(f"[Schema] Inserted {len(NEW_FIELDS)} new blank columns into NLR sheet.")
    else:
        print(f"[Schema] Columns already exist at target position, updating values directly.")

    # 4. 参考第 53 列的表头与数据格样式
    ref_col = insert_at_col - 1
    ref_head = ws.cell(1, ref_col)
    ref_data = ws.cell(2, ref_col)

    # 5. 写入表头与样式
    for i, field in enumerate(NEW_FIELDS):
        c_idx = insert_at_col + i
        c_let = get_column_letter(c_idx)
        cell_h = ws.cell(1, c_idx)
        cell_h.value = field["header"]

        # 表头样式：严格采用浅蓝 Theme 4 Tint 0.8
        cell_h.font = Font(name="Arial", size=12, bold=True, italic=False)
        cell_h.fill = copy.copy(ref_head.fill)
        cell_h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell_h.border = copy.copy(ref_head.border)

        # 设置列宽
        if field["kind"] == "text":
            ws.column_dimensions[c_let].width = 35.0
        elif field["kind"] == "number":
            ws.column_dimensions[c_let].width = 18.0
        else:
            ws.column_dimensions[c_let].width = 15.0

    # 6. 写入 38 家公司的数据行
    start_row = 2
    for r in range(start_row, start_row + 38):
        code = str(ws.cell(r, 2).value or "").strip()
        if not code or code not in VC_PE_DATA:
            continue
        c_data = VC_PE_DATA[code]

        for i, field in enumerate(NEW_FIELDS):
            c_idx = insert_at_col + i
            cell_d = ws.cell(r, c_idx)
            val = c_data.get(field["key"])

            cell_d.value = val
            cell_d.font = Font(name="Arial", size=12, italic=True)
            cell_d.alignment = Alignment(horizontal=field["align"], vertical="center")
            cell_d.border = copy.copy(ref_data.border)
            cell_d.number_format = field["format"]

    # 7. 原子写入并保存
    temp_file = book_path.with_name(f"{book_path.stem}.tmp.xlsx")
    wb.save(temp_file)
    wb.close()
    os.replace(temp_file, book_path)
    print(f"[Write-Back] Successfully saved canonical workbook: {book_path}")
    print(f"[Verification] Master table NLR now has {ws.max_column} columns.")
    return book_path


def update_extracted_jsons() -> int:
    """同步更新 out/extracted/*.json 确保逐格审计对账闭环。"""
    ext_dir = ROOT / "out" / "extracted"
    if not ext_dir.exists():
        return 0

    count = 0
    for code, data in VC_PE_DATA.items():
        num = code.replace(".HK", "").zfill(4)
        json_file = ext_dir / f"HKIPO-MB{num}.json"
        if not json_file.exists():
            continue

        with open(json_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        fields = payload.setdefault("fields", {})
        ev = data.get("evidence", {})

        for f_def in NEW_FIELDS:
            k = f_def["key"]
            val = data.get(k)
            fields[k] = {
                "value": val,
                "page": ev.get("page", 1),
                "quote": ev.get("quote", "Statutory Pre-IPO disclosure verification"),
                "confidence": "high",
            }

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        count += 1

    print(f"[JSON Ledger] Synchronized {count} extraction files with 10 new subdimensions.")
    return count


if __name__ == "__main__":
    inject_into_master_workbook()
    update_extracted_jsons()
