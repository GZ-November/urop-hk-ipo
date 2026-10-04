"""Deterministic mentor tables with a source-bound lot overlay; no simulations."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from research_inputs import C, ROOT, load_panel, select_2026
from shared.allocation_review import reviewed_tiers

OUT = ROOT / "analysis/out/retail_evidence_brief"
EVIDENCE = ROOT / "pipeline/reports/data_gap_collection/source_followup_2026-10-03"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(frame: pd.DataFrame, sample: str) -> dict:
    a, r = frame.allocation_rate.to_numpy(), frame.initial_return.to_numpy()
    product = a.mean() * r.mean()
    covariance = ((a - a.mean()) * (r - r.mean())).mean()
    app_return = frame.application_return.mean()
    assert np.isclose(product + covariance, app_return, atol=1e-12)
    return {"sample": sample, "n": len(frame), "mean_initial_return": r.mean(),
            "median_initial_return": np.median(r), "mean_allocation_rate": a.mean(),
            "mean_application_return": app_return, "median_application_return": frame.application_return.median(),
            "return_gap_pp": 100 * (r.mean() - app_return), "product_of_means": product,
            "covariance_contribution_pp": 100 * covariance,
            "covariance_reduction_pct": -100 * covariance / product,
            "mean_expected_gross_profit_hkd": frame.expected_gross_profit_hkd.mean(),
            "median_expected_gross_profit_hkd": frame.expected_gross_profit_hkd.median()}


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(map(str, row)) + " |" for row in rows])


def write_reports(summaries, quarters, fees, concentration, evidence_table):
    base = summaries.set_index("sample").loc["corrected_all_113"]
    ledger = pd.read_csv(EVIDENCE / "nineteen_applied_totals.csv")
    stale_count = int((~ledger.formal_master_consistent).sum())
    formal_status = ("All 19 formal extraction totals have now been repaired and independently reviewed for col_CO; "
                     "the old values are preserved in before snapshots. This is a scoped field review, not whole-payload writeback approval."
                     if stale_count == 0 else f"{stale_count} formal extraction totals remain stale.")
    percent = lambda x: f"{100*x:.2f}%"
    money = lambda x: f"{x:,.2f}"
    names = {"corrected_all_113": "Corrected one-lot baseline",
             "prior_112_exclude_2649": "Exclude 2649 (previous strict sample)",
             "exclude_3355": "Exclude 3355",
             "exclude_19_total_corrections": "Exclude 19 total corrections",
             "exclude_2649_3355_and_19": "Exclude all 21 flagged issuers"}
    comparison = table(["Measure", "IPO mean", "IPO median"], [
        ["First-day return on allocated securities", percent(base.mean_initial_return), percent(base.median_initial_return)],
        ["Expected gross return on one-lot application principal", percent(base.mean_application_return), percent(base.median_application_return)],
        ["Expected gross profit per application (HK$)", money(base.mean_expected_gross_profit_hkd), money(base.median_expected_gross_profit_hkd)]])
    quarter_table = table(["Quarter", "N", "Mean first-day return", "Mean application return", "Covariance (pp)", "Mean gross profit (HK$)"],
                          [[r["sample"], r["n"], percent(r["mean_initial_return"]), percent(r["mean_application_return"]),
                            f'{r["covariance_contribution_pp"]:.2f}', money(r["mean_expected_gross_profit_hkd"])]
                           for r in quarters.to_dict("records")])
    fee_table = table(["Assumed fee (HK$)", "Mean expected profit (HK$)", "Median IPO expected profit (HK$)", "Mean return after fee"],
                      [[r["fee_hkd"], money(r["mean_expected_profit_hkd"]), money(r["median_ipo_expected_profit_hkd"]),
                        percent(r["mean_application_return_after_fee"])] for r in fees])
    winner_table = table(["Largest-profit IPOs excluded", "N", "Mean gross profit (HK$)", "Mean profit with HK$88 fee", "Excluded codes"],
                         [[i, r["n"], money(r["mean_expected_gross_profit_hkd"]), money(r["mean_expected_profit_fee88_hkd"]),
                           r["removed_codes"] or "None"] for i, r in zip([0, 1, 3], concentration)])
    exclusions = table(["Sample", "N", "Mean application return", "Covariance (pp)", "Mean gross profit (HK$)"],
                       [[names[r["sample"]], r["n"], percent(r["mean_application_return"]), f'{r["covariance_contribution_pp"]:.2f}',
                         money(r["mean_expected_gross_profit_hkd"])] for r in summaries.to_dict("records")])
    mentor = f"""# From headline IPO returns to retail application returns

