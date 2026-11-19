#!/usr/bin/env python3
"""Parse cornerstone share allocations and base-offer % from cached allotment packets for confirmed CS IPOs."""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
OUT_DIR = ROOT / "analysis/out/subscription_cornerstone_repair"

LOCKUP_HEAD = re.compile(r"(?im)^\s*LOCK-?UP\s+UNDERTAKINGS\b|^\s*Shareholding\s+Structure\b")
NEXT_SEC_STOP = re.compile(
    r"(?im)(?:^|\n)\s*(?:LOCK-?UP\s+UNDERTAKINGS|Shareholding\s+Structure|"
    r"OVER-?ALLOTMENT\s+OPTION|STABILIS\w+|PUBLIC\s+FLOAT|USE\s+OF\s+PROCEEDS|"
    r"DESPATCH|COLLECTION\s+OF\s+(?:H\s+)?SHARE\s+CERTIFICATES|RESULTS\s+OF\s+APPLICATIONS|"
    r"BASIS\s+OF\s+ALLOCATION|LEVEL\s+OF\s+INDICATIONS|"
    r"(?:•|\*)\s*The\s+(?:final\s+)?number\s+of\s+Offer\s+Shares\s+(?:allocated|comprised|initially)|"
    r"(?:•|\*)\s*(?:H\s+)?Share\s+certificates|"
    r"On\s+the\s+basis\s+of\s+the\s+Offer\s+Price,\s+the\s+number\s+of\s+IPO\s+Shortfall|"
    r"Investor\s+Shareholders\s+will\s+hold)\b"
)

SHARE_UNIT = r"(?:offer\s+|h\s+|international\s+|placing\s+)?shares"

# Explicit aggregate share phrases in prose (ordered from most explicit aggregate to single-investor)
TOTAL_SHARE_PATS = [
    re.compile(
        r"(?is)(\d{1,3}(?:,\d{3})+|\d{6,})\s+" + SHARE_UNIT + r"\s+in\s+(?:total|aggregate)"
    ),
    re.compile(
        r"(?is)(?:corner\s*stone|corporate)\s+investors?.{0,450}?"
        r"(?:have|has|will|would)\s+(?:subscribed\s+for|purchased|acquired|been\s+allocated|been\s+allotted|agreed\s+to\s+(?:subscribe\s+for|purchase|acquire))"
        r"\s+(?:a\s+total\s+of|an\s+aggregate\s+of|in\s+aggregate(?:\s+of)?)\s+(?:approximately\s+)?"
        r"(\d{1,3}(?:,\d{3})+|\d{6,})\s+" + SHARE_UNIT
    ),
    re.compile(
        r"(?is)(?:in\s+all\s+totalling|totalling|an\s+aggregate\s+of|in\s+aggregate)\s+(?:approximately\s+)?"
        r"(\d{1,3}(?:,\d{3})+|\d{6,})\s+" + SHARE_UNIT
    ),
    re.compile(
        r"(?is)total\s+(?:number\s+of\s+)?(?:offer\s+|h\s+)?shares\s+(?:to\s+be\s+|agreed\s+to\s+be\s+)?"
        r"(?:subscribed\s+(?:for\s+)?|purchased\s+|acquired\s+|allocated\s+|allotted\s+)?by\s+"
        r"(?:the\s+)?(?:corner\s*stone|corporate)\s+investors?(?:[^.;]{0,220}?)"
        r"(?:is|will\s+be|was|were|has\s+been\s+determined\s+(?:at|to\s+be))\s+(?:approximately\s+)?"
        r"(\d{1,3}(?:,\d{3})+|\d{6,})(?:,\s*|\s+" + SHARE_UNIT + r"|\s+in\s+aggregate)?"
    ),
    re.compile(
        r"(?is)aggregate\s+(?:number\s+of\s+)?(?:offer\s+|h\s+)?shares\s+(?:to\s+be\s+)?"
        r"(?:subscribed\s+(?:for\s+)?|purchased\s+|acquired\s+)by\s+"
        r"(?:the\s+)?(?:corner\s*stone|corporate)\s+investors?[^.;]{0,140}?"
        r"(?:is|will\s+be|was|were)\s+(?:approximately\s+)?"
        r"(\d{1,3}(?:,\d{3})+|\d{6,})"
    ),
    re.compile(
        r"(?is)(?:corner\s*stone|corporate)\s+investors?[^.]{0,160}?"
        r"(?:subscribed\s+for|purchased|acquired|allocated|allotted)\s+(?:approximately\s+)?"
        r"(\d+(?:\.\d+)?)\s*million\s+" + SHARE_UNIT
    ),
]

