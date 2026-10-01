"""Literature-informed issuance-cost, allocation and retail-demand analyses.

Design: docs/OFFERING_ECONOMICS_DESIGN_2026.md. Exploratory associations,
113 IPO snapshot through 2026-09-30, without trading-performance outcomes.
"""
from __future__ import annotations

import hashlib
import json
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from scipy.special import expit
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.outliers_influence import variance_inflation_factor

from module_b_underpricing_regression import wild_cluster_p
from offer_facts_2026 import CUTOFF, build_frame, table
from research_helpers.regtable import regression_table
from research_inputs import MASTER, ROOT

OUT = ROOT / "analysis/out/offering_economics"
SEED = 20261001
BOOTSTRAP_DRAWS = 1000
BASE = ["ln_size"]
ISSUER = ["ln_size", "ln_age", "ah", "loss"]
FULL = [*ISSUER, "technology", "health", "q2", "q3"]
LABELS = {"const": "Intercept", "ln_size": "Log base proceeds", "ln_age": "Log firm age",
          "ah": "A+H issuer", "loss": "Loss-making", "technology": "Technology industry",
          "health": "Health industry", "q2": "Q2 listing", "q3": "Q3 listing",
          "corner_share": "Final cornerstone share"}


def prepare() -> pd.DataFrame:
    d, _ = build_frame()
    z = d.copy()
    z["code"] = d["Stock Code"]
    z["month_id"] = d.listing_date.dt.strftime("%Y-%m")
    z["ln_size"] = np.log(d.base_bn.where(d.base_bn > 0))
    z["ln_age"] = np.log(d.age.where(d.age > 0))
    z["ln_expense"] = np.log(d.expense_m.where(d.expense_m > 0))
    z["ln_applicants"] = np.log(d.applicants.where(d.applicants > 0))
    z["corner_share"] = d.corner / 100
    z["technology"] = d.sector.isin(["Semiconductors", "Software and AI", "Hardware and robotics"]).astype(float)
    z["health"] = d.sector.isin(["Biotech and pharma", "Medical devices and services"]).astype(float)
    z["coarse_sector"] = np.select([z.technology.eq(1), z.health.eq(1)], ["Technology", "Health"], default="Other")
    if d.sector.isin(["Unmapped", "Unknown"]).any():
        raise ValueError("Coarse-sector model cannot silently classify an unmapped industry")
    z["q2"] = d.listing_date.dt.quarter.eq(2).astype(float)
    z["q3"] = d.listing_date.dt.quarter.eq(3).astype(float)
    applied_value = d["Public valid applied shares"] * d["IPO Subscription Price (HK$)"]
    initial_value = d["Public Offer shares"] * d["IPO Subscription Price (HK$)"]
    avg_value = applied_value / d.applicants.where(d.applicants > 0)
    z["constructed_multiple"] = applied_value / initial_value.where(initial_value > 0)
    z["ln_multiple"] = np.log(z.constructed_multiple.where(z.constructed_multiple > 0))
    z["ln_avg_application"] = np.log(avg_value.where(avg_value > 0))
    z["ln_initial_public_value"] = np.log(initial_value.where(initial_value > 0))
    return z.replace([np.inf, -np.inf], np.nan)


def select_sample(d: pd.DataFrame, required: list[str], family: str) -> pd.DataFrame:
    """Fix each family on its largest specification and log every exclusion."""
    valid = d[required].notna().all(axis=1)
    log = d[["code", "month_id"]].copy()
    log["included"] = valid
    log["missing_or_invalid_fields"] = d[required].isna().apply(lambda s: "; ".join(s.index[s]), axis=1)
    log.to_csv(OUT / f"sample_{family}.csv", index=False)
    return d.loc[valid].copy()


def design(z: pd.DataFrame, xs: list[str]) -> pd.DataFrame:
    x = sm.add_constant(z[xs].astype(float), has_constant="add")
    if np.linalg.matrix_rank(x) != x.shape[1] or len(x) <= x.shape[1]:
        raise ValueError("Model requires full rank and positive residual degrees of freedom")
    h = np.einsum("ij,ji->i", x.to_numpy(), np.linalg.pinv(x.to_numpy()))
    if h.max() >= 1 - 1e-9:
        raise ValueError("Unit leverage makes HC3 unavailable")
    return x


