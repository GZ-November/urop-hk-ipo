# Delivery report template

Write the report in the user's language. Fill every section from command
output (`plan`, `status`, `audit`, `cross_check`, bundle `quality_summary.json`).
Write "none" for an empty section rather than dropping it.

```markdown
## HK IPO collection: <interval>, <boards>

**Delivery ZIP:** <absolute path>
**Observation cutoff:** <date> (Hong Kong)

### Coverage by job
| Board | Quarter | Status | Issuers | First–last listing date | Workbook / CSV (absolute paths) |
|---|---|---|---|---|---|

### Evidence and review
- Fully reviewed and written: <issuers per cohort>
- Review pending: <codes and targets>, reason
- Failed review / corrected: <codes and fields>

### Field coverage
- Supported fields missing from disclosures: <field: issuers>
- Audit discrepancies: <count and where to read them>

### Gaps and limitations
- Official coverage gaps: <job, message; not evidence of zero IPOs>
- Immature return windows: <which horizons, listings after which date>
- Source or network limitations: <stage, error>

### Reused stored cohorts
- <cohort id>: audit result

### Next actions for the user
- <for example: rerun the plan after HKEX publishes the Q4 report>
```