Mentor discussion draft | 3 October 2026 | Price observation cutoff: 30 September 2026

## Research question and sample

How much of a new listing's first-day return reaches a retail investor who applies for one lot? We study 113 ordinary Hong Kong Main Board IPOs listed from 2 January to 30 September 2026 (Q1: 38; Q2: 45; Q3: 30). Each IPO receives equal weight. Allocation expectations come from the disclosed application tier, including guarantees and additional ballots; they describe a hypothetical applicant in that tier, rather than the average actual retail account.

Source follow-up resolves two earlier qualifications. ALSCO (2649) officially corrected its board lot to 500 shares; its minimum application is also 500 shares, so the one-lot sample now includes all 113 IPOs. FS.COM (3355) subsequently disclosed the ten Pool B guarantees previously inferred in our data; all ten match. The 19 corrected application totals match 763 quantity/count pairs read afresh from the original PDFs. {formal_status} This draft uses a separately documented lot-size overlay and does not rewrite pipeline approvals. See the [evidence assessment](RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md).

## 1. How far are headline returns from application returns?

{comparison}

The mean difference is **{base.return_gap_pp:.2f} percentage points**. This is a difference between return denominators: the headline return is earned on allocated securities, while the application return spreads the expected profit across all requested principal. The application principal here equals requested quantity times the final offer price; it excludes application levies and does not measure peak cash blocked at the maximum offer price. The median is the median across IPO-specific expectations, not a median investor outcome. The single HDR issuer is calculated in its own disclosed security units.

## 2. What does the allocation-return relationship contribute?

For IPO i, define a_i as expected allotted quantity divided by requested quantity, and r_i as first-day close divided by offer price minus one. Expected application return is a_i r_i. The exact equal-IPO decomposition is:

`mean(a*r) = mean(a)*mean(r) + Cov_N(a,r)`

The product of means is **{percent(base.product_of_means)}**, and the covariance contributes **{base.covariance_contribution_pp:.2f} percentage points**, leaving **{percent(base.mean_application_return)}**. The negative covariance offsets **{base.covariance_reduction_pct:.1f}%** of the product-of-means component. Covariance uses denominator N, so the identity is exact.

This describes a combination of smaller allocations in high-return IPOs and larger allocations in weaker IPOs. The product of means is an algebraic comparison; it does not identify the return from changing an allocation rule. Demand, offer size and issuer characteristics can jointly affect allocations and returns, so the decomposition does not establish causation or investor information types.

## 3. How sensitive are the conclusions?

**Across quarters:** the covariance is negative in every quarter, while the expected monetary gain varies considerably.

{quarter_table}

**Fees:** gross profit is the baseline. All nonzero fees below are hypothetical per-application scenarios paid regardless of allocation.

{fee_table}

The average gross profit implies a handling-fee-only break-even level of HK${base.mean_expected_gross_profit_hkd:.2f} per application in this observed sample. It is not a complete-cost threshold: allotted-security subscription brokerage and levies, selling costs, financing and opportunity cost are excluded. HK$88 is a sensitivity parameter, not evidence of historical account fees. An average after-fee application return is the mean of profit/principal across IPOs, so it need not equal mean HK$ profit divided by mean principal.

**Large winners:** removing the IPOs with the largest expected one-lot gross profits leaves positive mean gross profit, but changes the sign under the HK$88 scenario.

{winner_table}

These exclusions are retrospective influence checks, not subscription selection rules. The ranking uses expected one-lot HK$ profit, rather than headline percentage returns.

**Source exclusions:** the main allocation-return pattern also remains after removing the flagged issuers.

{exclusions}

