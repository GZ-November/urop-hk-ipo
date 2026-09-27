"""4 大正交主题分片 Schema 定义与工具函数。

将 70 个招股书字段无损解耦为 4 个独立正交的主题包：
1. topic_offering: 基础发售与股本结构 (15 字段)
2. topic_financials: 历史财务与核心经营 (30 字段)
3. topic_ownership: 股权治理与特专科技途径 (20 字段)
4. topic_underwriting: 承销银团与基石名单 (5 字段)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TOPIC_DEFINITIONS: dict[str, dict[str, Any]] = {
    "topic_offering": {
        "id": "topic_offering",
        "title": "基础发售与股本结构 (Offering & Share Capital)",
        "description": "股份结构 (L–S/BI/CE)、价格区间 (T–U)、发售时间表 (CC–CD)、公司中文全称 (DP)",
        "groups": ["share_structure", "price", "offering", "chinese_name"],
        "expected_field_count": 15,
        "tools_recommended": ["sharecap"],
        "key_rules": [
            "严格依赖 Share Capital 汇总表，严禁采纳历史沿革中的发行数字",
            "核验 5 个股本恒等式：M=R+S、M=Q+P、L=N+Q、L=O+M",
            "价格区间 T/U 换算为港元原币，U <= T",
            "中文名 DP 必须填简体中文",
        ],
    },
    "topic_financials": {
        "id": "topic_financials",
        "title": "历史财务与核心经营 (Financials & Cash Flows)",
        "description": "三年资产/权益/负债/利润 (V–AN)、附加财务/研发/客户 (AT–AY)、有息负债 (BE)、会计准则 (BT/CF/CG/CH)",
        "groups": ["financials", "extra_financial"],
        "expected_field_count": 30,
        "tools_recommended": ["periods", "table financials"],
        "key_rules": [
            "合并报表唯一原则：严禁引用母公司单体报表（STATEMENT OF FINANCIAL POSITION OF THE COMPANY）",
            "根据 periods 权威判定确定 year-1/2/3；中期非全年销售/利润按系数年化",
            "AU 经营现金流、AW 研发费用、AX 当期资本化新增不年化；AV 年末现金及 BE 为期末余额",
            "AX 资本化研发新增表格明确为 '–'/nil 时填 0，AY 为客户集中度比例",
        ],
    },
    "topic_ownership": {
        "id": "topic_ownership",
        "title": "股权治理与特专科技途径 (Ownership, VC/PE & Route)",
        "description": "控股股东与投票权 (BB–BD)、成立日 (BP)、注册地 (BR)、VC/PE 投资体系 (BA 及细分)、业务与上市途径 (AR/AS/BF/BG)",
        "groups": ["ownership", "business"],
        "expected_field_count": 20,
        "tools_recommended": ["table sharecap"],
        "key_rules": [
            "col_AS 必须按招股书 basis of listing / 适用章节填写（如 Chapter 18C），不得主观猜测",
            "col_BP 必须引用公司法律成立条款（Incorporation/Establishment），不得引用定义页或前瞻事件",
            "col_BA 仅代表上市前是否有 VC/PE 投资机构入股；基石投资者身份本身不构成 BA",
            "BC/BD 分别为控股股东在上市时的经济权益与投票权百分比",
        ],
    },
    "topic_underwriting": {
        "id": "topic_underwriting",
        "title": "承销银团与基石名单 (Underwriting & Cornerstone)",
        "description": "承销佣金率 (AO/AP)、绿鞋上限 (AQ)、上市费用 (CI)、基石投资者名单全称 (CJ)",
        "groups": ["underwriting", "cornerstone"],
        "expected_field_count": 5,
        "tools_recommended": ["table cornerstone"],
        "key_rules": [
            "招股书按全球发售披露佣金时 AO=AP；仅按香港公开发售披露时 AP=0；不能将总上市费用当佣金",
            "AQ 绿鞋超额配售权只能按披露填写，不得默认 15%",
            "CJ 基石名单必须来自真正的 Cornerstone Placing 协议名单表，分号分隔全称；无基石填 NA",
        ],
    },
}

TOPIC_KEYS = list(TOPIC_DEFINITIONS.keys())


def get_topic_definition(topic_id: str) -> dict[str, Any]:
    if topic_id not in TOPIC_DEFINITIONS:
        raise KeyError(f"Unknown topic_id '{topic_id}'. Valid topics: {TOPIC_KEYS}")
    return TOPIC_DEFINITIONS[topic_id]


def get_topic_fields(topic_id: str, fields: list[dict]) -> list[dict]:
    defn = get_topic_definition(topic_id)
    groups = set(defn["groups"])
    return [f for f in fields if f.get("group") in groups]


def get_field_to_topic_map(fields: list[dict]) -> dict[str, str]:
    group_to_topic = {}
    for tid, defn in TOPIC_DEFINITIONS.items():
        for g in defn["groups"]:
            group_to_topic[g] = tid

    mapping = {}
    for f in fields:
        g = f.get("group")
        if g not in group_to_topic:
            raise ValueError(f"Field {f.get('key')} has unmapped group '{g}'")
        mapping[f["key"]] = group_to_topic[g]
    return mapping


def validate_topic_completeness(fields: list[dict]) -> dict[str, int]:
    """验证 4 个主题分片严格划分且覆盖全部字段，无遗漏、无重叠。"""
    all_keys = {f["key"] for f in fields}
    covered_keys = set()
    counts = {}

    for tid, defn in TOPIC_DEFINITIONS.items():
        t_fields = get_topic_fields(tid, fields)
        t_keys = {f["key"] for f in t_fields}
        overlap = covered_keys & t_keys
        if overlap:
            raise ValueError(f"Topic {tid} has overlapping fields with previous topics: {overlap}")
        expected = defn["expected_field_count"]
        if len(t_fields) != expected:
            raise ValueError(f"Topic {tid} has {len(t_fields)} fields, expected {expected}")
        covered_keys |= t_keys
        counts[tid] = len(t_fields)

    missing = all_keys - covered_keys
    if missing:
        raise ValueError(f"Missing fields not covered by any topic: {missing}")

    return counts
