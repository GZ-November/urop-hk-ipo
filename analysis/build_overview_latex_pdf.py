#!/usr/bin/env python3
"""Compile the Hong Kong IPO Overview and Deep Extensions monographs to LaTeX and PDF via Tectonic."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs" / "overview_paper"
FIGURES_DIR = DOCS_DIR / "figures"

MASTER_SPEC = {
    "md": DOCS_DIR / "HK_IPO_Financial_History_Master.md",
    "tex": DOCS_DIR / "HK_IPO_Financial_History_Master.tex",
    "pdf": DOCS_DIR / "HK_IPO_Financial_History_Master.pdf",
    "short_title": "Hong Kong’s IPO Market: A Financial History, 1891–2026",
    "volume_label": "Comprehensive Research Monograph",
    "is_journal_main": True,
    "include_toc": True,
}

DEFAULT_SPECS = [MASTER_SPEC]


def _escape_latex_text(text: str) -> str:
    """Escape plain-text LaTeX characters outside math and code spans."""
    text = text.replace("\u2212", "-")
    text = text.replace("\u00a0", " ")
    # Convert paired straight double quotes into proper LaTeX opening/closing quotes
    text = re.sub(r'"([^"\n]+)"', r"``\1''", text)
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("$", r"\$"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("^", r"\textasciicircum{}"),
        ("~", r"\textasciitilde{}"),
        ("<", r"\textless{}"),
        (">", r"\textgreater{}"),
    ]
    for src, dst in replacements:
        text = text.replace(src, dst)
    text = text.replace("\u013d", r"\v{L}").replace("\u013e", r"\v{l}")
    unicode_math_fallbacks = [
        ("→", r"$\to$"),
        ("≤", r"$\le$"),
        ("≥", r"$\ge$"),
        ("×", r"$\times$"),
        ("±", r"$\pm$"),
        ("α", r"$\alpha$"),
        ("β", r"$\beta$"),
        ("δ", r"$\delta$"),
        ("Δ", r"$\Delta$"),
        ("²", r"$^2$"),
    ]
    for src, dst in unicode_math_fallbacks:
        text = text.replace(src, dst)
    text = text.replace("HK\\$", r"HK\$")
    return text


def _escape_code_text(text: str) -> str:
    """Escape code spans for safe \\texttt rendering with wrap hints."""
    text = text.replace("\u2212", "-")
    out: list[str] = []
    for ch in text:
        if ch == "\\":
            out.append(r"\textbackslash{}")
        elif ch == "{":
            out.append(r"\{")
        elif ch == "}":
            out.append(r"\}")
        elif ch == "$":
            out.append(r"\$")
        elif ch == "&":
            out.append(r"\&")
        elif ch == "%":
            out.append(r"\%")
        elif ch == "#":
            out.append(r"\#")
        elif ch == "_":
            out.append(r"\_\allowbreak{}")
        elif ch == "/":
            out.append(r"/\allowbreak{}")
        elif ch == "^":
            out.append(r"\textasciicircum{}")
        elif ch == "~":
            out.append(r"\textasciitilde{}")
        elif ch == "<":
            out.append(r"\textless{}")
        elif ch == ">":
            out.append(r"\textgreater{}")
        elif ch == "-":
            out.append(r"-")
        else:
            out.append(ch)
    return "".join(out)


def _normalize_math_body(math_str: str) -> str:
    """Normalize Markdown-style LaTeX math for clean XeLaTeX compilation."""
    math_str = math_str.replace("\u2212", "-")
    math_str = math_str.replace("\u00a0", " ")
    # Flatten nested ($\%$) inside \text{...} so XeLaTeX never encounters nested math switches there.
    math_str = re.sub(r"\(\$\\%\$\)", r"(\\%)", math_str)
    math_str = math_str.replace(r"$\\%$", r"\\%")
    math_str = re.sub(r"\(\$\\\\%\$\)", r"(\\%)", math_str)
    math_str = math_str.replace(r"$\$\%$", r"\%")
    math_str = math_str.replace(r"($\%$)", r"(\%)")
    math_str = math_str.replace(r"$\%$", r"\%")
    math_str = math_str.replace(r"\mathbb{1}", r"\mathbf{1}")
    # Escape bare underscores inside \text{...} if not already escaped.
    def _fix_text_arg(match: re.Match[str]) -> str:
        inner = match.group(1)
        inner = re.sub(r"(?<!\\)_", r"\_", inner)
        return r"\text{" + inner + "}"

    # Apply carefully to simple non-nested \text{...} spans when no inner math exists.
    def _replace_simple_text(s: str) -> str:
        res: list[str] = []
        i = 0
        while i < len(s):
            if s.startswith(r"\text{", i):
                depth = 1
                j = i + 6
                while j < len(s) and depth > 0:
                    if s[j] == "\\" and j + 1 < len(s):
                        j += 2
                        continue
                    if s[j] == "{":
                        depth += 1
                    elif s[j] == "}":
                        depth -= 1
                    j += 1
                inner = s[i + 6 : j - 1]
                # Preserve intentional inline math like ($\beta_1$) inside \text{...}
                if "$" not in inner:
                    inner = re.sub(r"(?<!\\)_", r"\_", inner)
                    inner = re.sub(r"(?<!\\)&", r"\&", inner)
                res.append(r"\text{" + inner + "}")
                i = j
            else:
                res.append(s[i])
                i += 1
        return "".join(res)

    math_str = re.sub(
        r"\\mathbf\{([^}]*?)\\(Delta|Gamma|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega|alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|varphi|chi|psi|omega)\b",
        r"\\mathbf{\1\\boldsymbol{\\\2}",
        math_str,
    )
    return _replace_simple_text(math_str)


def _find_closing_math(text: str, start: int) -> int:
    """Find closing unescaped '$' for inline math starting right after opening '$'."""
    i = start
    brace_depth = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "{":
            brace_depth += 1
        elif ch == "}":
            brace_depth = max(0, brace_depth - 1)
        elif ch == "$" and brace_depth == 0:
            return i
        i += 1
    return -1


def _convert_inline(text: str, *, in_table: bool = False) -> str:
    """Convert inline Markdown (math, code, links, bold, italic, <br>) to LaTeX."""
    if not text:
        return ""

    placeholders: dict[str, str] = {}

    def _stash(latex_frag: str) -> str:
        key = f"@@LATEXPH{len(placeholders)}@@"
        placeholders[key] = latex_frag
        return key

    # 1. Replace <br> breaks cleanly via stashed LaTeX commands.
    if not in_table:
        text = re.sub(r"<br\s*/?>", lambda _: _stash(r"\par "), text, flags=re.IGNORECASE)
    else:
        text = re.sub(r"<br\s*/?>", lambda _: _stash(r" \\ "), text, flags=re.IGNORECASE)

    # 2. Extract inline code spans `...` and inline math $...$ sequentially so they don't collide.
    buf: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\":
            # Escaped currency \$ in prose outside math -> literal $ placeholder
            if i + 1 < n and text[i + 1] == "$":
                buf.append(_stash(r"\$"))
                i += 2
                continue
            buf.append(ch)
            if i + 1 < n:
                buf.append(text[i + 1])
                i += 2
            else:
                i += 1
            continue
        if ch == "`":
            end = text.find("`", i + 1)
            if end != -1:
                code_body = text[i + 1 : end]
                buf.append(_stash(r"\texttt{\small " + _escape_code_text(code_body) + "}"))
                i = end + 1
                continue
        if ch == "$":
            # Double $$ inline shouldn't usually appear, guard just in case
            if i + 1 < n and text[i + 1] == "$":
                end = text.find("$$", i + 2)
                if end != -1:
                    body = _normalize_math_body(text[i + 2 : end])
                    buf.append(_stash(f"$${body}$$"))
                    i = end + 2
                    continue
            end = _find_closing_math(text, i + 1)
            if end != -1:
                body = _normalize_math_body(text[i + 1 : end])
                buf.append(_stash(f"${body}$"))
                i = end + 1
                continue
        buf.append(ch)
        i += 1

    work = "".join(buf)

    # 3. Handle Markdown links [label](target) before escaping.
    # Resolve any stashed placeholders inside `label` first so nested backticks/math are preserved.
    def _link_repl(m: re.Match[str]) -> str:
        raw_lbl = m.group(1)
        while "@@LATEXPH" in raw_lbl:
            raw_lbl_new = re.sub(r"@@LATEXPH\d+@@", lambda pm: placeholders.get(pm.group(0), pm.group(0)), raw_lbl)
            if raw_lbl_new == raw_lbl:
                break
            raw_lbl = raw_lbl_new
        # If placeholders already contain LaTeX fragments (e.g. \texttt{...}), only escape unreplaced Markdown wrappers
        if "\\texttt{" in raw_lbl or "$" in raw_lbl:
            # Convert bold/italic inside already-resolved fragments carefully by splitting on existing LaTeX or simple bold
            label = re.sub(r"\*\*([^\*]+?)\*\*", r"\\textbf{\1}", raw_lbl)
            label = re.sub(r"(?<!\*)\*([^\*]+?)\*(?!\*)", r"\\textit{\1}", label)
        else:
            label = _convert_inline(raw_lbl, in_table=in_table)
        url = m.group(2).strip()
        if url.startswith("http://") or url.startswith("https://"):
            esc_url = url.replace("%", r"\%").replace("#", r"\#")
            return _stash(rf"\href{{{esc_url}}}{{{label}}}")
        # Local file/figure references render cleanly as regular cross-refs.
        return _stash(label)

    work = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_repl, work)

    # 4. Handle bold+italic ***...***, bold **...**, italic *...*.
    # Recursively parse inner text so placeholders stay intact.
    def _bold_italic_repl(m: re.Match[str]) -> str:
        inner = _format_plain_with_placeholders(m.group(1), placeholders)
        return _stash(rf"\textbf{{\textit{{{inner}}}}}")

    def _bold_repl(m: re.Match[str]) -> str:
        inner = _format_plain_with_placeholders(m.group(1), placeholders)
        return _stash(rf"\textbf{{{inner}}}")

    def _italic_repl(m: re.Match[str]) -> str:
        inner = _format_plain_with_placeholders(m.group(1), placeholders)
        return _stash(rf"\textit{{{inner}}}")

    work = re.sub(r"\*\*\*(?=\S)([^\*]+?)(?<=\S)\*\*\*", _bold_italic_repl, work)
    work = re.sub(r"\*\*(?=\S)([^\*]+?)(?<=\S)\*\*", _bold_repl, work)
    work = re.sub(r"(?<!\*)\*(?=\S)([^\*\n]+?)(?<=\S)\*(?!\*)", _italic_repl, work)

    return _format_plain_with_placeholders(work, placeholders)


def _format_plain_with_placeholders(work: str, placeholders: dict[str, str]) -> str:
    """Escape remaining plain segments while iteratively restoring nested placeholders."""
    parts = re.split(r"(@@LATEXPH\d+@@)", work)
    rebuilt: list[str] = []
    for part in parts:
        if part in placeholders:
            val = placeholders[part]
            while True:
                nxt = re.sub(r"@@LATEXPH\d+@@", lambda m: placeholders.get(m.group(0), m.group(0)), val)
                if nxt == val:
                    break
                val = nxt
            rebuilt.append(val)
        elif part:
            rebuilt.append(_escape_latex_text(part))
    return "".join(rebuilt)


def _split_md_row(line: str) -> list[str]:
    """Split a Markdown table row into stripped cell strings."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells: list[str] = []
    cur: list[str] = []
    i = 0
    while i < len(stripped):
        if stripped[i] == "\\" and i + 1 < len(stripped) and stripped[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if stripped[i] == "|":
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(stripped[i])
        i += 1
    cells.append("".join(cur).strip())
    return cells


def _parse_alignments(sep_line: str, ncols: int) -> list[str]:
    cells = _split_md_row(sep_line)
    aligns: list[str] = []
    for j in range(ncols):
        tok = cells[j] if j < len(cells) else "---"
        tok = tok.strip()
        if tok.startswith(":") and tok.endswith(":"):
            aligns.append("c")
        elif tok.endswith(":"):
            aligns.append("r")
        else:
            aligns.append("l")
    return aligns


def _visible_len(cell: str) -> int:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    s = s.replace("**", "").replace("*", "").replace("`", "")
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", s)
    s = s.replace("<br>", " ")
    return max(1, len(s.strip()))


@dataclass
class TableBlock:
    caption: str | None
    headers: list[str]
    aligns: list[str]
    rows: list[list[str]]


def _render_tabular_only(tbl: TableBlock) -> str:
    """Render a single booktabs tabular inside adjustbox (without outer \\begin{table})."""
    ncols = len(tbl.headers)
    max_col_lens = [_visible_len(h) for h in tbl.headers]
    for r in tbl.rows:
        is_panel = len(r) == ncols and r[0] and all(not c.strip() for c in r[1:])
        if is_panel:
            continue
        for j in range(min(ncols, len(r))):
            lines_in_cell = re.split(r"<br\s*/?>", r[j], flags=re.IGNORECASE)
            cell_max = max((_visible_len(seg) for seg in lines_in_cell), default=1)
            max_col_lens[j] = max(max_col_lens[j], cell_max)

    col_specs: list[str] = []
    is_wrapped: list[bool] = []
    target_cm = 16.5 if ncols >= 8 else 15.8

    raw_widths: list[float] = []
    for j, align in enumerate(tbl.aligns):
        maxlen = max_col_lens[j]
        hdr_len = _visible_len(tbl.headers[j])
        if j == 0 and maxlen > 26:
            raw_widths.append(min(6.2, max(3.6, maxlen * 0.115)))
            is_wrapped.append(True)
        elif maxlen > 24 or hdr_len > 22:
            raw_widths.append(min(5.8, max(2.2, max(maxlen, hdr_len) * 0.11)))
            is_wrapped.append(True)
        else:
            raw_widths.append(0.0)
            is_wrapped.append(False)

    sum_w = sum(raw_widths)
    fixed_est = sum(1.3 for w in raw_widths if w == 0.0)
    avail_w = max(8.0, target_cm - fixed_est)
    scale = min(1.0, avail_w / sum_w) if sum_w > 0 else 1.0

    for j, align in enumerate(tbl.aligns):
        if is_wrapped[j]:
            w = max(1.9, raw_widths[j] * scale)
            if align == "c":
                col_specs.append(rf">{{\centering\arraybackslash}}p{{{w:.2f}cm}}")
            elif align == "r":
                col_specs.append(rf">{{\raggedleft\arraybackslash}}p{{{w:.2f}cm}}")
            else:
                col_specs.append(rf">{{\raggedright\arraybackslash}}p{{{w:.2f}cm}}")
        else:
            col_specs.append(align)

    lines: list[str] = [
        r"\scriptsize" if ncols >= 9 else r"\footnotesize",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\renewcommand{\arraystretch}{1.18}",
        r"\begin{adjustbox}{max width=\textwidth}",
        rf"\begin{{tabular}}{{{''.join(col_specs)}}}",
        r"\toprule",
    ]

    def _render_cell(cell_md: str, align_ch: str, wrapped: bool) -> str:
        segs = re.split(r"<br\s*/?>", cell_md, flags=re.IGNORECASE)
        if len(segs) == 1:
            return _convert_inline(cell_md, in_table=True)
        if wrapped:
            return r" \newline ".join(_convert_inline(s.strip(), in_table=True) for s in segs)
        mc_align = "c" if align_ch == "c" else ("r" if align_ch == "r" else "l")
        inner = r" \\ ".join(_convert_inline(s.strip(), in_table=True) for s in segs)
        return rf"\makecell[{mc_align}]{{{inner}}}"

    hdr_tex = " & ".join(_render_cell(tbl.headers[j], tbl.aligns[j], is_wrapped[j]) for j in range(ncols)) + r" \\"
    lines.append(hdr_tex)
    lines.append(r"\midrule")

    for r_idx, row in enumerate(tbl.rows):
        padded = [row[j] if j < len(row) else "" for j in range(ncols)]
        is_panel = bool(padded[0].strip()) and all(not c.strip() for c in padded[1:])
        if is_panel:
            if r_idx > 0:
                lines.append(r"\addlinespace[4pt]")
            panel_tex = _convert_inline(padded[0], in_table=True)
            lines.append(rf"\rowcolor{{PanelTint}} \multicolumn{{{ncols}}}{{>{{\raggedright\arraybackslash}}p{{{target_cm:.1f}cm}}}}{{{panel_tex}}} \\")
        else:
            row_tex = " & ".join(_render_cell(padded[j], tbl.aligns[j], is_wrapped[j]) for j in range(ncols)) + r" \\"
            lines.append(row_tex)

    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{adjustbox}",
        ]
    )
    return "\n".join(lines)


