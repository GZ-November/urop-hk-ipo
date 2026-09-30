# Hong Kong IPO Research Dataset

This context defines the issuer records and time periods used to assemble the Hong Kong IPO research dataset.

## Language

**Issuer cohort**:
A set of Hong Kong IPO issuers selected for a research run by an inclusive date interval. The listing date determines membership; the prospectus date is used only when the listing date is unavailable.
_Avoid_: Batch, sample (when referring to the selected issuer set)

**Main Board ordinary IPO**:
A Main Board listing that raises capital through an ordinary public offering. Transfers from GEM, SPAC or de-SPAC transactions, and listings by introduction are outside this research population.
_Avoid_: New listing (when referring to the research population)

**Official listing report**:
HKEX's annual Main Board record of new listings, used to establish which issuers belong to an issuer cohort.
_Avoid_: Prospectus (when referring to the annual issuer list)

**Variable registry**:
The machine-readable, single-source contract (`HKIPO_Variable_Registry.yaml`) for the 202 research variables — column letter, header, slug, declared dtype, layer, unit. Rendered codebooks and the master panel must agree with it; `variable_catalog.py` holds the authored definitions and registry building flags any drift.
_Avoid_: Codebook (that word is the rendered per-cohort document), data dictionary

## Current analysis population

All descriptive statistics and regressions, including Module A, use issuers with an observed listing date in 2026. Historical cohort artifacts can remain in the collection layer; they are excluded by `analysis/module_a_stylized_facts.py:select_2026`. Cohort labels must agree with listing dates, issuer codes must be unique, and unknown classification flags remain missing.
