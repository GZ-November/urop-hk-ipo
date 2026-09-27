"""主题分片合并与契约完整性单元测试。"""
import json
import unittest
from pathlib import Path

from merge_topics import merge_topic_records
from topic_schema import TOPIC_KEYS, get_field_to_topic_map


class MergeTopicsTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        schema_path = root / "schema" / "fields.json"
        self.fields = json.loads(schema_path.read_text(encoding="utf-8"))["fields"]
        self.extracted_path = root / "out" / "extracted" / "HKIPO-MB6082.json"

    def test_merge_topic_records_success(self):
        """测试将 4 个分片合并为完整记录，验证 100% 无损还原与契约校验。"""
        if not self.extracted_path.exists():
            self.skipTest("官方抽取文件不存在，跳过")

        orig = json.loads(self.extracted_path.read_text(encoding="utf-8"))
        key_to_topic = get_field_to_topic_map(self.fields)

        topic_records = []
        for tid in TOPIC_KEYS:
            rec = {"code": orig["code"], "topic": tid, "fields": {}}
            for k, v in orig["fields"].items():
                if key_to_topic.get(k) == tid:
                    rec["fields"][k] = v
            topic_records.append(rec)

        merged = merge_topic_records(topic_records, self.fields)
        self.assertEqual(merged["code"], orig["code"])
        self.assertEqual(len(merged["fields"]), 70)
        self.assertEqual(merged["fields"], orig["fields"])

    def test_merge_rejects_missing_field(self):
        """测试当有分片缺失字段时阻断合并。"""
        if not self.extracted_path.exists():
            self.skipTest("官方抽取文件不存在，跳过")

        orig = json.loads(self.extracted_path.read_text(encoding="utf-8"))
        key_to_topic = get_field_to_topic_map(self.fields)

        topic_records = []
        for tid in TOPIC_KEYS:
            rec = {"code": orig["code"], "topic": tid, "fields": {}}
            for k, v in orig["fields"].items():
                if key_to_topic.get(k) == tid:
                    # 故意删除 col_L
                    if k == "col_L":
                        continue
                    rec["fields"][k] = v
            topic_records.append(rec)

        with self.assertRaises(ValueError) as ctx:
            merge_topic_records(topic_records, self.fields)
        self.assertIn("尚缺失", str(ctx.exception))

    def test_merge_rejects_key_conflict(self):
        """测试当字段归属主题不匹配或冲突时阻断合并。"""
        records = [
            {"code": "6082.HK", "topic": "topic_offering", "fields": {"col_V": {"value": 100, "page": 1, "quote": "", "confidence": "high"}}}
        ]
        with self.assertRaises(ValueError) as ctx:
            merge_topic_records(records, self.fields)
        self.assertIn("属于主题 'topic_financials'", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