def _render_table(tbl: TableBlock) -> str:
    """Render a standalone financial table inside a table float."""
    lines: list[str] = [
        r"\begin{table}[htbp]",
        r"\centering",
    ]
    if tbl.caption:
        lines.append(rf"\caption*{{{_convert_inline(tbl.caption)}}}")
    lines.append(r"\begin{adjustbox}{max width=\textwidth,max totalheight=0.80\textheight}")
    lines.append(r"\begin{minipage}{\textwidth}\centering")
    lines.append(_render_tabular_only(tbl))
    lines.append(r"\end{minipage}")
    lines.append(r"\end{adjustbox}")
    lines.append(r"\end{table}")
    lines.append("")
    return "\n".join(lines)


def _render_multipanel_table(
    caption: str,
    panels: list[tuple[str | None, TableBlock]],
    note_md: str | None,
    *,
    is_journal_main: bool = True,
) -> str:
    """Render a single- or multi-panel journal table with its caption and note in one unified float."""
    total_rows = sum(len(tb.rows) + 2 for _, tb in panels)
    float_pos = (
        "p"
        if is_journal_main and ((len(panels) >= 2 and total_rows >= 18) or total_rows >= 26)
        else "!htbp"
    )
    out: list[str] = [
        rf"\begin{{table}}[{float_pos}]",
        r"\centering",
        rf"\caption*{{{_convert_inline(caption)}}}",
        r"\begin{adjustbox}{max width=\textwidth,max totalheight=0.79\textheight}",
        r"\begin{minipage}{\textwidth}\centering",
    ]
    for p_idx, (p_title, tb) in enumerate(panels):
        if p_idx > 0:
            out.append(r"\par\vspace{5pt}")
        if p_title:
            out.append(rf"\par\noindent{{\footnotesize\bfseries {_convert_inline(p_title)}}}\par\vspace{{2pt}}")
        out.append(_render_tabular_only(tb))
    out.append(r"\end{minipage}")
    out.append(r"\end{adjustbox}")
    if note_md:
        out.append(rf"\par\vspace{{3pt}}\noindent\parbox{{\textwidth}}{{\scriptsize\raggedright {_convert_inline(note_md)}}}")
    out.append(r"\end{table}")
    out.append("")
    return "\n".join(out)


