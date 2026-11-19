#!/usr/bin/env python3
"""Run blind Haiku extraction on unresolved/discrepant cornerstone issuers and a 60-issuer random spot check."""
from __future__ import annotations

import glob
import json
import random
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "analysis/out/subscription_cornerstone_repair"
PARSED_CSV = OUT_DIR / "parsed_cornerstone_pct.csv"
EXTRA_JSONL = OUT_DIR / "allot_extra_sec2.jsonl"
PROS_SEC_JSONL = OUT_DIR / "cornerstone_sections.jsonl"
CACHE_JSONL = OUT_DIR / "haiku_cornerstone_cache.jsonl"

sys.path.insert(0, str(Path(__file__).parent))
import parse_allotment_cornerstone as P


def get_excerpt(key: str, extra_map: dict, pros_map: dict) -> str:
    # 1. Prefer full allotment PDF extraction if available and non-empty
    if key in extra_map and extra_map[key].strip():
        txt = extra_map[key]
        blks = P.find_cornerstone_blocks(txt)
        if blks:
            return "\n---\n".join(blks)[:5500]
        return txt[:5500]
    # 2. Cached Section 2 packet
    fs = glob.glob(str(ROOT / f"analysis/out/batch*_*_packets/{key}.md"))
    if fs:
        sec2 = P.extract_section2(Path(fs[0]).read_text(errors="ignore"))
        blks = P.find_cornerstone_blocks(sec2)
        if blks:
            return "\n---\n".join(blks)[:5500]
        if sec2:
            return sec2[:4000]
    # 3. Fallback: prospectus cornerstone section if allotment had none
    if key in pros_map:
        ctx = pros_map[key].get("ctx") or []
        if ctx:
            return "[PROSPECTUS EXCERPT]\n" + "\n".join(ctx)[:4000]
    return ""


def call_haiku(batch_items: list[dict]) -> list[dict]:
    prompt_parts = [
        "You are an expert Hong Kong IPO prospectus/allotment auditor.",
        "For EACH issuer below, extract the TOTAL number of Offer Shares subscribed/allocated to ALL Cornerstone Investors (sometimes called 'Corporate Investors' in 2005-2009 filings).",
        "Rules:",
        "1. Output ONLY a valid JSON array of objects, one per issuer, with keys:",
        '   {"key": str, "cs_shares": int_or_null, "explicit_offer_pct": float_or_null, "status": "ok"|"not_in_excerpt", "note": str}',
        "2. cs_shares = aggregate shares across ALL cornerstone/corporate investors (sum individual investors if no total line is printed). NEVER return total Global Offering shares or total issued share capital.",
        "3. explicit_offer_pct = stated % of the TOTAL Offer Shares (assuming Over-allotment Option is NOT exercised), e.g., 27.1 for 27.1%. Do NOT use '% of International Offer Shares' or '% of total issued share capital'. If only share counts or issued-capital % is stated, set explicit_offer_pct to null.",
        "4. If the excerpt lacks cornerstone share/percentage numbers, set cs_shares=null, explicit_offer_pct=null, status='not_in_excerpt'.",
        "",
    ]
    for it in batch_items:
        prompt_parts.append(f"=== ISSUER {it['key']} (base_offer_shares={int(it['base_shares']) if pd.notna(it['base_shares']) else 'unknown'}) ===")
        prompt_parts.append(it["excerpt"])
        prompt_parts.append("")
    prompt = "\n".join(prompt_parts)

    res = subprocess.run(
        ["claude", "-p", "--model", "haiku", "--output-format", "text"],
        input=prompt,
        text=True,
        capture_output=True,
        timeout=180,
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
    extra_map = {r["key"]: r["text"] for r in (json.loads(l) for l in EXTRA_JSONL.open()) if r.get("text")} if EXTRA_JSONL.exists() else {}
    pros_map = {r["key"]: r for r in (json.loads(l) for l in PROS_SEC_JSONL.open())} if PROS_SEC_JSONL.exists() else {}

    # 1. Identify unresolved + discrepant (>1.5pp from both base and post)
    unres = set(df[~df["status"].isin(["parsed_verified", "parsed_shares"])]["key"])
    both = df[df["old_pct"].notna() & df["calc_pct_base"].notna()].copy()
    discrep = set(both[((both["calc_pct_base"] - both["old_pct"]).abs() > 1.5) & ((both["calc_pct_post"] - both["old_pct"]).abs() > 1.5)]["key"])
    review_keys = sorted(unres | discrep)

    # 2. Stratified 60-issuer blind spot-check from cleanly parsed pool (not already in review_keys)
    clean_pool = df[df["status"].isin(["parsed_verified", "parsed_shares"]) & (~df["key"].isin(review_keys))].copy()
    rng = random.Random(20261118)
    spot_keys = []
    for b, target_n in [("2002-2007", 8), ("2008-2017", 26), ("2018-2024", 26)]:
        sub_k = sorted(clean_pool[clean_pool["batch"] == b]["key"].tolist())
        spot_keys.extend(rng.sample(sub_k, min(target_n, len(sub_k))))

    all_targets = [(k, "review" if k in review_keys else "spotcheck") for k in sorted(set(review_keys) | set(spot_keys))]
    print(f"Review targets: {len(review_keys)} | Spotcheck targets: {len(spot_keys)} | Total: {len(all_targets)}")

    # Load cache
    done = {}
    if CACHE_JSONL.exists():
        for l in CACHE_JSONL.open():
            r = json.loads(l)
            done[r["key"]] = r

    todo_items = []
    df_idx = df.set_index("key")
    for k, role in all_targets:
        if k in done:
            continue
        ex = get_excerpt(k, extra_map, pros_map)
        if not ex:
            rec = {"key": k, "role": role, "cs_shares": None, "explicit_offer_pct": None, "status": "no_excerpt", "note": ""}
            done[k] = rec
            with CACHE_JSONL.open("a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            continue
        todo_items.append({
            "key": k,
            "role": role,
            "base_shares": df_idx.loc[k, "base_shares"],
            "excerpt": ex,
        })

    print(f"Cached: {len(done)} | Calling Haiku on: {len(todo_items)} issuers...")
    batches = [todo_items[i:i + 10] for i in range(0, len(todo_items), 10)]
    role_map = {it["key"]: it["role"] for it in todo_items}

    def run_batch(b):
        try:
            out = call_haiku(b)
            return out, ""
        except Exception as e:
            return [], str(e)

    with ThreadPoolExecutor(4) as ex_pool, CACHE_JSONL.open("a") as f:
        for idx, (out, err) in enumerate(ex_pool.map(run_batch, batches), start=1):
            if err:
                print(f"  Batch {idx}/{len(batches)} ERROR: {err}", flush=True)
                continue
            for rec in out:
                k = rec.get("key")
                if k:
                    rec["role"] = role_map.get(k, "unknown")
                    done[k] = rec
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            print(f"  Batch {idx}/{len(batches)} done ({len(out)} records)", flush=True)

    # Save target manifest
    pd.DataFrame([{"key": k, "role": role} for k, role in all_targets]).to_csv(OUT_DIR / "haiku_targets.csv", index=False)
    print(f"Completed. Total cached Haiku records: {len(done)}")


if __name__ == "__main__":
    main()
