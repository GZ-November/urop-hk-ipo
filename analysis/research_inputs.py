"""Shared issuer-cohort inputs for the existing 2026 research scripts.

This module owns CSV/registry interpretation, missing-value semantics, cohort
selection and the shared regression frames. It imports no report, plotting or
estimation modules. Model specifications and complete-case estimation samples
remain the responsibility of each study.

New research can use select_2026(load_panel()) and the smallest applicable
prepare_* frame. Selection remains explicit: historical rows stay in storage.
The report scripts re-export their former input names for compatibility.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]


MASTER = ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"


ROUTE_ORDER = ["18A biotech", "18C specialist tech", "A+H (19A)", "Conventional"]


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


def load_panel(path: Path = MASTER) -> pd.DataFrame:
    """Interpret master observations and add shared issuer-level research measures."""
    df = pd.read_csv(path, low_memory=False).copy()
    registry = yaml.safe_load((ROOT / "pipeline/registry/HKIPO_Variable_Registry.yaml").read_text(encoding="utf-8"))
    numeric = [v["header"] for v in registry["variables"] if v["dtype"] in {"numeric", "boolean"}]
    converted = {column: pd.to_numeric(df[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
                 for column in [*numeric, "sponsor_reputation_tier"] if column in df}
    df = pd.concat([df.drop(columns=list(converted)), pd.DataFrame(converted, index=df.index)], axis=1)
    df["cohort"] = df["cohort"].astype(str)
    df["ir"] = df[C["ir"]]
    df["listing_date"] = pd.to_datetime(df[C["list_date"]], errors="coerce")
    df["month"] = df["listing_date"].dt.to_period("M")
    df["gross_proceeds"] = df[C["funds_hk"]] + df[C["funds_int"]]
    # Base-deal proceeds match the share base of money left on the table.
    df["base_proceeds"] = df[C["offer"]] * df[C["base_shares"]]
    df["loss_y1"] = (df[C["profit_y1"]] < 0).astype(float).where(df[C["profit_y1"]].notna())
    ah_text = df[C["route_text"]].astype("string").str.contains(r"other listed shares|A\+H", case=False, na=False)
    df["ah_true"] = df[C["ah"]].where(df[C["ah"]].isin([0, 1]))
    df.loc[ah_text, "ah_true"] = 1.0
    df["route"] = np.select(
        [df[C["c18a"]] == 1, df[C["c18c"]] == 1, df["ah_true"] == 1,
         (df[C["c18a"]] == 0) & (df[C["c18c"]] == 0) & (df["ah_true"] == 0)],
        ROUTE_ORDER,
        default="Unknown",
    )
    return df


def select_2026(df: pd.DataFrame) -> pd.DataFrame:
    """Select by actual listing year; reject cohort/date conflicts and duplicates."""
    year = df["listing_date"].dt.year
    cohort_2026 = df["cohort"].str.startswith("2026")
    if (cohort_2026 & ~year.eq(2026)).any() or (year.eq(2026) & ~cohort_2026).any():
        raise ValueError("2026 cohort labels must agree with observed listing dates")
    selected = df.loc[year.eq(2026)].copy()
    if selected["Stock Code"].duplicated().any():
        raise ValueError("Duplicate issuer stock codes in the 2026 analysis sample")
    if selected.empty:
        raise ValueError("No observed 2026 listings in the master panel")
    return selected


EXTENDED_HORIZONS = {
    "Day 5": ("Day-5 BHR from Day-1 close (%)", "Day-5 wealth relative vs HSI"),
    "Day 20": ("Day-20 BHR from Day-1 close (%)", "Day-20 wealth relative vs HSI"),
    "3 months": ("3-month BHR from Day-1 close (%)", "3-month wealth relative vs HSI"),
}


FINAL_GLOBAL_SHARES = "Final global offering shares (before over-allotment)"


def prepare_regression(y26: pd.DataFrame) -> pd.DataFrame:
    """Build the regression frame from the 2026 panel rows."""
    d = pd.DataFrame(index=y26.index)
    d["code"] = y26["Stock Code"]
    d["cohort"] = y26["cohort"]
    d["month"] = y26["month"].astype("string").where(y26["month"].notna())
    d["ir"] = y26["ir"]
    d["y"] = np.log1p(y26["ir"].where(y26["ir"] > -1))
    d["lage"] = np.log(y26[C["age"]].where(y26[C["age"]] > 0))
    d["lproc"] = np.log(y26["base_proceeds"].where(y26["base_proceeds"] > 0) / 1e9)
    d["ah"] = y26["ah_true"]
    d["vc"] = y26[C["vc"]].where(y26[C["vc"]].isin([0, 1]))
    d["tier1"] = (y26["sponsor_reputation_tier"] == 1).astype(float).where(y26["sponsor_reputation_tier"].isin([1, 2, 3]))
    d["corner"] = y26[C["corner"]]
    d["hsi"] = y26["HSI return over 20 trading days before prospectus (%)"]
    d["n90"] = y26["HK ordinary IPO count in 90 calendar days before prospectus"]
    d["lsub"] = np.log(y26[C["sub"]].where(y26[C["sub"]] > 0))
    d["hot"] = (y26["listing_date"].dt.year.eq(2026) & y26["listing_date"].dt.month.between(4, 6)).astype(float).where(y26["listing_date"].notna())
    d["q2"] = (y26["cohort"] == "2026Q2").astype(float)
    d["q3"] = (y26["cohort"] == "2026Q3").astype(float)
    return d


def prior_mean_ir(listing: pd.Series, ir: pd.Series, cutoff: pd.Series, days: int = 30, min_deals: int = 3) -> pd.Series:
    """Mean IR of 2026 deals already listed in [cutoff - days, cutoff): information available at the cutoff.

    A deal never counts itself or later listings, so the regressor has no look-ahead."""
    out = []
    for cut in cutoff:
        window = (listing < cut) & (listing >= cut - pd.Timedelta(days=days))
        out.append(ir[window].mean() if window.sum() >= min_deals else np.nan)
    return pd.Series(out, index=cutoff.index)


def subscription_overlap(start: pd.Series, end: pd.Series) -> pd.Series:
    """Number of other deals whose subscription window overlaps this deal's window."""
    return pd.Series([int(((start <= e) & (end >= s)).sum()) - 1 for s, e in zip(start, end)], index=start.index)