def _strip_heading_hashes(line: str) -> tuple[int, str] | None:
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if not m:
        return None
    return len(m.group(1)), m.group(2).strip()


def _toc_plain_title(raw_md: str) -> str:
    """Plain title for hyperref PDF bookmarks / running headers."""
    t = raw_md.replace("**", "").replace("`", "")
    t = re.sub(r"\\\$", "$", t)
    t = re.sub(r"\$([^$]*)\$", r"\1", t)
    return t


def convert_markdown_to_latex(
    md_path: Path,
    *,
    short_title: str,
    volume_label: str,
    is_journal_main: bool = True,
    include_toc: bool = False,
) -> str:
    """Convert an academic HK IPO overview Markdown monograph to a standalone XeLaTeX document."""
    raw = md_path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    # Extract H1 title + top metadata block before first `---`
    idx = 0
    doc_title = "HKEX IPO Monograph"
    meta_lines: list[str] = []
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx < len(lines) and lines[idx].startswith("# "):
        doc_title = lines[idx][2:].strip()
        idx += 1
    while idx < len(lines) and lines[idx].strip() != "---":
        ln = lines[idx].strip()
        if ln:
            meta_lines.append(ln)
        idx += 1
    if idx < len(lines) and lines[idx].strip() == "---":
        idx += 1

    body: list[str] = []
    pending_table_caption: str | None = None

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        # Blank line
        if not stripped:
            idx += 1
            continue

        # Horizontal rule
        if stripped == "---":
            if pending_table_caption:
                body.append(rf"\par\medskip\noindent\textbf{{{_convert_inline(pending_table_caption)}}}\par\smallskip")
                pending_table_caption = None
            # Suppress redundant rule immediately preceding a `# PART ...` banner
            la_hr = idx + 1
            while la_hr < len(lines) and not lines[la_hr].strip():
                la_hr += 1
            if la_hr < len(lines) and re.match(r"^#\s+", lines[la_hr].strip()):
                idx += 1
                continue
            if not is_journal_main:
                body.append(r"\clearpage")
            else:
                body.append(r"\par\medskip\noindent\rule{\linewidth}{0.35pt}\par\medskip")
            idx += 1
            continue

        # Headings
        hd = _strip_heading_hashes(stripped)
        if hd is not None:
            level, htext = hd
            # Consume a single- or multi-panel `#### Table ...` block (including Panel subheaders + optional *Note:*)
            if level >= 3 and re.match(r"^(Table|表)\b", htext, flags=re.IGNORECASE):
                la = idx + 1
                panels_acc: list[tuple[str | None, TableBlock]] = []
                cur_panel_lbl: str | None = None
                while la < len(lines):
                    while la < len(lines) and not lines[la].strip():
                        la += 1
                    if la >= len(lines):
                        break
                    s_la = lines[la].strip()
                    m_pan = re.match(r"^\*\*(Panel\s+[A-Z][^*]*)\*\*\s*$", s_la)
                    if m_pan:
                        cur_panel_lbl = m_pan.group(1).strip()
                        la += 1
                        continue
                    if s_la.startswith("|") and la + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[la + 1]):
                        hdrs = _split_md_row(lines[la])
                        alns = _parse_alignments(lines[la + 1], len(hdrs))
                        la += 2
                        rws: list[list[str]] = []
                        while la < len(lines) and lines[la].strip().startswith("|"):
                            rws.append(_split_md_row(lines[la]))
                            la += 1
                        panels_acc.append((cur_panel_lbl, TableBlock(caption=None, headers=hdrs, aligns=alns, rows=rws)))
                        cur_panel_lbl = None
                        continue
                    break
                if panels_acc:
                    note_str: str | None = None
                    la_note = la
                    while la_note < len(lines) and not lines[la_note].strip():
                        la_note += 1
                    if la_note < len(lines) and (
                        lines[la_note].strip().startswith("*Note")
                        or lines[la_note].strip().startswith("*Source")
                    ):
                        n_lines: list[str] = []
                        while la_note < len(lines) and lines[la_note].strip():
                            n_lines.append(lines[la_note].strip())
                            la_note += 1
                        note_str = " ".join(n_lines)
                        la = la_note
                    body.append(
                        _render_multipanel_table(
                            htext,
                            panels_acc,
                            note_str,
                            is_journal_main=is_journal_main,
                        )
                    )
                    idx = la
                    continue

            if pending_table_caption:
                body.append(rf"\par\medskip\noindent\textbf{{{_convert_inline(pending_table_caption)}}}\par\smallskip")
                pending_table_caption = None

            tex_h = _convert_inline(htext)
            # Plain string for PDF bookmark / running header
            bookmark = _escape_latex_text(_toc_plain_title(htext))
            if level == 1:
                body.append(
                    r"\par\vspace{16pt}\needspace{9\baselineskip}"
                    + "\n"
                    + r"\noindent\rule{\linewidth}{0.85pt}\par\vspace{5pt}"
                    + "\n"
                    + rf"{{\centering\Large\bfseries\color{{NavyAccent}} \texorpdfstring{{{tex_h}}}{{{bookmark}}}\par}}"
                    + "\n"
                    + r"\vspace{4pt}\noindent\rule{\linewidth}{0.85pt}\par\vspace{8pt}"
                    + "\n"
                    + rf"\addcontentsline{{toc}}{{section}}{{\texorpdfstring{{\textbf{{{tex_h}}}}}{{{bookmark}}}}}"
                )
                # Consume any trailing `---` immediately following a `# PART` banner
                la_after = idx + 1
                while la_after < len(lines) and not lines[la_after].strip():
                    la_after += 1
                if la_after < len(lines) and lines[la_after].strip() == "---":
                    idx = la_after + 1
                    continue
            elif level == 2:
                # Keep running header short so it never collides with fancyhead[L]
                raw_short = _toc_plain_title(htext).split(":", 1)[0].strip()
                if len(raw_short) > 50:
                    raw_short = raw_short[:47].rstrip() + "..."
                short_hdr = _escape_latex_text(raw_short)
                body.append(
                    rf"\section*{{\texorpdfstring{{{tex_h}}}{{{bookmark}}}}}"
                    + "\n"
                    + rf"\addcontentsline{{toc}}{{section}}{{\texorpdfstring{{{tex_h}}}{{{bookmark}}}}}"
                    + "\n"
                    + rf"\markright{{{short_hdr}}}"
                )
            elif level == 3:
                body.append(
                    rf"\subsection*{{\texorpdfstring{{{tex_h}}}{{{bookmark}}}}}"
                    + "\n"
                    + rf"\addcontentsline{{toc}}{{subsection}}{{\texorpdfstring{{{tex_h}}}{{{bookmark}}}}}"
                )
            else:
                body.append(rf"\subsubsection*{{\texorpdfstring{{{tex_h}}}{{{bookmark}}}}}")
            idx += 1
            continue

        # Display Math block $$ ... $$
        if stripped.startswith("$$"):
            if stripped.endswith("$$") and len(stripped) > 4:
                math_content = stripped[2:-2].strip()
                idx += 1
            else:
                math_lines = [stripped[2:]]
                idx += 1
                while idx < len(lines):
                    cur_s = lines[idx].strip()
                    if cur_s.endswith("$$"):
                        math_lines.append(cur_s[:-2])
                        idx += 1
                        break
                    math_lines.append(lines[idx])
                    idx += 1
                math_content = "\n".join(math_lines).strip()
            body.append("\\[\n" + _normalize_math_body(math_content) + "\n\\]\n")
            continue

        # Figure ![Caption](path)
        fig_m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if fig_m:
            cap = fig_m.group(1).strip()
            rel_path = fig_m.group(2).strip()
            candidate = DOCS_DIR / rel_path
            pdf_candidate = candidate.with_suffix(".pdf")
            chosen = pdf_candidate if pdf_candidate.exists() else candidate
            # Use path relative to DOCS_DIR so .tex compiles directly inside DOCS_DIR
            try:
                img_rel = chosen.relative_to(DOCS_DIR).as_posix()
            except ValueError:
                img_rel = chosen.as_posix()
            fig_cap_m = re.match(r"^(Figure\s+\d+(?:\.\d+)?\s*:)\s*(.*)$", cap)
            if fig_cap_m:
                cap_tex = rf"\textbf{{{_escape_latex_text(fig_cap_m.group(1))}}} {_convert_inline(fig_cap_m.group(2))}"
            else:
                cap_tex = _convert_inline(cap)
            body.extend(
                [
                    r"\begin{figure}[htbp]",
                    r"\centering",
                    rf"\includegraphics[width=\textwidth,height=0.80\textheight,keepaspectratio]{{{img_rel}}}",
                    rf"\caption*{{{cap_tex}}}",
                    r"\end{figure}",
                    "",
                ]
            )
            idx += 1
            continue

        # Blockquote / Alert callout
        if stripped.startswith(">"):
            q_lines: list[str] = []
            while idx < len(lines) and lines[idx].strip().startswith(">"):
                content_ln = re.sub(r"^>\s?", "", lines[idx].strip())
                q_lines.append(content_ln)
                idx += 1
            box_title = "Research Note"
            box_color = "NavyAccent"
            if q_lines and re.match(r"^\[!(IMPORTANT|NOTE|TIP|WARNING|CAUTION)\]$", q_lines[0].strip(), re.I):
                tag = q_lines[0].strip()[2:-1].upper()
                q_lines = q_lines[1:]
                if tag in {"IMPORTANT", "WARNING", "CAUTION"}:
                    box_color = "CrimsonAccent"
                    box_title = "Important Notice" if tag == "IMPORTANT" else tag.title()
                else:
                    box_title = "Methodological Note" if tag == "NOTE" else tag.title()
            body.append(rf"\begin{{calloutbox}}{{{box_color}}}{{{box_title}}}")
            # Group lines into paragraphs separated by empty quote lines
            para_buf: list[str] = []
            for ql in q_lines:
                if not ql.strip():
                    if para_buf:
                        body.append(_convert_inline(" ".join(para_buf)) + "\n")
                        para_buf = []
                else:
                    para_buf.append(ql)
            if para_buf:
                body.append(_convert_inline(" ".join(para_buf)))
            body.append(r"\end{calloutbox}" + "\n")
            continue

        # Markdown Table
        if stripped.startswith("|") and idx + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[idx + 1]):
            headers = _split_md_row(lines[idx])
            aligns = _parse_alignments(lines[idx + 1], len(headers))
            idx += 2
            rows: list[list[str]] = []
            while idx < len(lines) and lines[idx].strip().startswith("|"):
                rows.append(_split_md_row(lines[idx]))
                idx += 1
            tbl = TableBlock(caption=pending_table_caption, headers=headers, aligns=aligns, rows=rows)
            pending_table_caption = None
            body.append(_render_table(tbl))
            continue

        # Lists (bullet or ordered, supporting nested 2-3 space indented sub-bullets)
        if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line):
            list_lines: list[str] = []
            while idx < len(lines) and lines[idx].strip():
                ln_cur = lines[idx]
                if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", ln_cur) or (ln_cur.startswith("  ") and list_lines):
                    list_lines.append(ln_cur)
                    idx += 1
                else:
                    break
            body.append(_render_list_block(list_lines))
            continue

        # Normal paragraph (consume consecutive non-special prose lines)
        para_lines: list[str] = []
        while idx < len(lines):
            cur = lines[idx]
            cs = cur.strip()
            if (
                not cs
                or cs == "---"
                or cs.startswith("#")
                or cs.startswith("$$")
                or cs.startswith(">")
                or cs.startswith("|")
                or re.match(r"^!\[[^\]]*\]\(([^)]+)\)\s*$", cs)
                or re.match(r"^\s*(?:[-*+]|\d+\.)\s+", cur)
            ):
                break
            para_lines.append(cs)
            idx += 1
        if para_lines:
            joined = " ".join(para_lines)
            # Detect standalone italicized table source lines `*Source: ...*` and tighten spacing
            if joined.startswith("*Source") or joined.startswith("*Note"):
                body.append(r"\par\vspace{-4pt}\noindent{\footnotesize " + _convert_inline(joined) + r"}\par\medskip")
            else:
                body.append(_convert_inline(joined) + "\n")

    if pending_table_caption:
        body.append(rf"\par\medskip\noindent\textbf{{{_convert_inline(pending_table_caption)}}}\par\smallskip")

    # Build metadata / abstract header cleanly
    doc_pt = "11pt" if is_journal_main else "10pt"
    margin_spec = "margin=0.95in,top=0.95in,bottom=0.95in" if is_journal_main else "margin=0.85in,top=0.88in,bottom=0.88in"
    line_spread = "1.22" if is_journal_main else "1.14"

    if is_journal_main:
        # Parse author/date lines vs Abstract / JEL / Keywords lines
        author_tex_rows: list[str] = []
        abstract_tex_rows: list[str] = []
        in_abs = False
        for ml in meta_lines:
            if ml.lower().startswith("**abstract"):
                in_abs = True
                abs_body = re.sub(r"^\*\*abstract\.?\*\*\s*:?\s*", "", ml, flags=re.I)
                if abs_body:
                    abstract_tex_rows.append(r"\noindent " + _convert_inline(abs_body))
            elif in_abs:
                abstract_tex_rows.append(r"\par\smallskip\noindent " + _convert_inline(ml))
            else:
                author_tex_rows.append(_convert_inline(ml))
        author_block = " \\\\[4pt]\n".join(author_tex_rows)
        abstract_block = "\n".join(abstract_tex_rows)
        toc_frag = ""
        if include_toc:
            toc_frag = r"""
\clearpage
\begingroup
\small
\setlength{\parskip}{2pt}
\setcounter{tocdepth}{2}
\renewcommand{\contentsname}{Contents}
\tableofcontents
\endgroup
\clearpage
"""
        front_matter = rf"""\begin{{center}}
{{\LARGE\bfseries {_escape_latex_text(_toc_plain_title(doc_title))} \par}}
\vspace{{10pt}}
{{\normalsize {author_block} \par}}
\vspace{{10pt}}
\end{{center}}

\begin{{quote}}
\small
\begin{{center}}\textbf{{Abstract}}\end{{center}}
\vspace{{-4pt}}
{abstract_block}
\end{{quote}}
\vspace{{8pt}}
\noindent\rule{{\linewidth}}{{0.4pt}}
\vspace{{6pt}}
{toc_frag}"""
    else:
        meta_tex_rows = [_convert_inline(ml) for ml in meta_lines]
        meta_block = " \\\\[3pt]\n".join(meta_tex_rows)
        front_matter = rf"""\begin{{center}}
{{\small\bfseries\color{{MutedText}}\MakeUppercase{{{_escape_latex_text(volume_label)}}}}}\\[6pt]
{{\LARGE\bfseries\color{{NavyAccent}} {_escape_latex_text(_toc_plain_title(doc_title))} \par}}
\vspace{{8pt}}
\end{{center}}

\begin{{quote}}
\small
{meta_block}
\end{{quote}}

\vspace{{4pt}}
\setcounter{{tocdepth}}{{2}}
\renewcommand{{\contentsname}}{{Contents}}
\tableofcontents
\vspace{{8pt}}
\noindent\rule{{\linewidth}}{{0.6pt}}
\vspace{{6pt}}
"""

    preamble = rf"""\documentclass[{doc_pt},letterpaper]{{article}}
\usepackage[{margin_spec}]{{geometry}}
\usepackage{{fontspec}}
\usepackage{{xeCJK}}
\usepackage{{amsmath,amssymb}}
\usepackage{{booktabs,array,adjustbox,makecell}}
\usepackage[table]{{xcolor}}
\usepackage{{graphicx}}
\usepackage{{caption}}
\usepackage{{fancyhdr}}
\usepackage{{enumitem}}
\usepackage[most]{{tcolorbox}}
\usepackage[hidelinks,bookmarks=true,bookmarksnumbered=false]{{hyperref}}
\usepackage{{titlesec}}
\usepackage{{needspace}}

\setmainfont{{Palatino}}
\setmonofont[Scale=0.82]{{Menlo}}
\setCJKmainfont[AutoFakeBold=2.0,ItalicFont={{Kaiti SC}}]{{Songti SC}}
\setCJKsansfont{{PingFang SC}}
\setCJKmonofont{{PingFang SC}}
\xeCJKsetup{{CJKecglue=\hspace{{0.12em plus 0.04em minus 0.02em}}}}
\linespread{{{line_spread}}}
\setlength{{\heavyrulewidth}}{{0.09em}}
\setlength{{\lightrulewidth}}{{0.05em}}
\setlength{{\cmidrulewidth}}{{0.04em}}

\definecolor{{NavyAccent}}{{HTML}}{{111827}}
\definecolor{{CrimsonAccent}}{{HTML}}{{9B2C2C}}
\definecolor{{PanelTint}}{{HTML}}{{F8FAFC}}
\definecolor{{RuleGray}}{{HTML}}{{CBD5E1}}
\definecolor{{MutedText}}{{HTML}}{{374151}}

\captionsetup[table]{{
  font={{small,bf}},
  labelfont={{bf}},
  justification=raggedright,
  singlelinecheck=false,
  skip=4pt
}}
\captionsetup[figure]{{
  font={{small}},
  labelfont={{bf}},
  justification=centering,
  skip=6pt
}}

\titleformat{{\section}}[block]{{\large\bfseries\color{{NavyAccent}}}}{{}}{{0pt}}{{}}
\titlespacing*{{\section}}{{0pt}}{{15pt}}{{5pt}}
\titleformat{{\subsection}}[block]{{\normalsize\bfseries\itshape\color{{NavyAccent}}}}{{}}{{0pt}}{{}}
\titlespacing*{{\subsection}}{{0pt}}{{11pt}}{{4pt}}
\titleformat{{\subsubsection}}[block]{{\normalsize\itshape\color{{MutedText}}}}{{}}{{0pt}}{{}}
\titlespacing*{{\subsubsection}}{{0pt}}{{8pt}}{{3pt}}

\setlist[itemize]{{leftmargin=1.5em,itemsep=2pt,topsep=4pt,parsep=1pt}}
\setlist[enumerate]{{leftmargin=1.7em,itemsep=2pt,topsep=4pt,parsep=1pt}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{6pt}}
\setlength{{\emergencystretch}}{{3em}}
\sloppy

\newtcolorbox{{calloutbox}}[2]{{
  enhanced,
  breakable,
  colback={{#1!5!white}},
  colframe={{#1}},
  boxrule=0pt,
  leftrule=3pt,
  arc=2pt,
  left=8pt,
  right=8pt,
  top=6pt,
  bottom=6pt,
  fonttitle=\small\bfseries,
  coltitle={{#1}},
  colbacktitle={{#1!5!white}},
  title={{#2}}
}}

\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{\scriptsize\color{{MutedText}} {_escape_latex_text(short_title)}}}
\fancyhead[R]{{\scriptsize\color{{MutedText}} \rightmark}}
\fancyfoot[C]{{\small\color{{MutedText}} \thepage}}
\renewcommand{{\headrulewidth}}{{0.3pt}}
\renewcommand{{\footrulewidth}}{{0pt}}

\begin{{document}}
\thispagestyle{{plain}}

{front_matter}
"""

    return preamble + "\n" + "\n".join(body) + "\n\\end{document}\n"


