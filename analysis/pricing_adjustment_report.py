"""Generate a compact English LaTeX report from saved study output."""
from pathlib import Path
import numpy as np
import pandas as pd

from research_inputs import ROOT

OUT = ROOT/'analysis/out/pricing_adjustment'
REPORT = ROOT/'docs/reports/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.tex'


def pct(x, digits=2):
    return f'{100*x:.{digits}f}'


def escape(value):
    return str(value).replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')


def table(number, title, headers, rows, note='', widths=None):
    layout = widths or ('X'+'r'*(len(headers)-1))
    head = ' & '.join(r'\textbf{'+escape(x)+'}' for x in headers)+r' \\\midrule'
    body = '\n'.join(' & '.join(escape(x) for x in row)+r' \\' for row in rows)
    return (rf'\par\addvspace{{5pt}}\textbf{{Table {number}. {title}}}\par\nobreak\vspace{{2pt}}'+'\n'
            +r'{\small\renewcommand{\arraystretch}{1.12}\begin{tabularx}{\textwidth}{@{}'+layout+r'@{}}\toprule'+'\n'
            +head+'\n'+body+'\n'+r'\bottomrule\end{tabularx}}\par\addvspace{3pt}'+'\n'
            +r'{\footnotesize '+note+r'}\par'+'\n')