# Explicit "% of Offer Shares" (must be tied to cornerstone/corporate, NOT International/Public tranche or total issued share capital)
EXPLICIT_PCT_PAT = re.compile(
    r"(?is)(\d+(?:\.\d+)?)\s*(?:%|per\s*cent)\s+of\s+(?:the\s+)?"
    r"(?:total\s+(?:number\s+of\s+)?)?(?:initial\s+)?(?:offer\s+shares|shares\s+offered\s+(?:under|pursuant\s+to)\s+the\s+(?:global|share)\s+offer)"
    r"(?!\s+(?:available\s+)?under\s+the\s+international)"
)

PAGE_MARKER = re.compile(r"```\s*\n+### \[DOC: ALLOT[^\n]*\n+```text\s*\n", re.M)


def extract_section2(txt: str) -> str:
    m = re.search(r"^##\s*Section\s*2\b.*$", txt, re.M)
    if not m:
        return ""
    rest = txt[m.end():]
    e = re.search(r"^##\s*Section\s*3\b", rest, re.M)
    sec2 = rest[:e.start()] if e else rest
    return PAGE_MARKER.sub("\n", sec2)


def find_cornerstone_blocks(sec2: str) -> list[str]:
    """Return candidate text windows around Cornerstone disclosures (excluding lock-up tables)."""
    blocks: list[tuple[int, str]] = []
    lu_m = LOCKUP_HEAD.search(sec2)
    search_area = sec2[:lu_m.start()] if lu_m else sec2
    if not re.search(r"(?i)corner\s*stone|corporate\s+investor", search_area):
        search_area = sec2

    for m in re.finditer(r"(?im)(?:corner\s*stone\s+investors?|corner\s*stone\s+investment|corner\s*stone\s+plac\w+|corporate\s+investors?)", search_area):
        before = search_area[max(0, m.start() - 60):m.start()]
        if re.search(r"(?i)section\s+headed\s*[\"'“]?$|headed\s*[\"'“]?$", before):
            continue
        start = max(0, m.start() - 220)
        tail = search_area[m.start():m.start() + 5500]
        stop_m = NEXT_SEC_STOP.search(tail[60:])
        end = m.start() + (60 + stop_m.start() if stop_m else len(tail))
        blk = search_area[start:end]
        if any(abs(start - ps) < 400 for ps, _ in blocks):
            continue
        blocks.append((start, blk))
    return [b for _, b in blocks]


def parse_table_explicit_total(blk: str) -> tuple[float | None, float | None, str]:
    """Extract only an explicit Total / Subtotal row inside a cornerstone table."""
    lines = [ln.strip() for ln in blk.splitlines() if ln.strip()]
    for i, ln in enumerate(lines):
        if re.match(r"^(?:Total|Sub-?total)(?:\s+[\d,]+.*)?$", ln, re.I):
            window = " ".join(lines[i:i + 6])
            m_sh = re.search(r"\b(\d{1,3}(?:,\d{3})+|\d{6,})\b", window)
            if m_sh:
                sh = float(m_sh.group(1).replace(",", ""))
                if sh < 50000:
                    continue
                after_sh = window[m_sh.end():]
                pcts = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", after_sh[:80])]
                header_txt = " ".join(lines[:min(i, 40)]).lower()
                has_offer_pct_col = bool(re.search(r"%\s*of\s*(?:the\s*)?(?:total\s*(?:number\s*of\s*)?)?offer\s*shares|percentage\s*of\s*(?:the\s*)?(?:total\s*(?:number\s*of\s*)?)?offer\s*shares", header_txt))
                has_intl_pct_col = bool(re.search(r"%\s*of\s*(?:the\s*)?international", header_txt))
                exp_pct = pcts[0] if (pcts and has_offer_pct_col and not has_intl_pct_col) else None
                return sh, exp_pct, f"table_total: {window[:180]}"
    return None, None, ""


