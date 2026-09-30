# Tables, figures and replication packages

## Contents
1. Standard table sequence
2. Regression table conventions
3. LaTeX (booktabs) mechanics
4. Figures
5. Replication package

---

## 1. Standard table sequence for an IPO paper

1. **Sample construction.** Start from the population (e.g. all HKEX Main Board
   new listings in the period) and list each filter with the number removed
   and remaining: listings by introduction, GEM transfers, SPAC/de-SPAC,
   missing prospectus/allotment data, missing price data. Overlapping reasons:
   report the sequential count and the reason-level count.
2. **Distribution over time and industry.** N, proceeds, mean/median IR by
   year or month and by sector; hot/cold periods visible.
3. **Descriptive statistics.** N, mean, SD, p1/p25/median/p75/p99 for every
   variable used, *before* winsorization (and note where winsorized). Units
   in the variable name or a column.
4. **Correlation matrix** (Pearson below, Spearman above the diagonal) for key
   regressors; flag |ρ| > 0.7.
5. **Univariate comparisons.** Treated vs control (e.g. with vs without
   cornerstones): means with t-test, medians with Wilcoxon rank-sum.
6. **Main regressions.** Nested columns on one common sample.
7. **Identification / endogeneity.** IV first and second stage; matching
   balance and ATT; selection model.
8. **Robustness.** One table per threat.
9. **Long-run performance.** BHAR by horizon; calendar-time α.
10. **Appendix: variable definitions** with source document and timing.

## 2. Regression table conventions

- Dependent variable named in the header; one column per specification,
  numbered (1), (2), ….
- Coefficient with SE (or t-stat, but say which) beneath in parentheses.
- Rows at the bottom: FE indicators (Yes/No), SE type and cluster variable,
  number of clusters, N, adjusted R² (within R² for FE models if reported).
- Notes: variable definitions pointer, winsorization, SE method, significance
  convention. If the text relies on wild-bootstrap p-values, the stars must use
  them too (`regtable.regression_table(..., pvalues_override=...)`) or report
  the bootstrap p-values in a separate row.
- Stars: JF/JFE/RFS accept them; AEA journals do not. Three decimals for
  coefficients on decimal-scale returns; state if returns are in %.
- Economic magnitude in the text: effect of a one-SD change in the regressor
  on the LHS, relative to the LHS mean or median. For log IR, convert:
  exp(β·ΔX) − 1.

## 3. LaTeX (booktabs) mechanics

Preamble: `\usepackage{booktabs}`; with `pf.etable(type="tex")` also
`threeparttable`, `makecell` and `tabularx`. Optional: `siunitx` for decimal
alignment (`S` columns), `dcolumn` in older templates.

Minimal skeleton that `scripts/regtable.py` emits:

```latex
\begin{table}[!htbp]\centering
\caption{Cornerstone investors and initial returns}\label{tab:main}
\begin{tabular}{lccc}
\toprule
 & \multicolumn{3}{c}{Log initial return} \\
\cmidrule(lr){2-4}
 & (1) & (2) & (3) \\
\midrule
Cornerstone share & -0.412$^{**}$ & -0.388$^{**}$ & -0.301$^{*}$ \\
 & (0.171) & (0.165) & (0.158) \\
\midrule
Industry FE & No & Yes & Yes \\
Listing-month FE & No & No & Yes \\
SE & HC3 & Cluster (month) & Cluster (month) \\
Observations & 84 & 84 & 84 \\
Adj.\ $R^2$ & 0.143 & 0.201 & 0.238 \\
\bottomrule
\end{tabular}
\end{table}
```

(The numbers above are placeholders for layout only.) No vertical rules, no
`\hline`: booktabs uses `\toprule`, `\midrule`, `\cmidrule`, `\bottomrule`.

## 4. Figures

- IR distribution: histogram with the zero line and a log-scale or winsorized
  view; mark the share of IR < 0 and IR = 0 (price support).
- Time series: monthly IPO count and average IR (hot/cold markets, Ibbotson &
  Jaffe 1975).
- Long run: mean BHAR paths by month with confidence bands; IPO vs benchmark.
- Binned scatter for a key regressor (after partialling out controls).
- RD designs: binned outcome against running variable with the threshold and
  a density plot of the running variable.

## 5. Replication package

Journals increasingly require code and data availability statements (the AEA
Data Editor's template README is the de facto standard; JF, RFS and JFE have
code-sharing policies). Structure:

```
README.md          # data sources, access, software versions, run order, runtime
data/raw/          # read-only originals or instructions to obtain them
data/derived/      # produced by code only
code/00_master.py  # runs everything in order
code/01_build_sample.py ... code/05_tables.py
output/tables/  output/figures/
requirements.txt / uv.lock
```

Rules: raw data never edited by hand; every number in the paper is produced by
code; random seeds fixed and recorded; package versions pinned; sample-selection
log saved; hand-collected data (prospectus extraction) shipped with source
page references so a reviewer can verify a random subset.
