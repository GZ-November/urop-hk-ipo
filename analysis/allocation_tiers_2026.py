"""Extract disclosed retail allocation tiers; retain evidence and quarantine failures.

No workbook mutations. Counts and allocations are reconciled with master totals;
semantic review is separate from these deterministic checks.
"""
from __future__ import annotations

import hashlib
import json
import re

import pandas as pd

from research_inputs import ROOT, load_panel, select_2026

OUT = ROOT / "pipeline/reports/data_gap_collection"
DATA = ROOT / "pipeline/prospectus_pipeline/data/allot/text"
N = r"[\d,]+"
ROW = re.compile(rf"(?m)^\s*({N})\s+({N})\s+({N}\s+(?:out\s+of|(?:H\s+)?(?:Shares|HDRs)).*?)\s+(\d+(?:\.\d+)?)\s*%", re.S | re.I)
LOT = re.compile(rf"board\s+lots\s+of\s+({N})\s+(?:(?:Class\s+[AB]\s+)?(?:Ordinary\s+)?|H\s+)(?:Shares|HDRs)", re.I)
BALLOT = re.compile(rf"({N})\s+out\s+of\s+({N})\s+(?:(?:applicants?|applications?)\s+)?to\s+receive\s+(?:(?:an?\s+)?additional\s+)?({N})\s+(?:H\s+)?(?:Shares|HDRs)", re.I)
FIXED = re.compile(rf"^({N})\s+(?:H\s+)?(?:Shares|HDRs)(?:\s+plus\b|$)", re.I)


