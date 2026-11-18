#!/usr/bin/env python3
"""Build blind Haiku review batches for public-offer subscription multiples."""
import json, random, re, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import parse_allotment_subscription as P

ROOT = P.ROOT; OUT = P.OUT / "review"
KW = re.compile(r"valid\s+applications?|subscription\s+level|over-?\s?subscri\w*|under-?\s?subscri\w*|\btimes\b|hong\s*kong\s+public\s+offer\w*|public\s+offer\s+shares", re.I)


def excerpt(t, cap=3400):
    spans = []
    for m in KW.finditer(t):
        a, b = max(0, m.start() - 260), min(len(t), m.end() + 300)
        if spans and a <= spans[-1][1]:
            spans[-1][1] = b
        else:
            spans.append([a, b])
    return " [...] ".join(t[a:b] for a, b in spans)[:cap]


def main():
    d = pd.read_csv(P.OUT / "parsed_subscription.csv")
    n = pd.read_csv(ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False, usecols=["file", "batch", "funds_raised_public_hkd", "retail_sub_ratio_clean"])
    n["key"] = n.file.str.replace(".json", "", regex=False)
    m = n.merge(d, on="key"); m = m[m.batch != "2025-2026"]
    r = (m.parsed - m.retail_sub_ratio_clean).abs() / m.retail_sub_ratio_clean
    arith = m.how == "arithmetic_ok"; acc = arith | (m.parsed.notna() & (r <= .01))
    placing = (m.placing_only == True) & ~(m.funds_raised_public_hkd > 0)
    review = m[(m.allot_chars > 300) & ~acc & ~placing]
    check = m[arith].groupby("batch", group_keys=False).apply(lambda g: g.sample(min(20, len(g)), random_state=20261118))
    keys = [(k, "adjudicate") for k in review.key] + [(k, "holdout") for k in check.key]
    random.seed(20261118); random.shuffle(keys)
    (OUT / "batches").mkdir(parents=True, exist_ok=True); (OUT / "A").mkdir(exist_ok=True)
    json.dump(dict(keys), open(OUT / "roles.json", "w"))
    for i in range(0, len(keys), 25):
        out = []
        for k, _ in keys[i:i + 25]:
            f = next((ROOT / "analysis/out").glob(f"batch[123]_*_packets/{k}.md"))
            out += [f"\n## ISSUER {k}\n```", excerpt(P.section(f.read_text(errors="ignore"))), "```"]
        (OUT / "batches" / f"batch_{i//25+1:03d}.md").write_text("\n".join(out))
    print(len(review), len(check), (len(keys) + 24) // 25)


main()
