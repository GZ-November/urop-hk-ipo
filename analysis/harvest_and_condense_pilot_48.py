#!/usr/bin/env python3
"""48-Issuer Fast Deterministic Harvester & Condensed Packet Builder (1994-2024).

Implements Step 1 of the 48-Issuer Historical Pilot:
1. Refines HKEXnews document discovery for 43 online issuers (1999-2024):
   - Eliminates false positives (Application Forms, Web Proof / PHIP, Typographical errors).
   - Detects Multi-Section HTML Index (.htm) vs Single Full PDF (.pdf).
   - Strongly PREFERS Multi-Section HTML Index to selectively download only target section PDFs
     (Summary, Corporate Info, History, Business, Offering Structure, Underwriting, Financials).
   - Resolves Allotment Results HTML wrappers (.htm) to Cover + Summary PDFs (bypassing ID phonebooks).
   - Supports multi-anchor dates (listing date, prospectus date, Bloomberg pricing date).
2. Parallel zero-token downloading via ThreadPoolExecutor(max_workers=6).
3. Fast targeted text extraction using PyMuPDF (fitz) with Tier-1 keyword page filtering.
4. Generates ultra-compact Markdown packets (strictly within target 15 KB - 35 KB, ~8k tokens max) for all 48 issuers:
   - Section 0: Pre-filled Zero-Token Ground Truth from enriched 33y panel.
   - Section 1: Allotment Results / Offer Price Announcement Excerpts.
   - Section 2: Targeted Prospectus Excerpts with exact page citations.
   - Section 3: Harvester Metadata, Page Counts, and Scanned Image PDF Detection.
5. Emits master manifest: analysis/out/pilot_48_packets/pilot_48_packet_manifest.csv.
"""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import pymupdf  # PyMuPDF
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "analysis" / "out"
OVERVIEW_DIR = OUT_DIR / "overview_1994_2026"
PROBE_CSV = OVERVIEW_DIR / "pilot_48_source_probe.csv"
ENRICHED_CSV = OVERVIEW_DIR / "clean_33y_hkipo_panel_1994_2026_enriched.csv"

RAW_DOCS_DIR = OUT_DIR / "pilot_48_raw_docs"
PACKETS_DIR = OUT_DIR / "pilot_48_packets"
MANIFEST_CSV = PACKETS_DIR / "pilot_48_packet_manifest.csv"
CACHE_JSON = RAW_DOCS_DIR / "_hkex_query_cache.json"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
HKEX_BASE = "https://www1.hkexnews.hk"
HKEX_SEARCH_URL = "https://www1.hkexnews.hk/search/titleSearchServlet.do"


def clean_text(text: str) -> str:
    """Normalize whitespace and strip excessive empty lines."""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse 3+ newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple inline spaces/tabs
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def parse_date_safe(val) -> dt.date | None:
    if val is None or pd.isna(val):
        return None
    s = str(val).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


# ----------------------------------------------------------------------
# 1. Refined HKEXnews Querying & Candidate Picking
# ----------------------------------------------------------------------

EXCLUDE_PROS_KEYWORDS = [
    "application form", "green application", "yellow application", "white application", "pink application",
    "web proof", "phip", "post hearing", "application proof",
    "typographical error", "errata", "addendum", "supplemental prospectus", "supplemental document",
    "rights issue", "open offer", "placing of existing", "option scheme", "warrant",
    "allotment result", "basis of allotment", "monthly return", "constitutional",
    "articles of association", "terms of reference", "list of directors", "company information sheet",
    "board meeting", "notice of board", "poll results", "interim report", "annual report"
]

EXCLUDE_ALLOT_KEYWORDS = [
    "application form", "web proof", "phip", "application proof",
    "monthly return", "constitutional", "articles of association",
    "terms of reference", "list of directors", "company information sheet",
    "annual results", "interim results", "board meeting", "share option",
    "resumption", "suspension", "interim report", "annual report"
]


def query_hkex_filings(session: requests.Session, stock_id: int, sid_status: str, min_date: dt.date, max_date: dt.date, cache: dict) -> list[dict]:
    """Query HKEXnews for filings across min/max date anchors with local file caching."""
    sid_key = f"{stock_id}_{min_date}_{max_date}"
    if sid_key in cache:
        return cache[sid_key]

    frm = (min_date - dt.timedelta(days=45)).strftime("%Y%m%d")
    to = (max_date + dt.timedelta(days=25)).strftime("%Y%m%d")

    cats = ["1", "0"] if "inactive" in str(sid_status).lower() else ["0", "1"]
    docs: list[dict] = []

    for cat in cats:
        params = {
            "sortDir": "0",
            "sortByOptions": "DateTime",
            "category": cat,
            "market": "SEHK",
            "stockId": str(stock_id),
            "documentType": "-1",
            "fromDate": frm,
            "toDate": to,
            "title": "",
            "searchType": "0",
            "t1code": "-2",
            "t2Gcode": "-2",
            "t2code": "-2",
            "rowRange": "150",
            "lang": "EN",
        }
        try:
            r = session.get(HKEX_SEARCH_URL, params=params, headers={"User-Agent": UA}, timeout=15)
            r.raise_for_status()
            res_str = r.json().get("result") or "[]"
            d_list = json.loads(res_str)
            if d_list:
                docs = d_list
                break
        except Exception:
            pass
        time.sleep(0.1)

    # Fallback retry with wider window if 0 docs found
    if not docs:
        frm2 = (min_date - dt.timedelta(days=65)).strftime("%Y%m%d")
        to2 = (max_date + dt.timedelta(days=40)).strftime("%Y%m%d")
        for cat in cats:
            params["fromDate"] = frm2
            params["toDate"] = to2
            params["category"] = cat
            try:
                r = session.get(HKEX_SEARCH_URL, params=params, headers={"User-Agent": UA}, timeout=15)
                d_list = json.loads(r.json().get("result") or "[]")
                if d_list:
                    docs = d_list
                    break
            except Exception:
                pass
            time.sleep(0.1)

    cache[sid_key] = docs
    return docs