def integer(s: str) -> int:
    return int(s.replace(",", ""))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tiers, issuers = [], []
    for _, issuer in select_2026(load_panel()).iterrows():
        code = issuer["Stock Code"]
        path = DATA / f"HKIPO-MB{code.split('.')[0]}.jsonl"
        if not path.exists():
            issuers.append({"code": code, "status": "missing_source_text"})
            continue
        source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        original_pages = [json.loads(s) for s in path.read_text().splitlines()]
        pages = original_pages
        # Repair lost column separators only when the disclosed ballot denominator
        # is exactly the prefix of the concatenated applicants/winners token.
        def separate(match: re.Match) -> str:
            token, denominator = match[1], match[2]
            if token.startswith(denominator) and len(token) > len(denominator):
                return denominator + "\n" + token[len(denominator):] + " out of " + denominator
            return match[0]
        pages = [{**x, "text": re.sub(rf"({N})\s+out\s+of\s+({N})", separate, x["text"])} for x in pages]
        continuation_pages = {}
        for i in range(len(pages) - 1):
            tail = re.search(r"((?:out|receive|to)\s*)\n\s*([\d.]+%)(?:\s*\n\s*\d+)?\s*$", pages[i]["text"])
            head = re.match(r"\s*((?:of\s+[\d,]+\s+to\s+receive\s+additional\s+\d+\s+Shares)|(?:(?:receive\s+)?(?:(?:an?\s+)?additional\s+)?\d+\s+(?:H\s+)?Shares))", pages[i + 1]["text"], re.I)
            if tail and head:
                pages[i]["text"] = pages[i]["text"][:tail.start()] + tail[1] + " " + head[1] + "\n" + tail[2]
                continuation_pages[pages[i]["page"]] = pages[i + 1]["page"]
        distributions = {}
        if code in {"3636.HK", "0901.HK"}:
            fixed_rows = re.compile(rf"(?m)^\s*({N})\s*\n\s*({N})\s*\n\s*({N})\s+H\s+Shares(?:\s*\n\s*([\d.]+)%\s*)?", re.I)
            for page in original_pages:
                for match in fixed_rows.finditer(page["text"]):
                    applied = integer(match[1])
                    distributions.setdefault(applied, []).append(dict(count=integer(match[2]),
                        allotted=integer(match[3]), page=page["page"], quote=match[0].strip(),
                        pct=match[4]))
            transformed = []
            for applied, outcomes in distributions.items():
                count = sum(x["count"] for x in outcomes)
                low, high = min(x["allotted"] for x in outcomes), max(x["allotted"] for x in outcomes)
                winners = sum(x["count"] for x in outcomes if x["allotted"] == high)
                rule = f"{low} H Shares" if low else ""
                if high != low:
                    rule += (" plus " if low else "") + f"{winners} out of {count} applicants to receive " + ("an additional " if low else "") + f"{high-low} H Shares"
                pct = next((x["pct"] for x in outcomes if x["pct"]), None)
                if pct is not None:
                    transformed.append({"page": outcomes[0]["page"], "text": f"{applied}\n{count}\n{rule}\n{pct}%"})
            pages = transformed
        if code == "3355.HK":
            g_map = {
                "200,000": "100 Shares plus", "300,000": "100 Shares plus", "400,000": "100 Shares plus",
                "500,000": "200 Shares plus", "600,000": "200 Shares plus", "700,000": "200 Shares plus",
                "800,000": "200 Shares plus", "900,000": "200 Shares plus", "1,000,000": "200 Shares plus",
                "2,000,000": "300 Shares plus",
            }
            new_pages = []
            for p in pages:
                t = p["text"]
                if p["page"] == 15:
                    t = t.replace("008%", "0.08%")
                elif p["page"] == 16:
                    for app, prefix in g_map.items():
                        pattern = rf"(?m)^(\s*{re.escape(app)}\s*\n\s*[\d,]+\s*\n\s*)((?:[\d,]+\s+out\s+of\s+[\d,]+\s+to\s+receive\s+)(?:an?\s+additional\s+)?)(100\s+Shares)"
                        t = re.sub(pattern, rf"\g<1>{prefix} \g<2>an additional \g<3>", t)
                new_pages.append({**p, "text": t})
            pages = new_pages
        pool, rows, lots = "", [], []
        for page in original_pages:
            for match in LOT.finditer(page["text"]):
                lots.append((integer(match[1]), page["page"], match[0]))
        for page in pages:
            text = page["text"]
            for match in ROW.finditer(text):
                markers = list(re.finditer(r"POOL\s+([AB])\b", text[:match.start()], re.I))
                if markers:
                    pool = markers[-1][1].upper()
                rule = " ".join(match[3].split())
                # Exclude unrelated numeric tables; preserve unknown allocation rules.
                if not re.search(r"Shares|HDRs", rule, re.I):
                    continue
                applied, applicants = integer(match[1]), integer(match[2])
                fixed = FIXED.match(rule)
                ballot = BALLOT.search(rule)
                guaranteed = integer(fixed[1]) if fixed else 0
                winners = integer(ballot[1]) if ballot else 0
                denominator = integer(ballot[2]) if ballot else applicants
                extra = integer(ballot[3]) if ballot else 0
                residual = BALLOT.sub("", rule)
                residual = FIXED.sub("", residual).strip(" +")
                parsed = bool(fixed or ballot) and not residual
                allocated = guaranteed * applicants + winners * extra if parsed else None
                expected = allocated / applicants if parsed and applicants else None
                pct = float(match[4])
                errors = []
                if not parsed:
                    errors.append("unparsed_rule")
                if denominator != applicants or winners > applicants:
                    errors.append("ballot_count_mismatch")
                if expected is not None and abs(100 * expected / applied - pct) > .011:
                    errors.append("printed_percentage_mismatch")
                encoding = "derived_from_disclosed_count_distribution" if distributions else (
                    "typeset_base_shares_repaired" if code == "3355.HK" and pool == "B" else "disclosed_ballot_wording"
                )
                rows.append(dict(code=code, pool=pool, applied_shares=applied,
                                 applicants=applicants, guaranteed_shares=guaranteed if parsed else None,
                                 ballot_winners=winners if parsed else None, ballot_denominator=denominator if parsed else None,
                                 ballot_extra_shares=extra if parsed else None, expected_shares=expected,
                                 allocated_shares=allocated, printed_allocation_pct=pct,
                                 rule_original=rule, pdf_page=page["page"], continuation_page=continuation_pages.get(page["page"]) if match.end() >= len(text.rstrip()) - 2 else None, source_text=str(path.relative_to(ROOT)),
                                 source_sha256=source_hash, errors=";".join(errors),
                                 source_quote=json.dumps(distributions[applied], ensure_ascii=False) if distributions else match[0].strip(),
                                 original_page_text=next(x["text"] for x in original_pages if x["page"] == page["page"]),
                                 derivation_note="Inserted guarantee vector inferred from rounded percentages and pool totals; original page retained" if code == "3355.HK" and pool == "B" else "",
                                 rule_encoding=encoding))
            trailing_markers = list(re.finditer(r"POOL\s+([AB])\b", text, re.I))
            if trailing_markers:
                pool = trailing_markers[-1][1].upper()
        lot_values = sorted({x[0] for x in lots})
        unique = len({(x["pool"], x["applied_shares"]) for x in rows}) == len(rows)
        applied_total = sum(x["applied_shares"] * x["applicants"] for x in rows)
        applicants_total = sum(x["applicants"] for x in rows)
        allocated_total = sum(x["allocated_shares"] or 0 for x in rows)
        totals_pass = bool(rows) and unique and all(not x["errors"] for x in rows)
        employee_reserved = {"2476.HK": (482000, 2), "1377.HK": (60300, 20)}.get(code, (0, None))
        if employee_reserved[0]:
            evidence_page = next(x for x in original_pages if x["page"] == employee_reserved[1])
            if f"{employee_reserved[0]:,}" not in evidence_page["text"] or "Employee" not in evidence_page["text"]:
                raise ValueError(f"{code}: employee allocation evidence changed")
        checks = [(applicants_total, issuer["Public applicants"]),
                  (allocated_total, issuer["Final public offer shares"] - employee_reserved[0])]
        totals_pass &= all(pd.notna(expected) and abs(actual - expected) < .5 for actual, expected in checks)
        status = "totals_reconciled_pending_semantic_review" if totals_pass else "quarantined_reconciliation"
        if totals_pass and abs(applied_total - issuer["Public valid applied shares"]) >= .5:
            status = "applicants_allocation_reconciled_applied_total_conflict"
        for row in rows:
            row["issuer_status"] = status
            row["board_lot_units"] = lot_values[0] if len(lot_values) == 1 else None
            row["board_lot_unit"] = "HDR" if lots and "HDR" in lots[0][2] else "share"
        tiers.extend(rows)
        issuers.append(dict(code=code, company=issuer["Company Name at time of listing"], status=status,
                            tiers=len(rows), board_lot_units=lot_values[0] if len(lot_values) == 1 else None,
                            board_lot_unit="HDR" if lots and "HDR" in lots[0][2] else "share",
                            board_lot_page=lots[0][1] if lots else None, board_lot_quote=lots[0][2] if lots else "",
                            applicants_extracted=applicants_total, applicants_master=issuer["Public applicants"],
                            applied_shares_extracted=applied_total, applied_shares_master=issuer["Public valid applied shares"],
                            allocated_shares_extracted=allocated_total, allocated_shares_master=issuer["Final public offer shares"],
                            overseas_employee_reserved_shares=employee_reserved[0], employee_evidence_page=employee_reserved[1],
                            source_text=str(path.relative_to(ROOT)), source_sha256=source_hash))
    pd.DataFrame(tiers).to_csv(OUT / "allocation_tiers_candidates.csv", index=False)
    pd.DataFrame(issuers).to_csv(OUT / "allocation_coverage.csv", index=False)
    # Only candidates are produced here. Independent review and its bound hash
    # are required before a separate exporter may publish a clean relation.
    print(pd.DataFrame(issuers)["status"].value_counts().to_string())
    print(f"{len(tiers)} tiers; explicit board lots {sum(pd.notna(x.get('board_lot_units')) for x in issuers)}")
    print("Candidates only; clean outputs preserved pending independent review")


if __name__ == "__main__":
    main()
