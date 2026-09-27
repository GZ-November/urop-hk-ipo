# Academic Research Note: Econometric Hypotheses & Identification Strategies Unlocked by the Expanded Hong Kong IPO Panel

> **Author**: Empirical IPO Research Group  
> **Reference**: Lowry, Michaely, and Volkova (2017), *Foundations and Trends® in Finance*; HKEX Listing Rules & SFO Chapter 571W.  
> **Target Dataset**: Hong Kong Main Board IPO Panel (2021–2026 Master Panel + 2026 Q1 Microstructure Core).  

---

## 1. Overview of New Econometric Capabilities

Expanding the dataset across multiple dimensions—from a 38-firm cross-section to a multi-year panel ($N \approx 524$, 2021–2026), supplemented by event-level daily microstructure ($N = 5,489$ trading days), statutory stabilization actions, multi-horizon lockups, and relational investor/syndicate tables—transforms what can be empirically identified.

Researchers can now replace purely descriptive OLS cross-sectional regressions with **quasi-experimental causal designs**, including:
1. **Difference-in-Differences (DiD)** exploiting exogenous statutory reforms;
2. **Regression Discontinuity Designs (RDD)** around statutory eligibility and clawback thresholds;
3. **High-Frequency Event Studies** around price support cliffs and multi-stage unlock dates;
4. **Network and Intermediary Fixed-Effects Models**.

---

## 2. Testable Hypotheses & Econometric Specifications

### Hypothesis 1: The FINI Settlement Shock and Dynamic Information Extraction
- **Supported Literature & Ideas**: Idea 02 (FINI Digitalization & Mechanism A vs B), Idea 08 (Retail Subscription Frenzy), Idea 13 (Margin Financing Cascades); Benveniste and Spindt (1989), Hanley (1993).
- **Institutional Background**: On November 22, 2023, HKEX launched the Fast Interface for New Issuance (FINI), compressing settlement time from $T+5$ to $T+2$. Under $T+5$, retail investors locked up margin capital for nearly a week, incurring substantial HIBOR-linked interest expenses. Under $T+2$, margin borrowing costs plummeted by $\approx 60\%$.
- **Econometric Specification (DiD)**:
  $$\text{Underpricing}_i = \alpha + \beta_1 \text{PostFINI}_i + \beta_2 \text{MechanismB}_i + \beta_3 (\text{PostFINI}_i \times \text{MechanismB}_i) + \gamma \mathbf{X}_i + \varepsilon_i$$
  where $\text{MechanismB}_i$ identifies issuers adopting the flexible 10% clawback ceiling rather than statutory 50% Mechanism A.
- **Empirical Prediction**: FINI reduces retail subscription barriers, amplifying retail cascades in Mechanism A offerings, while Mechanism B dampens retail float expansion, curbing first-day flipping velocity.

---

### Hypothesis 2: The Underwriting Price Stabilization Cliff
- **Supported Literature & Ideas**: Idea 11 (Stabilization Cliff Effect & Delayed Discovery), Idea 05 (Syndicate Networks); Ellis, Michaely, and O'Hara (2000), Aggarwal (2000).
- **Institutional Background**: Under the Securities and Futures (Price Stabilizing) Rules (Cap. 571W), the stabilizing manager has a statutory window of exactly 30 calendar days from the close of the public offering to support the secondary market price up to the offer price.
- **Econometric Specification (Discontinuity Event Study)**:
  $$R_{it} - R_{mt} = \sum_{\tau = -20}^{+20} \delta_\tau \cdot \mathbb{I}(t = \tau) + \beta \text{OverAllocPct}_i + \lambda \text{StabilizationPurchases}_i + \alpha_i + \varepsilon_{it}$$
  where $\tau = 0$ is the official end date of the stabilization period (`stabilization_period_end`).
- **Empirical Prediction**: For IPOs with offer prices near or below day-1 close where stabilizing purchases occurred, there is an immediate, sharp drop in abnormal returns ($\delta_{\tau} < 0$ for $\tau \in [1, 5]$) immediately following the expiry of the 30-day window, demonstrating that underwriting support artificially delays price discovery rather than permanently supporting equilibrium valuation.

---

### Hypothesis 3: The Dual Unlock "Chip Avalanche" Effect
- **Supported Literature & Ideas**: Idea 09 (Dual Unlock Chip Avalanche), Idea 03 (Cornerstone Float Squeeze); Field and Hanka (2001), Brav and Gompers (2003).
- **Institutional Background**: Hong Kong imposes a unique multi-tier lockup structure:
  - Cornerstone investors: 6 months statutory lockup;
  - Controlling shareholders: 6 months absolute lockup + 6 months loss-of-control restriction (Listing Rule 10.07(1));
  - Chapter 18C pathfinders: 12 months (Senior) / 24 months (Controlling).