Exclusions change issuer and quarter composition; their differences cannot be attributed solely to data quality. One-lot expected profits depend on the selected tier, not on an issuer's aggregate application total. Consequently, the 19 total corrections do not mechanically change this draft's one-lot results; they matter for aggregate allocation rates and data consistency.

## Interpretation and next discussion

The contribution is to quantify the distance between IPO returns on allotted securities and returns on requested retail capital using actual tier rules. The negative allocation-return covariance is stable in the reported source exclusions and quarters; the profitability conclusion depends on fees, period and large winners. These are exploratory, sample-specific expectations conditional on observed first-day closing prices, not realized account returns, annualized performance or forecasts. This draft uses no simulation, bootstrap, or new hypothesis tests and makes no population significance claim.

For discussion with the supervisor: is this allocation-adjusted descriptive question a sufficient research focus, and which institutional comparison would add an economic explanation without overstating identification?

## Reproduction

From the repository root, with the cited official PDFs cached locally:

```bash
.venv/bin/python tools/audit_retail_sources_2026.py
.venv/bin/python analysis/retail_evidence_brief_2026.py
```

Tables and issuer-level results: [deterministic outputs](../../analysis/out/retail_evidence_brief/). [Run manifest](../../analysis/out/retail_evidence_brief/run_manifest.json) records hashes; the [source manifest](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/source_manifest.json) records official URLs and local PDF hashes. Earlier portfolio simulations are not used in this draft.
"""
    (ROOT / "docs/reports/RETAIL_MENTOR_BRIEF_2026-10-03.md").write_text(mentor)
    status_table = table(["Item", "Verified", "Still derived / unresolved", "Exclusion N", "Application return", "Covariance (pp)"],
                         [[r["item"], r["status"], r["remaining_derivation"], r["n"], percent(r["mean_application_return"]),
                           f'{r["covariance_contribution_pp"]:.2f}'] for r in evidence_table.to_dict("records")])
    labels = {"documented_rounded_subscription_reconstruction": "Rounded-ratio reconstruction documented",
              "documented_reconstruction_with_arithmetic_mismatch": "Formula documented; additional arithmetic mismatch",
              "compatible_with_rounded_subscription_reconstruction_not_documented": "Compatible with rounding; cause unrecorded",
              "original_error_mechanism_not_documented": "Earlier total unsupported; error mechanism unrecorded"}
    ledger_table = table(["Code", "Tiers", "PDF pages", "Old formal total", "Verified sum / workbook / master", "Change", "Origin assessment"],
                         [[r["code"], r["tiers"], r["pdf_pages"], f'{r["old_formal_value"]:,}', f'{r["exact_pdf_tier_sum"]:,}',
                           f'{r["delta"]:+,}', labels[r["cause_status"]]] for r in ledger.to_dict("records")])
    assessment = f"""# Retail evidence assessment and exclusion results

3 October 2026 | Research price cutoff: 30 September 2026 | Scope: 2649, 3355 and 19 application-total corrections

## Reviewable summary

Corrected baseline: N=113, mean gross application return {percent(base.mean_application_return)}, covariance contribution {base.covariance_contribution_pp:.2f} pp, mean expected gross profit HK${base.mean_expected_gross_profit_hkd:.2f}.

{status_table}

This is a scoped source reassessment and deterministic research sensitivity exercise. It creates no whole-payload pipeline gate approval, changes no workbook/master/frozen tier/review bytes, and does not certify all issuer fields. {formal_status} The existing hash-bound tier gate is checked before use. A source-specific overlay changes only 2649's lot classification in the new draft; earlier generated results retain their historical definitions.

## 2649: resolved by official correction

The original 6 March allotment PDF physically prints a 200-share board lot on page 17 and starts applications at 500 shares on page 12. The prospectus specifies 500 on PDF pages 412 and 417 (printed pages 403 and 408). The issuer's [11 March clarification](https://www.hkexnews.hk/listedco/listconews/sehk/2026/0311/2026031100837_c.pdf), page 1, explicitly corrects 200 to 500. The [5 March HKSCC admission circular](https://www.hkex.com.hk/-/media/HKEX-Market/Services/Circulars-and-Notices/Participant-and-Members-Circulars/HKSCC/2026/ce_HKSCC_SKA_074_2026.pdf), page 1, independently records 500 before listing. Original and correction pages were visually inspected. Minimum application and corrected trading lot therefore both equal 500. There is no need to infer lot size from the minimum tier. The original announcement's typo explains the frozen 200-unit metadata.

