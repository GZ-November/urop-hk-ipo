#!/usr/bin/env python3
"""Combine prospectus and allotment evidence into a cornerstone status for each IPO."""
import glob, json, re, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import parse_allotment_subscription as P

R = P.OUT
CS = re.compile(r"(?i:corner\s*stone\s+(?:investor|placing|subscription|tranche|investment))|\b(?:[Tt]he|[Oo]ur)\s+Corporate\s+(?:Investors?|Placing)\b")
BOILER = re.compile(r"(investment\s+commitments?\s+by\s+any|commitments?\s+(?:of|by)\s+(?:any\s+)?(?:the\s+)?corner\s*stone|no\s+corner\s*stone|not\s+(?:have|has|had)\s+(?:any\s+)?corner\s*stone|without\s+(?:any\s+)?corner\s*stone|(?:any|if)\s+corner\s*stone|other\s+than\s+(?:the\s+)?corner\s*stone\s+investors?\s*,?\s+if)", re.I)


def allot(key):
    fs = list((P.ROOT / "analysis/out").glob(f"batch[123]_*_packets/{key}.md"))
    if not fs:
        return 0, 0, 0, ""
    t = P.section(fs[0].read_text(errors="ignore"))
    pos, boil, q = 0, 0, ""
    for m in CS.finditer(t):
        w = t[max(0, m.start() - 90):m.end() + 90]
        if BOILER.search(w):
            boil += 1
        else:
            pos += 1
            q = q or t[max(0, m.start() - 200):m.end() + 240]
    return len(t), pos, boil, q


def main():
    sec = {json.loads(l)["key"]: json.loads(l) for l in open(R / "cornerstone_sections.jsonl")}
    ev = {json.loads(l)["key"]: json.loads(l) for l in open(R / "cornerstone_evidence.jsonl")}
    n = pd.read_csv(P.ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False, usecols=["file", "batch", "ext_has_cornerstone", "ext_cornerstone_pct", "col_CK__quote"])
    n["key"] = n.file.str.replace(".json", "", regex=False)
    rows = []
    for _, r in n[n.batch != "2025-2026"].iterrows():
        k = r.key; e = ev.get(k, {}); s = sec.get(k, {})
        chars, pos, boil, q = allot(k)
        ctx = s.get("ctx", []); real = [c for c in ctx if not BOILER.search(c)]
        sec_hit = bool(e.get("section_hit")); hits = s.get("hits", 0); scanned = s.get("files", 0) > 0
        if sec_hit or pos >= 1 or len(real) >= 1 and hits >= 3:
            st = "yes"
        elif real or (hits and not ctx):
            st = "review"
        elif scanned and chars > 300:
            st = "no"
        elif scanned:
            st = "no_prospectus_only"
        elif chars > 300:
            st = "no_allotment_only"
        else:
            st = "unknown"
        rows.append(dict(key=k, status=st, section=sec_hit, prospectus_hits=hits, allot_chars=chars, allot_pos=pos, allot_boiler=boil, quote=(q or (real[0] if real else ""))[:500]))
    d = pd.DataFrame(rows); d.to_csv(R / "cornerstone_status.csv", index=False)
    m = n.merge(d, on="key"); m["old"] = m.ext_has_cornerstone.fillna(-1)
    print(pd.crosstab(m.status, m.old, margins=True).to_string())
    print(pd.crosstab(m.status, m.batch).to_string())


if __name__ == "__main__":
    main()