def parse_prose_aggregate(blk: str) -> tuple[float | None, float | None, str]:
    """Extract explicit aggregate cornerstone shares or multi-investor sums in prose."""
    clean = re.sub(r"\s+", " ", blk)
    sh = None
    src_note = ""

    # 1. Explicit aggregate totals
    for idx, pat in enumerate(TOTAL_SHARE_PATS):
        m = pat.search(clean)
        if m:
            raw_num = m.group(1).replace(",", "")
            v = float(raw_num) * (1e6 if idx == len(TOTAL_SHARE_PATS) - 1 else 1.0)
            if v >= 50000:
                sh = v
                src_note = "prose_total: " + clean[max(0, m.start() - 30):m.end() + 120]
                break

    # 2. Multi-investor list ("subscribed for X, Y and Z Offer Shares")
    if sh is None:
        m_multi = re.search(
            r"(?is)(?:subscribed\s+for|purchased|acquired|agreed\s+to\s+(?:subscribe\s+for|purchase))"
            r"((?:\s*,?\s*(?:and\s+)?\d{1,3}(?:,\d{3})+){2,})\s+" + SHARE_UNIT,
            clean,
        )
        if m_multi:
            nums = [float(x.replace(",", "")) for x in re.findall(r"\d{1,3}(?:,\d{3})+", m_multi.group(1))]
            if len(nums) >= 2 and all(n >= 50000 for n in nums):
                sh = sum(nums)
                src_note = f"prose_multi_sum({len(nums)}): " + m_multi.group(0)[:180]

    # 3. Separate clauses in cornerstone block ("has subscribed for X Shares ... has subscribed for Y Shares")
    if sh is None:
        sub_clean = re.split(r"(?i)\b(?:Notes?:|Please\s+refer\s+to|The\s+Cornerstone\s+Investors?\s+(?:are|will\s+not))\b", clean)[0]
        ind_matches = list(re.finditer(
            r"(?is)(?:has|have|will|would)\s+(?:subscribed?\s+for|purchased?|acquired?|subscribe\s+for)\s+(?:approximately\s+)?(\d{1,3}(?:,\d{3})+)\s+" + SHARE_UNIT,
            sub_clean,
        ))
        if ind_matches:
            nums = [float(x.group(1).replace(",", "")) for x in ind_matches if float(x.group(1).replace(",", "")) >= 50000]
            if nums:
                sh = sum(nums)
                src_note = f"prose_sent_sum({len(nums)}): " + sub_clean[max(0, ind_matches[0].start() - 50):ind_matches[0].end() + 100]

    # Explicit % of Offer Shares in prose (must be in a cornerstone sentence, not tranche/clawback/over-allotment)
    exp_pct = None
    for m_pct in EXPLICIT_PCT_PAT.finditer(clean):
        ctx_before = clean[max(0, m_pct.start() - 260):m_pct.start()]
        if re.search(r"(?i)(?:over-?allotment|clawback|final\s+number\s+of|initially\s+(?:offered|available)|reallocated\s+from)", ctx_before[-160:]):
            continue
        if not re.search(r"(?i)(?:corner\s*stone|corporate\s+investor)", ctx_before):
            continue
        val = float(m_pct.group(1))
        if 0 < val <= 100:
            exp_pct = val
            break
    return sh, exp_pct, src_note