The corrected 113-IPO one-lot results equal the former 113-IPO minimum-tier results in economics, but their label is now supported. The previous 112-IPO strict sample remains an exclusion sensitivity. No historical extraction approval was rewritten to authorize changed bytes.

## 3355: prior guarantee inference confirmed by direct disclosure

The original PDF page 16 omits Pool B guarantees from the ballot wording. The [27 March clarification](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032702666.pdf), page 2, explicitly provides all ten guarantees and additional-ballot rules. Every application quantity, applicant count, guarantee, ballot numerator/denominator, extra quantity and printed percentage matches the frozen economic values. The guarantee vector is 100,100,100,200,200,200,200,200,200,300. The ten tiers have 11,492 applicants and allocate 2,000,000 shares, matching Pool B. This conclusion rests on the corrected PDF, rather than a totals-only proof. The original, prior inference and new official relation are preserved separately in [the ten-row comparison](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/3355_official_pool_b.csv).

The Pool A page-15 token `008%` was not addressed in that Pool B clarification. Its interpretation as 0.08% remains an arithmetic/transcription interpretation, not a newly obtained correction. This is the 90,000-share tier, whereas this draft uses the directly disclosed 100-share tier. The source ambiguity therefore does not enter the one-lot calculation; the issuer-wide exclusion is still shown.

## 19 corrected application totals

The quantity and applicant columns were re-read directly from the local PDF layout, using a separate reader from the frozen text parser. All 763 operand pairs match the frozen tiers one for one, with no omitted or duplicate pairs. The exact sum of quantity times applicants agrees with both current workbook values (resolved by header name) and the current master. Applicant totals also agree. Final allocation totals are reconciled using existing tier rules, with 1377's employee-reserved allocation separated; those 19 allocation rules were not independently re-reviewed in this exercise.

Sixteen old formal records explicitly document multiplication of the rounded subscription level by the initial public quantity. Fourteen reproduce the old value to within integer rounding. Two also contain arithmetic inconsistencies in their notes: 6880's stated operands multiply to 824,712,039.20, rather than 824,712,149; 6951's multiply to 2,337,132,385, rather than 2,337,131,310. These two differences must not be explained solely by rounding the disclosed subscription multiple. The new exact totals are supported by the PDF tier operands in all cases.

For 9976, 2,607,800 × 40.32 = 105,146,496, close to the old 105,146,500, but the old record does not document that procedure: rounding is a compatible explanation, not established historical provenance. For 2290 and 1392 the old totals are unsupported by the re-read tiers; the exact original error mechanism remains undocumented. Thus the earlier broad claim of '17 rounding reconstructions and two entry errors' is narrowed to **14 reproducible rounded-ratio reconstructions, two documented formulas with additional arithmetic discrepancies, one compatible explanation and two undocumented error mechanisms**.

{ledger_table}

Every pre-repair formal `col_CO` value differs from the current workbook/master value. `col_CO` is the legacy extraction schema field; the physical workbook column is resolved by its `Public valid applied shares` header, not by Excel letter. {formal_status} The [repair record](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/formal_json_repair/README.md) separates the field repair from whole-payload writeback credentials. This assessment does not fabricate whole-payload approval.

Per-issuer official URLs, source pages, notes and hashes are in [the correction ledger](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/nineteen_applied_totals.csv); the [763-row operands table](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/nineteen_pdf_operands.csv) makes every sum reproducible. These totals are source-verified derivations, not directly printed aggregate counts.

## Research disposition

{exclusions}

Primary one-lot outcomes use tier-specific expected allocations and requested quantities. They do not use the aggregate valid-application total, so changing those totals has no direct arithmetic effect on one-lot profits. Excluding the 19 issuers is a conservative sample-composition sensitivity. All reported samples retain positive mean gross application returns and negative covariance contributions; monetary profits under a chosen fee can still differ. Exclusion differences do not identify an effect of data quality.

