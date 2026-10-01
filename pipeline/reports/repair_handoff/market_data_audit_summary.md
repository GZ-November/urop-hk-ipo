# Market data audit at 2026-09-30 (HKT cutoff)

Issuers: 106; clean 97, documented suspension 1, needing review 8.

## Benchmarks

- hsi_bars: 350 bars 2025-05-06 to 2026-09-30; findings: none
- hstech_bars: 350 bars 2025-05-06 to 2026-09-30; findings: none

## Issuers needing review

| code | findings |
|---|---|
| 2720.HK | large_one_day_moves:1;raw:large_one_day_moves:1 |
| 2706.HK | large_one_day_moves:1 |
| 2632.HK | large_one_day_moves:1;raw:large_one_day_moves:1 |
| 0068.HK | large_one_day_moves:1;raw:large_one_day_moves:1 |
| 6871.HK | large_one_day_moves:1 |
| 2723.HK | large_one_day_moves:1;raw:large_one_day_moves:1 |
| 2553.HK | large_one_day_moves:1;raw:large_one_day_moves:1 |
| 2797.HK | large_one_day_moves:2;raw:large_one_day_moves:1 |

Gaps are measured against HSI trading days; a gap is reported, never filled. Large moves are flagged for review only. Raw (as-traded) first-day closes are compared with the workbook; the adjusted cache is forward-adjusted and is not an as-traded price series.
