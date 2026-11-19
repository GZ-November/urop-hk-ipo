"""
run_intermediaries_and_ctp_econometrics.py

Executes econometric analyses for Section E6 of the Hong Kong IPO Overview:
1. 33-Year Geopolitical Power Shift in HK Investment Banking (1994-2026):
   - Lead sponsor shares across 4 epochs and annual series (PRC vs Bulge Bracket vs HK/Asia).
   - Syndicate bloat: mean n_sponsors, n_bookrunners, n_global_coords across time.
   - Fintech broker penetration.
2. Megginson-Weiss Sponsor Prestige & Big-4 Auditor Certification regressions:
   - Initial Return log(1+IR), 1Y BHAR, Day-1 Break, Severe Distress (1Y BHAR <= -50%).
3. Mitchell & Stafford (2000) / Fama-French Calendar-Time Portfolio (CTP) Regressions:
   - 12M & 36M Main Board and GEM CTP Alphas against HSI and SMB proxy.
   - Newey-West HAC t-statistics.

Outputs tables to analysis/out/overview_extensions/:
- ext_table8_intermediary_power_shift.csv
- ext_table9_sponsor_prestige_and_auditor_regressions.csv
- ext_table10_calendar_time_portfolio_alphas.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

BASE_DIR = Path(__file__).resolve().parent.parent
EXT_DIR = BASE_DIR / "analysis" / "out" / "overview_extensions"
PANEL_CSV = EXT_DIR / "clean_33y_intermediaries_greenshoe.csv"
CTP_CSV = EXT_DIR / "clean_monthly_ctp_portfolios_1994_2026.csv"

def run_power_shift(df: pd.DataFrame) -> pd.DataFrame:
    print("--- 1. Computing 33-Year Intermediary Power Shift ---")
    mb = df[df["board"] == "Main Board"].copy()
    
    # Define epochs
    # Epoch I: 1994-1999, Epoch II: 2000-2007, Epoch III: 2008-2017, Epoch IV: 2018-2022, Epoch V: 2023-2026
    def get_epoch(yr):
        if yr <= 1999: return "Epoch I (1994-1999)"
        elif yr <= 2007: return "Epoch II (2000-2007)"
        elif yr <= 2017: return "Epoch III (2008-2017)"
        elif yr <= 2022: return "Epoch IV (2018-2022)"
        else: return "Epoch V (2023-2026)"
        
    mb["epoch_5"] = mb["cohort_year"].apply(get_epoch)
    
    rows = []
    for ep, sub in mb.groupby("epoch_5"):
        n = len(sub)
        prc_s = (sub["lead_sponsor_group"] == "PRC_Mainland_IB").mean() * 100
        bb_s = (sub["lead_sponsor_group"] == "US_EU_Bulge_Bracket").mean() * 100
        hk_s = (sub["lead_sponsor_group"] == "HK_British_Legacy_and_Asia").mean() * 100
        
        # Syndicate bloat
        n_sp = sub["n_sponsors"].mean()
        n_br = sub["n_bookrunners"].mean()
        n_gc = sub["n_global_coords"].mean()
        fintech = sub["has_fintech_retail_broker"].mean() * 100
        big4 = (sub["auditor_tier"] == "Big4_Big5").mean() * 100
        
        rows.append({
            "Epoch": ep,
            "N_MB": n,
            "PRC_Lead_Sponsor_Pct": round(prc_s, 2),
            "Bulge_Bracket_Lead_Pct": round(bb_s, 2),
            "HK_British_Lead_Pct": round(hk_s, 2),
            "Mean_Sponsors": round(n_sp, 2),
            "Mean_Bookrunners": round(n_br, 2),
            "Mean_Global_Coords": round(n_gc, 2) if not np.isnan(n_gc) else np.nan,
            "Fintech_Broker_Pct": round(fintech, 2),
            "Big4_Auditor_Pct": round(big4, 2),
        })
        
    # Full MB
    n_all = len(mb)
    rows.append({
        "Epoch": "All Main Board (1994-2026)",
        "N_MB": n_all,
        "PRC_Lead_Sponsor_Pct": round((mb["lead_sponsor_group"] == "PRC_Mainland_IB").mean() * 100, 2),
        "Bulge_Bracket_Lead_Pct": round((mb["lead_sponsor_group"] == "US_EU_Bulge_Bracket").mean() * 100, 2),
        "HK_British_Lead_Pct": round((mb["lead_sponsor_group"] == "HK_British_Legacy_and_Asia").mean() * 100, 2),
        "Mean_Sponsors": round(mb["n_sponsors"].mean(), 2),
        "Mean_Bookrunners": round(mb["n_bookrunners"].mean(), 2),
        "Mean_Global_Coords": round(mb["n_global_coords"].mean(), 2),
        "Fintech_Broker_Pct": round(mb["has_fintech_retail_broker"].mean() * 100, 2),
        "Big4_Auditor_Pct": round((mb["auditor_tier"] == "Big4_Big5").mean() * 100, 2),
    })
    
    res_df = pd.DataFrame(rows)
    out_path = EXT_DIR / "ext_table8_intermediary_power_shift.csv"
    res_df.to_csv(out_path, index=False)
    print(f"Saved {out_path}")
    print(res_df.to_string(index=False))
    return res_df

def run_sponsor_regressions(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- 2. Estimating Sponsor Prestige & Certification Regressions ---")
    mb = df[df["board"] == "Main Board"].copy()
    
    # Key variables
    mb["log_proceeds"] = np.log(pd.to_numeric(mb["funds_raised_total_hkd"], errors="coerce") / 1e6).replace([np.inf, -np.inf], np.nan)
    mb["ir_raw"] = pd.to_numeric(mb["ir_close_pct"], errors="coerce") / 100.0
    mb["log_1_plus_ir"] = np.log(1.0 + mb["ir_raw"].clip(lower=-0.99))
    mb["day1_break"] = (mb["ir_raw"] < 0).astype(int)
    mb["bhar_1y"] = pd.to_numeric(mb["after_bhar_1y_pct"], errors="coerce") / 100.0
    mb["severe_distress_1y"] = (mb["bhar_1y"] <= -0.50).astype(int)
    
    mb["rep_lag3y"] = pd.to_numeric(mb["sponsor_rep_lag3y_proceeds_share"], errors="coerce")
    mb["is_big4"] = (mb["auditor_tier"] == "Big4_Big5").astype(int)
    mb["is_prc_sponsor"] = (mb["lead_sponsor_group"] == "PRC_Mainland_IB").astype(int)
    mb["is_bb_sponsor"] = (mb["lead_sponsor_group"] == "US_EU_Bulge_Bracket").astype(int)
    mb["is_h_share"] = (mb["is_prc_joint_stock"] == 1).astype(int)
    
    # Models:
    # Model 1: log(1 + IR) on rep_lag3y + is_big4 + log_proceeds + is_h_share
    # Model 2: Day-1 Break (Linear Probability)
    # Model 3: 1Y BHAR
    # Model 4: Severe Distress 1Y (<= -50%)
    
    dep_vars = [
        ("log_1_plus_ir", "Log(1 + Day-1 IR)"),
        ("day1_break", "Day-1 Break Indicator"),
        ("bhar_1y", "1-Year Aftermarket BHAR"),
        ("severe_distress_1y", "1Y Severe Distress (BHAR <= -50%)")
    ]
    
    results = []
    
    for dep, label in dep_vars:
        sub = mb.dropna(subset=[dep, "rep_lag3y", "is_big4", "log_proceeds", "is_h_share"]).copy()
        X = sm.add_constant(sub[["rep_lag3y", "is_big4", "log_proceeds", "is_h_share", "is_bb_sponsor", "is_prc_sponsor"]])
        y = sub[dep]
        
        # OLS with HC3 robust standard errors
        mod = sm.OLS(y, X).fit(cov_type="HC3")
        
        row = {
            "Dependent_Variable": label,
            "N": int(mod.nobs),
            "R2": round(mod.rsquared, 4),
            "Coef_Sponsor_Rep": round(mod.params["rep_lag3y"], 4),
            "t_Sponsor_Rep": round(mod.tvalues["rep_lag3y"], 2),
            "Coef_Big4_Auditor": round(mod.params["is_big4"], 4),
            "t_Big4_Auditor": round(mod.tvalues["is_big4"], 2),
            "Coef_Log_Proceeds": round(mod.params["log_proceeds"], 4),
            "t_Log_Proceeds": round(mod.tvalues["log_proceeds"], 2),
            "Coef_H_Share": round(mod.params["is_h_share"], 4),
            "t_H_Share": round(mod.tvalues["is_h_share"], 2),
            "Coef_Bulge_Bracket": round(mod.params["is_bb_sponsor"], 4),
            "t_Bulge_Bracket": round(mod.tvalues["is_bb_sponsor"], 2),
            "Coef_PRC_IB": round(mod.params["is_prc_sponsor"], 4),
            "t_PRC_IB": round(mod.tvalues["is_prc_sponsor"], 2),
        }
        results.append(row)
        
    res_df = pd.DataFrame(results)
    out_path = EXT_DIR / "ext_table9_sponsor_prestige_and_auditor_regressions.csv"
    res_df.to_csv(out_path, index=False)
    print(f"Saved {out_path}")
    print(res_df.to_string(index=False))
    return res_df

def run_ctp_regressions(ctp: pd.DataFrame) -> pd.DataFrame:
    print("\n--- 3. Estimating Mitchell & Stafford (2000) Calendar-Time Portfolio Alphas ---")
    
    # Portfolio series to analyze:
    # 1. Main Board 12M EW
    # 2. Main Board 12M VW
    # 3. Main Board 36M EW
    # 4. Main Board 36M VW
    # 5. GEM 12M EW
    # 6. GEM 36M EW
    
    portfolios = [
        ("ctp_12m_mb_ew_ret", "MB 12M Equal-Weighted"),
        ("ctp_12m_mb_vw_ret", "MB 12M Value-Weighted"),
        ("ctp_36m_mb_ew_ret", "MB 36M Equal-Weighted"),
        ("ctp_36m_mb_vw_ret", "MB 36M Value-Weighted"),
        ("ctp_12m_gem_ew_ret", "GEM 12M Equal-Weighted"),
        ("ctp_36m_gem_ew_ret", "GEM 36M Equal-Weighted"),
    ]
    
    rows = []
    
    for col, name in portfolios:
        sub = ctp.dropna(subset=[col, "hsi_monthly_return_pct", "hk_smb_proxy_pct"]).copy()
        
        # 1-Factor CAPM Model: R_p,t = alpha + beta * R_m,t + e_t
        y = sub[col]
        X1 = sm.add_constant(sub["hsi_monthly_return_pct"])
        
        # Newey-West HAC with 6 lags
        mod1 = sm.OLS(y, X1).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        
        # 2-Factor Model: R_p,t = alpha + beta_m * R_m,t + s * SMB_t + e_t
        X2 = sm.add_constant(sub[["hsi_monthly_return_pct", "hk_smb_proxy_pct"]])
        mod2 = sm.OLS(y, X2).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        
        rows.append({
            "Portfolio": name,
            "Months_T": int(mod2.nobs),
            "Mean_Monthly_Ret_Pct": round(sub[col].mean(), 2),
            "CAPM_Alpha_Mo_Pct": round(mod1.params["const"], 3),
            "CAPM_t_NW": round(mod1.tvalues["const"], 2),
            "CAPM_Beta_HSI": round(mod1.params["hsi_monthly_return_pct"], 3),
            "TwoFactor_Alpha_Mo_Pct": round(mod2.params["const"], 3),
            "TwoFactor_t_NW": round(mod2.tvalues["const"], 2),
            "TwoFactor_Beta_HSI": round(mod2.params["hsi_monthly_return_pct"], 3),
            "TwoFactor_Beta_SMB": round(mod2.params["hk_smb_proxy_pct"], 3),
            "TwoFactor_t_SMB": round(mod2.tvalues["hk_smb_proxy_pct"], 2),
            "TwoFactor_R2": round(mod2.rsquared, 4),
        })
        
    res_df = pd.DataFrame(rows)
    out_path = EXT_DIR / "ext_table10_calendar_time_portfolio_alphas.csv"
    res_df.to_csv(out_path, index=False)
    print(f"Saved {out_path}")
    print(res_df.to_string(index=False))
    return res_df

def main():
    print("Loading data...")
    df = pd.read_csv(PANEL_CSV, low_memory=False)
    ctp = pd.read_csv(CTP_CSV, low_memory=False)
    
    run_power_shift(df)
    run_sponsor_regressions(df)
    run_ctp_regressions(ctp)
    print("\nAll econometric analyses successfully finished!")

if __name__ == "__main__":
    main()