def pick_refined_prospectus(docs: list[dict]) -> dict | None:
    """Select the genuine prospectus, prioritizing multi-section HTML indexes when available."""
    candidates = []
    for d in docs:
        title = (d.get("TITLE") or "").strip().lower()
        link = (d.get("FILE_LINK") or "").strip()
        cat = (d.get("SHORT_TEXT") or "").strip().lower()
        long_txt = (d.get("LONG_TEXT") or "").strip().lower()
        full_meta = f"{title} {cat} {long_txt}"

        # Hard exclusions
        if any(bad in title for bad in EXCLUDE_PROS_KEYWORDS):
            continue
        if any(bad in full_meta for bad in ["web proof information pack", "application proof", "post hearing information pack"]):
            continue

        score = 0
        # Category bonus
        if "listing documents" in cat or "listing documents" in long_txt:
            score += 50
        elif "formal notice" in cat:
            score += 5  # notices are lower priority than actual prospectus

        # Title bonus
        if "prospectus" in title:
            score += 65
        elif "global offering" in title:
            score += 55
        elif "share offer" in title:
            score += 55
        elif "placing and public offer" in title or "public offer and placing" in title:
            score += 55
        elif "offer for subscription" in title or "offer for placing" in title:
            score += 50
        elif "placing" in title:
            score += 45
        elif "public offer" in title:
            score += 45
        elif "new listing" in title:
            score += 40

        # CRITICAL: Prefer Multi-Section HTML Index (.htm / .html) over full PDF!
        is_html = link.lower().endswith((".htm", ".html"))
        is_pdf = link.lower().endswith(".pdf")
        if is_html:
            score += 30  # HTML index bonus!
        elif is_pdf:
            score += 15

        if score >= 35:
            candidates.append((score, d))

    if not candidates:
        return None

    # Sort descending by score; if tied, favor earlier or more specific
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def pick_refined_allotment(session: requests.Session, docs: list[dict]) -> dict | None:
    """Identify the genuine Allotment Results announcement."""
    good_kw = [
        "allotment results", "allotment result", "basis of allotment", "offer price and allotment",
        "results of allocation", "results of the placing", "results of applications", "pricing announcement",
        "announcement of offer price"
    ]
    candidates = []
    for d in docs:
        title = (d.get("TITLE") or "").strip().lower()
        link = (d.get("FILE_LINK") or "").strip()
        cat = (d.get("SHORT_TEXT") or "").strip().lower()
        long_txt = (d.get("LONG_TEXT") or "").strip().lower()

        if any(bad in title for bad in EXCLUDE_ALLOT_KEYWORDS):
            continue

        score = 0
        if "allotment results" in cat or "allotment results" in long_txt:
            score += 60

        if any(g in title for g in good_kw):
            score += 60
        elif "allotment" in title or "allocation" in title:
            score += 40
        elif "offer price" in title:
            score += 30

        if score >= 30:
            candidates.append((score, d))

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    # Special handling for early digital transition (1999-2003) where title was generically "Announcement"
    for d in docs:
        title = (d.get("TITLE") or "").strip().lower()
        link = (d.get("FILE_LINK") or "").strip()
        if "announcement" in title and link.lower().endswith((".htm", ".html")):
            try:
                full_url = urljoin(HKEX_BASE, link)
                r = session.get(full_url, headers={"User-Agent": UA}, timeout=8)
                body = r.text[:4000].lower()
                if any(k in body for k in ["offer price", "basis of allocation", "basis of allotment", "results of the placing", "results of application"]):
                    return d
            except Exception:
                pass

    return None


# ----------------------------------------------------------------------
# 2. Section Resolution (HTML Index vs Full PDF)
# ----------------------------------------------------------------------

TARGET_SECTION_KEYS = {
    "cover": ["cover"],
    "summary": ["summary", "summary and highlights"],
    "corporate_info": ["corporate information", "parties involved", "directors and parties"],
    "history": ["history", "group structure", "development and reorganisation", "reorganisation"],
    "business": ["business", "our business"],
    "controlling_shareholders": ["controlling shareholder", "substantial shareholder", "initial management shareholder"],
    "share_capital": ["share capital"],
    "offering_structure": [
        "structure of the global offering", "conditions of the", "corporate placing",
        "information about this prospectus and the placing", "information about this prospectus and the share offer",
        "information about this prospectus and the global offering", "share offer", "placing"
    ],
    "cornerstone": ["cornerstone", "corporate placing"],
    "underwriting": ["underwriting", "underwriting arrangements"],
    "financial_info": ["financial information"],
    "accountants_report": ["accountants' report", "accountant's report", "accountants report", "appendix i - accountant"]
}


def parse_prospectus_html_sections(session: requests.Session, html_url: str) -> dict[str, tuple[str, str]]:
    """Parse a Multi-Section HTML index and map to target chapter PDFs."""
    r = session.get(html_url, headers={"User-Agent": UA}, timeout=15)
    r.raise_for_status()
    matches = re.findall(r"<a\s+[^>]*href=[\x27\x22]([^\x27\x22]+)[\x27\x22][^>]*>(.*?)</a>", r.text, re.IGNORECASE | re.DOTALL)

    resolved: dict[str, tuple[str, str]] = {}
    for href, raw_txt in matches:
        clean_txt = re.sub(r"<[^>]+>", "", raw_txt).strip()
        full_href = urljoin(html_url, href)
        if not full_href.lower().endswith(".pdf"):
            continue
        ltxt = clean_txt.lower()

        # Classify link
        for sec_key, patterns in TARGET_SECTION_KEYS.items():
            if any(pat in ltxt for pat in patterns):
                if sec_key not in resolved:
                    resolved[sec_key] = (clean_txt, full_href)
                break

    return resolved


