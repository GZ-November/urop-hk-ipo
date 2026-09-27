"""基石投资者「确认不存在」的确定性证据，以及 col_CK 的零值回填。

手册要求「确定的零写 0，不写 NaN」。基石投资者要么在配发结果公告的基石表里出现，
要么在招股书里有专门的 Cornerstone Investors 章节；两者都搜不到，就是确认没有，
col_CK 应填 0。这里把「搜不到」这个事实固化成可复现的记录，而不是让 AI 凭感觉填。

输出 out/allot/cornerstone_absence.json：
  {code: {verdict: none|present, prospectus_hits, prospectus_pages,
          announcement_hits, announcement_pages, sample: [页码...]}}
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from storage import atomic_json, official_files

# 只认「基石投资者」这个意思。单搜 "cornerstone" 会误判修辞用法
# （"the cornerstone of our growth"）和恰好叫这个名字的老股东
# （2729 的 Linghui/Anhui Cornerstone 是 2022 年 E 轮股东，不是 IPO 基石）。
PAT = re.compile(r"cornerstone\s+investor", re.I)
# 配发结果公告里若有基石投资者，会有独立的 CORNERSTONE INVESTORS 章节头。
SECTION = re.compile(r"^\s*CORNERSTONE\s+INVESTORS?\s*$", re.I | re.M)
ZH_PAT = re.compile(r"基石投资者")


def _scan(path: Path) -> tuple[int, int, list[int], int]:
    """返回 (investor 命中次数, 页数, 命中页码样本, 章节头数)。"""
    if not path.exists():
        return -1, 0, [], 0
    hits, pages, where, secs = 0, 0, [], 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            p = json.loads(line)
            pages += 1
            secs += len(SECTION.findall(p["text"]))
            n = len(PAT.findall(p["text"])) + len(ZH_PAT.findall(p["text"]))
            if n:
                hits += n
                where.append(p["page"])
    return hits, pages, where[:8], secs


def assess(cfg: dict, code: str) -> dict:
    """Return present/absent/unknown from the current complete local evidence."""
    digits = "".join(ch for ch in code if ch.isdigit())
    name = f"HKIPO-MB{digits}.jsonl"
    ph, pp, pw, _ = _scan(cfg["paths"]["text"] / name)
    ah, ap, aw, asec = _scan(cfg["paths"]["allot_text"] / name)
    complete = ph >= 0 and ah >= 0 and pp > 0 and ap > 0
    if not complete:
        verdict = "unknown"
    # Announcement prose may mention that a connected placee could also act as
    # a cornerstone investor. Only a dedicated announcement section, or an
    # actual prospectus disclosure, proves that this IPO has cornerstone investors.
    elif ph > 0 or asec > 0:
        verdict = "present"
    else:
        verdict = "absent"
    return {"verdict": verdict, "evidence_complete": complete,
            "prospectus_hits": ph, "prospectus_pages": pp,
            "announcement_hits": ah, "announcement_pages": ap,
            "announcement_sections": asec, "sample_pages": (pw or aw)}


def scan(cfg: dict, only=None, log=print) -> dict:
    out_path = cfg["paths"]["allot_out"] / "cornerstone_absence.json"
    result = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    pdir = cfg["paths"]["text"]
    adir = cfg["paths"]["allot_text"]
    for f in sorted(pdir.glob("HKIPO-MB*.jsonl")):
        digits = f.stem.replace("HKIPO-MB", "")
        code = f"{digits}.HK"
        if only and code not in set(only):
            continue
        result[code] = assess(cfg, code)
        rec = result[code]
        label = {"absent": "无基石", "present": "有基石", "unknown": "证据不完整"}[rec["verdict"]]
        log(f"  {code:9s} 招股书 {rec['prospectus_hits']:5d} 命中/{rec['prospectus_pages']:4d} 页  "
            f"公告 {rec['announcement_hits']:4d} 命中/{rec['announcement_sections']} 章节 -> {label}")
    atomic_json(out_path, result)
    n_none = sum(1 for v in result.values() if v["verdict"] == "absent")
    log(f"基石核实：{len(result)} 家，其中 {n_none} 家确认无基石 -> {out_path}")
    return result


def apply_ck(cfg: dict, only=None, log=print) -> int:
    """把「确认无基石」的 col_CK 写成 0（覆盖 agent 的 NaN）。"""
    out_dir = cfg["paths"]["allot_out"]
    p = out_dir / "cornerstone_absence.json"
    if not p.exists():
        return 0
    ca = json.loads(p.read_text(encoding="utf-8"))
    ext = out_dir / "extracted"
    n = 0
    for code, fp in official_files(ext, only=only).items():
        rec_ca = ca.get(code)
        if (not rec_ca or rec_ca.get("verdict") != "absent"
                or rec_ca.get("evidence_complete") is not True):
            continue
        rec = json.loads(fp.read_text(encoding="utf-8"))
        fields = rec.setdefault("fields", {})
        fields["col_CK"] = {
            "value": 0, "page": None,
            "quote": (f"招股书全文 {rec_ca['prospectus_pages']} 页 0 处「基石投资者」、"
                      f"配发公告 {rec_ca['announcement_pages']} 页 0 个基石章节 "
                      f"-> 确认无基石投资者，按手册填确定的零"),
            "source": "cornerstone_absence", "confidence": "high",
        }
        atomic_json(fp, rec)
        n += 1
    log(f"col_CK 零值回填：{n} 家")
    return n