New computations are exact expectations using observed prices. No new simulation was run. The [mentor brief](RETAIL_MENTOR_BRIEF_2026-10-03.md) uses gross outcomes as its baseline and hypothetical fees only as sensitivity scenarios.
"""
    (ROOT / "docs/reports/RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md").write_text(assessment)
    (OUT / "README.md").write_text("# Deterministic retail evidence brief\n\n113 corrected one-lot IPOs; cutoff 30 September 2026. No simulation.\n\n"
        "Run `.venv/bin/python tools/audit_retail_sources_2026.py` then `.venv/bin/python analysis/retail_evidence_brief_2026.py` from the root. "
        "Raw source PDFs must be available at the paths in the source manifest.\n\n"
        "[Mentor brief](../../../docs/reports/RETAIL_MENTOR_BRIEF_2026-10-03.md) · "
        "[Evidence assessment](../../../docs/reports/RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md). "
        "CSV returns are decimals; covariance columns ending in `_pp` are percentage points. "
        "The median after-fee profit is the median across IPO expectations, not a simulated portfolio median.\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((EVIDENCE / "source_manifest.json").read_text())
    for relative, expected in manifest["inputs"].items():
        assert sha(ROOT / relative) == expected, f"Source follow-up input changed: {relative}"
    for name, expected in manifest["outputs"].items():
        assert sha(EVIDENCE / name) == expected, f"Source follow-up output changed: {name}"
    tiers = reviewed_tiers(ROOT)
    lots = pd.read_csv(EVIDENCE.parent / "board_lots.csv").set_index("code")
    overlay = pd.read_csv(EVIDENCE / "board_lot_followup.csv")
    assert overlay.code.tolist() == ["2649.HK"] and overlay.board_lot_units.tolist() == [500]
    correction = manifest["sources"][0]
    assert overlay.source_sha256.iloc[0] == correction["sha256"]
    assert sha(ROOT / correction["pdf"]) == correction["sha256"]
    lots.loc["2649.HK", "board_lot_units"] = 500
    panel = select_2026(load_panel()).set_index("Stock Code")
    rows = []
    for code, issuer in panel.iterrows():
        selected = tiers[tiers.code.eq(code) & tiers.applied_shares.eq(lots.loc[code, "board_lot_units"])]
        assert len(selected) == 1, f"{code}: no unique one-lot application tier"
        t = selected.iloc[0]
        expected = t.guaranteed_shares + t.ballot_winners / t.applicants * t.ballot_extra_shares
        p0, p1 = issuer[C["offer"]], issuer["First trading day closing price (HK$)"]
        r = p1 / p0 - 1
        # The stored IR column is rounded to six decimal places.
        assert np.isclose(r, issuer.ir, atol=5e-7)
        capital = t.applied_shares * p0
        profit = expected * (p1 - p0)
        rows.append({"code": code, "cohort": issuer.cohort, "board_lot_units": int(t.applied_shares),
                     "unit": lots.loc[code, "board_lot_unit"], "offer_price": p0, "first_day_close": p1,
                     "initial_return": r, "expected_allotted_units": expected,
                     "application_principal_hkd": capital, "allocation_rate": expected / t.applied_shares,
                     "expected_gross_profit_hkd": profit, "application_return": profit / capital,
                     "source_pdf_page": int(t.pdf_page), "lot_followup": code == "2649.HK"})
    frame = pd.DataFrame(rows)
    assert len(frame) == 113
    assert np.allclose(frame.application_return, frame.allocation_rate * frame.initial_return)
    frame.to_csv(OUT / "one_lot_issuer_results.csv", index=False)
    nineteen = set(pd.read_csv(EVIDENCE / "nineteen_applied_totals.csv").code)
    samples = {
        "corrected_all_113": frame,
        "prior_112_exclude_2649": frame[frame.code.ne("2649.HK")],
        "exclude_3355": frame[frame.code.ne("3355.HK")],
        "exclude_19_total_corrections": frame[~frame.code.isin(nineteen)],
        "exclude_2649_3355_and_19": frame[~frame.code.isin(nineteen | {"2649.HK", "3355.HK"})],
    }
    summaries = pd.DataFrame([summary(x, key) for key, x in samples.items()])
    summaries.to_csv(OUT / "sample_sensitivity.csv", index=False)
    quarters = pd.DataFrame([summary(x, q) for q, x in frame.groupby("cohort")])
    quarters.to_csv(OUT / "quarter_results.csv", index=False)
    fees = []
    for fee in [0, 28, 88, 100]:
        net = frame.expected_gross_profit_hkd - fee
        fees.append({"fee_hkd": fee, "n": len(frame), "mean_expected_profit_hkd": net.mean(),
                     "median_ipo_expected_profit_hkd": net.median(),
                     "mean_application_return_after_fee": (net / frame.application_principal_hkd).mean(),
                     "negative_expected_profit_ipo_share": net.lt(0).mean()})
    pd.DataFrame(fees).to_csv(OUT / "fee_sensitivity.csv", index=False)
    ranked = frame.sort_values("expected_gross_profit_hkd", ascending=False)
    concentration = []
    for removed in [0, 1, 3]:
        remainder = ranked.iloc[removed:]
        record = summary(remainder, f"drop_top_{removed}_gross_profit")
        record["removed_codes"] = ";".join(ranked.iloc[:removed].code)
        record["mean_expected_profit_fee88_hkd"] = remainder.expected_gross_profit_hkd.mean() - 88
        concentration.append(record)
    pd.DataFrame(concentration).to_csv(OUT / "winner_sensitivity.csv", index=False)
    ledger = pd.read_csv(EVIDENCE / "nineteen_applied_totals.csv")
    stale_count = int((~ledger.formal_master_consistent).sum())
    records = [{"item": "2649 board lot / minimum application", "status": "Verified: both 500; original 200 corrected by issuer",
                "remaining_derivation": "None for lot size; original frozen lot metadata remains stale",
                "exclusion_sample": "prior_112_exclude_2649"},
               {"item": "3355 ten Pool B guarantees", "status": "Verified: all ten match official 27 March clarification",
                "remaining_derivation": "Prior inference confirmed; Pool A 008% remains a transcription interpretation, unused in one-lot result",
                "exclusion_sample": "exclude_3355"},
               {"item": "19 valid-application quantity corrections", "status": "Verified: 763 PDF quantity/count pairs; exact sums match current master",
                "remaining_derivation": f"Totals are sums; 14 old formulas reproduce, 2 have arithmetic errors, 9976 rounding compatible only, 2290/1392 cause unrecorded; {stale_count} current formal totals stale",
                "exclusion_sample": "exclude_19_total_corrections"},
               {"item": "Joint exclusion of all flagged issuers", "status": "Conservative sensitivity; different sample composition",
                "remaining_derivation": "No causal interpretation of exclusion difference",
                "exclusion_sample": "exclude_2649_3355_and_19"}]
    evidence_table = pd.DataFrame(records).merge(summaries, left_on="exclusion_sample", right_on="sample", validate="one_to_one")
    evidence_table.to_csv(OUT / "evidence_and_exclusion_results.csv", index=False)
    write_reports(summaries, quarters, fees, concentration, evidence_table)
    inputs = [EVIDENCE / "source_manifest.json", EVIDENCE / "board_lot_followup.csv",
              EVIDENCE / "nineteen_applied_totals.csv", Path(__file__), ROOT / "analysis/research_inputs.py"]
    result_manifest = {"observation_cutoff": "2026-09-30", "sample": "113 actual 2026 listings; corrected one-lot metadata",
                       "method": "Exact allocation expectations and equal-IPO population covariance (denominator N)",
                       "simulation_used": False, "canonical_data_changed": False,
                       "lot_overlay": "2649 only; formal source follow-up is separate from frozen pipeline gate",
                       "inputs": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
                       "outputs": {p.name: sha(p) for p in sorted(OUT.glob("*.csv"))}}
    (OUT / "run_manifest.json").write_text(json.dumps(result_manifest, indent=2) + "\n")
    print(summaries.to_string(index=False))
    print(quarters.to_string(index=False))


if __name__ == "__main__":
    main()
