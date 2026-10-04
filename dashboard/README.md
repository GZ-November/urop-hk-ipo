# HK IPO Observatory

A single-file, English dashboard for the existing Hong Kong IPO research data.

## Open

On macOS, double-click **Open Dashboard.command** in the repository root.
On any platform, open **dashboard/index.html** in a modern browser. You can copy
that HTML elsewhere and open it offline; the data, styles and charts are embedded.
No server, account, JavaScript package install or internet connection is required.
From the repository root, `make dashboard` also opens the snapshot.

## Explore

- **2026 overview:** filter by quarter and listing route; compare issuance,
  first-day returns and retail subscription demand. Cards show their observed N.
- **Issuer explorer:** search company names, stock codes and sponsors, sort,
  open full company records and download the filtered records as CSV.
  Quarter and route filters apply to 2026 records. Historical archive views
  display the stored 2025 Q1–Q2 records without changing research statistics.
- **Data coverage:** search all 202 registered fields, filter source layers and
  rank availability. This view follows the 2026 overview filters.

Use the reset button on the overview to clear quarter and route filters. Missing
numeric values display as an em dash, and remain blank in CSV downloads. Company
details preserve original source values and text, including decimal percentages.
CSV exports prefix formula-like text with an apostrophe for safe spreadsheet use.

## Data and interpretation

The snapshot embeds `pipeline/exports/HKIPO-MB-MASTER_clean.csv`, with types supplied
by `pipeline/registry/HKIPO_Variable_Registry.yaml`. It contains 155 issuer records:
113 actual 2026 listings and 42 historical 2025 listings. The current observation
cutoff is **30 September 2026**. It is a dated snapshot, not a live market feed.
The footer includes input SHA-256 hashes so the embedded version can be identified.

The overview and field-availability statistics use actual 2026 listing dates.
Gross funds raised sum Hong Kong public-offer and international-placement funds,
only for records with both components observed. First-day returns use the stored
raw offer-to-close return. Percentage source decimals are multiplied by 100 for
chart/card display. Retail demand is the stored public subscription multiple;
scatter points require a positive multiple and an observed first-day return.
Histogram intervals include the lower bound and exclude the upper bound.

Routes follow the research input precedence: 18A, 18C, A+H, conventional, unknown.
A+H is established by its flag or the existing route text convention. Availability
is not an evidence audit. Missing windows, unknown classifications and intentionally
reserved fields remain missing. These descriptive views do not establish causality.
Historical archive coverage is partial, not a complete 2025 population.

## Refresh and validate

After updating canonical exports or definitions:

```bash
make dashboard-build
make dashboard-check
make check-code
```

`dashboard-build` uses the existing project Python environment and PyYAML, then
creates a deterministic, portable HTML snapshot. It rejects duplicate issuer/year
identities, cohort/date conflicts, missing registered headers and invalid numeric
values. `dashboard-check` verifies snapshot freshness and runs data and JavaScript
interaction tests. It requires Node.js for the JavaScript checks; Node is not needed
to open the dashboard. Rebuild after a data cutoff change and update the cutoff in
`tools/build_dashboard.py` to match the refreshed observation period.

Edit `template.html` for layout and interaction changes; do not edit generated
`index.html` directly. The footer's repository-relative document links work when
the HTML stays in this checkout; the dashboard itself works when copied alone.