def parse_allotment_html(session: requests.Session, html_url: str) -> tuple[list[tuple[str, str]], str | None]:
    """Parse Allotment HTML wrapper: return child PDFs (Cover/Summary) or raw HTML body if inline."""
    r = session.get(html_url, headers={"User-Agent": UA}, timeout=15)
    r.raise_for_status()
    matches = re.findall(r"<a\s+[^>]*href=[\x27\x22]([^\x27\x22]+)[\x27\x22][^>]*>(.*?)</a>", r.text, re.IGNORECASE | re.DOTALL)

    pdf_links = []
    for href, raw_txt in matches:
        clean_txt = re.sub(r"<[^>]+>", "", raw_txt).strip()
        full_href = urljoin(html_url, href)
        if not full_href.lower().endswith(".pdf"):
            continue
        ltxt = clean_txt.lower()
        # STRICTLY skip telephone-book sized applicant ID lists!
        if any(bad in ltxt for bad in ["identification document", "id number", "identity card", "id no", "id. no", "id card"]):
            continue
        if re.search(r"\bid\s*no\b", ltxt):
            continue
        pdf_links.append((clean_txt, full_href))

    if pdf_links:
        return pdf_links, None

    # Pure inline HTML announcement (no child PDFs)
    return [], r.text


# ----------------------------------------------------------------------
# 3. Parallel File Downloader
# ----------------------------------------------------------------------

def download_file(session: requests.Session, url: str, dest_path: Path, max_retries: int = 3) -> bool:
    """Download a file with polite retries; skip if already present and nonzero."""
    if dest_path.exists() and dest_path.stat().st_size > 0:
        return True

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(max_retries):
        try:
            r = session.get(url, headers={"User-Agent": UA}, timeout=30, stream=True)
            if r.status_code == 200:
                with open(dest_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                return True
            time.sleep(1.0 * (attempt + 1))
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return False


# ----------------------------------------------------------------------
# 4. Text Extraction & Keyword Filtering with PyMuPDF
# ----------------------------------------------------------------------

TIER1_PROS_PAGE_KEYWORDS = [
    # Category 1: Offering Statistics & Cover
    ["offer price", "maximum offer price", "sale shares", "new shares", "public offer shares", "placing shares", "over-allotment", "rule 8.05", "chapter 18a", "chapter 18c", "chapter 19a"],
    # Category 2: Corporate Information
    ["registered office", "principal place of business", "headquarter", "incorporated in"],
    # Category 3: History & Controlling Shareholders
    ["founded", "commenced", "predecessor", "established in", "controlling shareholder", "substantial shareholder"],
    # Category 4: Underwriting & Expenses
    ["underwriting commission", "total listing expenses", "aggregate fees", "listing expenses"],
    # Category 5: Financial Summary Statements
    ["consolidated statement of profit or loss", "consolidated income statement", "consolidated statement of financial position", "consolidated balance sheet", "consolidated statement of cash flows"]
]


def extract_pdf_pages_matching(pdf_path: Path, section_name: str, max_pages: int = 4) -> tuple[list[tuple[int, str]], int, int]:
    """Extract pages from a PDF. If section_name is known, extracts high-signal pages; otherwise applies Tier-1 filters."""
    pages_extracted = []
    total_chars = 0
    total_pages = 0

    try:
        doc = pymupdf.open(str(pdf_path))
        total_pages = len(doc)

        for p_idx in range(total_pages):
            page = doc[p_idx]
            raw_text = page.get_text()
            p_len = len(raw_text.strip())
            total_chars += p_len
            p_low = raw_text.lower()

            # Page selection logic
            select = False
            if section_name in ("cover", "corporate_info", "cornerstone"):
                select = True
            elif section_name == "summary" and p_idx < 4:
                select = True
            elif section_name in ("history", "controlling_shareholders", "share_capital", "offering_structure", "underwriting") and p_idx < 3:
                select = True
            elif section_name == "business" and p_idx < 2:
                select = True
            elif section_name in ("financial_info", "accountants_report"):
                # ONLY financial statement tables, NOT footnote pages!
                if any(stmt in p_low for stmt in [
                    "consolidated statement of profit or loss", "consolidated income statement",
                    "statements of profit or loss", "consolidated statement of financial position",
                    "consolidated balance sheet", "statements of financial position",
                    "consolidated statement of cash flows", "statements of cash flows"
                ]):
                    if "notes to the consolidated" not in p_low or p_len < 3000:
                        select = True
            else:
                # Monolithic full PDF: evaluate Tier-1 keyword categories
                for kw_group in TIER1_PROS_PAGE_KEYWORDS:
                    matches = sum(1 for kw in kw_group if kw in p_low)
                    if matches >= 2:
                        select = True
                        break

            if select:
                pages_extracted.append((p_idx + 1, clean_text(raw_text)))
                if len(pages_extracted) >= max_pages:
                    break

        doc.close()
    except Exception:
        pass

    return pages_extracted, total_chars, total_pages


def extract_allotment_text(pdf_paths: list[Path], html_body: str | None, max_total_pages: int = 4) -> tuple[list[tuple[int, str]], int, int, bool]:
    """Extract text from Allotment results (either PDFs or inline HTML)."""
    excerpts = []
    tot_chars = 0
    tot_pages = 0
    is_scanned = False

    if pdf_paths:
        for p in pdf_paths:
            try:
                doc = pymupdf.open(str(p))
                tot_pages += len(doc)
                for idx in range(len(doc)):
                    if len(excerpts) >= max_total_pages:
                        break
                    page = doc[idx]
                    t = clean_text(page.get_text())
                    tot_chars += len(t)
                    t_low = t.lower()

                    # Strict check: skip ID phonebook pages
                    if any(bad in t_low for bad in ["identification document number", "hong kong identity card", "id card no", "id no.:", "id no."]):
                        break
                    if re.search(r"identification\s+document\s+number", t_low) or ("identification" in t_low and "allotted" in t_low and "number" in t_low):
                        break

                    excerpts.append((idx + 1, t))
                doc.close()
            except Exception:
                pass
        avg_c = (tot_chars / max(tot_pages, 1))
        if tot_pages > 0 and avg_c < 50:
            is_scanned = True
    elif html_body:
        # Clean inline HTML
        tot_pages = 1
        clean_html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_body, flags=re.DOTALL | re.IGNORECASE)
        clean_html = re.sub(r"<br\s*/?>", "\n", clean_html, flags=re.IGNORECASE)
        clean_html = re.sub(r"</(p|div|tr|h[1-6])>", "\n", clean_html, flags=re.IGNORECASE)
        plain = clean_text(re.sub(r"<[^>]+>", " ", clean_html))
        # Remove massive tables of identity cards if any
        lines = []
        for line in plain.split("\n"):
            if re.search(r"[A-Z]\d{6}\(\d\)", line) or re.search(r"\d{7,8}\s+\d{2,}", line):
                continue
            lines.append(line)
        cleaned_body = "\n".join(lines).strip()
        tot_chars = len(cleaned_body)
        excerpts.append((1, cleaned_body[:10000]))

    return excerpts, tot_chars, tot_pages, is_scanned


