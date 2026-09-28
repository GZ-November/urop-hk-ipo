"""build_escalation_plan（验证驱动定向重抽）的单元测试。"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from auto_fill import build_escalation_plan  # noqa: E402
from contracts import strict_load_file  # noqa: E402
from topic_schema import get_field_to_topic_map  # noqa: E402

SCHEMA_FIELDS = strict_load_file(ROOT / "schema" / "fields.json")["fields"]
FIELD_TOPIC = get_field_to_topic_map(SCHEMA_FIELDS)


class EscalationPlanTests(unittest.TestCase):
    def make_packet_dir(self, tmp: Path, codes_with_shards=(), codes_with_full=()):
        packet_dir = tmp / "packets"
        packet_dir.mkdir(parents=True, exist_ok=True)
        for digits in codes_with_shards:
            for topic in ("offering", "financials", "ownership", "underwriting"):
                (packet_dir / f"HKIPO-MB{digits}-topic_{topic}.md").write_text("x", encoding="utf-8")
        for digits in codes_with_full:
            (packet_dir / f"HKIPO-MB{digits}.md").write_text("full", encoding="utf-8")
        return packet_dir

    def test_missing_field_maps_to_topic_shard(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            col = next(k for k, v in FIELD_TOPIC.items() if v == "topic_offering")
            packet_dir = self.make_packet_dir(tmp, codes_with_shards=["0001"])
            validation = {"pending_missing_fields": [{"code": "0001.HK", "fields": [col]}]}
            payload = build_escalation_plan(validation, SCHEMA_FIELDS, packet_dir)
            self.assertEqual(len(payload["topic_packets"]), 1)
            entry = payload["topic_packets"][0]
            self.assertEqual(entry["code"], "0001.HK")
            self.assertIn("topic_offering", " ".join(entry["topic_packets"]))
            self.assertNotIn("topic_financials", " ".join(entry["topic_packets"]))
            self.assertEqual(payload["only_fields"]["0001.HK"], [col])
            self.assertTrue(payload["verify"])

    def test_falls_back_to_full_packet_when_no_shards(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            col = next(k for k, v in FIELD_TOPIC.items() if v == "topic_underwriting")
            packet_dir = self.make_packet_dir(tmp, codes_with_full=["0002"])
            validation = {"records": [
                {"code": "0002.HK", "status": "fail", "fields_missing": [col]}]}
            payload = build_escalation_plan(validation, SCHEMA_FIELDS, packet_dir)
            entry = payload["topic_packets"][0]
            self.assertIn("packet_path", entry)  # 完整包回退
            self.assertNotIn("topic_packets", entry)

    def test_company_without_packets_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            packet_dir = self.make_packet_dir(tmp, codes_with_shards=["0003"])
            validation = {"pending_missing_fields": [{"code": "9999.HK", "fields": ["col_U"]}]}
            payload = build_escalation_plan(validation, SCHEMA_FIELDS, packet_dir)
            self.assertEqual(payload["topic_packets"], [])


if __name__ == "__main__":
    unittest.main()