def ols(z: pd.DataFrame, y: str, xs: list[str]):
    x = design(z, xs)
    ordinary = sm.OLS(z[y].astype(float), x).fit()
    # Preserve named coefficients for reusable table helpers.
    robust = sm.OLS(z[y].astype(float), x).fit(cov_type="HC3")
    return ordinary, robust, x


def inferential_table(frame: pd.DataFrame) -> str:
    """Do not round small positive p-values to an apparent exact zero."""
    display = frame.copy()
    for c in display:
        if c.endswith(" p"):
            display[c] = display[c].map(lambda p: "—" if pd.isna(p) else "<0.001" if p < .001 else f"{p:.4f}")
    return table(display)


def focal_test(z: pd.DataFrame, y: str, xs: list[str], focus: str, null: float = 0) -> dict:
    ordinary, robust, x = ols(z, y, xs)
    j = list(x.columns).index(focus)
    cluster = ordinary.get_robustcov_results(cov_type="cluster", groups=z.month_id,
                                           use_correction=True, use_t=True)
    g = z.month_id.nunique()
    if g < 2:
        raise ValueError("At least two listing months required")
    hc_p = float(robust.t_test(f"{focus} = {null}").pvalue)
    cluster_p = float(2 * stats.t.sf(abs((ordinary.params[focus] - null) / cluster.bse[j]), g - 1))
    shifted_y = z[y].to_numpy(float) - null * x[focus].to_numpy()
    wild_p = wild_cluster_p(shifted_y, x.to_numpy(), z.month_id.to_numpy(), j)
    ci = robust.conf_int().loc[focus]
    return {"N": len(z), "Months G": g, "Coefficient": robust.params[focus], "HC3 SE": robust.bse[focus],
            "HC3 lower": ci.iloc[0], "HC3 upper": ci.iloc[1], "Null": null, "HC3 p": hc_p,
            "CR1 p": cluster_p, "Restricted wild p": wild_p, "R squared": ordinary.rsquared}


def family(z: pd.DataFrame, y: str, name: str, models: list[tuple[str, list[str]]]):
    rows, diag, fits = [], [], []
    for model, xs in models:
        ordinary, robust, x = ols(z, y, xs)
        fits.append(robust)
        for key in x:
            rows.append({"Model": model, "Term": key, "Coefficient": robust.params[key],
                         "HC3 SE": robust.bse[key], "HC3 p": robust.pvalues[key], "N": len(z)})
        influence = ordinary.get_influence()
        vif = [variance_inflation_factor(x.to_numpy(), j) for j in range(1, x.shape[1])]
        diag.append({"Family": name, "Model": model, "N": len(z), "Parameters": x.shape[1],
                     "Residual df": ordinary.df_resid, "Months G": z.month_id.nunique(),
                     "Max leverage": influence.hat_matrix_diag.max(), "Max VIF excluding intercept": max(vif),
                     "R squared": ordinary.rsquared, "Adjusted R squared": ordinary.rsquared_adj,
                     "Largest Cook code": z.iloc[np.argmax(influence.cooks_distance[0])].code,
                     "Max Cook distance": influence.cooks_distance[0].max()})
    coef = pd.DataFrame(rows)
    coef.to_csv(OUT / f"coefficients_{name}.csv", index=False)
    (OUT / f"regressions_{name}.tex").write_text(regression_table(
        fits, labels=LABELS, depvar=y, stars=False,
        extra_rows={"Industry controls": ["Yes" if "technology" in xs else "No" for _, xs in models],
                    "Quarter controls": ["Yes" if "q2" in xs else "No" for _, xs in models],
                    "Listing months": [str(z.month_id.nunique())] * len(models),
                    "Standard errors": ["HC3"] * len(models)},
        notes="Exploratory associations. Common estimation sample within each family. No significance stars; see separate wild-cluster focal tests."))
    wide = coef.pivot(index="Term", columns="Model", values="Coefficient").rename(index=LABELS).reset_index()
    return wide, pd.DataFrame(diag)


