#!/usr/bin/env python3
"""Add verified timing/scope metadata to the margin source ledger (no amounts are changed).

Inputs: pipeline/reports/margin_review/source_verification/verify_src_<i>.json (one per ledger source,
re-opened pages with verbatim wording) and conflict_7656.json. Existing observations are kept exactly;
the only observation additions are rows that the verified pages print but the ledger omitted.
Run from the repository root.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LEDGER = ROOT / "pipeline/prospectus_pipeline/data/margin/reported_snapshots.json"
VERIFY = ROOT / "pipeline/reports/margin_review/source_verification"
ADDITIONS = {  # (source index) -> [(stock_code, amount in HKD 100 million as printed on the verified page)]
    15: [("2523.HK", 14.80)],
    16: [("2523.HK", 439.92)],
}
SCOPE_CLASS = {"zhitong_futu_phillip_others": "futu_phillip_and_unnamed_other_brokers",
               "zhitong_market_data_unspecified": "unspecified", "guandian_unspecified": "unspecified"}


def main():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    for i, source in enumerate(ledger["sources"]):
        v = json.loads((VERIFY / f"verify_src_{i}.json").read_text(encoding="utf-8"))
        assert v["fetched_ok"], i
        mismatches = [c for c in v["ledger_comparison"]
                      if c["result"] not in ("match", "page_row_missing_from_ledger")]
        assert not mismatches, (i, mismatches)
        shown = v["published_at_hkt"]
        if source.get("published_at_hkt") and source["published_at_hkt"][:16] != shown[:16]:
            raise SystemExit(f"source {i}: ledger time {source['published_at_hkt']} != page {shown}")
        source["published_at_hkt"] = shown
        source["published_time_basis"] = ("time printed on the page with no timezone label; Hong Kong time assumed; "
                                          "page-displayed 'updated' times are not used")
        source["survey_scope_wording"] = v["survey_scope_wording"]
        source["measurement_wording"] = v["measurement_time_wording"]
        source["scope_class"] = SCOPE_CLASS.get(source["survey"], "unspecified")
        source["verification"] = {"page_reopened": True, "ledger_amounts_match_page": True,
                                  "record": f"pipeline/reports/margin_review/source_verification/verify_src_{i}.json"}
        for code, amount in ADDITIONS.get(i, []):
            if not any(o["stock_code"] == code for o in source["observations"]):
                source["observations"].append({"stock_code": code, "amount_100m_hkd": amount})
    ledger["conflicts_unresolved"] = [{
        "stock_code": "7656.HK",
        "description": ("Reports for 7656.HK on 2026-07-02/03 describe different series and scopes and are not combined. "
                        "The 2026-07-02 Zhitong survey (226.32亿港元 as of 7月2日, Futu/Phillip and other brokers) is the ledger observation. "
                        "A Ta Kung Pao print report of 2026-07-04 gives 771.7亿元 for the subscription close on 7月3日 under 'broker data' with no named scope; "
                        "the Zhitong 7月3日 roundup does not list 7656; an Infocast headline/snippet gives 221億元 as of 7月2日 (page not fetchable). "
                        "No value is selected or interpolated."),
        "record": "pipeline/reports/margin_review/source_verification/conflict_7656.json"}]
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sources:", len(ledger["sources"]), "observations:", sum(len(s["observations"]) for s in ledger["sources"]))


if __name__ == "__main__":
    main()
