"""Automated referee and replication gate for the 33-year Hong Kong IPO journal monograph.

Audits both Markdown sources, LaTeX-compiled PDFs, sequential tables/figures, verbatim JSON table sync,
prose hygiene / zero-code-leakage rules, methodological safeguards, and 1-to-1 citation sync.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs" / "overview_paper"
MANUSCRIPT_MD = DOCS_DIR / "HK_IPO_Overview_1994_2026_Manuscript.md"
MANUSCRIPT_TEX = DOCS_DIR / "HK_IPO_Overview_1994_2026_Manuscript.tex"
MANUSCRIPT_PDF = DOCS_DIR / "HK_IPO_Overview_1994_2026_Manuscript.pdf"
APPENDIX_MD = DOCS_DIR / "HK_IPO_Overview_1994_2026_Online_Appendix.md"
APPENDIX_TEX = DOCS_DIR / "HK_IPO_Overview_1994_2026_Online_Appendix.tex"
APPENDIX_PDF = DOCS_DIR / "HK_IPO_Overview_1994_2026_Online_Appendix.pdf"
TABLES_JSON = ROOT / "analysis" / "out" / "journal_edition" / "tables_and_stats.json"


def _strip_math_dollars(line: str) -> int:
    """Count unescaped '$' delimiters outside backtick code spans on a line."""
    cleaned = re.sub(r"`[^`]*`", "", line)
    return len(re.findall(r"(?<!\\)\$", cleaned))


def _pdf_pages(pdf_path: Path) -> int:
    """Return page count of a compiled PDF via pdfinfo."""
    out = subprocess.check_output(["pdfinfo", str(pdf_path)], text=True)
    m = re.search(r"^Pages:\s+(\d+)", out, flags=re.MULTILINE)
    if not m:
        raise RuntimeError(f"Could not parse page count from pdfinfo for {pdf_path}")
    return int(m.group(1))


def _extract_markdown_tables(md_text: str, prefix: str) -> dict[str, tuple[str, str]]:
    """Extract {heading_label: (table_markdown, note_line)} for '#### {prefix}X: ...'."""
    lines = md_text.splitlines()
    found: dict[str, tuple[str, str]] = {}
    pat = re.compile(rf"^#### ({re.escape(prefix)}\d+):\s+.+$")
    i = 0
    while i < len(lines):
        m = pat.match(lines[i].strip())
        if m:
            label = m.group(1)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            tbl_lines: list[str] = []
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith("|") or s.startswith("**Panel "):
                    tbl_lines.append(lines[j])
                    j += 1
                elif s == "" and tbl_lines and j + 1 < len(lines) and lines[j + 1].strip().startswith(("|", "**Panel ")):
                    tbl_lines.append("")
                    j += 1
                else:
                    break
            while j < len(lines) and not lines[j].strip():
                j += 1
            note_line = lines[j].strip() if j < len(lines) and lines[j].strip().startswith("*Note:*") else ""
            found[label] = ("\n".join(tbl_lines).strip(), note_line)
            i = j
        else:
            i += 1
    return found


def _check_table_pipes_and_math(md_text: str, label: str, errors: list[str]) -> None:
    """Verify uniform Markdown pipe counts inside table blocks and paired '$' per line."""
    lines = md_text.splitlines()
    in_tbl = False
    expected_pipes = 0
    for idx, line in enumerate(lines, start=1):
        if _strip_math_dollars(line) % 2 != 0:
            errors.append(f"{label} line {idx}: odd unescaped '$' delimiter count -> {line[:90]}")
        s = line.strip()
        if s.startswith("|"):
            pipes = s.count("|")
            if not in_tbl:
                in_tbl = True
                expected_pipes = pipes
            elif pipes != expected_pipes:
                errors.append(f"{label} line {idx}: pipe count {pipes} != {expected_pipes}")
        else:
            in_tbl = False
            expected_pipes = 0


def _normalize_ref_surnames(entry: str) -> tuple[tuple[str, ...], str]:
    """Parse reference entry bullet into canonical lowercase (surnames_tuple, year)."""
    m_yr = re.search(r"\((\d{4}[a-z]?)\)\.", entry)
    if not m_yr:
        raise ValueError(f"Missing (YEAR). in reference line: {entry}")
    year = m_yr.group(1)
    author_part = entry[: m_yr.start()].lstrip("- ").strip()
    author_part = author_part.replace(" & ", ", ")
    chunks = [c.strip() for c in author_part.split(",")]
    surnames: list[str] = []
    for chunk in chunks:
        if chunk and not re.match(r"^(?:[A-Z]\.(?:\s*[-–]?\s*[A-Z]\.)*|[A-Z]\.?)$", chunk):
            if "." not in chunk:
                surnames.append(chunk.lower())
    return (tuple(surnames), year)


def _extract_text_citations(body_text: str) -> set[tuple[tuple[str, ...], str]]:
    """Extract all (normalized_surnames_tuple, year) citations from narrative + note text."""
    body = body_text.split("## References")[0]
    found: set[tuple[tuple[str, str], str]] = set()  # type: ignore[assignment]
    # Support multi-word surnames like "Montiel Olea" and hyphen/en-dash coauthors like "Anderson–Rubin"
    surname_tok = r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ'\-]*(?:\s+Olea)?"
    pair_or_tok = rf"{surname_tok}(?:\s*[–\-]\s*{surname_tok})?"
    authors_pat = rf"({pair_or_tok}(?:\s*,\s*{pair_or_tok})*(?:,?\s+and\s+{pair_or_tok})?(?:'s)?)"

    for m in re.finditer(rf"{authors_pat}\s*\((\d{{4}}[a-z]?)\)", body):
        raw_auth, yr = m.group(1), m.group(2)
        if _looks_like_false_positive(raw_auth):
            continue
        found.add((_parse_cite_authors(raw_auth), yr))

    for parens in re.finditer(r"\(([^()]{4,240})\)", body):
        inner = parens.group(1)
        if not re.search(r"\b(?:19|20)\d{2}[a-z]?\b", inner):
            continue
        for seg in re.split(r";\s*", inner):
            m2 = re.search(rf"{authors_pat}\s*,\s*(\d{{4}}[a-z]?)\b", seg)
            if m2:
                raw_auth, yr = m2.group(1), m2.group(2)
                if _looks_like_false_positive(raw_auth):
                    continue
                found.add((_parse_cite_authors(raw_auth), yr))

    return found


def _looks_like_false_positive(raw_auth: str) -> bool:
    bad_first = {
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December", "Epoch", "Table", "Panel",
        "Figure", "Section", "Model", "Column", "Columns", "Rule", "Chapter", "Article",
        "Decree", "Mechanism", "Option", "Main", "Pre-FINI", "Post-FINI", "Post-Aug",
        "HKEX", "CSRC", "IPOs", "Board", "Applicants",
    }
    first = raw_auth.split()[0].rstrip(",")
    if first in bad_first or first.startswith(("19", "20")) or (first.isupper() and len(first) >= 2):
        return True
    return False


def _parse_cite_authors(raw_auth: str) -> tuple[str, ...]:
    s = re.sub(r"'s\b", "", raw_auth)
    s = re.sub(r"\s*[–]\s*", ", ", s)
    s = re.sub(r"\band\b", ",", s)
    parts = [p.strip() for p in s.split(",") if p.strip()]
    return tuple(p.lower() for p in parts)


def run_audit() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for req in [MANUSCRIPT_MD, MANUSCRIPT_TEX, MANUSCRIPT_PDF, APPENDIX_MD, APPENDIX_TEX, APPENDIX_PDF, TABLES_JSON]:
        if not req.exists():
            errors.append(f"Missing required file: {req}")
    if errors:
        print("\n".join(errors))
        return 1

    ms_txt = MANUSCRIPT_MD.read_text(encoding="utf-8")
    ia_txt = APPENDIX_MD.read_text(encoding="utf-8")
    ms_tex = MANUSCRIPT_TEX.read_text(encoding="utf-8")
    ia_tex = APPENDIX_TEX.read_text(encoding="utf-8")
    tables_json = json.loads(TABLES_JSON.read_text(encoding="utf-8"))

    # 1. Code / internal workflow leakage check
    leak_patterns = [
        (r"[A-Za-z0-9_]+\.py\b", "Python filename"),
        (r"[A-Za-z0-9_]+\.csv\b", "CSV filename"),
        (r"\bcol_[A-Za-z0-9_]+\b", "Spreadsheet column variable"),
        (r"\bbatch[0-9_]+\b", "Internal batch label"),
        (r"\bfillna\b", "Pandas method"),
        (r"\bnotna\b", "Pandas method"),
        (r"Teacher's Manual", "Internal manual reference"),
        (r"\[!NOTE\]", "GitHub alert tag"),
        (r"foundations-and-trends", "Internal slug"),
        (r"\{\{Table\s+\d+\}\}", "Unsubstituted table placeholder"),
    ]
    for doc_name, txt in [
        ("Manuscript.md", ms_txt),
        ("Online_Appendix.md", ia_txt),
        ("Manuscript.tex", ms_tex),
        ("Online_Appendix.tex", ia_tex),
    ]:
        for pat, desc in leak_patterns:
            hits = re.findall(pat, txt)
            if hits:
                errors.append(f"{doc_name} leaks {desc}: {hits[:5]}")

    # 2. Prose hygiene / Humanizer checks on Main Manuscript prose
    prose_lines = [
        ln for ln in ms_txt.split("## References")[0].splitlines()
        if ln.strip() and not ln.strip().startswith(("|", "![", "#### Table", "**Panel"))
    ]
    for idx_line, ln in enumerate(prose_lines, start=1):
        if "—" in ln:
            errors.append(f"Manuscript prose contains em-dash: {ln[:90]}")
        for bad_phrase in [
            "delve", "tapestry", "vibrant", "paramount", "testament",
            "seamlessly", "it is worth noting", "underscores the",
        ]:
            if re.search(rf"\b{bad_phrase}\b", ln, flags=re.IGNORECASE):
                errors.append(f"Manuscript prose contains AI phrase '{bad_phrase}': {ln[:80]}")
        if re.search(r"\bnot only\b.{1,80}\bbut also\b", ln, flags=re.IGNORECASE):
            errors.append(f"Manuscript prose contains 'not only ... but also': {ln[:80]}")

    # 3. Word, Table Share, Abstract & PDF Page Budgets
    m_abs = re.search(r"\*\*Abstract\.\*\*\s+(.+)", ms_txt)
    if not m_abs:
        errors.append("Missing '**Abstract.**' paragraph")
    else:
        abs_wc = len(m_abs.group(1).split())
        print(f"[CHECK] Abstract words: {abs_wc} (target 120-165)")
        if not (120 <= abs_wc <= 165):
            errors.append(f"Abstract word count {abs_wc} outside [120, 165]")

    if "**JEL Classification:** G15, G18, G24, G32, K22" not in ms_txt:
        errors.append("Missing exact JEL Classification line")

    clean_all_words = [w for w in ms_txt.split() if not set(w) <= set("|-:")]
    total_wc = len(clean_all_words)
    main_tbl_json = tables_json["main_tables"]
    tbl_wc = sum(
        len([w for w in main_tbl_json[f"Table {i}"].split() if not set(w) <= set("|-:")])
        for i in range(1, 14)
    )
    tbl_share = 100.0 * tbl_wc / max(total_wc, 1)
    ms_pages = _pdf_pages(MANUSCRIPT_PDF)
    ia_pages = _pdf_pages(APPENDIX_PDF)
    print(f"[CHECK] Manuscript clean words: {total_wc} (target 14,500-18,500)")
    print(f"[CHECK] Table clean words: {tbl_wc} ({tbl_share:.2f}%, gate <20.0%)")
    print(f"[CHECK] Manuscript PDF pages: {ms_pages} (gate 36-44, ideal 38-42)")
    print(f"[CHECK] Online Appendix PDF pages: {ia_pages}")

    if not (14500 <= total_wc <= 18500):
        errors.append(f"Manuscript word count {total_wc} outside [14500, 18500]")
    if tbl_share >= 20.0:
        errors.append(f"Table word share {tbl_share:.2f}% >= 20.0%")
    if not (36 <= ms_pages <= 44):
        errors.append(f"Manuscript PDF pages {ms_pages} outside [36, 44]")

    # 4. Sequential Tables (Main 1..13 & IA 1..18) + verbatim JSON sync
    ms_tbls = _extract_markdown_tables(ms_txt, "Table ")
    if list(ms_tbls.keys()) != [f"Table {i}" for i in range(1, 14)]:
        errors.append(f"Main tables not sequential 1..13: {list(ms_tbls.keys())}")
    for i in range(1, 14):
        k = f"Table {i}"
        if k in ms_tbls:
            body_md, note_ln = ms_tbls[k]
            if body_md.strip() != main_tbl_json[k].strip():
                errors.append(f"{k} Markdown differs from tables_and_stats.json")
            if not note_ln.startswith("*Note:*"):
                errors.append(f"{k} missing '*Note:*' caption below table")
            if f"Table {i}" not in ms_txt.replace(f"#### Table {i}:", ""):
                errors.append(f"{k} not cited in prose")

    ia_tbls = _extract_markdown_tables(ia_txt, "Table IA.")
    if list(ia_tbls.keys()) != [f"Table IA.{i}" for i in range(1, 22)]:
        errors.append(f"IA tables not sequential 1..21: {list(ia_tbls.keys())}")
    ia_json = tables_json["ia_tables"]
    for i in range(1, 22):
        k = f"Table IA.{i}"
        if k in ia_tbls:
            body_md, note_ln = ia_tbls[k]
            if body_md.strip() != ia_json[k].strip():
                errors.append(f"{k} Markdown differs from tables_and_stats.json")
            if not note_ln.startswith("*Note:*"):
                errors.append(f"{k} missing '*Note:*' caption")

    # 5. Sequential Figures (1..9) + files exist
    figs = re.findall(r"^!\[Figure (\d+):[^\]]+\]\((figures/journal_fig\d+\.pdf)\)", ms_txt, flags=re.MULTILINE)
    if [int(n) for n, _ in figs] != list(range(1, 10)):
        errors.append(f"Figures not sequential 1..9: {figs}")
    for n, rel in figs:
        fig_path = DOCS_DIR / rel
        if not fig_path.exists():
            errors.append(f"Missing figure file: {fig_path}")
        if f"Figure {n}" not in ms_txt.replace(f"![Figure {n}:", ""):
            errors.append(f"Figure {n} not cited in prose")

    # 6. Pipe, math parity, and LaTeX typography hygiene across both files
    _check_table_pipes_and_math(ms_txt, "Manuscript.md", errors)
    _check_table_pipes_and_math(ia_txt, "Online_Appendix.md", errors)

    for doc_name, txt in [("Manuscript.md", ms_txt), ("Online_Appendix.md", ia_txt)]:
        if "`" in txt:
            errors.append(f"{doc_name} contains inline backtick code spans")
        for idx_ln, ln in enumerate(txt.splitlines(), start=1):
            masked = ln.replace(r"\$", "DOLLAR")
            masked = re.sub(r"!\[[^\]]*\]\([^)]+\)", "IMG", masked)
            masked = re.sub(r"\[[^\]]*\]\([^)]+\)", "LNK", masked)
            nomath = re.sub(r"\$[^$]+\$", "MATH", masked)
            if re.search(r"(?:^|[\s;(])\*{2,3}\s*,|\*\s+denote\b", nomath):
                errors.append(f"{doc_name} line {idx_ln}: unbracketed significance stars collide with Markdown emphasis")
            if "_" in nomath:
                errors.append(f"{doc_name} line {idx_ln}: bare underscore outside math span -> {ln[:90]}")

    for tex_name, t_txt in [("Manuscript.tex", ms_tex), ("Online_Appendix.tex", ia_tex)]:
        if r"\textbackslash{}" in t_txt:
            errors.append(f"{tex_name} contains literal '\\textbackslash{{}}' artifact")
        if r"\textbf{, }" in t_txt or ", ,  denote" in t_txt:
            errors.append(f"{tex_name} contains swallowed significance-star markup")

    # 7. Methodological safeguard verification
    for req_substr, desc in [
        ("Anderson–Rubin", "Anderson-Rubin weak-IV test cited"),
        ("+18.21", "PN18 15x first stage cited"),
        ("fail modern weak-IV", "Cornerstone weak-IV disclaimer"),
        ("50x (first-stage jump $+0.92$ pp", "PN18 50x/100x null first-stage caveat"),
        ("statistically imprecise", "Aug 2025 Mechanism B DiD IR uncertainty"),
        ("Fuzzy RDD", "Rejected HK$5.0B Fuzzy RDD audit"),
        ("+1.52", "Stacked Official Entrant Southbound DiD"),
        ("3,706.0", "Bessembinder net tranche wealth"),
    ]:
        if req_substr not in ms_txt:
            errors.append(f"Missing mandatory empirical safeguard ({desc}): '{req_substr}'")

    # 8. Zero backticks in publication Markdown
    for doc_name, txt in [("Manuscript.md", ms_txt), ("Online_Appendix.md", ia_txt)]:
        if "`" in txt:
            errors.append(f"{doc_name} contains raw Markdown backticks")

    # 9. Figure PDF panel-title verification via pdftotext
    fig_dir = DOCS_DIR / "figures"
    fig_checks = {
        "journal_fig1.pdf": ["Main Board", "U.S."],
        "journal_fig2.pdf": ["Data Pitfall Incidence", "Split-Cleaned Main Board"],
        "journal_fig3.pdf": ["Bookrunner", "Rule 144A"],
        "journal_fig5.pdf": ["GEM", "125M"],
        "journal_fig6.pdf": ["First Stage", "Reduced Form"],
        "journal_fig9.pdf": ["Lockup", "Turnover"],
    }
    for fname, req_words in fig_checks.items():
        fpath = fig_dir / fname
        if not fpath.exists():
            errors.append(f"Missing figure PDF: {fpath}")
        else:
            ftxt = subprocess.check_output(["pdftotext", str(fpath), "-"], text=True)
            for w in req_words:
                if w not in ftxt:
                    errors.append(f"Figure {fname} panel alignment check missing '{w}'")

    # 10. Statutory & cross-document invariant guards
    for doc_name, txt in [("Manuscript.md", ms_txt), ("Online_Appendix.md", ia_txt)]:
        for stale, reason in [
            ("RTGS liquidity pool", "Incorrect FINI/RTGS description"),
            ("10x / 30x / 50x", "Deprecated Mech A consultation brackets"),
            ("45 A+H", "Stale 45-deal A+H count"),
            ("Roster of 45 A+H", "Stale 45-deal Table IA.16 header"),
            ("Pre=2.69%", "Contaminated CCASS Fast-Entry pre-entry"),
            ("Pre=1.88%", "Contaminated CCASS WVR pre-entry"),
            ("exact pricing neutrality", "Overclaimed Mech B null return wording"),
        ]:
            if stale in txt:
                errors.append(f"{doc_name} contains remediated claim ({reason}): '{stale}'")
        if re.search(r"Rule 8\.09.{0,60}May\s+2018|May\s+2018.{0,60}Rule 8\.09", txt, flags=re.IGNORECASE):
            errors.append(f"{doc_name} misdates Rule 8.09 to May 2018 (enacted 2018-02-15)")

    t9 = tables_json["main_tables"].get("Table 9", "")
    if "Weak FS" not in t9 or "Cov.-Adj. RF" not in t9:
        errors.append("Table 9 missing Weak FS suppression or Cov.-Adj. RF row")
    t13 = tables_json["main_tables"].get("Table 13", "")
    if "| Unit |" not in t13 or "100.0%" not in t13:
        errors.append("Table 13 Panel B missing Unit column or 100.0% A+H auto-inclusion audit")
    tia13 = tables_json["ia_tables"].get("Table IA.13", "")
    if "FAILS EXCLUSION" not in tia13 or "Panel C: Oster" not in tia13:
        errors.append("Table IA.13 missing FAILS EXCLUSION flag or separate Panel C Oster bounds")
    tia16_rows = [l for l in tables_json["ia_tables"].get("Table IA.16", "").splitlines() if l.startswith("|") and ".HK" in l]
    if len(tia16_rows) != 57:
        errors.append(f"Table IA.16 expected 57 A+H rows, found {len(tia16_rows)}")

    # 11. 1-to-1 Citation <-> References sync
    if "## References" not in ms_txt:
        errors.append("Missing '## References' section")
    else:
        ref_block = ms_txt.split("## References", 1)[1].strip()
        ref_lines = [ln.strip() for ln in ref_block.splitlines() if ln.strip().startswith("- ")]
        ref_keys = {_normalize_ref_surnames(ln): ln for ln in ref_lines}
        cited_keys = _extract_text_citations(ms_txt)
        missing_in_refs = sorted(cited_keys - set(ref_keys.keys()))
        uncited_in_refs = sorted(set(ref_keys.keys()) - cited_keys)
        print(f"[CHECK] Unique References: {len(ref_keys)}, Text Citations Matched: {len(cited_keys)}")
        if missing_in_refs:
            errors.append(f"Cited in text but missing from References: {missing_in_refs}")
        if uncited_in_refs:
            errors.append(f"Listed in References but never cited in text: {uncited_in_refs}")

    if warnings:
        print("WARNINGS:\n  - " + "\n  - ".join(warnings))
    if errors:
        print("AUDIT FAILED:")
        for e in errors:
            print(f"  [ERROR] {e}")
        return 1

    print("AUDIT PASSED: 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(run_audit())
