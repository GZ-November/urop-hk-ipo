"""Existing exploratory 2026 underpricing specifications and common-sample policy."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class Var:
    name: str
    label: str
    block: str
    sign: str        # predicted sign: "+", "-" or "+/-"
    theory: str
    definition: str


VARS = [
    Var("lage", "ln firm age", "uncertainty", "-",
        "Beatty & Ritter (1986): older firms have more track record",
        "ln(years from incorporation to listing)"),
    Var("lproc", "ln offer size", "uncertainty", "-",
        "Ritter (1984); Beatty & Ritter (1986): size proxies for information available",
        "ln(offer price x base offer shares, HK$bn), before over-allotment"),
    Var("ah", "A+H issuer", "uncertainty", "-",
        "Rock (1986): a public A-share price removes much of the information asymmetry",
        "1 if the issuer already trades on the A-share market"),
    Var("vc", "VC/PE-backed", "certification", "+/-",
        "Megginson & Weiss (1991) certification (-) vs Gompers (1996), Lee & Wahal (2004) (+)",
        "1 if any pre-IPO VC or PE investor"),
    Var("tier1", "Top-tier sponsor", "certification", "+/-",
        "Carter & Manaster (1990) (-) vs Hoberg (2007): top banks underprice more (+)",
        "1 if the best sponsor is tier 1 of the 2025 HK underwriter ranking"),
    Var("corner", "Cornerstone allocation", "certification", "+/-",
        "Anchor certification (-) vs smaller float and demand signal (+); see Module C",
        "Final cornerstone allocation, share of base offer"),
    Var("hsi", "HSI return, prior 20 days", "market", "+",
        "Lowry & Schwert (2002): market momentum passes into initial returns",
        "HSI return over the 20 trading days before the prospectus"),
    Var("n90", "IPO count, prior 90 days", "market", "+/-",
        "Sentiment and volume (+) vs underwriter capacity and supply crowding (-)",
        "HK ordinary IPOs in the 90 days before the prospectus"),
    Var("hot", "April-June hot window", "time", "+",
        "2026 research plan: control for the observed April-June hot window",
        "1 if listing occurs in April-June 2026; exploratory time control"),
    Var("lsub", "ln subscription ratio", "demand", "+",
        "Rock (1986), Welch (1992): retail demand; endogenous, descriptive only",
        "ln(public offer subscription multiple)"),
]
V = {v.name: v for v in VARS}
BLOCK_VARS = {b: [v.name for v in VARS if v.block == b] for b in ("uncertainty", "certification", "market", "demand")}

MODELS = {
    "M1": BLOCK_VARS["uncertainty"] + ["hot"],
    "M2": BLOCK_VARS["uncertainty"] + BLOCK_VARS["certification"] + ["hot"],
    "M3": BLOCK_VARS["uncertainty"] + BLOCK_VARS["certification"] + BLOCK_VARS["market"] + ["hot"],
}
MODELS["M4"] = MODELS["M3"] + BLOCK_VARS["demand"]
BASELINE = "M3"
BLOCK_LABEL = {"uncertainty": "Uncertainty", "certification": "Certification", "market": "Market conditions", "time": "Time control"}


def estimation_sample(d: pd.DataFrame) -> pd.DataFrame:
    """Use one finite complete-case sample for all nested models and inference."""
    columns = list(dict.fromkeys(["y", "code", "month", *MODELS["M4"]]))
    return d.replace([np.inf, -np.inf], np.nan).dropna(subset=columns).copy()

