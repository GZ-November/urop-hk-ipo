# From theory to testable predictions

Use this map to ground a hypothesis in a mechanism and to pick proxies whose
predicted sign distinguishes *between* theories. For the full literature
synthesis, the `lowry-ipo-research` skill (Lowry, Michaely & Volkova 2017)
covers each model in depth; Ljungqvist (2007, Handbook of Corporate Finance)
and Ritter & Welch (2002, JF) are the standard surveys.

## Underpricing theories

| Theory | Mechanism | Testable prediction | Typical proxies | Distinguishing test |
|---|---|---|---|---|
| Winner's curse (Rock 1986) | Uninformed investors get more of bad issues; underpricing keeps them in | IR ↑ with ex-ante uncertainty; uninformed allocation-weighted returns ≈ 0 | Range width, age, size, pre-revenue status, IPO volatility | Allocation-adjusted retail returns (HK allotment tables make this feasible: Koh & Walter 1989 did it for Singapore) |
| Information revelation / bookbuilding (Benveniste & Spindt 1989) | Underpricing rewards institutions for revealing demand | Partial adjustment: IR ↑ with positive price revision | Price revision, placing oversubscription | Asymmetry: upward revisions only partially passed on (Hanley 1993) |
| Public information / prospect theory (Loughran & Ritter 2002) | Issuers "sum" wealth gain and dilution loss; underwriters exploit | Market return during bookbuilding predicts revision *and* IR | Pre-pricing index return | Public info should be fully incorporated under BS89 |
| Signaling (Allen & Faulhaber 1989; Welch 1989; Grinblatt & Hwang 1989) | Good firms underprice to sell later at higher prices | IR predicts subsequent SEOs / insider sales | Follow-on issue within 3 yrs, insider retention | Weak empirical support (Jegadeesh, Weinstein & Welch 1993) |
| Certification / reputation (Booth & Smith 1986; Carter & Manaster 1990; Megginson & Weiss 1991) | Reputable intermediaries certify quality | Reputable sponsor/VC → lower IR (in 1980s US); sign reversed in the 1990s (Loughran & Ritter 2004) | Sponsor market share, VC backing, auditor | Control for endogenous matching |
| Agency / spinning / allocation favours (Loughran & Ritter 2004; Reuter 2006; Jenkinson, Jones & Suntheim 2018) | Underwriters allocate underpriced shares to favoured clients | IR ↑ with bank's commission-generating clients; allocation concentration | Placee concentration, connected placees | HK allotment disclosures of top placees |
| Market sentiment (Ljungqvist, Nanda & Singh 2006; Derrien 2005; Cornelli, Goldreich & Ljungqvist 2006) | Optimistic retail pay above fundamentals; issuer leaves money to regulars | IR ↑ with retail demand and grey-market prices; long-run reversal | Retail oversubscription, margin financing, grey-market return | IR high *and* subsequent BHAR negative for high-sentiment IPOs |
| Lawsuit avoidance (Tinic 1988) | Underpricing as insurance against litigation | IR ↑ with legal exposure | Legal regime changes | Weak outside US |
| Price support (Ruud 1993; Aggarwal 2000) | Stabilization truncates the left tail | Fewer first-day returns just below zero | Greenshoe exercise, stabilization actions | Distribution mass at IR = 0 |
| Ownership and control (Brennan & Franks 1997) | Underpricing creates oversubscription → dispersed ownership | IR ↑ where insiders retain control | Dual-class/WVR, retained stake | Placee dispersion |
| Cornerstone certification (HK/Asia) | Committed anchors signal quality and reduce uncertainty | Cornerstone share ↓ uncertainty; effect on IR ambiguous (certification lowers IR; demand signal raises it) | Cornerstone %, SOE cornerstone, reputable-investor indicator | Endogenous: use pre-determined cornerstone supply or event-based variation |

## Long-run performance theories

| Theory | Prediction | Test |
|---|---|---|
| Windows of opportunity / overoptimism (Ritter 1991; Loughran & Ritter 1995) | IPOs underperform, more so in hot periods and for young firms | BHAR by cohort volume; calendar-time α |
| Risk / characteristics (Brav & Gompers 1997; Brav, Geczy & Gompers 2000) | Underperformance concentrated in small, low-B/M firms; disappears with size/BM benchmarks | Compare market-adjusted vs matched-firm BHARs |
| Divergence of opinion (Miller 1977) | High dispersion + short-sale constraints → high IR, low long-run return | Interaction of dispersion proxies with IR on BHAR |
| Lockup overhang (Field & Hanka 2001) | Negative abnormal return and volume spike at lockup expiry | CAR around +180 days (HK cornerstones) |

## Writing the hypothesis

A good hypothesis statement names the mechanism, the direction, the proxy and
the competing explanation:

> H1 (certification). If cornerstone commitments certify issuer quality, a
> larger cornerstone share reduces valuation uncertainty and therefore the
> initial return, holding demand constant. The competing demand-signal channel
> predicts the opposite sign; we separate them by conditioning on pre-pricing
> retail demand (margin financing) and by testing the effect on range width.

Then list the threats: reverse causality (high expected IR attracts
cornerstones), omitted quality, and mechanical links (cornerstone shares reduce
the free float and can raise day-one prices through limited supply).