def parse_table_row_sum(blk: str) -> tuple[float | None, float | None, str]:
    """Fallback: sum individual investor rows when no Total row or prose aggregate exists."""
    lines = [ln.strip() for ln in blk.splitlines() if ln.strip()]
    header_joined = " ".join(lines[:40]).lower()
    if not re.search(r"number\s+of\s+(?:offer\s+|h\s+)?shares|no\.\s*of\s+(?:offer\s+)?shares\s+allocated", header_joined):
        return None, None, ""
    has_offer_pct_col = bool(re.search(r"%\s*of\s*(?:the\s*)?(?:total\s*(?:number\s*of\s*)?)?offer\s*shares|percentage\s*of\s*(?:the\s*)?(?:total\s*(?:number\s*of\s*)?)?offer\s*shares", header_joined))
    has_intl_pct_col = bool(re.search(r"%\s*of\s*(?:the\s*)?international", header_joined))

    row_shares: list[float] = []
    row_pcts: list[float] = []
    in_body = False
    for idx, ln in enumerate(lines):
        if re.search(r"(?i)(?:total\s+issued|share\s+capital|existing\s+shareholders|close\s+associates|\(%\))", ln):
            in_body = True
            continue
        if in_body and re.match(r"^(?:Notes?:|Please\s+refer|To\s+the\s+best|Each\s+of\s+the|The\s+Cornerstone)", ln, re.I):
            break
        if not in_body and idx > 15:
            in_body = True
        if in_body:
            m_int = re.match(r"^(\d{1,3}(?:,\d{3})+)(?:\s+([\d.]+)%?)?$", ln)
            if m_int:
                v = float(m_int.group(1).replace(",", ""))
                if v >= 50000:
                    row_shares.append(v)
                    if m_int.group(2) and has_offer_pct_col and not has_intl_pct_col:
                        row_pcts.append(float(m_int.group(2)))
    if not row_shares:
        return None, None, ""
    if len(row_shares) >= 3 and abs(row_shares[-1] - sum(row_shares[:-1])) <= 10:
        row_shares = row_shares[:-1]
    return sum(row_shares), (sum(row_pcts) if len(row_pcts) == len(row_shares) else None), f"table_sum({len(row_shares)} rows)"


def parse_text_blocks(key: str, text_sec: str, base_shares: float, post_shares: float) -> dict | None:
    blocks = find_cornerstone_blocks(text_sec)
    if not blocks:
        return None
    best = None
    for blk in blocks:
        sh_p, exp_p, note_p = parse_prose_aggregate(blk)
        sh_t, exp_t, note_t = parse_table_explicit_total(blk)
        sh_s, exp_s, note_s = (None, None, "")
        if sh_p is None and sh_t is None:
            sh_s, exp_s, note_s = parse_table_row_sum(blk)

        cands = []
        for sh, exp, note in ((sh_t, exp_t, note_t), (sh_p, exp_p, note_p), (sh_s, exp_s, note_s)):
            exp_use = exp if exp is not None else (exp_p if exp_p is not None else exp_t)
            if sh is None and exp_use is None:
                continue
            calc_base = (sh / base_shares * 100.0) if (sh is not None and base_shares > 0) else np.nan
            calc_post = (sh / post_shares * 100.0) if (sh is not None and post_shares > 0) else np.nan
            ok_range = bool(pd.notna(calc_base) and 0 < calc_base <= 100.0)
            agree_exp = bool(ok_range and exp_use is not None and abs(calc_base - exp_use) <= max(1.5, 0.05 * exp_use))
            cands.append({
                "key": key,
                "cs_shares": sh,
                "base_shares": base_shares,
                "post_shares": post_shares,
                "calc_pct_base": round(calc_base, 4) if pd.notna(calc_base) else np.nan,
                "calc_pct_post": round(calc_post, 4) if pd.notna(calc_post) else np.nan,
                "explicit_offer_pct": exp_use,
                "agree_explicit": agree_exp,
                "ok_range": ok_range,
                "how": note.split(":")[0] if note else "explicit_pct_only",
                "quote": re.sub(r"\s+", " ", note)[:260],
            })
        for cand in cands:
            score = (3 if cand["agree_explicit"] else 2 if cand["ok_range"] else 1 if cand["explicit_offer_pct"] else 0)
            best_score = (3 if best["agree_explicit"] else 2 if best["ok_range"] else 1 if best["explicit_offer_pct"] else 0) if best else -1
            if score > best_score:
                best = cand
        if best and best["agree_explicit"]:
            break
    if best is None:
        return None
    if best["agree_explicit"]:
        best["status"] = "parsed_verified"
    elif best["ok_range"]:
        best["status"] = "parsed_shares"
    elif best["explicit_offer_pct"] is not None:
        best["status"] = "explicit_pct_only"
    else:
        best["status"] = "out_of_range"
    return best