# ----------------------------------------------------------------------
# 5. Packet Formatting & Size Enforcement
# ----------------------------------------------------------------------

def format_section_0(row: pd.Series) -> str:
    """Generate Section 0: Pre-filled Zero-Token Ground Truth."""
    code = row.get("stock_code")
    name = row.get("company_name_enr") or row.get("company_name")
    board = row.get("board_enr") or row.get("board")
    yr = int(row.get("cohort_year", 0))
    ld = row.get("listing_date_enr") or row.get("listing_date")
    pd_date = row.get("prospectus_date_enr") or row.get("prospectus_date")
    bbg_date = row.get("bbg_pricing_date") or "N/A"

    p_hkd = row.get("offer_price_hkd")
    p_str = f"HK$ {p_hkd:.3f}" if pd.notna(p_hkd) else "N/A"

    tot_hkd = row.get("funds_raised_total_hkd_enr") or row.get("funds_raised_total_hkd")
    tot_str = f"HK$ {tot_hkd:,.0f}" if pd.notna(tot_hkd) else "N/A"

    pub_hkd = row.get("funds_raised_public_hkd")
    pub_str = f"HK$ {pub_hkd:,.0f}" if pd.notna(pub_hkd) else "N/A"

    int_hkd = row.get("funds_raised_int_hkd")
    int_str = f"HK$ {int_hkd:,.0f}" if pd.notna(int_hkd) else "N/A"

    pub_share = row.get("public_tranche_proceeds_share")
    pub_share_str = f"{pub_share * 100:.2f}%" if pd.notna(pub_share) else "N/A"

    sponsors = row.get("sponsors") or "N/A"
    lead_sp = row.get("lead_sponsor") or "N/A"
    auditor = row.get("auditor") or "N/A"
    valuer = row.get("valuer") or "N/A"

    # GEM specifics
    is_gem = (board == "GEM")
    gem_inc = row.get("gem_incorporation") if is_gem and pd.notna(row.get("gem_incorporation")) else "N/A (Main Board)"
    gem_ind = row.get("gem_industry") if is_gem and pd.notna(row.get("gem_industry")) else "N/A (Main Board)"
    gem_mthd = row.get("gem_listing_method") if is_gem and pd.notna(row.get("gem_listing_method")) else "N/A (Main Board)"
    gem_shrs = row.get("gem_shares_at_listing") if is_gem and pd.notna(row.get("gem_shares_at_listing")) else "N/A"
    gem_mcap = row.get("gem_market_cap_hkd") if is_gem and pd.notna(row.get("gem_market_cap_hkd")) else "N/A"

    # Bloomberg ECDR & Governance
    isin = row.get("bbg_isin_enr") or row.get("bbg_isin") or "N/A"
    dom_code = row.get("isin_domicile_code") or "N/A"
    dom_jur = row.get("isin_domicile_jurisdiction") or "N/A"
    off_type = row.get("bbg_offer_type_raw") or "N/A"
    pe_vc = "True (1)" if row.get("bbg_pe_vc_backed_flag") == 1 else "False (0)"
    sec_sale = "True (1)" if row.get("bbg_secondary_sale_flag") == 1 else "False (0)"
    first_seller = row.get("bbg_first_selling_stockholder_raw") or "None (Pure Primary)"

    sub_ratio = row.get("retail_sub_ratio_clean_enr") or row.get("retail_sub_ratio_clean")
    sub_str = f"{sub_ratio:.2f}x" if pd.notna(sub_ratio) else "N/A"

    spread = row.get("gross_spread_clean_pct")
    spread_str = f"{spread:.2f}%" if pd.notna(spread) else "N/A"

    shoe_fac = row.get("greenshoe_facility_m")
    shoe_fac_str = f"{shoe_fac:.2f}M shares" if pd.notna(shoe_fac) else "N/A"
    shoe_ex = row.get("greenshoe_shares_exercised_m")
    shoe_ex_str = f"{shoe_ex:.2f}M shares" if pd.notna(shoe_ex) else "N/A"

    recycled = "True" if row.get("flag_recycled_or_transferred_ticker") == 1 else "False"
    delisted = "True" if row.get("flag_delisted_or_acquired") == 1 else "False"
    tercile = row.get("offer_size_tercile") or "N/A"
    role = row.get("stratification_role") or "N/A"

    sec0 = f"""## Section 0: Pre-filled Zero-Token Ground Truth

### A. Issuer & Offering Profile
| Attribute | Panel Value | Benchmark / Rule Field |
| :--- | :--- | :--- |
| **Stock Code** | `{code}` | Exchange Ticker |
| **Company Name** | **{name}** | Registered Corporate Title |
| **Market Board** | `{board}` | Listing Tier (Main Board / GEM) |
| **Cohort Year & Epoch** | `{yr}` ({row.get('epoch', 'N/A')}) | 33-Year Historical Period |
| **Listing Date** | `{ld}` | First Trading Day |
| **Prospectus Date** | `{pd_date}` | Formal Document Date |
| **Bloomberg Pricing Date** | `{bbg_date}` | ECDR Deal Pricing Anchor |
| **Offer Size Tercile** | `{tercile}` | Cohort Size Benchmark |
| **Stratification Role** | *{role}* | Stratified Pilot Sample Role |

### B. Capital Structure & Deal Economics
| Metric | Reported Value | Benchmark Definition |
| :--- | :--- | :--- |
| **Final Offer Price** | `{p_str}` | Offer Price per Share |
| **Total Funds Raised** | `{tot_str}` | Gross Proceeds (All Tranches) |
| **Public Tranche Proceeds** | `{pub_str}` | HK Public Offering Size |
| **Placing Tranche Proceeds** | `{int_str}` | International Placing Size |
| **Public Tranche Share** | `{pub_share_str}` | Retail Proportion of Total Issue |
| **Retail Subscription Ratio**| `{sub_str}` | Retail Oversubscription Multiple |
| **Gross Underwriting Spread**| `{spread_str}` | Total Syndicate Commission Rate |
| **Greenshoe Facility** | `{shoe_fac_str}` | Overallotment Option Granted |
| **Greenshoe Exercised** | `{shoe_ex_str}` | Overallotment Shares Issued |

### C. Advisory & Syndicate Governance
| Role | Appointed Institution | Source |
| :--- | :--- | :--- |
| **Lead Sponsor** | {lead_sp} | HKEX Official Record |
| **All Sponsors** | {sponsors} | HKEX Official Record |
| **Auditor / Reporting Accountants** | {auditor} | HKEX Official Record |
| **Property Valuer** | {valuer} | HKEX Official Record |

### D. Corporate Domicile, ECDR & Microstructure Flags
| Field | Value | Notes |
| :--- | :--- | :--- |
| **ISIN Code** | `{isin}` | Bloomberg International Identifier |
| **ISIN Domicile Jurisdiction** | `{dom_jur} ({dom_code})` | Statutory Incorporation Domicile |
| **Bloomberg Offer Type** | `{off_type}` | Primary / Secondary Classification |
| **PE / VC Backed Flag** | `{pe_vc}` | Financial Sponsor Presence |
| **Secondary Sale Flag** | `{sec_sale}` | Existing Shareholder Divestment |
| **First Selling Stockholder** | {first_seller} | Vendor Share Seller Details |
| **GEM Incorporation** | {gem_inc} | Official GEM Record |
| **GEM Industry Classification**| {gem_ind} | Official GEM Sector |
| **GEM Listing Method** | {gem_mthd} | Placing vs Public Offer |
| **GEM Shares at Listing** | {gem_shrs} | Total Shares in Issue |
| **GEM Market Capitalisation** | {gem_mcap} | Cap at Offer Price |
| **Recycled / Transferred Ticker** | `{recycled}` | Microstructure Cleaned Flag |
| **Delisted / Acquired Issuer** | `{delisted}` | Historical Survival Status |
"""
    return sec0


