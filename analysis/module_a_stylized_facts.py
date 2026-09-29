"""Module A — stylized facts for 2026 HK Main Board ordinary IPOs.

Follows the descriptive layer of Lowry, Michaely & Volkova (2017), Ch. 3:
distribution of initial returns, money left on the table, cuts by listing
route and pricing position, a US benchmark comparison, and short-horizon
aftermarket returns. 2025H1 (2025Q1-Q2) is shown alongside as the pre-reform
comparison group.

Outputs (analysis/out/module_a/):
    table1_stylized_facts.md / .tex   Panels A-D
    table2_aftermarket.md / .tex      Short-horizon BHR and wealth relatives
    fig1_monthly_cycle.png            Monthly IPO count and initial returns
    fig2_ir_distribution.png          Histogram of initial returns
    fig3_ir_by_route.png              Initial returns by listing route

Usage:
    python3 analysis/module_a_stylized_facts.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"
OUT = ROOT / "analysis" / "out" / "module_a"

# Lowry, Michaely & Volkova (2017), Tables 3.1, 3.3, 3.4 (US, 1973-2016).
US_BENCH = {
    "mean_ir": 0.173,
    "ir_below_range": 0.039,
    "ir_within_range": 0.122,
    "ir_above_range": 0.502,
    "vc_share": 0.352,
    "ir_vc": 0.274,
    "ir_nonvc": 0.119,
    "age": 17.1,
    "age_vc": 8.8,
    "age_nonvc": 21.6,
}

# Chart palette: dataviz reference instance (light mode).
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUE, ORANGE = "#2a78d6", "#eb6834"

ROUTE_ORDER = ["18A biotech", "18C specialist tech", "A+H (19A)", "Conventional"]
PRICING_ORDER = ["At low", "Within range", "At high", "Fixed price"]

C = {
    "ir": "First-day return / Underpricing (%)",
    "list_date": "Date of Listing (dd/mm/yy)",
    "offer": "IPO Subscription Price (HK$)",
    "base_shares": "Final global offering shares (before over-allotment)",
    "funds_hk": "Funds Raised HK (a)",
    "funds_int": "Funds Raised Int.(b)",
    "mlot": "Money left on the table (HK$)",
    "sub": "Subscription Ratio (times)",
    "pricing": "Pricing position in filing range",
    "vc": "Pre-IPO VC/PE backing (1=yes; 0=no)",
    "age": "Firm age at IPO (years)",
    "profit_y1": "Profit for the year in year-1",
    "c18a": "Chapter 18A flag",
    "c18c": "Chapter 18C flag",
    "ah": "A+H issuer flag",
    "wvr": "WVR flag",
    "route_text": "Listing route / applicable chapter",
    "corner": "Final cornerstone allocation (% of base offer)",
    "float": "Unrestricted public shareholding at listing (%)",
}

HORIZONS = [
    ("Day 5", "Day-5 BHR from Day-1 close (%)", "Day-5 wealth relative vs HSI", None),
    ("Day 20", "Day-20 BHR from Day-1 close (%)", "Day-20 wealth relative vs HSI", None),
    ("1 month", "1-month BHR from Day-1 close (%)", "1-month wealth relative vs HSI", "1-month HSI return (%)"),
    ("3 months", "3-month BHR from Day-1 close (%)", "3-month wealth relative vs HSI", None),
    ("6 months", "6-month BHR from Day-1 close (%)", "6-month wealth relative vs HSI", "6-month HSI return (%)"),
]


# ---------------------------------------------------------------- data

def load_panel(path: Path = MASTER) -> pd.DataFrame:
    """Load the master panel and add the analysis columns Module A needs."""
    df = pd.read_csv(path, low_memory=False).copy()
    df["cohort"] = df["cohort"].astype(str)
    df["ir"] = df[C["ir"]]
    df["listing_date"] = pd.to_datetime(df[C["list_date"]])
    df["month"] = df["listing_date"].dt.to_period("M")
    df["gross_proceeds"] = df[C["funds_hk"]] + df[C["funds_int"]]
    # Base-deal proceeds match the share base of money left on the table.
    df["base_proceeds"] = df[C["offer"]] * df[C["base_shares"]]
    df["loss_y1"] = (df[C["profit_y1"]] < 0).astype(float).where(df[C["profit_y1"]].notna())
    df["ah_true"] = (
        (df[C["ah"]] == 1)
        | df[C["route_text"]].str.contains(r"other listed shares|A\+H", case=False, na=False)
    ).astype(int)
    df["route"] = np.select(
        [df[C["c18a"]] == 1, df[C["c18c"]] == 1, df["ah_true"] == 1],
        ROUTE_ORDER[:3],
        default="Conventional",
    )
    return df


def split_samples(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (2026 IPOs, 2025H1 comparison IPOs)."""
    return df[df["cohort"].str.startswith("2026")], df[df["cohort"].str.startswith("2025")]


