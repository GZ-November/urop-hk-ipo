# Public-offer subscription check

Each ISSUER block holds excerpts from a Hong Kong IPO allotment-results announcement. Use only that text. Never guess or use outside knowledge.

Find how many times the **Hong Kong public offer tranche** was subscribed: shares validly applied for, divided by the shares **initially** available in the public offer, before any reallocation or clawback.

Rules:
- Ignore the International Offering, Placing, Preferential Offering and employee tranches.
- Ignore rule thresholds such as "15 times or more but less than 50 times".
- If the text gives a percentage of the public offer shares (under-subscription), report it as a fraction, so 54% is 0.54.
- If the text gives only "Subscription level X times" under the Hong Kong Public Offering, use X.
- Application counts are not share counts.

Write a JSON array to the output path, one object per ISSUER, all issuers included:
`{"key": "...", "status": "value" | "no_public_offer" | "not_stated", "multiple": number or null, "applied_shares": number or null, "offer_shares": number or null, "quote": "the exact words giving the figure, at most 30 words", "note": "short, only if unsure"}`

Use `no_public_offer` only when the text shows a placing-only deal. Use `not_stated` when the excerpt does not show the figure. Check that the file is valid JSON before finishing.