def write_report(d, regressions, margin, rolling):
    groups = pd.read_csv(OUT/'group_statistics.csv')
    sensitivity = pd.read_csv(OUT/'range_sensitivity.csv')
    identity = pd.read_csv(OUT/'midpoint_identity.csv').set_index('outcome')
    selected = regressions[regressions.model.eq('quarter_controls')].set_index('outcome')
    controlled_margin = margin[margin.model.eq('margin_and_launch_size')].set_index('outcome')
    z = d[d.price_status.eq('two_sided_range')]
    full_apr = d.application_return.mean()
    ceiling_apr = d.ceiling_principal_return.mean()
    range_close = selected.loc['log_close']
    stage_identity_error = abs(range_close.coefficient-selected.loc['log_opening','coefficient']
                               -selected.loc['log_intraday','coefficient'])
    assert stage_identity_error < 1e-10
    names = {'two_sided_range':'Two-sided price range', 'equal_endpoints':'Equal price endpoints',
             'undisclosed_lower_bound':'Lower bound not disclosed'}
    rows = []
    for key in names:
        g = groups[(groups.grouping=='price_status') & groups.group.eq(key)].iloc[0]
        rows.append([names[key],int(g.n),pct(g.mean_close),pct(g.median_close),
                     pct(g.mean_application_return),pct(g.mean_ceiling_principal_return)])
    t1 = table(1,'Coverage and returns',['Price evidence','N','Mean IR','Median IR','APR','Ceiling APR'],rows,
               'All return columns are percent. IR uses the offer price and first-day close. '
               'APR uses requested units at the final offer price. Ceiling APR uses the published maximum price. '
               'These are allocation expectations, not observed account returns.')
    rows = []
    for key in ['At low','Inside range','At high']:
        g = groups[(groups.grouping=='pricing_group') & groups.group.eq(key)].iloc[0]
        rows.append([key,int(g.n),pct(g.mean_close),pct(g.mean_opening),pct(g.mean_application_return),
                     pct(g.median_application_return)])
    t2 = table(2,'Within the 43 range-priced offers',['Final position','N','Mean IR','Mean open','Mean APR','Median APR'],rows,
               'No offer in this range sample is outside its recorded range. Group means are descriptive. '
               'Mean intraday return is not the difference between mean close and opening returns.')
    labels = {'log_close':'Log offer-to-close', 'log_opening':'Log offer-to-open',
              'log_intraday':'Log open-to-close', 'allocation_rate':'Allocation fraction',
              'application_return':'Application return', 'log_mair_subscription':'Log HSI-adjusted close',
              'close':'Raw offer-to-close'}
    rows = []
    for key,label in labels.items():
        r = selected.loc[key]
        rows.append([label,f'{10*r.coefficient:.3f}',f'{10*r.hc3_se:.3f}',
                     f'{r.hc3_p:.3f}',f'{r.wild_cluster_p:.3f}',f'{r.holm_wild_p:.3f}'])
    t3 = table(3,'Common-sample regressions with quarter controls',
               ['Outcome','Slope','HC3 SE','HC3 p','WCR p','Holm WCR p'],rows,
               'N=43, nine listing-month clusters, intercept and Q2/Q3 indicators in every column. '
               'Slope and SE are scaled for a +10 percentage point revision: log points for log outcomes, '
               'percentage points for fractions and raw returns. HC3 uses a t reference. '
               'WCR is restricted wild cluster-t with all 512 Rademacher sign vectors. '
               'Holm adjustment covers all seven outcomes in this table. With only nine month clusters, inference remains fragile. No significance stars are used.')
    rows = []
    model_labels = {'revision_only':'Revision only', 'quarter_controls':'Quarter controls',
                    'launch_size_and_ah':'Launch size and A+H',
                    'subscription_market_and_size':'Subscription HSI and launch size'}
    for key,label in model_labels.items():
        g = regressions[regressions.model.eq(key)].set_index('outcome')
        rows.append([label,f'{10*g.loc["log_close","coefficient"]:.3f}',
                     f'{10*g.loc["log_intraday","coefficient"]:.3f}',
                     f'{10*g.loc["application_return","coefficient"]:.3f}'])
    t4 = table(4,'All four declared control designs',
               ['Controls','Log close slope','Log day slope','APR slope'],rows,
               'Same 43 IPOs in every design; slopes have the Table 3 scaling. These are alternative '
               'specifications, not a nested sequence. All 28 focused estimates and all coefficients are in the CSV output. '
               'Subscription HSI runs from prospectus-day close to subscription-day close; it is an explanatory '
               'market-window check, not verified actual-pricing-date information.')
    rows = []
    exclude_names = {'full':'All range offers', 'without_2026Q1':'Remove Q1',
                     'without_2026Q2':'Remove Q2', 'without_2026Q3':'Remove Q3',
                     'without_top_three_close_returns':'Remove three largest IRs',
                     'without_top_three_application_returns':'Remove three largest APRs'}
    for key,label in exclude_names.items():
        g = sensitivity[sensitivity.exclusion.eq(key)].set_index('outcome')
        rows.append([label,int(g.loc['log_close','n']),f'{10*g.loc["log_close","coefficient"]:.3f}',
                     f'{10*g.loc["log_intraday","coefficient"]:.3f}',
                     f'{10*g.loc["application_return","coefficient"]:.3f}'])
    t5 = table(5,'Quarter and large-winner sensitivity',
               ['Retained sample','N','Log close slope','Log day slope','APR slope'],rows,
               'Each row uses the available quarter indicators. Exclusions retain identical firms across outcomes. '
               'Removing return leaders and removing application-return leaders answer different questions. '
               'Full leave-one-IPO-out results are also saved.')
    rows = []
    margin_labels = {'log_close':'Log offer-to-close', 'allocation_rate':'Allocation fraction',
                     'ceiling_principal_return':'Ceiling-principal return'}
    for key,label in margin_labels.items():
        r = controlled_margin.loc[key]
        rows.append([label,f'{100*r.coefficient:.3f}',f'{100*r.hc3_se:.3f}',
                     f'{r.hc3_p:.3f}',f'{r.wild_cluster_p:.3f}',f'{r.holm_wild_p:.3f}'])
    t6 = table(6,'Pre-deadline margin information: selected 25-IPO sample',
               ['Outcome','Slope','HC3 SE','HC3 p','WCR p','Holm WCR p'],rows,
               'The regressor is ln(latest safely published margin multiple); intercept and launch size are included. '
               'Slope units are 100 times the coefficient: log points or percentage points per one log unit of margin. '
               'N=25; six month clusters; WCR enumerates 64 signs. Holm covers the three controlled outcomes. '
               'Six clusters give coarse inference. The broker-survey scope is incomplete and coverage is selected.')
    rows = []
    for _,r in rolling.iterrows():
        rows.append(['Expanding historical mean' if r.model=='expanding_mean' else 'Launch size and A+H',
                     int(r.n),pct(r.mae,3),pct(r.rmse,3),f'{100*r.relative_mse_gain:.2f}'])
    t7 = table(8,'Retrospective temporal prediction check',
               ['Model','N','MAE (pp)','RMSE (pp)','MSE gain (%)'],rows,
               'Target: gross expected return on maximum-price requested principal. Each target uses at least '
               '40 prior IPOs whose first-day close precedes its prospectus date. The regression uses only filed '
               'offer size and A+H status. MSE gain is relative to the expanding-mean forecast. '
               'The current sample was already explored; this is not a new untouched holdout or a trading backtest.')
    t8 = table(7,'Data use and information timing', ['Data','Meaning and permitted use'],[
        ['Filed range and global quantity','Launch terms; measure price uncertainty and planned deal scale.'],
        ['Final offer price','Pricing outcome; construct revision and return, not a presumed deadline feature.'],
        ['Final requests and allocation','Allotment outcomes; measure rationing and expected payoff, not advance signals.'],
        ['Published margin snapshot','Partial broker demand before deadline; requires timestamp and survey-scope checks.'],
        ['Opening and closing prices','Later outcomes; locate price changes and label training returns only after listing.'],
        ['Recorded pricing date','Often expected or proxy date; cannot certify the actual information cutoff.'],
    ],widths='p{40mm}X')
    gain = rolling.set_index('model').loc['launch_size_and_ah','relative_mse_gain']
    b = identity.loc['log_close','coefficient']
    loo = sensitivity[sensitivity.exclusion.str.startswith('leave_out_')]
    bounds = loo.groupby('outcome').coefficient.agg(['min','max'])
    main_effect = 100*np.expm1(.1*range_close.coefficient)
    tex = r'''\documentclass[10pt,a4paper]{article}
\usepackage[margin=17mm,headheight=14pt]{geometry}
\usepackage[T1]{fontenc}\usepackage{lmodern}
\usepackage{amsmath,booktabs,array,tabularx}
\usepackage[hidelinks]{hyperref}\usepackage{fancyhdr}\usepackage{titlesec}
\titleformat{\section}{\normalsize\bfseries}{}{0pt}{}
\titlespacing*{\section}{0pt}{7pt}{3pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}\setlength{\tabcolsep}{3.5pt}
\setlength{\emergencystretch}{2em}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small HK IPO pricing and retail information}
\fancyhead[R]{\small Cutoff: 30 September 2026}\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
\hypersetup{pdftitle={HK IPO 2026: Price Adjustment and Retail Information},pdfauthor={}}
\begin{document}
{\LARGE\bfseries Price Adjustment and Retail Information}\par\addvspace{4pt}
{\large Hong Kong Main Board IPOs in 2026}\par\addvspace{4pt}
Prepared on 4 October 2026. English research report for supervisor discussion.

\section*{1. Findings, sample and definitions}
We study the existing 113 ordinary IPOs listed from 2 January to 30 September 2026.
The main price outcome remains offer-to-first-day-close return. Opening and intraday
returns locate price changes. The existing HSI adjustment checks market sensitivity.

Only 43 offers have a usable two-sided filing range. The old field labels 70 offers
``Fixed price'', but 31 of them lack a disclosed lower endpoint. The 39 equal-endpoint
offers and the 31 missing-lower offers are separate here. We do not invent a midpoint
or assign zero revision to either group. Original workbooks and extraction records
were not changed. This study corrects the research classification, not source fields.

The revision--close association is positive but uncertain. A day-stage association is
visible in some designs, but it does not pass the main adjusted inference. Higher
price return also does not imply higher application return. Pre-deadline margin
coverage is too selected for a general prediction claim.
'''+t1+t2+r'''
Let $P_L,P_H$ be the filed endpoints, $P_M=(P_L+P_H)/2$, $P_0$ the final offer
price, $P_O$ the opening price and $P_C$ the first-day close. For range offers,
\[
v=P_0/P_M-1,\qquad z=(P_0-P_L)/(P_H-P_L),\qquad w=(P_H-P_L)/P_M.
\]
Let $a=E[\text{allotted units}]/\text{requested units}$. The existing gross
application return is $a(P_C/P_0-1)$. The maximum-price principal measure is
$a(P_C-P_0)/P_H$. Both exclude brokerage, levies, fees, borrowing and tax. The latter
uses a price known at launch as its principal base; it is not a measured account payoff.
'''+f'For all 113 offers, these two application means are {pct(full_apr)}\\% and {pct(ceiling_apr)}\\%, respectively.\n'+r'''
\newpage
\section*{2. Price adjustment across the trading stages}
The test asks whether a higher final price relative to the filed midpoint accompanies
a higher later price return. Hanley (1993) motivates this partial-adjustment association
[1]. It does not by itself identify bookbuilding information, intentional underpricing,
or market inefficiency. The 43 range offers include 16 Q1, 14 Q2 and 13 Q3 IPOs,
with nine A+H issuers. No new sector fixed effects are fitted to this small sample.
\[
y_i=\alpha+\beta v_i+\delta_2 Q2_i+\delta_3 Q3_i+\varepsilon_i.
\]
Each outcome uses exactly the same firms and controls. Log outcomes are used to reduce
the influence of very large gains; raw close return remains reported. Allocation and
application return enter on their original fractional scale.
'''+t3+f'''
A +10 pp revision has an estimated {main_effect:.2f}\\% multiplicative change in the
close/offer ratio, not a {main_effect:.2f} pp increase in raw return. Its uncertainty
is large (Table 3). None of the seven main outcome tests survives Holm adjustment.
The unadjusted day-stage p-values are near 0.05; they do not establish a robust mechanism.
'''+t4+r'''
The price stages obey exact accounting:
\[
\ln(P_C/P_0)=\ln(P_O/P_0)+\ln(P_C/P_O),\quad
\ln(P_C/P_M)=\ln(P_0/P_M)+\ln(P_C/P_0).
\]
The first identity makes the close slope the sum of the opening and day slopes.
The second is a shared-price warning. Using $\ln(P_0/P_M)$ as regressor with the same
quarter controls gives a midpoint-close slope that is exactly one plus the offer-close slope.
'''+f'The two estimates are {1+b:.3f} and {b:.3f}; their difference is accounting, not an independent test.\n'+r'''
\newpage
\section*{3. Sensitivity and pre-deadline demand information}
'''+t5+f'''
Single-issuer exclusions retain positive log-close slopes, from
{10*bounds.loc['log_close','min']:.3f} to {10*bounds.loc['log_close','max']:.3f}
log points per +10 pp revision. Application slopes remain negative in single exclusions,
but turn positive when the three largest application-return winners are removed.
Thus, the mean application pattern is sensitive to a small group of large payoffs.
The lower-range group is not established as a superior investment rule.
'''+r'''
Final demand, offer price and allocation are later outcomes. The margin exercise uses
only snapshots published on a date strictly before the subscription closing date.
Of 93 source observations, 78 meet that condition, 13 are after the deadline, and two
have unresolved closing-day timing. We use the latest eligible observation for each
covered issuer. This leaves 25 IPOs across six listing months; 14 are in July.
The survey amounts cover named brokers and unspecified others, not the full market.
'''+t6+r'''
More reported margin demand accompanies higher price returns in the point estimates
and lower allocation fractions. Its application-return estimate is also positive,
but uncertain. None of the controlled tests passes Holm adjustment. These associations
cannot show that borrowing causes demand or that the signal predicts a general IPO cohort.
'''+t8+r'''
Range and planned-quantity inputs match the stored extraction values in all 113 IPOs:
308 non-missing field comparisons and 31 missing lower endpoints. The audit saves
quotes, source pages, disclosure URLs and extraction hashes. A matching value does not
replace independent semantic review of the disclosure. For example, OmniVision's
prospectus expressly permits disclosure of the maximum price only [2].

Only 36 of the 43 range offers have a recorded pricing-date proxy; seven lack that
anchor. These are not verified actual pricing dates. We therefore use the complete
subscription-to-listing HSI window for the return check. This prevents date availability
from changing the main firm sample, but it does not measure the true bookbuilding window.

\newpage
\section*{4. Temporal assessment and research conclusion}
We also test a small model using two launch variables: log planned proceeds and A+H
status. Planned proceeds use the filed global quantity times the midpoint for range
offers, or the published ceiling when no two-sided range exists. Final proceeds,
final demand and final allocation do not enter the forecast.

For each target, training IPOs must have completed their first trading day before the
target prospectus date. Each prediction requires at least 40 such IPOs. This gives
70 evaluated targets. Outcomes of later or same-day listings cannot enter training.
An expanding historical mean is the benchmark. No allocation strategy is simulated.
'''+t7+f'''
The size-and-A+H model reduces mean squared prediction error by only {100*gain:.2f}\\%.
This small retrospective gain does not establish useful advance selection. Mean actual
ceiling-principal return in the evaluated subset is {pct(rolling.iloc[0].mean_actual)}\\%.
Forecast errors are large relative to that mean. The exercise uses already explored
data and offers no untouched test of future performance.
'''+r'''
\textbf{Conclusion.} The current data do not establish a strong partial-adjustment
mechanism in Hong Kong's 2026 range offers. Positive share-return slopes coexist with
weak allocation evidence and winner-sensitive application returns. The available
pre-deadline broker data do not yet support a reliable selection claim.

\textbf{Next evidence work.} First verify the actual price-determination dates and
the maximum-only status against disclosures. Next expand timestamped margin coverage
across months and document the same broker scope. Then freeze a parsimonious model
before collecting a later, untouched IPO cohort. Test price return, allocation and
application-principal return separately. Use observed costs only in a later net-return
exercise. Grey-market trading after subscription closes cannot be an application signal.

\section*{Supervisor discussion draft}
The earlier study found a large gap between first-day share returns and retail
application returns. This follow-up tests the pricing stage and the information
available before applications close. Of 113 IPOs, 43 disclose usable price ranges;
31 other offers were incorrectly grouped with fixed-price offers when their lower
bound was missing. Within the common range sample, price revision has a positive
but uncertain association with first-day close return. Application-return results
depend on a few large winners. Timestamped margin data cover only 25 selected IPOs.
A retrospective launch-information model offers little forecast improvement. We
therefore retain the close return as the main outcome and prioritise timing and
coverage checks before making an information-based or predictive claim.

\section*{Sources and reproduction}
{\footnotesize
[1] Hanley, K. W. (1993). The underpricing of initial public offerings and the partial
adjustment phenomenon. \emph{Journal of Financial Economics}, 34, 231--250.
\href{https://doi.org/10.1016/0304-405X(93)90019-8}{Publisher DOI}.\par
[2] OmniVision Integrated Circuits Group, prospectus dated 31 December 2025, waiver discussion; extraction
PDF page 109 (printed page 101). \href{https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1231/2025123100089.pdf}{HKEX disclosure}.\par
[3] Project source ledger: prospectus PDFs, frozen retail tiers, raw first-day prices,
HSI daily cache, and timestamped broker-survey observations. The report is an extension
of these stored sources, not a new full-data certification.\par
Run \texttt{python run.py analysis --study pricing\_adjustment} from the repository root.\par
Study output: \texttt{analysis/out/pricing\_adjustment/}. The source audit, common samples,
all models, exclusions, timing ledger and rolling training membership are saved.
Input hashes and software versions are in \texttt{run\_manifest.json}.}
\end{document}
'''
    REPORT.write_text(tex,encoding='utf-8')
    md = f'''# HK IPO 2026: Price adjustment and retail information

Prepared 4 October 2026; cutoff 30 September 2026.

The existing sample has 113 IPOs: 43 two-sided ranges, 39 equal endpoints and 31
undisclosed lower bounds. The latter 31 must not be assigned zero midpoint revision
or silently treated as fixed prices. Original source records were not changed.

On the common 43-IPO range sample, the quarter-controlled revision slope is
{range_close.coefficient:.6f} for log close return (HC3 t p={range_close.hc3_p:.6f};
exact restricted wild-cluster p={range_close.wild_cluster_p:.6f}; nine month clusters).
None of the seven main outcome tests survives Holm adjustment. The application
return association changes sign after the three largest application winners are excluded.

The gross mean application return at final-price requested principal is {pct(full_apr)}%.
At maximum-price requested principal it is {pct(ceiling_apr)}%. Both exclude all costs
and are allocation expectations, not actual account performance.

Only 25 IPOs have a safely pre-deadline margin observation. The three controlled
margin tests do not survive multiplicity adjustment. On 70 retrospectively evaluated
targets, launch size and A+H status reduce forecast MSE by {100*gain:.2f}% relative to
an expanding mean. This is not an untouched holdout or a trading strategy test.

Full English report: [LaTeX](HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.tex).
PDF: [latest export](exported_pdfs/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.pdf).
Reproduction: `python run.py analysis --study pricing_adjustment`.
Data, all estimates, timing audit and training membership: `analysis/out/pricing_adjustment/`.
'''
    REPORT.with_suffix('.md').write_text(md,encoding='utf-8')