- **Econometric Specification**:
  $$\text{CAR}[-5, +5]_{ik} = \alpha + \beta_1 \text{LockedPctFloat}_{ik} + \beta_2 \text{CornerstoneIndicator}_{ik} + \beta_3 \text{PreIPOReturn}_{ik} + \gamma \mathbf{X}_i + \varepsilon_{ik}$$
  where $k \in \{\text{Cornerstone 6M}, \text{Controlling 6M}, \text{Controlling 12M}\}$.
- **Empirical Prediction**: Unlock abnormal returns are substantially more negative when the locked tranche represents a larger fraction of free float and when the firm has posted positive run-up returns prior to unlock, consistent with institutional liquidity rebalancing.

---

### Hypothesis 4: Crossover Fund Certification vs. Agency Conflicts
- **Supported Literature & Ideas**: Idea 14 (Crossover Funds Dual Identity), Idea 04 (VC/PE Heterogeneity); Megginson and Weiss (1991), Gompers (1996).
- **Institutional Background**: In several high-profile listings, pre-IPO institutional funds also participate as cornerstone investors in the global offering.
- **Econometric Specification**:
  $$\text{Underpricing}_i = \alpha + \beta_1 \text{CrossoverStake}_i + \beta_2 \text{PureCornerstoneStake}_i + \beta_3 \text{PureVCStake}_i + \gamma \mathbf{X}_i + \varepsilon_i$$
- **Empirical Prediction**: Dual-identity crossover investors reduce information asymmetry (curbing underpricing) more effectively than traditional cornerstones because their pre-IPO diligence provides credible insider certification to uncommitted international placees.

---

### Hypothesis 5: Long-Run Underperformance and Benchmark Contamination
- **Supported Literature & Ideas**: Idea 20 (Long-Run Underperformance & Wealth Relatives); Fama (1998), Lowry, Michaely, and Volkova (2017 Ch 7).
- **Institutional Background**: Traditional Hong Kong IPO studies benchmark returns exclusively against the broad Hang Seng Index (HSI), which is heavily weighted toward mature financials, real estate, and state-owned conglomerates.
- **Econometric Specification**:
  $$\text{WR}_{\text{HSTECH}, i, T} - \text{WR}_{\text{HSI}, i, T} = \alpha + \beta \text{TechIssuerFlag}_i + \gamma \text{FirmAge}_i + \varepsilon_i$$
  across $T \in \{1\text{M}, 3\text{M}, 6\text{M}, 12\text{M}\}$.
- **Empirical Prediction**: The apparent "long-run underperformance" of Hong Kong new economy IPOs is primarily an artifact of benchmark contamination: when evaluated against the Hang Seng TECH Index or matched industry portfolios, abnormal underperformance attenuates or disappears entirely ($\text{WR}_{\text{HSTECH}} \approx 1.00$).

---

## 3. Summary of Econometric Identifiers Populated

| Econometric Variable | Theoretical Construct | Operational Definition in Deliverable Tables |
| :--- | :--- | :--- |
| `fini_regime` | Regulatory policy shock | `PRE_FINI` ($< 2023-11-22$) vs. `POST_FINI` ($\ge 2023-11-22$) in `issuer_master.csv` |
| `cliff_return_m5_p5` | Underwriting price support cliff | Cumulative return $[-5, +5]$ trading days around Sec 9(2) end date in `stabilization_events.csv` |
| `volume_decay_post_stab` | Aftermarket liquidity withdrawal | Ratio of turnover $[0, +20]$ post-stabilization to turnover $[-20, 0]$ pre-stabilization |
| `car_m20_p20` | Information leakage & selling anticipation | Cumulative Abnormal Return $[-20, +20]$ trading days around unlock in `lockup_events.csv` |
| `amihud_illiq` | Microstructure price impact | $(|R_{it}| / \text{Turnover}_{it}) \times 10^6$ in `daily_market_panel.csv` |
| `wr_hsi` vs. `wr_hstech` | Benchmark contamination test | Wealth relatives across 9 standardized event horizons in `horizon_summary.csv` |
| `commercial_bank_affiliate` | Intermediary lending certification | Indicator for bank-affiliated sponsor in `underwriter_relational.csv` |
| `crossover_flag` | Institutional dual identity | Indicator for investor active in both pre-IPO rounds and cornerstone tranche in `investor_relational.csv` |