def influence_checks(z: pd.DataFrame, y: str, xs: list[str], focus: str, name: str, null: float = 0) -> pd.DataFrame:
    ordinary, _, _ = ols(z, y, xs)
    cook_code = z.iloc[np.argmax(ordinary.get_influence().cooks_distance[0])].code
    subsets = [("Full model", z), ("Drop largest three offerings", z.drop(z.nlargest(3, "base_bn").index)),
               (f"Drop highest Cook observation ({cook_code})", z[z.code != cook_code])]
    rows = [{"Analysis": name, "Check": label, **focal_test(sample, y, xs, focus, null)} for label, sample in subsets]
    for month in sorted(z.month_id.unique()):
        sample = z[z.month_id != month]
        _, robust, _ = ols(sample, y, xs)
        rows.append({"Analysis": name, "Check": "Leave out " + month, "N": len(sample), "Months G": sample.month_id.nunique(),
                     "Coefficient": robust.params[focus], "HC3 SE": robust.bse[focus], "Null": null})
    return pd.DataFrame(rows)


def doubling_share(params: np.ndarray, x: np.ndarray, size_column: int) -> float:
    """Standardized finite contrast in cornerstone share, percentage points."""
    changed = x.copy()
    changed[:, size_column] += np.log(2)
    return float(100 * np.mean(expit(changed @ params) - expit(x @ params)))


