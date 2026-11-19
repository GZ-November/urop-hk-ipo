"""Shared filing-grounded parsers for historical HKEX IPO packets (1994-2024).

Fixes two critical archival extraction bugs identified in peer-review audit:
1. Short-circuit `fn_text or all_text` bug that skipped `pros_text`/`allot_text`
   when `fn_text` was non-empty but lacked the indicative offer price range.
2. Single-line regex (`[^.\\n\\r]*?`) & unconditional `0.0` fallback on `col_CK`
   (cornerstone / corporate investor allocation %), replacing it with multi-line
   share/percentage parsing and strict three-state separation:
   - Verified positive commitment (`col_CK > 0`, `has_cs = 1`),
   - Verified presence with truncated share count (`col_CK = None`, `has_cs = 1`),
   - Verified absence in substantive allotment filing (`col_CK = 0.0`, `has_cs = 0`),
   - Unverified / missing allotment text (`col_CK = None`, `has_cs = None`).
"""

from __future__ import annotations

import re
from typing import Optional


def _norm(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()


def _parse_float(s: str | None) -> Optional[float]:
    if not s:
        return None
    cleaned = str(s).replace(",", "").strip().rstrip(".")
    try:
        val = float(cleaned)
        return val if val > 0 else None
    except ValueError:
        return None


def refine_indicative_price_range(
    fn_text: str,
    allot_text: str,
    pros_text: str,
    offer_price: Optional[float],
    existing_t: Optional[float],
    existing_u: Optional[float],
    existing_t_quote: str,
    existing_u_quote: str,
) -> tuple[Optional[float], Optional[float], str, str]:
    """Search across fn_text, allot_text, and pros_text sequentially without short-circuiting."""
    t_val, u_val = existing_t, existing_u
    t_quote, u_quote = existing_t_quote or "", existing_u_quote or ""

    def _plausible(p: Optional[float]) -> bool:
        if p is None or p <= 0:
            return False
        if offer_price and offer_price > 0:
            ratio = p / float(offer_price)
            return 0.45 <= ratio <= 2.20
        return 0.01 <= p <= 2000.0

    if not _plausible(t_val):
        t_val, t_quote = None, ""
    if not _plausible(u_val):
        u_val, u_quote = None, ""

    sources = [_norm(fn_text), _norm(allot_text), _norm(pros_text)]

    range_patterns = [
        # (group1_is_max, regex)
        (
            True,
            r"not\s+more\s+than\s+HK\$\s*([\d\.]+)\s*(?:per\s+(?:Offer\s+|Placing\s+|H\s+)?Share\s*)?(?:and\s+)?(?:is\s+)?(?:currently\s+)?expected\s+to\s+be\s+not\s+less\s+than\s+HK\$\s*([\d\.]+)",
        ),
        (
            True,
            r"not\s+more\s+than\s+HK\$\s*([\d\.]+).{0,80}?not\s+less\s+than\s+HK\$\s*([\d\.]+)",
        ),
        (
            False,
            r"(?:indicative\s+)?(?:Offer|Placing|Issue|Subscription)\s+Price\s+range\s+(?:is\s+|of\s+|was\s+|between\s+)?HK\$\s*([\d\.]+)\s*(?:per\s+Share\s*)?(?:to|and|-|–)\s*HK\$\s*([\d\.]+)",
        ),
        (
            False,
            r"between\s+HK\$\s*([\d\.]+)\s+and\s+HK\$\s*([\d\.]+)\s+per\s+(?:Offer\s+|Placing\s+|H\s+)?Share",
        ),
    ]

    for src in sources:
        if not src:
            continue
        if t_val is not None and u_val is not None:
            break
        for first_is_max, pat in range_patterns:
            m = re.search(pat, src, re.I)
            if m:
                v1 = _parse_float(m.group(1))
                v2 = _parse_float(m.group(2))
                if _plausible(v1) and _plausible(v2):
                    hi = max(v1, v2)
                    lo = min(v1, v2)
                    t_val, u_val = hi, lo
                    q = _norm(m.group(0))[:240]
                    t_quote, u_quote = q, q
                    break

    # Individual bounds fallback across all sources
    if t_val is None:
        for src in sources:
            if not src:
                continue
            m_max = re.search(
                r"(?:maximum\s+(?:offer|placing)\s+price|not\s+more\s+than|expected\s+to\s+be\s+not\s+more\s+than)\s*(?:is\s+|of\s+|:)?\s*HK\$\s*([\d\.]+)",
                src,
                re.I,
            )
            if m_max:
                cand = _parse_float(m_max.group(1))
                if _plausible(cand):
                    t_val = cand
                    t_quote = _norm(m_max.group(0))[:220]
                    break

    if u_val is None:
        for src in sources:
            if not src:
                continue
            m_min = re.search(
                r"(?:minimum\s+(?:offer|placing)\s+price|not\s+less\s+than|expected\s+to\s+be\s+not\s+less\s+than|(?:low-end|bottom\s+end|low\s+end)\s+of\s+the\s+(?:indicative\s+)?(?:Offer|Placing)\s+Price\s+range.{0,25}?)\s*HK\$\s*([\d\.]+)",
                src,
                re.I,
            )
            if m_min:
                cand = _parse_float(m_min.group(1))
                if _plausible(cand):
                    u_val = cand
                    u_quote = _norm(m_min.group(0))[:220]
                    break

    # Explicit fixed-price offers (only when NO range wording appears anywhere in prospectus or formal notice)
    combined = " ".join(s for s in sources if s)
    has_range_wording = bool(
        re.search(
            r"not\s+more\s+than|not\s+less\s+than|price\s+range|maximum\s+(?:offer|placing)\s+price|indicative\s+(?:offer|placing)\s+price",
            combined,
            re.I,
        )
    )
    if t_val is None and u_val is None and not has_range_wording:
        for src in (_norm(fn_text), _norm(pros_text)):
            if not src:
                continue
            m_fix = re.search(
                r"(?:Offer|Placing|Subscription|Issue)\s+Price\s*[:\s]+HK\$\s*([\d\.]+)\s+per\s+(?:Offer\s+|Placing\s+|H\s+)?Share",
                src,
                re.I,
            )
            if m_fix:
                cand = _parse_float(m_fix.group(1))
                if _plausible(cand):
                    t_val, u_val = cand, cand
                    q = _norm(m_fix.group(0))[:220]
                    t_quote, u_quote = q, q
                    break

    if t_val is not None and u_val is not None and u_val > t_val:
        t_val, u_val = u_val, t_val

    return t_val, u_val, t_quote, u_quote


def parse_cornerstone_commitment(
    allot_text: str,
    pros_text: str,
    m_val: Optional[float],
    l_val: Optional[float],
    cohort_year: int,
    is_placing_only: bool = False,
) -> tuple[Optional[float], Optional[float], str]:
    """Extract Cornerstone / Corporate Investor allocation % of Offer Shares (`col_CK`).

    Returns:
        (ck_pct, has_cs_flag, quote)
        - ck_pct: float in [0.0, 95.0] or None (when unverified or share count truncated)
        - has_cs_flag: 1.0 (verified present), 0.0 (verified absent), or None (unverified)
    """
    if cohort_year <= 2004:
        return (
            0.0,
            0.0,
            "Pre-cornerstone era (HKEX cornerstone/corporate lockup placing introduced in 2005).",
        )
    if is_placing_only and cohort_year <= 2012:
        # Check if explicit cornerstone mentioned anyway; if not, 0.0
        if "cornerstone" not in (allot_text or "").lower() and "cornerstone" not in (pros_text or "").lower():
            return (0.0, 0.0, "GEM placing-only offering without cornerstone tranche (0.0%).")

    norm_allot = _norm(allot_text)
    norm_pros = _norm(pros_text)
    low_allot = norm_allot.lower()
    low_pros = norm_pros.lower()

    # Detect genuine cornerstone / locked-up corporate investor placing signals
    # Exclude certificate collection boilerplate ("authorised representative of a corporate investor")
    clean_allot_for_flag = re.sub(
        r"authorised\s+representative\s+of\s+a\s+corporate\s+investor", "", low_allot
    )
    clean_allot_for_flag = re.sub(
        r"\d+\s+individual\s+investors?,\s+\d+\s+corporate\s+investors?", "", clean_allot_for_flag
    )

    has_explicit_cs_signal = bool(
        re.search(
            r"cornerstone\s+(?:investor|placing|investment|offer)|"
            r"corporate\s+placing|"
            r"pursuant\s+to\s+the\s+placing\s+agreements?\s+with\s+(?:the\s+|our\s+)?corporate\s+investors?|"
            r"section\s+headed\s+[\"'“”]?corporate\s+investors?[\"'“”]?|"
            r"purchased\s+by\s+the\s+corporate\s+investors?\s+will\s+be|"
            r"subscribed\s+for\s+by\s+the\s+corporate\s+investors?",
            clean_allot_for_flag + " " + low_pros,
            re.I,
        )
    )

    def _valid_pct(val: Optional[float]) -> bool:
        return val is not None and 0.2 <= val <= 92.0

    # Priority 1: Explicit "% of the Offer Shares / Global Offering" in allotment text
    pct_offer_patterns = [
        r"(?:Cornerstone|Corporate)\s+Investors?\s+(?:have|has|will)?\s*(?:subscribed\s+for|purchased|been\s+allotted|acquired).{0,280}?(?:representing|approximately|amounts?\s+to|equivalent\s+to)\s+(?:in\s+aggregate\s+)?(?:approximately\s+)?([\d\.]+)\s*%\s+of\s+(?:the\s+)?(?:total\s+number\s+of\s+)?(?:Offer\s+Shares|H\s+Shares\s+initially\s+available|Shares\s+initially\s+available\s+under\s+the\s+Global\s+Offering|Shares\s+in\s+the\s+Global\s+Offering)",
        r"total\s+number\s+of\s+(?:Offer\s+|H\s+)?Shares\s+(?:subscribed\s+for|purchased|to\s+be\s+subscribed\s+for)\s+(?:or\s+purchased\s+)?by\s+(?:the\s+)?(?:Cornerstone|Corporate)\s+Investors?.{0,220}?([\d\.]+)\s*%\s+of\s+(?:the\s+)?(?:total\s+number\s+of\s+)?(?:Offer\s+Shares|Global\s+Offering)",
        r"Total.{0,40}?Cornerstone.{0,80}?([\d\.]+)\s*%\s+of\s+(?:the\s+)?Offer\s+Shares",
    ]
    for pat in pct_offer_patterns:
        m = re.search(pat, norm_allot, re.I)
        if m:
            cand = _parse_float(m.group(1))
            if _valid_pct(cand):
                return (round(float(cand), 2), 1.0, _norm(m.group(0))[:260])

    # Priority 2: Explicit aggregate share count subscribed by Cornerstone / Corporate Investors -> divide by m_val
    if m_val and m_val > 0:
        agg_share_patterns = [
            r"(?:total\s+number\s+of\s+(?:Cornerstone\s+)?(?:Offer\s+|H\s+)?Shares\s+(?:to\s+be\s+)?(?:subscribed|purchased|allotted|acquired)(?:\s+for)?(?:\s+or\s+purchased)?\s+by\s+(?:the\s+|our\s+)?(?:Cornerstone|Corporate)\s+Investors?|Shares\s+to\s+be\s+allotted\s+and\s+issued\s+to\s+the\s+(?:Cornerstone|Corporate)\s+Investors?)\s*(?:will\s+be|is|was|are|were|:)?\s*(?:an\s+aggregate\s+of\s+|approximately\s+)?([\d,]+(?:\.\d+)?)\s*(million)?",
            r"(?:Cornerstone|Corporate)\s+Investors?,?\s+(?:have|has|will|would)\s+(?:subscribe|subscribed|purchase|purchased|acquire|acquired)(?:\s+for)?(?:\s+or\s+purchased)?\s+(?:an\s+aggregate\s+of\s+|a\s+total\s+of\s+|approximately\s+)?([\d,]+(?:\.\d+)?)\s*(million)?\s+(?:Offer\s+|H\s+)?Shares",
            r"(?:A\s+total\s+of|An\s+aggregate\s+of)\s+([\d,]+(?:\.\d+)?)\s*(million)?\s+(?:Offer\s+|H\s+)?Shares\s+(?:have\s+been|were|will\s+be)\s+(?:subscribed|purchased)(?:\s+for)?\s+by\s+[^\.;]{0,120}?(?:Cornerstone|Corporate)\s+Investor",
            r"total\s+number\s+of\s+Cornerstone\s+Offer\s+Shares\s*[:\s]+([\d,]+)\s*()",
        ]
        for pat in agg_share_patterns:
            m = re.search(pat, norm_allot, re.I)
            if m:
                raw_n = _parse_float(m.group(1))
                is_mil = bool(m.group(2))
                if raw_n:
                    shrs = raw_n * 1e6 if is_mil else raw_n
                    if shrs >= 10_000:
                        pct = round((shrs / float(m_val)) * 100.0, 2)
                        if _valid_pct(pct):
                            return (
                                pct,
                                1.0,
                                f"{_norm(m.group(0))[:200]} [{int(shrs):,} / {int(m_val):,} Offer Shares = {pct:.2f}%]",
                            )

        # Priority 3: Bounded Cornerstone / Corporate Investors section in allotment text -> sum individual investor share allocations
        m_sec = re.search(
            r"(?:CORNERSTONE\s+INVESTORS?|CORPORATE\s+INVESTORS?)(.{40,2200}?)(?:PLACING|INTERNATIONAL\s+(?:OFFERING|PLACING)|PUBLIC\s+FLOAT|OVER-ALLOTMENT|BASIS\s+OF\s+ALLOTMENT|RESULTS\s+OF\s+ALLOCATIONS|SHAREHOLDING|LOCK-UP|$)",
            norm_allot,
        )
        if not m_sec and has_explicit_cs_signal:
            m_sec = re.search(
                r"(?:pursuant\s+to\s+the\s+cornerstone\s+(?:investor|investment|placing)\s+agreements?|allocations?\s+of\s+each\s+of\s+the\s+cornerstone\s+investors?)(.{30,1800}?)(?:PUBLIC\s+FLOAT|OVER-ALLOTMENT|INTERNATIONAL\s+PLACING|RESULTS\s+OF|$)",
                norm_allot,
                re.I,
            )
        if m_sec:
            block = m_sec.group(1)
            # Case 3a: "each of A, B and C has agreed to purchase X Shares"
            m_each = re.search(
                r"each\s+of\s+(.{10,260}?)\s+has\s+(?:agreed\s+to\s+purchase|purchased|subscribed\s+for)\s+([\d,]+)\s+(?:Offer\s+|H\s+)?Shares",
                block,
                re.I,
            )
            if m_each:
                per_sh = _parse_float(m_each.group(2))
                names_part = m_each.group(1)
                n_inv = names_part.count(",") + (1 if " and " in names_part.lower() else 0) + 1
                if per_sh and 2 <= n_inv <= 12:
                    tot_sh = per_sh * n_inv
                    pct = round((tot_sh / float(m_val)) * 100.0, 2)
                    if _valid_pct(pct):
                        return (
                            pct,
                            1.0,
                            f"Equal cornerstone tranches ({n_inv} x {int(per_sh):,} = {int(tot_sh):,} shares, {pct:.2f}%): {_norm(m_each.group(0))[:180]}",
                        )

            # Case 3b: Explicit verb + share counts ("has purchased 88,068,000 Shares")
            verb_shares = [
                _parse_float(x)
                for x in re.findall(
                    r"(?:has\s+purchased|have\s+purchased|agreed\s+to\s+purchase|has\s+subscribed\s+for|subscribed\s+for|be\s+allotted)\s+([\d,]{6,})\s+(?:Offer\s+|H\s+)?Shares",
                    block,
                    re.I,
                )
            ]
            verb_shares = [v for v in verb_shares if v and v < float(m_val) * 0.92]
            if verb_shares:
                # If last number equals sum of prior numbers, it's a total row
                if len(verb_shares) >= 3 and abs(verb_shares[-1] - sum(verb_shares[:-1])) / max(verb_shares[-1], 1.0) < 0.01:
                    tot_sh = verb_shares[-1]
                else:
                    tot_sh = sum(verb_shares)
                pct = round((tot_sh / float(m_val)) * 100.0, 2)
                if _valid_pct(pct):
                    return (
                        pct,
                        1.0,
                        f"Summed cornerstone investor share allocations ({int(tot_sh):,} / {int(m_val):,} = {pct:.2f}%): {_norm(block)[:180]}",
                    )

            # Case 3c: Tabular rows inside `NUMBER OF SHARES` cornerstone table
            if "NUMBER OF SHARES" in block.upper() or "OFFER SHARES SUBSCRIBED" in block.upper():
                tab_nums = [
                    _parse_float(x)
                    for x in re.findall(r"\b(\d{1,3}(?:,\d{3})+)\b", block)
                ]
                tab_nums = [v for v in tab_nums if v and 50_000 <= v <= float(m_val) * 0.90]
                if tab_nums:
                    if len(tab_nums) >= 3 and abs(tab_nums[-1] - sum(tab_nums[:-1])) / max(tab_nums[-1], 1.0) < 0.01:
                        tot_sh = tab_nums[-1]
                    else:
                        tot_sh = sum(tab_nums)
                    pct = round((tot_sh / float(m_val)) * 100.0, 2)
                    if _valid_pct(pct):
                        return (
                            pct,
                            1.0,
                            f"Tabular cornerstone shares ({int(tot_sh):,} / {int(m_val):,} = {pct:.2f}%): {_norm(block)[:180]}",
                        )

    # Priority 4: "% of enlarged/issued share capital" converted via (l_val / m_val)
    if m_val and l_val and m_val > 0 and l_val >= m_val:
        m_cap = re.search(
            r"(?:Cornerstone|Corporate)\s+Investors?.{0,260}?([\d\.]+)\s*%\s+of\s+(?:the\s+|interest\s+in\s+the\s+)?(?:Company.{0,20}?)?(?:enlarged\s+)?(?:total\s+)?issued\s+share\s+capital",
            norm_allot,
            re.I,
        )
        if m_cap:
            pct_cap = _parse_float(m_cap.group(1))
            if pct_cap and 0.1 <= pct_cap <= 50.0:
                pct_off = round(pct_cap * (float(l_val) / float(m_val)), 2)
                if _valid_pct(pct_off):
                    return (
                        pct_off,
                        1.0,
                        f"{_norm(m_cap.group(0))[:190]} [Converted via L/M = {pct_off:.2f}% of Offer Shares]",
                    )

    # Priority 5: Explicit cornerstone presence in filing, even if share/percentage excerpt was condensed
    if has_explicit_cs_signal:
        return (
            None,
            1.0,
            "[CONFIRMED_CS_PRESENT] Cornerstone / locked-up corporate investor tranche confirmed in filing, but exact share allocation omitted in condensed excerpt (left as NaN, never zero-imputed).",
        )

    # Priority 6: Distinguish verified absence (`0.0`) from missing/condensed allotment text (`None`)
    has_substantive_allot = (
        len(norm_allot) >= 1600
        and bool(
            re.search(
                r"international\s+(?:placing|offering)|basis\s+of\s+allotment|results\s+of\s+allocations|placees",
                low_allot,
            )
        )
    )
    if has_substantive_allot:
        return (
            0.0,
            0.0,
            "[VERIFIED_NO_CS] Substantive allotment announcement inspected; no cornerstone or locked-up corporate investors disclosed (0.0%).",
        )

    return (
        None,
        None,
        "[UNVERIFIED_ALLOT] Allotment placing breakdown absent or condensed in archival packet; left as NaN rather than zero-filled.",
    )
