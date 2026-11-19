#!/usr/bin/env python3
"""Expand Haiku verification to all remaining non-prose_total parsed_shares, missing-old_pct prose_total,
denominator anomalies, and re-extract previous not_in_excerpt cases using untruncated PDF/prospectus text."""
from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "analysis/out/subscription_cornerstone_repair"
PARSED_CSV = OUT_DIR / "parsed_cornerstone_pct.csv"
PANEL = ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
EXTRA_JSONL = OUT_DIR / "allot_extra_sec2.jsonl"
FALLBACK_JSON = OUT_DIR / "cs_extra_fallback.json"
CACHE_JSONL = OUT_DIR / "haiku_cornerstone_cache.jsonl"

sys.path.insert(0, str(Path(__file__).parent))
import parse_allotment_cornerstone as P

CS_PAT = re.compile(r"corner\s*stone|comerstone|corporate\s+investor", re.I)


def pdf_cs_excerpt(key: str) -> str:
    """Gather highest-signal cornerstone pages from local allot_pdfs or pros_cs_pdfs without truncation at cover/lockup."""
    pdfs = (
        sorted(glob.glob(str(OUT_DIR / f"allot_pdfs/{key}*.pdf")))
        + sorted(glob.glob(str(OUT_DIR / f"pros_cs_pdfs/{key}_p_*.pdf")))
        + sorted(glob.glob(str(OUT_DIR / f"pros_cs_pdfs/{key}_a_*.pdf")))
    )
    if not pdfs:
        return ""
    scored_pages: list[tuple[int, str]] = []
    for pf in pdfs[:14]:
        try:
            with fitz.open(pf) as doc:
                for i, pg in enumerate(doc):
                    t = pg.get_text("text")
                    if not CS_PAT.search(t):
                        continue
                    dot_lines = len(re.findall(r"\.\s*\.\s*\.\s*\.", t))
                    if dot_lines >= 4:
                        continue
                    score = 0
                    if re.search(r"(?im)^\s*(?:THE\s+)?CORNERSTONE\s+(?:PLACING|INVESTORS?)|^\s*THE\s+CORPORATE\s+PLACING", t):
                        score += 10
                    if re.search(r"(?:no\.\s*of\s*offer\s*shares|shares\s+allocated|cornerstone\s+placing|corporate\s+placing|have\s+(?:agreed\s+to\s+)?subscribe)", t, re.I):
                        score += 5
                    if re.search(r"\btotal\b|\baggregate\b", t, re.I):
                        score += 3
                    if re.search(r"lock-?up\s+undertakings|stock\s+borrowing|allotees\s+with\s+waivers", t, re.I):
                        score -= 4
                    blk = f"[{Path(pf).name} p{i+1}]\n{t}"
                    if i + 1 < doc.page_count:
                        nt = doc[i + 1].get_text("text")
                        if not CS_PAT.search(nt) and re.search(r"\btotal\b|\d{1,3}(?:,\d{3})+", nt, re.I):
                            blk += f"\n[{Path(pf).name} p{i+2} CONT]\n{nt[:2500]}"
                    scored_pages.append((score, blk))
        except Exception:
            continue
    if not scored_pages:
        return ""
    scored_pages.sort(key=lambda x: -x[0])
    out = []
    tot_len = 0
    for _, blk in scored_pages:
        if tot_len + len(blk) > 11500 and out:
            break
        out.append(blk)
        tot_len += len(blk)
    return "\n---\n".join(out)[:11500]