def trim_packet_budget(packet_text: str, target_bytes: int = 34000) -> str:
    """Multi-pass progressive condensation to guarantee total packet size <= target_bytes."""
    cur_len = len(packet_text.encode("utf-8"))
    if cur_len <= target_bytes:
        return packet_text

    # Progressive pass caps
    pass_caps = [900, 650, 450, 300, 200]
    blocks = packet_text.split("```text\n")
    if len(blocks) <= 1:
        return packet_text[:target_bytes]

    header_block = blocks[0]
    body_blocks = blocks[1:]

    for cap in pass_caps:
        condensed_blocks = [header_block]
        for blk in body_blocks:
            parts = blk.split("\n```")
            content = parts[0]
            remainder = "\n```" + ("\n```".join(parts[1:]) if len(parts) > 1 else "")
            if len(content) > cap:
                content = content[:cap].rstrip() + "\n... [Excerpt condensed for token efficiency] ..."
            condensed_blocks.append(content + remainder)

        candidate = "```text\n".join(condensed_blocks)
        if len(candidate.encode("utf-8")) <= target_bytes:
            return candidate

    # Fallback safety: truncate tail if still over target
    return candidate[:target_bytes]


def build_markdown_packet(
    row: pd.Series,
    allot_meta: dict | None,
    allot_excerpts: list[tuple[int, str]],
    pros_meta: dict | None,
    pros_excerpts: list[tuple[str, int, str]],
    allot_pages_count: int,
    pros_pages_count: int,
    is_scanned: bool,
    harvest_status: str
) -> str:
    """Assemble ultra-compact Markdown packet (target 15 KB - 35 KB)."""
    code = row["stock_code"]
    name = row.get("company_name_enr") or row.get("company_name")
    yr = int(row["cohort_year"])

    lines = []
    lines.append(f"# Pilot Issuer Packet: {code} - {name} ({yr})")
    lines.append(f"> **Pilot Stratification**: Batch {row.get('batch_id')} ({row.get('batch_name')}) | {row.get('stratification_role')}\n")

    # Section 0
    lines.append(format_section_0(row))

    # Section 1: Allotment Results
    lines.append("## Section 1: Allotment Results / Offer Price Announcement Excerpts\n")
    if harvest_status == "pre_1999_hkexnews_cutoff":
        lines.append("> **Historical Note**: Pre-1999 listing (April 1999 HKEXnews digital publication cutoff). Official IPO data preserved in Section 0 above from HKEX New Listing Reports and Bloomberg ECDR archival records.\n")
    elif allot_meta:
        lines.append(f"- **Document Title**: {allot_meta.get('TITLE', 'Allotment Announcement')}")
        lines.append(f"- **Filing Date**: {allot_meta.get('DATE_TIME', 'N/A')}")
        lines.append(f"- **Source URL**: {urljoin(HKEX_BASE, allot_meta.get('FILE_LINK', ''))}")
        lines.append(f"- **Document Type**: {allot_meta.get('doc_type', 'PDF')}\n")

        if allot_excerpts:
            for p_num, text in allot_excerpts:
                lines.append(f"### [DOC: ALLOT, PAGE: {p_num}]")
                lines.append(f"```text\n{text}\n```\n")
        else:
            lines.append("*[Notice: Document was indexed on HKEXnews but contains scanned image tables without OCR layer.]*\n")
    else:
        lines.append("*[Notice: No separate allotment results filing indexed within HKEXnews listing window.]*\n")

    # Section 2: Targeted Prospectus Excerpts
    lines.append("## Section 2: Targeted Prospectus Excerpts\n")
    if harvest_status == "pre_1999_hkexnews_cutoff":
        lines.append("> **Historical Note**: Pre-1999 listing. Primary physical prospectus published prior to digital archiving. See Section 0 for ground truth metrics.\n")
    elif pros_meta:
        lines.append(f"- **Document Title**: {pros_meta.get('TITLE', 'Prospectus')}")
        lines.append(f"- **Filing Date**: {pros_meta.get('DATE_TIME', 'N/A')}")
        lines.append(f"- **Source URL**: {urljoin(HKEX_BASE, pros_meta.get('FILE_LINK', ''))}")
        lines.append(f"- **Document Structure**: {pros_meta.get('doc_type', 'Single Full PDF')}\n")

        if pros_excerpts:
            for sec_name, p_num, text in pros_excerpts:
                lines.append(f"### [DOC: PROS, SECTION: {sec_name.upper()}, PAGE: {p_num}]")
                lines.append(f"```text\n{text}\n```\n")
        else:
            lines.append("*[Notice: Prospectus was indexed on HKEXnews but text extraction yielded image scans or empty text layer.]*\n")
    else:
        lines.append("*[Notice: Prospectus filing was not resolved in online query window.]*\n")

    # Section 3: Metadata & Audit Trail
    lines.append("## Section 3: Harvester Metadata & Audit Trail\n")
    now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"- **Harvest Timestamp**: `{now_str}`")
    lines.append(f"- **Harvest Status**: `{harvest_status}`")
    lines.append(f"- **Total Allotment Pages Extracted**: `{allot_pages_count}`")
    lines.append(f"- **Total Prospectus Pages Extracted**: `{pros_pages_count}`")
    lines.append(f"- **Is Scanned Image PDF**: `{'True' if is_scanned else 'False'}`")
    if is_scanned:
        lines.append("- **Scanned PDF Note**: Text density < 50 chars/page. Issuer document requires OCR layer if character-level inspection is needed.")

    raw_packet = "\n".join(lines).strip()

    # Enforce strict packet size budget: <= 34,500 bytes (target max ~8,000 tokens)
    if len(raw_packet.encode("utf-8")) > 34500:
        raw_packet = trim_packet_budget(raw_packet, target_bytes=34000)

    return raw_packet