# ---------------------------------------------------------------- stats

def summarize(g: pd.DataFrame) -> dict[str, float]:
    ir = g["ir"].dropna()
    return {
        "N": len(g),
        "Gross proceeds, total (HK$bn)": g["gross_proceeds"].sum() / 1e9,
        "Gross proceeds, median deal (HK$m)": g["gross_proceeds"].median() / 1e6,
        "Initial return, mean": ir.mean(),
        "Initial return, median": ir.median(),
        "Initial return, std. dev.": ir.std(),
        "Share with IR < 0": (ir < 0).mean(),
        "Share with IR = 0": (ir == 0).mean(),
        "Value-weighted IR (MLOT / base proceeds)": g[C["mlot"]].sum() / g["base_proceeds"].sum(),
        "Money left on table, total (HK$bn)": g[C["mlot"]].sum() / 1e9,
        "Public subscription ratio, median (x)": g[C["sub"]].median(),
        "Share fixed-price offers": (g[C["pricing"]] == "Fixed price").mean(),
        "Share VC/PE-backed": g[C["vc"]].mean(),
        "Share loss-making (year-1)": g["loss_y1"].mean(),
        "Firm age, median (years)": g[C["age"]].median(),
        "Share Chapter 18A": (g["route"] == "18A biotech").mean(),
        "Share Chapter 18C": (g["route"] == "18C specialist tech").mean(),
        "Share A+H": (g["route"] == "A+H (19A)").mean(),
        "Cornerstone allocation, mean (% base offer)": g[C["corner"]].mean(),
        "Unrestricted public float, median": g[C["float"]].median(),
    }


PCT_ROWS = {
    "Initial return, mean", "Initial return, median", "Initial return, std. dev.",
    "Share with IR < 0", "Share with IR = 0", "Value-weighted IR (MLOT / base proceeds)",
    "Share fixed-price offers", "Share VC/PE-backed", "Share loss-making (year-1)",
    "Share Chapter 18A", "Share Chapter 18C", "Share A+H",
    "Cornerstone allocation, mean (% base offer)", "Unrestricted public float, median",
}


def fmt(row: str, v: float) -> str:
    if pd.isna(v):
        return "—"
    if row == "N":
        return f"{int(v)}"
    if row in PCT_ROWS:
        return f"{100 * v:.1f}%"
    return f"{v:,.1f}"


