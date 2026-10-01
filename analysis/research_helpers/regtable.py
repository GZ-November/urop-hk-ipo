"""Booktabs (three-line) LaTeX regression tables from Python results.

For pyfixest models prefer ``pf.etable(models, type="tex", ...)``. Use this
module for statsmodels / linearmodels results, or when the paper wants a plain
``tabular`` (no tabularx / makecell) that compiles with only ``booktabs``.

    from regtable import regression_table
    tex = regression_table(
        [m1, m2, m3],
        labels={"cornerstone_pct": "Cornerstone share", "ln_proceeds": "Ln(proceeds)"},
        keep=["cornerstone_pct", "ln_proceeds"],
        extra_rows={"Industry FE": ["No", "Yes", "Yes"],
                    "Listing-month FE": ["No", "No", "Yes"],
                    "SE": ["HC3", "Cluster (month)", "Cluster (month)"]},
        depvar="Initial return (log)",
        notes=r"Standard errors in parentheses. $^{*}p<0.10$, $^{**}p<0.05$, $^{***}p<0.01$.",
    )

Works with any result exposing ``params`` and ``pvalues`` plus ``bse``
(statsmodels) or ``std_errors`` (linearmodels); ``nobs`` and an R-squared are
read when available. Custom inference (e.g. wild-bootstrap p-values) can be
passed through ``pvalues_override`` so stars match the inference reported.
"""
from __future__ import annotations

from typing import Mapping, Optional, Sequence

import numpy as np
import pandas as pd


def _get(res, *names):
    for n in names:
        if hasattr(res, n):
            v = getattr(res, n)
            return v() if callable(v) and n != "params" else v
    return None


def _stars(p: float, cuts=(0.10, 0.05, 0.01)) -> str:
    if p is None or pd.isna(p):
        return ""
    return "*" * sum(p < c for c in cuts)


def _tex_escape(s: str) -> str:
    mapping = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
               "_": r"\_", "#": r"\#", "$": r"\$", "{": r"\{",
               "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(mapping.get(char, char) for char in str(s))


def regression_table(models: Sequence, labels: Optional[Mapping[str, str]] = None,
                     keep: Optional[Sequence[str]] = None,
                     extra_rows: Optional[Mapping[str, Sequence[str]]] = None,
                     depvar: Optional[str] = None, digits: int = 3,
                     stars: bool = True, show_t: bool = False,
                     pvalues_override: Optional[Sequence[Optional[Mapping[str, float]]]] = None,
                     notes: str = "", caption: Optional[str] = None,
                     label: Optional[str] = None) -> str:
    """Return a LaTeX table: coefficients with SEs (or t-stats) beneath.

    ``notes`` is inserted verbatim (write LaTeX, e.g. ``$p<0.10$``); labels and
    row names, extra-row values and caption are escaped. A mapping override
    replaces all star p-values for that model: unlisted coefficients have no
    stars. Use None for a model that intentionally retains conventional p-values.
    Notes remain raw LaTeX; disclose any mixture of inference methods.

    Star rules follow the p-values actually used for inference. Journals differ:
    AEA journals forbid stars; JF/JFE/RFS accept them. Set ``stars=False`` and
    report SEs/p-values when targeting a no-stars outlet.
    """
    labels = dict(labels or {})
    k = len(models)
    if not k:
        raise ValueError("at least one model is required")
    if isinstance(digits, bool) or not isinstance(digits, int) or digits < 0:
        raise ValueError("digits must be a nonnegative integer")
    if any(len(values) != k for values in (extra_rows or {}).values()):
        raise ValueError("each extra row must have one value per model")
    if pvalues_override is not None and len(pvalues_override) != k:
        raise ValueError("pvalues_override must have one entry per model")
    params = [pd.Series(_get(m, "params")) for m in models]
    ses = [pd.Series(_get(m, "bse", "std_errors")) for m in models]
    tvals = [pd.Series(_get(m, "tvalues", "tstats")) for m in models]
    pvals = [pd.Series(_get(m, "pvalues")) for m in models]
    order = list(keep) if keep is not None else list(dict.fromkeys(n for p in params for n in p.index))
    if pvalues_override is not None:
        for j, ov in enumerate(pvalues_override):
            if ov is not None:
                if set(ov) - set(params[j].index):
                    raise ValueError("p-value override contains unknown coefficients")
                # Omitted coefficients get no stars, never a conventional fallback.
                pvals[j] = pd.Series(ov, dtype=float)
    for values in pvals:
        if ((values.dropna() < 0) | (values.dropna() > 1)).any():
            raise ValueError("p-values must be in [0, 1] or missing")

    fmt = f"{{:.{digits}f}}"
    lines = []
    lines.append(r"\begin{table}[!htbp]\centering")
    if caption:
        lines.append(rf"\caption{{{_tex_escape(caption)}}}")
    if label:
        if any(c in label for c in "{}\\%#&$~^") or any(c.isspace() for c in label):
            raise ValueError("label must be a plain LaTeX identifier")
        lines.append(rf"\label{{{label}}}")
    lines.append(r"\begin{tabular}{l" + "c" * k + "}")
    lines.append(r"\toprule")
    if depvar:
        lines.append(rf" & \multicolumn{{{k}}}{{c}}{{{_tex_escape(depvar)}}} \\")
        lines.append(rf"\cmidrule(lr){{2-{k + 1}}}")
    lines.append(" & " + " & ".join(f"({i + 1})" for i in range(k)) + r" \\")
    lines.append(r"\midrule")
    for name in order:
        row, sub = [], []
        for j in range(k):
            if name in params[j].index and np.isfinite(params[j][name]):
                s = _stars(pvals[j].get(name)) if stars else ""
                row.append(fmt.format(params[j][name]) + (f"$^{{{s}}}$" if s else ""))
                below = tvals[j].get(name) if show_t else ses[j].get(name)
                if below is None or not np.isfinite(below):
                    sub.append("")
                else:
                    sub.append(f"[{fmt.format(below)}]" if show_t else f"({fmt.format(below)})")
            else:
                row.append("")
                sub.append("")
        lines.append(_tex_escape(labels.get(name, name)) + " & " + " & ".join(row) + r" \\")
        lines.append(" & " + " & ".join(sub) + r" \\")
    lines.append(r"\midrule")
    for rname, vals in (extra_rows or {}).items():
        lines.append(_tex_escape(rname) + " & " + " & ".join(_tex_escape(v) for v in vals) + r" \\")
    nobs = [_get(m, "nobs") for m in models]
    lines.append("Observations & " + " & ".join(
        "" if n is None else f"{int(n):,}" for n in nobs) + r" \\")
    adj = all(hasattr(m, "rsquared_adj") for m in models)
    r2 = [_get(m, "rsquared_adj") if adj else _get(m, "rsquared") for m in models]
    if any(v is not None for v in r2):
        lines.append((r"Adj.\ $R^2$" if adj else r"$R^2$") + " & " + " & ".join(
            "" if v is None else fmt.format(float(v)) for v in r2) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    if notes:
        lines.append(r"\par\vspace{2pt}\begin{minipage}{0.95\linewidth}\footnotesize "
                     + notes + r"\end{minipage}")
    lines.append(r"\end{table}")
    return "\n".join(lines)
