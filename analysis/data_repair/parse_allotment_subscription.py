#!/usr/bin/env python3
"""Read the public-tranche subscription multiple from cached allotment announcements."""
import glob, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis/out/subscription_cornerstone_repair"
PUB = r"hong\s*kong\s+public\s+offer\w*|public\s+offer\w*|hong\s*kong\s+offer\w*|public\s+subscription|hong\s*kong\s+tranche|public\s+tranche"
INST = r"international\s+(?:offer\w*|placing|tranche)|\bplacing\b|placees?|preferential\s+offer\w*|employee|reserved\s+shares|bank\s+of\s+china\s+group"
NUM = re.compile(r"(?<![\d.,])(\d[\d,]*(?:\.\d+)?)\s*(?:times|x\b)", re.I)
COND = re.compile(r"(more\s+than|less\s+than|or\s+more|at\s+least|exceed\w*|not\s+more|up\s+to|between|equal\s+to|but\s+less|below|above)\W+(?:\w+\W+){0,2}$", re.I)
TEST = re.compile(r"\b(?:if|where|in\s+the\s+event|clawback|claw-?back\s+mechanism|triggered|pursuant\s+to\s+practice|reallocat\w+\s+(?:procedure|mechanism))\b", re.I)


def section(text):
    m = re.search(r"^##\s*Section\s*2\b.*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    e = re.search(r"^##\s*Section\s*3\b", rest, re.M)
    return re.sub(r"\s+", " ", rest[:e.start()] if e else rest)


def parse(text):
    hits = []
    for m in NUM.finditer(text):
        before, after = text[max(0, m.start() - 320):m.start()], text[m.end():m.end() + 120]
        if COND.search(before[-40:]):
            continue
        sent = re.split(r"(?<=[.;])\s+(?=[A-Z])", before)[-1]
        if TEST.search(sent):
            continue
        pub = [x.end() for x in re.finditer(PUB, before, re.I)]
        ins = [x.end() for x in re.finditer(INST, before, re.I)]
        if not pub or (ins and ins[-1] > pub[-1]):
            # "... times of the Hong Kong Offer Shares" names the tranche after the number
            if not re.match(r"\W*(?:the\s+)?(?:\w+\s+){0,6}?(?:" + PUB + ")", after, re.I) or re.match(r"\W*(?:the\s+)?(?:\w+\s+){0,6}?(?:" + INST + ")", after, re.I):
                continue
        if not re.search(r"approximately|represent|subscri|applications?|about", before[-180:] + after[:40], re.I):
            continue
        v = float(m.group(1).replace(",", ""))
        hits.append((v, re.sub(r"\s+", " ", (before[-170:] + m.group(0) + after[:50]))))
    if not hits:
        return None, "", 0
    vals = sorted({round(v, 2) for v, _ in hits})
    return hits[0][0], hits[0][1], len(vals)


INT = r"(\d{1,3}(?:,\d{3})+|\d{4,})"
VALID = re.compile(r"valid\s+applications?", re.I)


def block_parse(text):
    """Read 'valid applications ... total of A shares ... X times / P% of B' and test A/B."""
    out = []
    for m in VALID.finditer(text):
        w = text[m.start():m.start() + 620]
        head = w[:260]
        if re.search(INST, head, re.I) and not re.search(PUB, head, re.I):
            continue
        # Pool A and pool B are parts of the tranche, not the tranche.
        if re.search(r"\bpool\s+[AB]\b|each\s+of\s+which\s+was\s+(?:applied|for)|applied\s+for\s+not\s+more\s+than", w[:300], re.I):
            continue
        a = re.search(r"(?:for\s+)?(?:a\s+)?total\s+of\s+" + INT + r"\s+(?:[\w\-]+\s+){0,5}?(?:shares|units)", w, re.I)
        if not a:
            continue
        rest = w[a.end():]
        cut = re.search(r"\s[•●]\s|\bThe\s+(?:Offer|International|Placing)\b", rest)
        rest = rest[:cut.start()] if cut else rest
        t = re.search(r"(\d[\d,]*(?:\.\d+)?)\s*times", rest, re.I)
        pc = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|per\s*cent)", rest, re.I)
        b = re.search(r"(?:total\s+number\s+of|initial\s+number\s+of|number\s+of|the)\s+(?:the\s+)?" + INT + r"\s+(?:[\w\-]+\s+){0,5}?(?:shares|units)", rest, re.I)
        A = float(a.group(1).replace(",", "")); B = float(b.group(1).replace(",", "")) if b else None
        v = float(t.group(1).replace(",", "")) if t and not COND.search(rest[:t.start()][-40:]) else None
        if v is None and pc and (not t or pc.start() < t.start()):
            v = float(pc.group(1)) / 100
        calc = A / B if B else None
        ok = bool(v is not None and calc and abs(calc - v) <= max(0.015 * v, 0.006))
        if v is None and calc:
            v = None
        if v is not None:
            out.append((v, calc, ok, w[:300]))
    out.sort(key=lambda x: not x[2])
    return out[0] if out else None


def level_parse(text):
    m = re.search(r"HONG\s*KONG\s+PUBLIC\s+OFFER\w*.{0,220}?Subscription\s+level\s+(\d[\d,]*(?:\.\d+)?)\s*times", text, re.I)
    return float(m.group(1).replace(",", "")) if m else None


def main():
    rows = []
    for f in glob.glob(str(ROOT / "analysis/out/batch[123]_*_packets/*.md")):
        p = Path(f)
        t = section(p.read_text(errors="ignore"))
        v, q, n = parse(t)
        bp = block_parse(t); lv = level_parse(t)
        placing_only = not re.search(PUB, t, re.I) and bool(re.search(r"\bplacing\b", t, re.I))
        val, how, calc = v, "sentence" if v is not None else "", None
        if lv is not None:
            val, how = lv, "subscription_level"
        if bp:
            calc = bp[1]
            if bp[2] or val is None:
                sentence = v
                val, how, q = bp[0], "arithmetic_ok" if bp[2] else "valid_applications", bp[3]
                if bp[2] and sentence is not None and abs(sentence - bp[0]) > 0.02 * max(abs(bp[0]), 0.01):
                    how = "conflict"
        rows.append(dict(key=p.stem, allot_chars=len(t), parsed=val, how=how, calc=calc, distinct=n, placing_only=placing_only, sentence_value=v, quote=q))
    pd.DataFrame(rows).to_csv(OUT / "parsed_subscription.csv", index=False)


if __name__ == "__main__":
    main()