# ----------------------------------------------------------------------
# 6. Main Harvester Workflow
# ----------------------------------------------------------------------

def process_issuer(
    row: pd.Series,
    session: requests.Session,
    query_cache: dict
) -> dict:
    """Harvest documents and build condensed packet for a single pilot issuer."""
    b_id = int(row["batch_id"])
    code = str(row["stock_code"]).strip()
    name = str(row.get("company_name_enr") or row.get("company_name")).strip()
    yr = int(row["cohort_year"])
    board = str(row.get("board_enr") or row.get("board")).strip()
    tercile = str(row.get("offer_size_tercile", "N/A"))

    code_clean = code.replace(".", "_")
    issuer_raw_dir = RAW_DOCS_DIR / f"{b_id}_{code_clean}"
    issuer_raw_dir.mkdir(parents=True, exist_ok=True)
    packet_path = PACKETS_DIR / f"{b_id}_{code_clean}.md"

    # Pre-1999 issuers (1994-1998)
    if yr <= 1998:
        harvest_status = "pre_1999_hkexnews_cutoff"
        pkt_text = build_markdown_packet(
            row=row,
            allot_meta=None,
            allot_excerpts=[],
            pros_meta=None,
            pros_excerpts=[],
            allot_pages_count=0,
            pros_pages_count=0,
            is_scanned=False,
            harvest_status=harvest_status
        )
        packet_path.write_text(pkt_text, encoding="utf-8")
        pkt_size = packet_path.stat().st_size
        return {
            "batch_id": b_id,
            "batch_name": row.get("batch_name"),
            "stock_code": code,
            "company_name": name,
            "cohort_year": yr,
            "board": board,
            "offer_size_tercile": tercile,
            "harvest_status": harvest_status,
            "prospectus_title": "Archival Print Prospectus (Pre-1999 Cutoff)",
            "prospectus_format": "pre_1999_cutoff",
            "prospectus_url": "N/A (Pre-1999 Physical Archive)",
            "allotment_title": "Archival Print Announcement (Pre-1999 Cutoff)",
            "allotment_format": "pre_1999_cutoff",
            "allotment_url": "N/A (Pre-1999 Physical Archive)",
            "packet_path": str(packet_path.relative_to(ROOT)),
            "packet_size_bytes": pkt_size,
            "packet_char_count": len(pkt_text),
            "allotment_pages_extracted": 0,
            "prospectus_pages_extracted": 0,
            "is_scanned_image_pdf": False,
            "notes": "Pre-1999 HKEXnews digital publication cutoff; Section 0 populated from NLR & Bloomberg ECDR"
        }

    # Online Issuers (1999-2024)
    harvest_status = "online_hkexnews_harvested"
    stock_id = int(row["hkex_stock_id"])
    sid_status = str(row.get("hkex_probe_status", "online_query_success"))

    # Multi-anchor date span: take min and max across all date fields
    date_anchors = []
    for f in ["listing_date_enr", "listing_date", "prospectus_date_enr", "prospectus_date", "bbg_pricing_date"]:
        val = row.get(f)
        d = parse_date_safe(val)
        if d:
            date_anchors.append(d)
    if not date_anchors:
        date_anchors = [dt.date(yr, 6, 1)]

    min_date = min(date_anchors)
    max_date = max(date_anchors)

    docs = query_hkex_filings(session, stock_id, sid_status, min_date, max_date, query_cache)

    pros_doc = pick_refined_prospectus(docs)
    allot_doc = pick_refined_allotment(session, docs)

    # 1. Harvest Allotment Results
    allot_excerpts = []
    allot_pages_count = 0
    allot_scanned = False
    allot_format = "none_found"
    allot_url = ""

    if allot_doc:
        allot_link = allot_doc.get("FILE_LINK") or ""
        allot_url = urljoin(HKEX_BASE, allot_link)
        allot_doc["doc_type"] = "Single PDF" if allot_link.lower().endswith(".pdf") else "HTML Announcement"

        if allot_link.lower().endswith((".htm", ".html")):
            child_pdfs, inline_html = parse_allotment_html(session, allot_url)
            if child_pdfs:
                allot_format = "multi_section_html_pdf"
                allot_doc["doc_type"] = "HTML Wrapper (Cover + Summary PDFs)"
                downloaded_allot_pdfs = []
                for idx, (title, curl) in enumerate(child_pdfs[:2]):  # Download Cover + Summary
                    fn = f"allot_sec_{idx+1}_{curl.split('/')[-1]}"
                    dp = issuer_raw_dir / fn
                    if download_file(session, curl, dp):
                        downloaded_allot_pdfs.append(dp)
                allot_excerpts, _, allot_pages_count, allot_scanned = extract_allotment_text(downloaded_allot_pdfs, None, max_total_pages=4)
            else:
                allot_format = "inline_html"
                allot_doc["doc_type"] = "Inline HTML Announcement"
                html_path = issuer_raw_dir / "allotment_announcement.htm"
                html_path.write_text(inline_html or "", encoding="utf-8")
                allot_excerpts, _, allot_pages_count, allot_scanned = extract_allotment_text([], inline_html, max_total_pages=1)
        else:
            allot_format = "single_pdf"
            pdf_path = issuer_raw_dir / "allotment_announcement.pdf"
            if download_file(session, allot_url, pdf_path):
                allot_excerpts, _, allot_pages_count, allot_scanned = extract_allotment_text([pdf_path], None, max_total_pages=4)

    # 2. Harvest Prospectus
    pros_excerpts = []
    pros_pages_count = 0
    pros_scanned = False
    pros_format = "none_found"
    pros_url = ""

    if pros_doc:
        pros_link = pros_doc.get("FILE_LINK") or ""
        pros_url = urljoin(HKEX_BASE, pros_link)

        if pros_link.lower().endswith((".htm", ".html")):
            # Check if this HTML is a Multi-Section index of PDFs
            sec_links = parse_prospectus_html_sections(session, pros_url)
            if sec_links:
                pros_format = "multi_section_html_pdf"
                pros_doc["doc_type"] = "Multi-Section HTML Index"
                for sec_key, (sec_title, sec_href) in sec_links.items():
                    fn = f"pros_sec_{sec_key}_{sec_href.split('/')[-1]}"
                    sec_path = issuer_raw_dir / fn
                    if download_file(session, sec_href, sec_path):
                        pages, chars, tot_p = extract_pdf_pages_matching(sec_path, sec_key, max_pages=2)
                        for p_idx, text in pages:
                            pros_excerpts.append((sec_key, p_idx, text))
                            pros_pages_count += 1
                        if tot_p > 0 and (chars / tot_p) < 50:
                            pros_scanned = True
            else:
                # Early inline announcement
                pros_format = "inline_html"
                pros_doc["doc_type"] = "Formal Notice / Inline HTML"
                r = session.get(pros_url, headers={"User-Agent": UA}, timeout=15)
                html_p = issuer_raw_dir / "prospectus_notice.htm"
                html_p.write_text(r.text, encoding="utf-8")
                clean_body = clean_text(re.sub(r"<[^>]+>", " ", r.text))
                pros_excerpts.append(("notice", 1, clean_body[:8000]))
                pros_pages_count = 1
        else:
            pros_format = "single_pdf"
            pros_doc["doc_type"] = "Single Full PDF"
            pdf_path = issuer_raw_dir / "prospectus_full.pdf"
            if download_file(session, pros_url, pdf_path):
                pages, chars, tot_p = extract_pdf_pages_matching(pdf_path, "full_pdf", max_pages=10)
                for p_idx, text in pages:
                    pros_excerpts.append(("prospectus", p_idx, text))
                    pros_pages_count += 1
                if tot_p > 0 and (chars / tot_p) < 50:
                    pros_scanned = True

    overall_scanned = allot_scanned or pros_scanned

    # Build Markdown Packet
    pkt_text = build_markdown_packet(
        row=row,
        allot_meta=allot_doc,
        allot_excerpts=allot_excerpts,
        pros_meta=pros_doc,
        pros_excerpts=pros_excerpts,
        allot_pages_count=allot_pages_count,
        pros_pages_count=pros_pages_count,
        is_scanned=overall_scanned,
        harvest_status=harvest_status
    )
    packet_path.write_text(pkt_text, encoding="utf-8")
    pkt_size = packet_path.stat().st_size

    notes = []
    if overall_scanned:
        notes.append("Scanned image PDF detected (low char density)")
    if pros_format == "multi_section_html_pdf":
        notes.append("Selective section PDFs downloaded")
    elif pros_format == "single_pdf":
        notes.append("Full PDF page filtered")
    if allot_format == "multi_section_html_pdf":
        notes.append("Allotment ID numbers skipped")

    return {
        "batch_id": b_id,
        "batch_name": row.get("batch_name"),
        "stock_code": code,
        "company_name": name,
        "cohort_year": yr,
        "board": board,
        "offer_size_tercile": tercile,
        "harvest_status": harvest_status,
        "prospectus_title": (pros_doc.get("TITLE") if pros_doc else "Not Found"),
        "prospectus_format": pros_format,
        "prospectus_url": pros_url or "Not Found",
        "allotment_title": (allot_doc.get("TITLE") if allot_doc else "Not Found"),
        "allotment_format": allot_format,
        "allotment_url": allot_url or "Not Found",
        "packet_path": str(packet_path.relative_to(ROOT)),
        "packet_size_bytes": pkt_size,
        "packet_char_count": len(pkt_text),
        "allotment_pages_extracted": allot_pages_count,
        "prospectus_pages_extracted": pros_pages_count,
        "is_scanned_image_pdf": overall_scanned,
        "notes": "; ".join(notes) or "Harvested cleanly"
    }


