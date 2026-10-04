# HK IPO 2026: Price adjustment and retail information

Prepared 4 October 2026; cutoff 30 September 2026.

The existing sample has 113 IPOs: 43 two-sided ranges, 39 equal endpoints and 31
undisclosed lower bounds. The latter 31 must not be assigned zero midpoint revision
or silently treated as fixed prices. Original source records were not changed.

On the common 43-IPO range sample, the quarter-controlled revision slope is
1.597794 for log close return (HC3 t p=0.251357;
exact restricted wild-cluster p=0.207031; nine month clusters).
None of the seven main outcome tests survives Holm adjustment. The application
return association changes sign after the three largest application winners are excluded.

The gross mean application return at final-price requested principal is 2.08%.
At maximum-price requested principal it is 1.91%. Both exclude all costs
and are allocation expectations, not actual account performance.

Only 25 IPOs have a safely pre-deadline margin observation. The three controlled
margin tests do not survive multiplicity adjustment. On 70 retrospectively evaluated
targets, launch size and A+H status reduce forecast MSE by 1.62% relative to
an expanding mean. This is not an untouched holdout or a trading strategy test.

Full English report: [LaTeX](HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.tex).
PDF: [latest export](exported_pdfs/HK_IPO_2026_PRICING_AND_RETAIL_INFORMATION.pdf).
Reproduction: `python run.py analysis --study pricing_adjustment`.
Data, all estimates, timing audit and training membership: `analysis/out/pricing_adjustment/`.
