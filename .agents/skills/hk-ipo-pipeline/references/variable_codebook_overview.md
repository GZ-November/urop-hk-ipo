# Variable definitions and provenance

The current canonical workbook contains 202 variables. Counts and physical column
positions can change; resolve live schemas/headers rather than relying on an old
120-variable layout. The registry and cohort codebooks are generated snapshots,
not substitutes for original evidence.

## Authoritative definitions

Paths below are relative to the repository root:

| Resource | Role |
|---|---|
| `pipeline/prospectus_pipeline/schema/fields.json` | Prospectus extraction fields (currently 70) and source requirements |
| `pipeline/prospectus_pipeline/schema/allot_fields.json` | Allotment extraction fields (currently 18) |
| `pipeline/prospectus_pipeline/src/variable_catalog.py` | Authored semantic definitions, layers, units and groups |
| `pipeline/prospectus_pipeline/src/workbook_reader.py` | Header normalization and schema-to-workbook resolution |
| `pipeline/prospectus_pipeline/src/expansion_mapping.py` | Academic/event expansion mapping (currently fields 162–202) |
| `pipeline/registry/HKIPO_Variable_Registry.yaml` | Cross-cohort registry snapshot and derived definitions |
| `pipeline/prospectus_pipeline/src/panel.py` | Registry-driven pandas loading with stable slugs |

Schema keys such as `col_CK` retain historical identifiers; they are not proof of
the current Excel column letter. Clean CSVs use semantic headers. Inserting a
column must not attach a variable's meaning to its old position.

## Source layers

- Official HKEX new-listing reports establish issuer identity, offering metadata
  and membership candidates. Reconcile listing dates and exclusions for each
  requested interval; do not treat configured expected counts as coverage proof.
- Prospectuses provide share structure, price range, financials, underwriting,
  investor background and corporate disclosures. Preserve page/quote evidence,
  original units and period definitions; normalize deterministically.
- Allotment results establish final subscriptions, allocations, share counts and
  proceeds. Distinguish final allocation from prospectus plans.
- External data supply OHLC/turnover, index returns, HIBOR, aggregate balance,
  industry classifications and market-status observations; retain provider/date
  provenance and distinguish missing observations from true zeros.
- Derived fields combine sources: first-day return, money left on the table,
  pricing revision, age, aftermarket horizons, liquidity, stabilization and lockup
  windows. Trace each through its producer and inputs, including maturity.

Unknown flags remain missing unless the source establishes yes/no. A+H flags and
exclusive listing-route categories have different definitions. For cornerstone
absence, positive final allocation takes precedence over a stale absence verdict;
zero final allocation confirms absence. Known absence means no cornerstone event,
so cornerstone unlock CAR/volume fields should remain missing.

Run `registry --check` for definition drift, and inspect `master` warnings for
cohort fill rates, identities and membership. A full fill rate is not evidence
completeness; audit formal extractions and their authorization separately.
