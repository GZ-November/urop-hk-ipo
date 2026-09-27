"""确定性多主题分片抽取结果合并引擎 (Topic Merge Engine)。

将 4 个正交主题分片（topic_offering, topic_financials, topic_ownership, topic_underwriting）
的独立抽取结果安全、确定性地合并为满足 contracts.py 要求的统一招股书抽取 JSON。

执行严格校验：
1. 校验公司代码一致性与主题覆盖完整性；
2. 校验字段键名正交性，严防交叉覆盖；
3. 校验 70 个字段无遗漏、无多余；
4. 调用 contracts.validate_record 进行结构与证据链最终自检；
5. 原子写盘至 out/extracted/{safe_code}.json。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from contracts import (
    normalize_code,
    strict_loads,
    validate_record,
)
from storage import atomic_json
from topic_schema import (
    TOPIC_DEFINITIONS,
    TOPIC_KEYS,
    get_field_to_topic_map,
    get_topic_fields,
    validate_topic_completeness,
)


def _safe_name(code: str) -> str:
    return "HKIPO-MB" + "".join(ch for ch in code if ch.isdigit())


def merge_topic_records(
    topic_records: list[dict[str, Any]],
    fields_schema: list[dict[str, Any]],
) -> dict[str, Any]:
    """将多个分片抽取记录合并为一个完整记录。"""
    if not topic_records:
        raise ValueError("topic_records 为空，无法执行合并")

    codes = {normalize_code(r.get("code")) for r in topic_records if r.get("code")}
    if len(codes) != 1:
        raise ValueError(f"分片记录中包含不一致的公司代码: {codes}")
    unified_code = list(codes)[0]

    all_schema_keys = {f["key"] for f in fields_schema}
    key_to_topic = get_field_to_topic_map(fields_schema)

    merged_fields: dict[str, Any] = {}
    seen_keys_by_topic: dict[str, set[str]] = {}

    for rec in topic_records:
        r_fields = rec.get("fields", {})
        topic_id = rec.get("topic")

        for key, entry in r_fields.items():
            if key not in all_schema_keys:
                raise ValueError(f"未知字段 '{key}' 不属于招股书 schema 规范")

            expected_topic = key_to_topic[key]
            if topic_id and topic_id != expected_topic:
                raise ValueError(
                    f"字段 '{key}' 属于主题 '{expected_topic}'，但在主题 '{topic_id}' 的分片中出现"
                )

            if key in merged_fields:
                prev_val = merged_fields[key].get("value")
                curr_val = entry.get("value") if isinstance(entry, dict) else None
                if prev_val != curr_val:
                    raise ValueError(
                        f"主题合并冲突：字段 '{key}' 在不同分片中值不一致 ('{prev_val}' vs '{curr_val}')"
                    )

            merged_fields[key] = entry
            if topic_id:
                seen_keys_by_topic.setdefault(topic_id, set()).add(key)

    # 检查是否 70 字段齐全
    missing = all_schema_keys - set(merged_fields.keys())
    if missing:
        raise ValueError(
            f"合并失败：尚缺失 {len(missing)} 个字段: {sorted(missing)[:10]}..."
        )

    merged_record = {
        "code": unified_code,
        "fields": merged_fields,
    }

    # 严格运行 contracts 结构检验
    schema_dict = {"fields": fields_schema} if isinstance(fields_schema, list) else fields_schema
    issues = validate_record(merged_record, schema_dict)
    if issues:
        err_msg = "\n".join(str(i) for i in issues)
        raise ValueError(f"合并结果未能通过 contracts 校验:\n{err_msg}")

    return merged_record


def merge_topic_files(
    topic_files: list[Path],
    fields_schema: list[dict[str, Any]],
    out_path: Path | None = None,
) -> dict[str, Any]:
    """从分片文件读取并合并。"""
    records = []
    for fp in topic_files:
        if not fp.exists():
            raise FileNotFoundError(f"分片文件不存在: {fp}")
        rec = strict_loads(fp.read_text(encoding="utf-8"), str(fp))
        # 若文件内未写明 topic，可从文件名推断
        if "topic" not in rec:
            for tid in TOPIC_KEYS:
                if tid in fp.name:
                    rec["topic"] = tid
                    break
        records.append(rec)

    merged = merge_topic_records(records, fields_schema)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path, merged)

    return merged


def merge_topics_for_code(cfg: dict, code: str, log=print) -> Path | None:
    """按指定股票代码在 cfg 目录下查找分片并执行合并。"""
    schema_path = cfg["_root"] / "schema" / "fields.json"
    fields_schema = json.loads(schema_path.read_text(encoding="utf-8"))["fields"]

    safe = _safe_name(code)
    # 查找候选分片目录
    topics_dir = cfg["paths"]["out"] / "extracted_topics"
    if not topics_dir.exists():
        topics_dir = cfg["paths"]["out"] / "extracted"

    files = []
    for tid in TOPIC_KEYS:
        candidate = topics_dir / f"{safe}-{tid}.json"
        if candidate.exists():
            files.append(candidate)
        else:
            # 兼容别名
            alt = topics_dir / f"{safe}_{tid}.json"
            if alt.exists():
                files.append(alt)

    if len(files) != len(TOPIC_KEYS):
        log(f"[{code}] 分片文件不完整：找到 {len(files)}/{len(TOPIC_KEYS)} 个")
        return None

    dest = cfg["paths"]["out"] / "extracted" / f"{safe}.json"
    merge_topic_files(files, fields_schema, out_path=dest)
    log(f"[{code}] 成功合并 4 大主题分片 -> {dest}")
    return dest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="合并主题分片 JSON")
    parser.add_argument("--code", required=True, help="股票代码 (如 6082.HK)")
    args = parser.parse_args()

    # 寻找 root
    root = Path(__file__).resolve().parent.parent
    ws = root.parent
    import yaml
    with open(root / "config.yaml") as f:
        cfg = yaml.safe_load(f)
    cfg["_root"] = root
    cfg["_ws"] = ws
    for k, v in cfg["paths"].items():
        cfg["paths"][k] = ws / v

    merge_topics_for_code(cfg, args.code)