def _render_list_block(lines: list[str]) -> str:
    """Render Markdown bullet or numbered lists (with one level of nesting)."""
    items: list[tuple[int, bool, str]] = []  # (indent_level, is_ordered, text)
    for ln in lines:
        m_ord = re.match(r"^(\s*)(\d+)\.\s+(.*)$", ln)
        m_bul = re.match(r"^(\s*)[-*+]\s+(.*)$", ln)
        if m_ord:
            indent = 1 if len(m_ord.group(1)) >= 2 else 0
            items.append((indent, True, m_ord.group(3).strip()))
        elif m_bul:
            indent = 1 if len(m_bul.group(1)) >= 2 else 0
            items.append((indent, False, m_bul.group(2).strip()))
        elif items:
            ind, is_ord, prev = items[-1]
            items[-1] = (ind, is_ord, prev + " " + ln.strip())

    out: list[str] = []
    if not items:
        return ""
    top_env = "enumerate" if items[0][1] else "itemize"
    out.append(rf"\begin{{{top_env}}}")
    sub_env: str | None = None
    for ind, is_ord, txt in items:
        if ind == 0:
            if sub_env is not None:
                out.append(rf"\end{{{sub_env}}}")
                sub_env = None
            out.append(rf"\item {_convert_inline(txt)}")
        else:
            want_sub = "enumerate" if is_ord else "itemize"
            if sub_env is None:
                sub_env = want_sub
                out.append(rf"\begin{{{sub_env}}}")
            out.append(rf"\item {_convert_inline(txt)}")
    if sub_env is not None:
        out.append(rf"\end{{{sub_env}}}")
    out.append(rf"\end{{{top_env}}}")
    out.append("")
    return "\n".join(out)