def main():
    print("=" * 80)
    print("STEP 1: 48-ISSUER PILOT HARVESTER & CONDENSED PACKET BUILDER")
    print("=" * 80)

    RAW_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    PACKETS_DIR.mkdir(parents=True, exist_ok=True)

    df_probe = pd.read_csv(PROBE_CSV)
    df_enr = pd.read_csv(ENRICHED_CSV)
    merged = pd.merge(df_probe, df_enr, on=["stock_code", "cohort_year"], suffixes=("_probe", "_enr"))
    print(f"Loaded {len(merged)} stratified pilot issuers (Probe N={len(df_probe)}, Enriched N={len(df_enr)}).")

    session = requests.Session()

    # Load or initialize query cache
    query_cache = {}
    if CACHE_JSON.exists():
        try:
            query_cache = json.loads(CACHE_JSON.read_text(encoding="utf-8"))
            print(f"Loaded existing HKEX query cache: {len(query_cache)} queries cached.")
        except Exception:
            query_cache = {}

    start_time = time.time()
    manifest_rows = []

    print("\nProcessing all 48 pilot issuers with ThreadPoolExecutor(max_workers=6)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_code = {
            executor.submit(process_issuer, row, session, query_cache): row["stock_code"]
            for _, row in merged.iterrows()
        }
        for future in concurrent.futures.as_completed(future_to_code):
            code = future_to_code[future]
            try:
                res = future.result()
                manifest_rows.append(res)
                print(f"  [DONE] {res['batch_id']} | {res['stock_code']:8} | {res['company_name'][:25]:25} | Pkt: {res['packet_size_bytes']/1024:5.1f} KB | Pros: {res['prospectus_format']:22} | Allot: {res['allotment_format']}")
            except Exception as exc:
                print(f"  [ERROR] {code}: {exc}")

    # Save query cache
    try:
        CACHE_JSON.write_text(json.dumps(query_cache, indent=2), encoding="utf-8")
    except Exception:
        pass

    # Sort manifest rows by batch_id and stock_code
    manifest_rows.sort(key=lambda x: (x["batch_id"], x["stock_code"]))
    df_manifest = pd.DataFrame(manifest_rows)
    df_manifest.to_csv(MANIFEST_CSV, index=False)
    print(f"\nSaved master manifest to: {MANIFEST_CSV}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print("SUMMARY AUDIT REPORT")
    print("=" * 80)
    print(f"Total Issuers Processed: {len(df_manifest)}/48")
    print(f"Pre-1999 Cutoff: {(df_manifest['harvest_status'] == 'pre_1999_hkexnews_cutoff').sum()}")
    print(f"Online Harvested: {(df_manifest['harvest_status'] == 'online_hkexnews_harvested').sum()}")
    print(f"Prospectuses Found: {(df_manifest['prospectus_format'] != 'none_found').sum()}/48")
    print(f"Allotments Found: {(df_manifest['allotment_format'] != 'none_found').sum()}/48")
    print(f"Multi-Section HTML Prospectuses: {(df_manifest['prospectus_format'] == 'multi_section_html_pdf').sum()}")
    print(f"Single Full PDF Prospectuses: {(df_manifest['prospectus_format'] == 'single_pdf').sum()}")
    print(f"Scanned Image PDFs: {df_manifest['is_scanned_image_pdf'].sum()}")

    sizes_kb = df_manifest["packet_size_bytes"] / 1024
    print("\nPacket Size Distribution (KB):")
    print(f"  Min:    {sizes_kb.min():.1f} KB")
    print(f"  Mean:   {sizes_kb.mean():.1f} KB")
    print(f"  Median: {sizes_kb.median():.1f} KB")
    print(f"  Max:    {sizes_kb.max():.1f} KB")
    print(f"  Issuers <= 35 KB: {(sizes_kb <= 35.0).sum()}/48")
    print(f"  Issuers between 15 KB and 35 KB: {sizes_kb.between(15.0, 35.0).sum()}/48")
    print(f"Total Execution Time: {elapsed:.1f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    main()