def fractional_cornerstone(z: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    x = design(z, FULL)
    model = sm.GLM(z.corner_share, x, family=sm.families.Binomial())
    fit = model.fit(cov_type="HC0", maxiter=100)
    if not fit.converged or not np.isfinite(fit.params).all():
        raise ValueError("Fractional logit did not converge")
    coef = pd.DataFrame({"Term": x.columns, "Coefficient": fit.params.to_numpy(), "HC0 SE": fit.bse.to_numpy(), "HC0 p": fit.pvalues.to_numpy()})
    coef.to_csv(OUT / "fractional_cornerstone_coefficients.csv", index=False)
    j = list(x.columns).index("ln_size")
    observed = doubling_share(fit.params.to_numpy(), x.to_numpy(), j)
    rng = np.random.default_rng(SEED)
    clusters = [np.flatnonzero(z.month_id.to_numpy() == m) for m in sorted(z.month_id.unique())]
    draws, diagnostics = [], []
    attempts = 0
    while len(draws) < BOOTSTRAP_DRAWS and attempts < 5 * BOOTSTRAP_DRAWS:
        attempts += 1
        idx = np.concatenate([clusters[c] for c in rng.integers(0, len(clusters), len(clusters))])
        xb, yb = x.to_numpy()[idx], z.corner_share.to_numpy()[idx]
        status = "accepted"
        if np.linalg.matrix_rank(xb) != xb.shape[1]:
            status = "rank deficient"
        else:
            with warnings.catch_warnings(record=True) as caught:
                try:
                    boot = sm.GLM(yb, xb, family=sm.families.Binomial()).fit(maxiter=100)
                    if not boot.converged or not np.isfinite(boot.params).all():
                        status = "nonconverged/nonfinite"
                    elif any("separation" in str(w.message).lower() for w in caught):
                        status = "separation warning"
                    else:
                        draws.append(doubling_share(boot.params, x.to_numpy(), j))
                except (ValueError, np.linalg.LinAlgError):
                    status = "fit error"
        diagnostics.append({"Attempt": attempts, "N resampled": len(idx), "Status": status})
    if len(draws) < BOOTSTRAP_DRAWS:
        raise ValueError("Insufficient valid fractional-logit bootstrap draws")
    pd.DataFrame(diagnostics).to_csv(OUT / "fractional_bootstrap_diagnostics.csv", index=False)
    pd.DataFrame({"Draw": np.arange(1, len(draws)+1), "Doubling size contrast (pp)": draws}).to_csv(OUT / "fractional_bootstrap_draws.csv", index=False)
    lo, hi = np.quantile(draws, [.025, .975])
    result = pd.DataFrame([{"N": len(z), "Months G": len(clusters), "Doubling-size share contrast (pp)": observed,
                            "Month-pairs lower": lo, "Month-pairs upper": hi, "Valid draws": len(draws),
                            "Rejected attempts": attempts-len(draws)}])
    result.to_csv(OUT / "fractional_cornerstone_contrast.csv", index=False)
    predictions = z[["code", "corner_share"]].copy()
    predictions["Fitted share"] = fit.predict(x)
    predictions.to_csv(OUT / "fractional_cornerstone_predictions.csv", index=False)
    diagnostics_summary = {"attempts": attempts, "valid": len(draws), "rejected": attempts-len(draws),
                           "seed": SEED, "percentile_intervals": "exploratory; nine month clusters"}
    return coef, result, diagnostics_summary


def overlap(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for col in ["route", "coarse_sector"]:
        for name, g in d.groupby(col):
            backed = int(g.vcpe.eq(1).sum())
            unbacked = int(g.vcpe.eq(0).sum())
            rows.append({"Grouping": col, "Group": name, "Backed N": backed, "Non-backed N": unbacked,
                         "Unknown N": int(g.vcpe.isna().sum()), "Both groups observed": backed > 0 and unbacked > 0})
    support = pd.DataFrame(rows)
    support.to_csv(OUT / "backing_overlap.csv", index=False)
    balances = []
    for key in ["ln_size", "ln_age", "ah", "loss", "technology", "health", "q2", "q3"]:
        a = d.loc[d.vcpe.eq(1), key].dropna()
        b = d.loc[d.vcpe.eq(0), key].dropna()
        pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        smd = (a.mean()-b.mean()) / pooled if pooled > 0 else np.nan
        balances.append({"Variable": LABELS[key], "Backed N": len(a), "Non-backed N": len(b),
                         "Backed mean": a.mean(), "Non-backed mean": b.mean(), "Standardized mean difference": smd})
    balance = pd.DataFrame(balances)
    balance.to_csv(OUT / "backing_balance.csv", index=False)
    return support, balance


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    d = prepare()
    designs = [("M1", BASE), ("M2", ISSUER), ("M3", FULL)]
    cost = select_sample(d, ["ln_expense", "month_id", *FULL], "expenses")
    fee = select_sample(d, ["fee_hk", "month_id", *FULL], "commission")
    cornerstone = select_sample(d, ["corner_share", "month_id", *FULL], "cornerstone")
    applicants = select_sample(d, ["ln_applicants", "corner_share", "month_id", *FULL], "applicants")
    specifications = [(cost, "ln_expense", "expenses", designs), (fee, "fee_hk", "commission", designs),
                      (cornerstone, "corner_share", "cornerstone", designs),
                      (applicants, "ln_applicants", "applicants", [*designs, ("M4", [*FULL, "corner_share"])])]
    tables, diagnostics = {}, []
    for sample, y, name, models in specifications:
        tab, diag = family(sample, y, name, models)
        tables[name] = tab
        diagnostics.append(diag)
    pd.concat(diagnostics, ignore_index=True).to_csv(OUT / "model_diagnostics.csv", index=False)
    tests = []
    focal_specs = [(cost, "ln_expense", FULL, "ln_size", 1., "Expense elasticity = 1"),
                   (fee, "fee_hk", FULL, "ln_size", 0., "Commission size slope = 0"),
                   (cornerstone, "corner_share", FULL, "ln_size", 0., "Cornerstone size slope = 0 (OLS)"),
                   (applicants, "ln_applicants", FULL, "ln_size", 0., "Applicant size slope = 0 (M3)"),
                   (applicants, "ln_applicants", [*FULL, "corner_share"], "corner_share", 0., "Applicant cornerstone slope = 0 (M4)")]
    for sample, y, xs, focus, null, label in focal_specs:
        tests.append({"Focal test": label, **focal_test(sample, y, xs, focus, null)})
    tests = pd.DataFrame(tests)
    tests["HC3 Holm p"] = multipletests(tests["HC3 p"], method="holm")[1]
    tests["Wild Holm p"] = multipletests(tests["Restricted wild p"], method="holm")[1]
    tests.to_csv(OUT / "focal_tests.csv", index=False)
    sensitivity = pd.concat([influence_checks(sample, y, xs, focus, label, null)
                             for sample, y, xs, focus, null, label in focal_specs], ignore_index=True)
    sensitivity.to_csv(OUT / "influence_and_month_sensitivity.csv", index=False)
    _, fractional, boot_info = fractional_cornerstone(cornerstone)
    support, balance = overlap(d)
    required = ["ln_multiple", "ln_applicants", "ln_avg_application", "ln_initial_public_value", "month_id", *FULL]
    demand = select_sample(d, required, "demand_decomposition")
    decomposition = []
    for y in ["ln_multiple", "ln_applicants", "ln_avg_application", "ln_initial_public_value"]:
        _, fit, _ = ols(demand, y, FULL)
        decomposition.append({"Component": y, "N": len(demand), "Coefficient": fit.params.ln_size,
                              "HC3 SE": fit.bse.ln_size})
    decomposition = pd.DataFrame(decomposition)
    decomposition.to_csv(OUT / "demand_decomposition.csv", index=False)
    b = decomposition.set_index("Component")["Coefficient"]
    residual = float(b.ln_multiple - b.ln_applicants - b.ln_avg_application + b.ln_initial_public_value)
    if abs(residual) > 1e-9:
        raise ValueError("Shared-sample demand coefficient identity failed")
    discrepancies = d[["code", "subscription", "constructed_multiple", "Public subscription original wording"]].copy()
    discrepancies["Relative difference"] = discrepancies.constructed_multiple / discrepancies.subscription - 1
    discrepancies["Above 1 percent difference"] = discrepancies["Relative difference"].abs() > .01
    discrepancies.to_csv(OUT / "subscription_definition_comparison.csv", index=False)
    mismatch = discrepancies[discrepancies["Above 1 percent difference"]]
    cost_result, fee_result, corner_result, app_result, app_corner = [tests.iloc[k] for k in range(5)]
    report = ["# Offering Economics: Costs, Cornerstones and Retail Demand",
              "## Research question and sample",
              "This report develops the offering-facts analysis into conditional models of issuance costs, disclosed commissions, cornerstone allocation and retail participation. It uses 113 unique Hong Kong Main Board IPOs listed through 30 September 2026; first-day and aftermarket performance are excluded. The data are existing export observations, without a new source audit.",
              "These are literature-informed exploratory associations. The [design record](../../../docs/OFFERING_ECONOMICS_DESIGN_2026.md) was written before these new models were run, after existing facts had been examined. The [literature review](../../../docs/IPO_LITERATURE_METHODS_2026.md) documents inspected papers and limits to transferring their methods.",
              "## Main results",
              f"1. **Expense scaling.** The fully adjusted log-expense elasticity is {cost_result['Coefficient']:.3f} (HC3 SE {cost_result['HC3 SE']:.3f}, N={len(cost)}). Doubling proceeds is associated with {100*(2**cost_result['Coefficient']-1):.1f}% higher absolute expenses and {100*(2**(cost_result['Coefficient']-1)-1):.1f}% change in the expense/proceeds ratio. The null tested is elasticity=1: restricted wild p={cost_result['Restricted wild p']:.4f}, family-adjusted wild Holm p={cost_result['Wild Holm p']:.4f}.",
              f"2. **Disclosed commissions.** Doubling base proceeds is associated with a {fee_result['Coefficient']*np.log(2):.3f}-percentage-point change in the disclosed Hong Kong tranche rate (N={len(fee)}; wild p={fee_result['Restricted wild p']:.4f}; wild Holm p={fee_result['Wild Holm p']:.4f}). This is not a causal fee reduction or a full gross-spread estimate.",
              f"3. **Cornerstone composition.** In the linear model, doubling proceeds is associated with {100*corner_result['Coefficient']*np.log(2):.2f} percentage points in cornerstone share (N={len(cornerstone)}; wild p={corner_result['Restricted wild p']:.4f}; wild Holm p={corner_result['Wild Holm p']:.4f}). The fractional-logit finite contrast is reported separately below. Offer size and allocation are selected together, so this does not identify certification or the effect of mechanically enlarging a deal.",
              f"4. **Retail participation.** The applicant-count size elasticity is {app_result['Coefficient']:.3f} (N={len(applicants)}; wild Holm p={app_result['Wild Holm p']:.4f}). Adding final cornerstone share gives a slope of {app_corner['Coefficient']:.3f} per 100 percentage points, or {100*(np.exp(.1*app_corner['Coefficient'])-1):.1f}% in applicants per additional 10 percentage points (wild Holm p={app_corner['Wild Holm p']:.4f}). This is an association with final allocation, not a causal demand effect.",
              "## Focal inference and multiplicity", inferential_table(tests),
              "HC3 treats IPO residuals as independent; listing-month CR1 and restricted wild-bootstrap tests allow within-month dependence. There are nine calendar clusters. All 512 Rademacher sign patterns are enumerated, removing Monte Carlo noise but not finite-cluster approximation error. Separate Holm corrections cover five adjusted OLS focal tests; supplementary models, decomposition tests and the earlier exploration are outside this narrow family. No stars are used.",
              "## Specifications",
              "M1 contains log proceeds; M2 adds log age, A+H and loss status; M3 adds technology and health indicators plus Q2/Q3 indicators. Applicants M4 adds final cornerstone share. Each family fixes its common sample using the largest specification. Coefficient files include HC3 standard errors and p-values; separate model diagnostics report rank, leverage, VIF and residual degrees of freedom."]
    for name, tab in tables.items():
        report += [f"### {name.title()}", table(tab)]
    report += ["## Bounded cornerstone-share model", "The fractional-logit specification follows the conditional-mean approach of [Papke and Wooldridge](https://www.nber.org/papers/t0147). Zeros are retained and fitted shares lie in [0,1]; binomial quasi-likelihood is used with HC0 sandwich covariance. A finite doubling-size contrast averages fitted share changes over the original model sample. Percentile intervals refit on resampled listing-month blocks. Nine clusters make these intervals exploratory; the linear restricted bootstrap is not applied to nonlinear models.",
               table(fractional), f"Bootstrap: {boot_info['valid']} valid draws from {boot_info['attempts']} attempts; {boot_info['rejected']} rejected attempts. Diagnostics and draws are saved. These conditional draws omit rank-deficient resamples, and their interval is not a finite-sample-valid confidence statement.",
               "## Retail-demand denominator decomposition", table(decomposition),
               f"The conditional size gradient in the constructed multiple is {b.ln_multiple:.3f}: applicant participation ({b.ln_applicants:.3f}) plus nominal application intensity ({b.ln_avg_application:.3f}) minus initial public-tranche value ({b.ln_initial_public_value:.3f}). The denominator therefore matters substantially. Lower subscription multiples for larger deals should not automatically be described as fewer participating investors; the applicant slope is small and imprecisely estimated.",
               f"On the shared N={len(demand)} sample, the size slope of the constructed subscription multiple equals the applicant slope plus the average nominal-application slope minus the initial-tranche-value slope. Identity residual={residual:.2e}. This is accounting plus OLS linearity, not three independently identified behavioral mechanisms.",
               f"{len(mismatch)} IPOs differ by more than 1% between the reported multiple and valid applied shares/initial public shares:", table(mismatch.drop(columns="Public subscription original wording")),
               "Reported wording, rounding, tranche definitions and share quantities require source reconciliation before attributing these differences. No reported value is overwritten. Applicants are IPO-specific counts, not unique investors across deals; nominal application values are not actual net cash commitments.",
               "## VC/PE comparison readiness", table(support), table(balance),
               "Some sectors/routes lack both backed and non-backed IPOs, while important covariates may be imbalanced. The combined VC/PE category also differs from the original VC-only certification literature. No matching-based treatment effect is estimated; balance diagnostics do not remove unobserved selection.",
               "## Influence and stability", inferential_table(sensitivity[sensitivity.Check.str.startswith(('Full', 'Drop'))]),
               "All leave-one-month-out slopes are saved in influence_and_month_sensitivity.csv. Removing influential IPOs changes the estimand and sample; stable coefficients are not proof of causality. All attempted checks are retained.",
               "The cost model's most influential observation is 6228.HK, a sale-only depositary-receipt offering rather than a new-share capital raise. Its current final base quantity is 89,668,600 HDRs, consistent with the recorded HDR unit review; the historical tenfold base quantity is not used. Its different offering structure is a further reason to read the drop-one cost specification alongside the pooled estimate.",
               "## Limits and next research steps",
               "Expenses can be estimated rather than final and may already include commissions. Final cornerstone shares and retail demand can respond jointly to expected interest and final offering terms. Coarse industry and quarter controls cannot remove issuer quality, sponsor matching or market-timing selection. The completed-IPO cross-section cannot estimate listing likelihood without private-firm and unsuccessful-applicant controls. An all-post-reform 2026 sample provides no policy before/after comparison.",
               "The most useful additions are investor-level allocation/bid information, source-verified initial cornerstone commitments and timestamps, repaired investor classifications, comparable private firms, and several years of offerings. A genuine later-cohort validation should freeze these models before Q4 outcomes are inspected.",
               "## Replication",
               "Run `python3 analysis/offering_economics_2026.py` or `make offering-economics`. Tables, model coefficients, common-sample logs, booktabs LaTeX fragments, inference, influence checks, subscription discrepancies, overlap diagnostics, nonlinear draws and predictions are saved beside this report. The input manifest fixes dates, source bytes, method and software versions.",
               "![Costs and demand decomposition](fig_offering_economics.png)"]
    (OUT / "analysis.md").write_text("\n\n".join(report)+"\n")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ah, label, color in [(0, "Other issuers", "#2a78d6"), (1, "A+H issuers", "#eb6834")]:
        g = cost[cost.ah.eq(ah)]
        axes[0].scatter(g.base_bn, g.expense_m, c=color, alpha=.75, label=label)
    axes[0].legend(frameon=False, fontsize=9)
    axes[0].set(xscale="log", yscale="log", xlabel="Base proceeds (HKD billion, log scale)",
                ylabel="Listing expenses (HKD million, log scale)", title="Absolute issuance expenses")
    vals = [b.ln_applicants, b.ln_avg_application, -b.ln_initial_public_value, b.ln_multiple]
    axes[1].bar(["Applicants", "Application\nintensity", "Minus public\ntranche size", "Constructed\nmultiple"], vals,
                color=["#2a78d6", "#2a78d6", "#eb6834", "#555555"])
    axes[1].axhline(0, color="black", lw=.7)
    axes[1].set(ylabel="Conditional log-proceeds slope", title="Subscription denominator decomposition")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle(f"Offering economics | 113 IPOs through 30 September 2026 | cost N={len(cost)}, demand N={len(demand)}", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "fig_offering_economics.png", dpi=180)
    plt.close(fig)
    manifest = {"cutoff": str(CUTOFF.date()), "sample_n": len(d), "input": str(MASTER.relative_to(ROOT)),
                "sha256": hashlib.sha256(MASTER.read_bytes()).hexdigest(), "seed": SEED,
                "script_sha256": hashlib.sha256((ROOT / "analysis/offering_economics_2026.py").read_bytes()).hexdigest(),
                "design_sha256": hashlib.sha256((ROOT / "docs/OFFERING_ECONOMICS_DESIGN_2026.md").read_bytes()).hexdigest(),
                "family_n": {"expenses": len(cost), "commission": len(fee), "cornerstone": len(cornerstone),
                             "applicants": len(applicants), "decomposition": len(demand)},
                "bootstrap": boot_info, "language": "English", "design": "docs/OFFERING_ECONOMICS_DESIGN_2026.md",
                "versions": {"pandas": pd.__version__, "numpy": np.__version__, "scipy": scipy.__version__, "statsmodels": statsmodels.__version__}}
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(manifest, indent=2))
    print(tests[["Focal test", "Coefficient", "Restricted wild p", "Wild Holm p"]].to_string(index=False))


if __name__ == "__main__":
    main()