def smart_sec2_excerpt(sec2: str) -> str:
    """Keep all cornerstone blocks in sec2 prioritizing allocation blocks over lock-up/stock-borrowing boilerplate."""
    blks = P.find_cornerstone_blocks(sec2)
    if not blks:
        return ""
    scored = []
    for b in blks:
        sc = 0
        if re.search(r"(?:no\.\s*of\s*offer\s*shares|shares\s+allocated|subscribed\s+for|total\b|aggregate)", b, re.I):
            sc += 4
        if re.search(r"lock-?up\s+undertakings|placee\s+concentration", b, re.I) and not re.search(r"cornerstone\s+investors?\s*\n.*shares", b, re.I):
            sc -= 3
        scored.append((sc, b))
    scored.sort(key=lambda x: -x[0])
    return "\n---\n".join(b for _, b in scored)[:11000]


def build_excerpt(key: str, extra_map: dict, fb_map: dict) -> str:
    parts = []
    if key in fb_map and fb_map[key].strip():
        parts.append("[FALLBACK PDF EXTRACT]\n" + fb_map[key][:9500])
    pdf_txt = pdf_cs_excerpt(key)
    if pdf_txt:
        parts.append(pdf_txt)
    if key in extra_map and extra_map[key].strip():
        s = smart_sec2_excerpt(extra_map[key]) or extra_map[key][:6000]
        parts.append(s)
    fs = glob.glob(str(ROOT / f"analysis/out/batch*_*_packets/{key}.md"))
    if fs:
        sec2 = P.extract_section2(Path(fs[0]).read_text(errors="ignore"))
        s2_blk = smart_sec2_excerpt(sec2)
        if s2_blk:
            parts.append("[PACKET SEC2]\n" + s2_blk)
        elif sec2:
            parts.append("[PACKET SEC2 HEAD]\n" + sec2[:3500])
    joined = "\n\n".join(parts)
    return joined[:11500]


def call_haiku(batch_items: list[dict]) -> list[dict]:
    prompt_parts = [
        "You are an expert Hong Kong IPO prospectus/allotment auditor.",
        "For EACH issuer below, extract the TOTAL number of Offer Shares subscribed/allocated to ALL Cornerstone Investors (called 'Corporate Investors' in 2005-2009 filings).",
        "Rules:",
        "1. Output ONLY a valid JSON array of objects, one per issuer, with keys:",
        '   {"key": str, "cs_shares": int_or_null, "explicit_offer_pct": float_or_null, "stated_base_offer_shares": int_or_null, "hkd_commitment": float_or_null, "status": "ok"|"not_in_excerpt", "note": str}',
        "2. cs_shares = aggregate shares across ALL cornerstone/corporate investors (sum EVERY individual investor row/sentence if no total line is printed). NEVER return total Global Offering shares or total issued share capital.",
        "3. explicit_offer_pct = stated % of TOTAL Offer Shares (assuming Over-allotment Option is NOT exercised), e.g., 27.1 for 27.1%. Do NOT use '% of International Offer Shares' or '% of total issued share capital'.",
        "4. stated_base_offer_shares = if the excerpt explicitly states the total number of Offer Shares in the Global Offering (assuming Over-allotment not exercised), extract it; else null.",
        "5. hkd_commitment = ONLY if share count cs_shares is NOT stated directly and the prospectus states total cornerstone investment in HK$ (convert US$ to HK$ ONLY if HK$ equivalent is printed; e.g. HK$1,872 million -> 1872000000); else null.",
        "6. If the excerpt lacks cornerstone allocation share/percentage/HK$-commitment numbers (e.g., only lock-up boilerplate Note 2 or cover page), set status='not_in_excerpt' with nulls.",
        "",
    ]
    for it in batch_items:
        base_s = int(it["base_shares"]) if pd.notna(it["base_shares"]) else "unknown"
        op = it["offer_price"] if pd.notna(it["offer_price"]) else "unknown"
        prompt_parts.append(f"=== ISSUER {it['key']} (panel_base_shares={base_s}, offer_price_hkd={op}) ===")
        prompt_parts.append(it["excerpt"])
        prompt_parts.append("")
    prompt = "\n".join(prompt_parts)

    res = subprocess.run(
        ["claude", "-p", "--model", "haiku", "--output-format", "text"],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=240,
    )
    if res.returncode != 0:
        raise RuntimeError(f"claude exit {res.returncode}: {res.stderr[:200]}")
    raw = res.stdout.strip()
    m = re.search(r"\[.*\]", raw, re.S)
    if not m:
        raise ValueError(f"No JSON array in response: {raw[:200]}")
    return json.loads(m.group(0))