def parse_one(key: str, base_shares: float, post_shares: float, extra_text: str = "") -> dict:
    fs = glob.glob(str(ROOT / f"analysis/out/batch*_*_packets/{key}.md"))
    if not fs:
        return {"key": key, "status": "no_packet"}
    txt = Path(fs[0]).read_text(errors="ignore")
    sec2 = extract_section2(txt)
    best = parse_text_blocks(key, sec2, base_shares, post_shares) if sec2 else None

    if (best is None or best["status"] not in ("parsed_verified", "parsed_shares")) and extra_text:
        best2 = parse_text_blocks(key, extra_text, base_shares, post_shares)
        if best2 is not None:
            s1 = (3 if best and best.get("agree_explicit") else 2 if best and best.get("ok_range") else 1 if best else 0)
            s2 = (3 if best2.get("agree_explicit") else 2 if best2.get("ok_range") else 1)
            if s2 > s1:
                best = best2

    if best is None:
        if not sec2 and not extra_text:
            return {"key": key, "status": "no_sec2"}
        if not find_cornerstone_blocks(sec2) and not (extra_text and find_cornerstone_blocks(extra_text)):
            return {"key": key, "status": "no_cs_in_sec2", "base_shares": base_shares}
        return {"key": key, "status": "unparsed", "base_shares": base_shares}
    return best


def main():
    m = pd.read_csv(PANEL, low_memory=False)
    cs1 = m[(m["batch"] != "2025-2026") & (m["ext_has_cornerstone"] == 1)].copy()
    cs1["key"] = cs1["file"].str.replace(".json", "", regex=False)
    cs1["base_shares"] = pd.to_numeric(cs1["col_R"], errors="coerce") + pd.to_numeric(cs1["col_S"], errors="coerce")
    cs1["post_shares"] = pd.to_numeric(cs1["col_M"], errors="coerce")

    extra_map = {}
    extra_path = OUT_DIR / "allot_extra_sec2.jsonl"
    if extra_path.exists():
        for ln in extra_path.open():
            rec = json.loads(ln)
            if rec.get("text"):
                extra_map[rec["key"]] = rec["text"]

    rows = []
    for _, r in cs1.iterrows():
        rec = parse_one(r["key"], float(r["base_shares"]), float(r["post_shares"]), extra_map.get(r["key"], ""))
        rec["batch"] = r["batch"]
        rec["cohort_year"] = int(r["cohort_year"])
        rec["old_pct"] = r["ext_cornerstone_pct"]
        rows.append(rec)

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "parsed_cornerstone_pct.csv", index=False)
    print("Status counts (N = 725):")
    print(df["status"].value_counts(dropna=False).to_string())
    print("\nBy batch:")
    print(pd.crosstab(df["batch"], df["status"], margins=True).to_string())

    both = df[df["old_pct"].notna() & df["calc_pct_base"].notna()].copy()
    both["diff_base"] = (both["calc_pct_base"] - both["old_pct"]).abs()
    both["diff_post"] = (both["calc_pct_post"] - both["old_pct"]).abs()
    print(f"\nComparable with old_pct: {len(both)}")
    print(f"  Matches old_pct within 1.5pp (using base):  {(both['diff_base'] <= 1.5).sum()}")
    print(f"  Matches old_pct within 1.5pp (using post!): {((both['diff_base'] > 1.5) & (both['diff_post'] <= 1.5)).sum()}")
    print(f"  Differs > 1.5pp from both:                  {((both['diff_base'] > 1.5) & (both['diff_post'] > 1.5)).sum()}")


if __name__ == "__main__":
    main()
