# Evidence coverage summary

Generated 2026-10-01T09:43:52+08:00 HKT from the extraction JSON files and local gate credentials. Classification only; no semantic verification.

## Review provenance (issuers per cohort x target)

| cohort | target | n | named_reviewer | bulk_stamp | stale | absent | failed |
|---|---|---:|---:|---:|---:|---:|---:|
| 2026Q1 | prospectus | 38 | 0 | 38 | 0 | 0 | 0 |
| 2026Q1 | allot | 38 | 0 | 38 | 0 | 0 | 0 |
| 2026Q2 | prospectus | 45 | 15 | 30 | 0 | 0 | 0 |
| 2026Q2 | allot | 45 | 1 | 0 | 0 | 44 | 0 |
| 2026Q3 | prospectus | 23 | 0 | 23 | 0 | 0 | 0 |
| 2026Q3 | allot | 23 | 0 | 23 | 0 | 0 | 0 |

## Research-field evidence status (issuer x field cells)

| cohort | target | cells | value_with_quote | derived_rule | unknown | value_without_quote | unit_conflict_with_quote | field_absent | json_absent |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026Q1 | prospectus | 1140 | 1114 | 0 | 26 | 0 | 0 | 0 | 0 |
| 2026Q1 | allot | 608 | 566 | 32 | 10 | 0 | 0 | 0 | 0 |
| 2026Q2 | prospectus | 1350 | 1276 | 0 | 74 | 0 | 0 | 0 | 0 |
| 2026Q2 | allot | 720 | 609 | 81 | 30 | 0 | 0 | 0 | 0 |
| 2026Q3 | prospectus | 690 | 620 | 0 | 70 | 0 | 0 | 0 | 0 |
| 2026Q3 | allot | 368 | 299 | 53 | 16 | 0 | 0 | 0 | 0 |

`named_reviewer` means a record names a reviewer and matches the current file bytes (see `review_scope`: this repair's reviews cover only the stated fields, not the whole payload); `bulk_stamp` is a pass record with no reviewer identity. A quote that contains the value is not a semantic review.