def compile_spec(spec: dict[str, Path | str | bool], *, compile_pdf: bool = True) -> None:
    md_path = Path(str(spec["md"]))
    tex_path = Path(str(spec["tex"]))
    tex_src = convert_markdown_to_latex(
        md_path,
        short_title=str(spec["short_title"]),
        volume_label=str(spec["volume_label"]),
        is_journal_main=bool(spec.get("is_journal_main", True)),
        include_toc=bool(spec.get("include_toc", False)),
    )
    tex_path.write_text(tex_src, encoding="utf-8")
    print(f"Wrote LaTeX: {tex_path} ({len(tex_src.splitlines())} lines)")

    if compile_pdf:
        cmd = ["/opt/homebrew/bin/tectonic", "-X", "compile", tex_path.name]
        proc = subprocess.run(cmd, cwd=DOCS_DIR, capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
            raise RuntimeError(f"Tectonic failed on {tex_path.name} with code {proc.returncode}")
        pdf_path = Path(spec["pdf"])
        size_kb = pdf_path.stat().st_size / 1024.0
        print(f"Compiled PDF: {pdf_path} ({size_kb:.1f} KB)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build LaTeX & PDF versions of HK IPO overview monographs.")
    parser.add_argument("--no-pdf", action="store_true", help="Only write .tex files without running tectonic.")
    parser.add_argument("--master", action="store_true", help="Compile only HK_IPO_Financial_History_Master.{tex,pdf}.")
    args = parser.parse_args()

    specs = [MASTER_SPEC] if args.master else DEFAULT_SPECS
    for spec in specs:
        compile_spec(spec, compile_pdf=not args.no_pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