def prepare_extended(y26: pd.DataFrame) -> pd.DataFrame:
    """Add shared demand and timing variables; sort by listing date and issuer code."""
    d = prepare_regression(y26)
    d["ld"] = y26["listing_date"]
    start = pd.to_datetime(y26["Subscription opening date"], errors="coerce")
    end = pd.to_datetime(y26["Subscription closing date"], errors="coerce")
    d["prior_ir"] = prior_mean_ir(d["ld"], d["ir"], start)
    d["conc"] = subscription_overlap(start, end)
    d["sameday"] = d.groupby("ld")["code"].transform("count") - 1
    d["mech"] = y26["Offer mechanism"]
    d["mechA"] = (d["mech"] == "Mechanism A").astype(float).where(d["mech"].notna())
    d["r18a"] = (y26["route"] == "18A biotech").astype(float).where(y26["route"] != "Unknown")
    d["r18c"] = (y26["route"] == "18C specialist tech").astype(float).where(y26["route"] != "Unknown")
    d["fixed"] = (y26[C["pricing"]] == "Fixed price").astype(float)
    d["lapp"] = np.log(y26["Public applicants"].where(y26["Public applicants"] > 0))
    shares_value = y26["Public valid applied shares"] * y26[C["offer"]] / y26["Public applicants"]
    d["lavg"] = np.log(shares_value.where(shares_value > 0))
    d["stab"] = y26["Stabilization purchases occurred"]
    d["greenshoe"] = y26["Greenshoe exercise rate (%)"]
    for name, (bhr, wr) in EXTENDED_HORIZONS.items():
        d[f"bhr_{name}"] = y26[bhr]
        d[f"wr_{name}"] = y26[wr]
    return d.sort_values(["ld", "code"]).reset_index(drop=True)


def prepare_academic(y26: pd.DataFrame) -> pd.DataFrame:
    """Add allocation, fee and contractual-event inputs, matched by issuer code."""
    d = prepare_extended(y26)
    extra = pd.DataFrame({
        "code": y26["Stock Code"],
        "base_shares": y26[FINAL_GLOBAL_SHARES],
        "retail_shares": y26["Final public offer shares"],
        "corner_shares": y26[C["corner"]] * y26[FINAL_GLOBAL_SHARES],
        "offer": y26[C["offer"]],
        "close1": y26["First trading day closing price (HK$)"],
        "applied": y26["Public valid applied shares"],
        "applicants": y26["Public applicants"],
        "gross": y26["gross_proceeds"],
        "fee": (y26["Underwriting Commission (% of fund raised HK (a)"] * y26[C["funds_hk"]]
                + y26["Underwriting Commission (% of fund raised Int.(b)"] * y26[C["funds_int"]]),
        "fee_rate_hk": y26["Underwriting Commission (% of fund raised HK (a)"],
        "mlot": y26[C["mlot"]],
        "lockup_date": pd.to_datetime(y26["Earliest cornerstone unlock date (dd/mm/yy)"], errors="coerce").fillna(
            pd.to_datetime(y26["Controlling shareholder 6-month disposal lockup expiry date"], errors="coerce")),
        "stab_end": pd.to_datetime(y26["Stabilization period end date"], errors="coerce"),
        "range_min": y26["Minimum Offer Price"],
        "range_max": y26["Maximum Offer Price"],
        "revision": y26["Filing price revision (%)"],
        "sponsor": y26["Sponsor(s)"].astype("string").str.split("/").str[0].str.replace(r"\s+", " ", regex=True).str.strip(),
    })
    return d.merge(extra, on="code", how="left")