def panel_a(y26: pd.DataFrame, y25: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    cols = {q: summarize(g) for q, g in y26.groupby("cohort")}
    cols["2026 all"] = summarize(y26)
    cols["2025H1 (comparison)"] = summarize(y25)
    tab = pd.DataFrame(cols)
    tab = tab.apply(lambda s: [fmt(r, v) for r, v in s.items()])

    ir = y26["ir"].dropna()
    quarters = [g["ir"].dropna() for _, g in y26.groupby("cohort")]
    q2, q3 = (y26.loc[y26.cohort == q, "ir"].dropna() for q in ("2026Q2", "2026Q3"))
    notes = [
        f"2026 mean IR > 0: t = {stats.ttest_1samp(ir, 0).statistic:.2f} "
        f"(p = {stats.ttest_1samp(ir, 0).pvalue:.3g}); median IR > 0: Wilcoxon p = {stats.wilcoxon(ir).pvalue:.3g}.",
        f"IR equal across 2026 quarters: Kruskal-Wallis H = {stats.kruskal(*quarters).statistic:.2f} "
        f"(p = {stats.kruskal(*quarters).pvalue:.3g}).",
        f"2026Q2 vs 2026Q3: Mann-Whitney p = {stats.mannwhitneyu(q2, q3).pvalue:.3g}; "
        f"Welch t p = {stats.ttest_ind(q2, q3, equal_var=False).pvalue:.3g}.",
        f"2026 vs 2025H1: Mann-Whitney p = {stats.mannwhitneyu(ir, y25['ir'].dropna()).pvalue:.3g}; "
        f"Welch t p = {stats.ttest_ind(ir, y25['ir'].dropna(), equal_var=False).pvalue:.3g}.",
    ]
    return tab, notes


def route_stats(g: pd.DataFrame) -> dict[str, str]:
    ir = g["ir"].dropna()
    return {
        "N": f"{len(g)}",
        "Mean IR": f"{100 * ir.mean():.1f}%",
        "Median IR": f"{100 * ir.median():.1f}%",
        "IR < 0": f"{100 * (ir < 0).mean():.0f}%",
        "VW IR": f"{100 * g[C['mlot']].sum() / g['base_proceeds'].sum():.1f}%",
        "Median proceeds (HK$m)": f"{g['gross_proceeds'].median() / 1e6:,.0f}",
        "Median age (yrs)": f"{g[C['age']].median():.1f}",
        "Loss-making": f"{100 * g['loss_y1'].mean():.0f}%",
        "VC/PE-backed": f"{100 * g[C['vc']].mean():.0f}%",
    }


def panel_b(y26: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    rows = {r: route_stats(y26[y26.route == r]) for r in ROUTE_ORDER}
    rows["Memo: WVR (any route)"] = route_stats(y26[y26[C["wvr"]] == 1])
    groups = [y26.loc[y26.route == r, "ir"].dropna() for r in ROUTE_ORDER]
    n_fixed = int(((y26[C["ah"]] == 0) & (y26["ah_true"] == 1)).sum())
    notes = [
        f"IR equal across routes: Kruskal-Wallis H = {stats.kruskal(*groups).statistic:.2f} "
        f"(p = {stats.kruskal(*groups).pvalue:.3g}).",
        "Routes are mutually exclusive in the order 18A > 18C > A+H > Conventional; WVR overlaps.",
        f"A+H is flag OR route text 'PRC issuer with other listed shares': {n_fixed} issuers "
        "have the text but a 0 flag in the panel (pending fix).",
    ]
    return pd.DataFrame(rows).T, notes


def panel_c(y26: pd.DataFrame) -> pd.DataFrame:
    us = {
        "At low": US_BENCH["ir_below_range"],
        "Within range": US_BENCH["ir_within_range"],
        "At high": US_BENCH["ir_above_range"],
        "Fixed price": np.nan,
    }
    rows = {}
    for p in PRICING_ORDER:
        g = y26[y26[C["pricing"]] == p]
        rows[p] = {
            "N": f"{len(g)}",
            "Share of sample": f"{100 * len(g) / len(y26):.0f}%",
            "Mean IR": f"{100 * g['ir'].mean():.1f}%",
            "Median IR": f"{100 * g['ir'].median():.1f}%",
            "US mean IR (LMV Table 3.3)": "—" if pd.isna(us[p]) else f"{100 * us[p]:.1f}%",
        }
    return pd.DataFrame(rows).T


def panel_d(y26: pd.DataFrame) -> pd.DataFrame:
    vc, nonvc = y26[y26[C["vc"]] == 1], y26[y26[C["vc"]] == 0]
    b = US_BENCH
    rows = [
        ("Mean initial return", y26["ir"].mean(), b["mean_ir"], True),
        ("Share VC/PE-backed", y26[C["vc"]].mean(), b["vc_share"], True),
        ("Mean IR, VC/PE-backed", vc["ir"].mean(), b["ir_vc"], True),
        ("Mean IR, not VC/PE-backed", nonvc["ir"].mean(), b["ir_nonvc"], True),
        ("Mean firm age (years)", y26[C["age"]].mean(), b["age"], False),
        ("Mean age, VC/PE-backed", vc[C["age"]].mean(), b["age_vc"], False),
        ("Mean age, not VC/PE-backed", nonvc[C["age"]].mean(), b["age_nonvc"], False),
    ]
    f = lambda v, pct: f"{100 * v:.1f}%" if pct else f"{v:.1f}"
    return pd.DataFrame(
        {"HK 2026": [f(hk, p) for _, hk, _, p in rows], "US 1973-2016": [f(us, p) for _, _, us, p in rows]},
        index=[r[0] for r in rows],
    )


def table2(y26: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    rows = {}
    for label, bhr_col, wr_col, bench_col in HORIZONS:
        g = y26[y26[bhr_col].notna()]
        bhr = g[bhr_col]
        agg_wr = (1 + bhr.mean()) / (1 + g[bench_col].mean()) if bench_col else np.nan
        by_q = "/".join(str(int(y26.loc[y26.cohort == q, bhr_col].notna().sum())) for q in ("2026Q1", "2026Q2", "2026Q3"))
        rows[label] = {
            "N (Q1/Q2/Q3)": f"{len(g)} ({by_q})",
            "Mean BHR": f"{100 * bhr.mean():.1f}%",
            "Median BHR": f"{100 * bhr.median():.1f}%",
            "BHR > 0": f"{100 * (bhr > 0).mean():.0f}%",
            "Wilcoxon p (median = 0)": f"{stats.wilcoxon(bhr).pvalue:.3f}",
            "Median WR vs HSI": f"{g[wr_col].median():.3f}",
            "WR < 1": f"{100 * (g[wr_col] < 1).mean():.0f}%",
            "Aggregate WR vs HSI (LMV)": "—" if pd.isna(agg_wr) else f"{agg_wr:.3f}",
        }
    notes = [
        "BHR is measured from the day-1 close, so it excludes the initial return.",
        "Aggregate WR = (1 + mean IPO BHR) / (1 + mean HSI return) as in Lowry et al. (2017) Ch. 7; "
        "shown only where the HSI horizon return is in the panel.",
        "Horizons are unbalanced: 6-month returns cover 2026Q1 only. Event-time Wilcoxon p-values ignore "
        "calendar clustering (Mitchell & Stafford 2000) — treat them as descriptive.",
    ]
    return pd.DataFrame(rows).T, notes


# ---------------------------------------------------------------- writers

def to_markdown(df: pd.DataFrame, index_name: str = "") -> str:
    header = "| " + " | ".join([index_name] + [str(c) for c in df.columns]) + " |"
    sep = "|" + "---|" * (len(df.columns) + 1)
    body = ["| " + " | ".join([str(i)] + [str(v) for v in r]) + " |" for i, r in zip(df.index, df.values)]
    return "\n".join([header, sep, *body])


def to_latex(df: pd.DataFrame, caption: str) -> str:
    esc = lambda s: str(s).replace("%", r"\%").replace("&", r"\&").replace("$", r"\$").replace("_", r"\_")
    lines = [
        r"\begin{table}[htbp]\centering\small",
        rf"\caption{{{esc(caption)}}}",
        r"\begin{tabular}{l" + "r" * len(df.columns) + "}",
        r"\hline",
        " & ".join([""] + [esc(c) for c in df.columns]) + r" \\",
        r"\hline",
        *(" & ".join([esc(i)] + [esc(v) for v in r]) + r" \\" for i, r in zip(df.index, df.values)),
        r"\hline",
        r"\end{tabular}",
        r"\end{table}",
    ]
    return "\n".join(lines)


def write_tables(y26: pd.DataFrame, y25: pd.DataFrame) -> None:
    a, a_notes = panel_a(y26, y25)
    b, b_notes = panel_b(y26)
    c, d = panel_c(y26), panel_d(y26)
    t2, t2_notes = table2(y26)

    sample = (
        f"Sample: {len(y26)} HK Main Board ordinary IPOs listed "
        f"{y26.listing_date.min():%d %b %Y} – {y26.listing_date.max():%d %b %Y}; "
        f"comparison group 2025H1 (n = {len(y25)}). IR = day-1 close / offer price − 1."
    )
    bullet = lambda ns: "\n".join(f"- {n}" for n in ns)
    md1 = "\n\n".join([
        "# Table 1 — Stylized facts, 2026 HK Main Board IPOs",
        sample,
        "## Panel A. By listing quarter", to_markdown(a), bullet(a_notes),
        "## Panel B. By listing route (2026)", to_markdown(b, "Route"), bullet(b_notes),
        "## Panel C. By pricing position in the filing range (2026)", to_markdown(c, "Pricing"),
        "- HK offers cannot price above the top of the range, so \"At high\" is compared with the US \"above range\" bucket.",
        "## Panel D. HK 2026 vs US benchmark (Lowry, Michaely & Volkova 2017, Tables 3.1 and 3.4)", to_markdown(d),
        "- HK backing counts any pre-IPO VC or PE investor; the US figure is VC only (SDC flag), so the HK share is an upper bound for a like-for-like comparison.",
    ]) + "\n"
    md2 = "\n\n".join([
        "# Table 2 — Short-horizon aftermarket returns, 2026 IPOs",
        to_markdown(t2, "Horizon"), bullet(t2_notes),
    ]) + "\n"
    (OUT / "table1_stylized_facts.md").write_text(md1, encoding="utf-8")
    (OUT / "table2_aftermarket.md").write_text(md2, encoding="utf-8")

    tex1 = "\n\n".join([
        to_latex(a, "Table 1A. Stylized facts by listing quarter"),
        to_latex(b, "Table 1B. Initial returns by listing route, 2026"),
        to_latex(c, "Table 1C. Initial returns by pricing position, 2026"),
        to_latex(d, "Table 1D. HK 2026 vs US 1973-2016"),
    ])
    (OUT / "table1_stylized_facts.tex").write_text(tex1 + "\n", encoding="utf-8")
    (OUT / "table2_aftermarket.tex").write_text(to_latex(t2, "Table 2. Short-horizon aftermarket returns, 2026") + "\n", encoding="utf-8")


# ---------------------------------------------------------------- figures

def style_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(SURFACE)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelcolor=INK2, length=0, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def pct_axis(ax: plt.Axes, axis: str = "y") -> None:
    fmtr = matplotlib.ticker.FuncFormatter(lambda v, _: f"{100 * v:.0f}%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmtr)


def new_fig(*args, **kw):
    fig, ax = plt.subplots(*args, **kw)
    fig.patch.set_facecolor(SURFACE)
    return fig, ax


def fig1_monthly(y26: pd.DataFrame) -> None:
    months = pd.period_range(y26.month.min(), y26.month.max(), freq="M")
    m = y26.groupby("month")["ir"].agg(["count", "mean", "median"]).reindex(months)
    x = np.arange(len(months))
    labels = [p.strftime("%b") for p in months]

    fig, (top, bot) = new_fig(2, 1, figsize=(8, 6), sharex=True, gridspec_kw={"height_ratios": [1, 2]})
    for ax in (top, bot):
        style_axes(ax)

    top.bar(x, m["count"].fillna(0), width=0.6, color=BLUE)
    for xi, n in zip(x, m["count"].fillna(0)):
        top.text(xi, n + 0.5, f"{int(n)}", ha="center", va="bottom", fontsize=8, color=INK2)
    top.set_ylabel("IPOs listed", color=INK2, fontsize=9)
    top.set_ylim(0, m["count"].max() * 1.25)

    rng = np.random.default_rng(0)
    idx = {p: i for i, p in enumerate(months)}
    xs = y26["month"].map(idx).to_numpy() + rng.uniform(-0.18, 0.18, len(y26))
    bot.scatter(xs, y26["ir"], s=14, color=MUTED, alpha=0.45, linewidths=0, label="Individual IPO")
    bot.plot(x, m["mean"], color=BLUE, lw=2, marker="o", ms=5, label="Monthly mean")
    bot.plot(x, m["median"], color=ORANGE, lw=2, marker="o", ms=5, label="Monthly median")
    bot.axhline(0, color=AXIS, lw=1)
    bot.text(x[-1] + 0.3, m["mean"].iloc[-1], "Mean", color=INK2, fontsize=8, va="center")
    bot.text(x[-1] + 0.3, m["median"].iloc[-1], "Median", color=INK2, fontsize=8, va="center")
    pct_axis(bot)
    bot.set_ylabel("First-day return", color=INK2, fontsize=9)
    bot.set_xticks(x, labels)
    bot.set_xlim(-0.6, len(x) - 0.1)
    bot.legend(frameon=False, fontsize=8, loc="upper left", labelcolor=INK2)

    fig.suptitle("2026 HK Main Board IPOs: monthly volume and first-day returns", x=0.08, ha="left",
                 fontsize=11, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_monthly_cycle.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def fig2_distribution(y26: pd.DataFrame) -> None:
    ir = y26["ir"].dropna()
    fig, ax = new_fig(figsize=(8, 4.2))
    style_axes(ax)
    bins = np.arange(np.floor(ir.min() * 10) / 10, ir.max() + 0.2, 0.2)
    ax.hist(ir, bins=bins, color=BLUE, edgecolor=SURFACE, linewidth=2)
    top = ax.get_ylim()[1]
    # (value, label, colour, label side, label height as share of y-range)
    marks = [
        (ir.median(), f"Median {100 * ir.median():.0f}%", INK, "left", 0.95),
        (ir.mean(), f"Mean {100 * ir.mean():.0f}%", INK, "right", 0.95),
        (US_BENCH["mean_ir"], "US mean 17%\n(1973–2016)", MUTED, "right", 0.62),
    ]
    for v, lab, col, side, h in marks:
        ax.axvline(v, color=col, lw=1.2, ls="--" if col == MUTED else "-")
        dx = 0.03 if side == "right" else -0.03
        ax.text(v + dx, top * h, lab, color=col, fontsize=8, va="top", ha="left" if side == "right" else "right",
                bbox={"facecolor": SURFACE, "edgecolor": "none", "pad": 1})
    ax.axvline(0, color=AXIS, lw=1)
    pct_axis(ax, "x")
    ax.set_xlabel("First-day return", color=INK2, fontsize=9)
    ax.set_ylabel("Number of IPOs", color=INK2, fontsize=9)
    ax.set_title(f"Distribution of first-day returns, 2026 (n = {len(ir)}); {100 * (ir < 0).mean():.0f}% close below offer",
                 loc="left", fontsize=11, color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "fig2_ir_distribution.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def fig3_routes(y26: pd.DataFrame) -> None:
    fig, ax = new_fig(figsize=(8, 3.8))
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    rng = np.random.default_rng(1)
    order = ROUTE_ORDER[::-1]
    for i, r in enumerate(order):
        ir = y26.loc[y26.route == r, "ir"].dropna()
        ax.scatter(ir, i + rng.uniform(-0.15, 0.15, len(ir)), s=18, color=BLUE, alpha=0.55, linewidths=0)
        ax.plot([ir.median()] * 2, [i - 0.3, i + 0.3], color=INK, lw=2.2, solid_capstyle="round")
        ax.text(ir.median(), i + 0.34, f"median {100 * ir.median():.0f}%", color=INK2, fontsize=8, ha="center", va="bottom")
    ax.axvline(0, color=AXIS, lw=1)
    ax.set_yticks(range(len(order)), [f"{r} (n={int((y26.route == r).sum())})" for r in order])
    pct_axis(ax, "x")
    ax.set_xlabel("First-day return (bar = median)", color=INK2, fontsize=9)
    ax.set_title("First-day returns by listing route, 2026", loc="left", fontsize=11, color=INK, fontweight="bold")
    ax.set_ylim(-0.5, len(order) - 0.35)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_ir_by_route.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    y26, y25 = split_samples(load_panel())
    write_tables(y26, y25)
    fig1_monthly(y26)
    fig2_distribution(y26)
    fig3_routes(y26)
    print(f"Module A written to {OUT.relative_to(ROOT)}/ ({len(y26)} IPOs in 2026, {len(y25)} in 2025H1)")


if __name__ == "__main__":
    main()