def main():
    df = pd.read_csv(PARSED_CSV)
    m = pd.read_csv(PANEL, low_memory=False)
    m["key"] = m["file"].str.replace(".json", "", regex=False)
    op_map = m.set_index("key")["offer_price_hkd"].to_dict()

    extra_map = {r["key"]: r["text"] for r in (json.loads(l) for l in EXTRA_JSONL.open()) if r.get("text")} if EXTRA_JSONL.exists() else {}
    fb_map = json.loads(FALLBACK_JSON.read_text()) if FALLBACK_JSON.exists() else {}

    existing = {}
    if CACHE_JSONL.exists():
        for l in CACHE_JSONL.open():
            if l.strip():
                d = json.loads(l)
                existing[d["key"]] = d

    # Keys needing Haiku:
    # (a) previously not_in_excerpt -> re-try with full PDF/prospectus excerpts
    retry_keys = {k for k, v in existing.items() if v.get("status") != "ok"}
    # (b) parsed_shares not yet reviewed whose method is NOT prose_total, OR prose_total with old_pct missing
    need_df = df[
        (~df["key"].isin(existing.keys()))
        & (df["status"] == "parsed_shares")
        & ((df["how"] != "prose_total") | (df["old_pct"].isna()))
    ]
    # (c) denominator anomaly keys even if already parsed
    anom_keys = {"2011_1296.HK", "2012_2236.HK", "2013_1680.HK", "2017_8152.HK"}
    todo_keys = sorted(retry_keys | set(need_df["key"]) | (anom_keys - set(existing.keys())))

    df_idx = df.set_index("key")
    items = []
    for k in todo_keys:
        ex = build_excerpt(k, extra_map, fb_map)
        base_s = df_idx.loc[k, "base_shares"] if k in df_idx.index else float("nan")
        items.append({
            "key": k,
            "base_shares": base_s,
            "offer_price": op_map.get(k, float("nan")),
            "excerpt": ex,
        })

    print(f"Total existing cached: {len(existing)} (retrying {len(retry_keys)} not_in_excerpt)")
    print(f"Total queued for Haiku expansion: {len(items)}")

    batches = [items[i:i + 8] for i in range(0, len(items), 8)]

    def run_b(idx_b):
        idx, b = idx_b
        for att in range(3):
            try:
                out = call_haiku(b)
                return idx, out, None
            except Exception as e:
                if att == 2:
                    return idx, None, str(e)
                time.sleep(2 * (att + 1))

    new_records = {}
    with ThreadPoolExecutor(4) as ex:
        for idx, out, err in ex.map(run_b, enumerate(batches)):
            if err:
                print(f"Batch {idx} FAILED: {err}", flush=True)
                continue
            for r in out:
                k = r.get("key")
                if k:
                    prev_role = existing.get(k, {}).get("role", "verify")
                    r["role"] = prev_role
                    new_records[k] = r
                    existing[k] = r
            with open(CACHE_JSONL, "w") as f:
                for k in sorted(existing.keys()):
                    f.write(json.dumps(existing[k], ensure_ascii=False) + "\n")
            if (idx + 1) % 5 == 0 or idx + 1 == len(batches):
                print(f"  Batch {idx + 1}/{len(batches)} done ({len(new_records)} updated)", flush=True)

    ok_n = sum(1 for v in existing.values() if v.get("status") == "ok")
    print(f"Done. Total cached: {len(existing)} | ok={ok_n} | non-ok={len(existing) - ok_n}")


if __name__ == "__main__":
    main()
