"""主题分片 Schema 规范性与正交性单元测试。"""
import json
import unittest
from pathlib import Path

from topic_schema import (
    TOPIC_DEFINITIONS,
    TOPIC_KEYS,
    get_field_to_topic_map,
    get_topic_definition,
    get_topic_fields,
    validate_topic_completeness,
)


class TopicSchemaTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.schema_path = root / "schema" / "fields.json"
        self.fields = json.loads(self.schema_path.read_text(encoding="utf-8"))["fields"]

    def test_topic_completeness_and_coverage(self):
        """测试 4 个正交主题分片 100% 覆盖 70 个招股书字段，无遗漏、无重叠。"""
        counts = validate_topic_completeness(self.fields)
        self.assertEqual(len(counts), 4)
        self.assertEqual(counts["topic_offering"], 15)
        self.assertEqual(counts["topic_financials"], 30)
        self.assertEqual(counts["topic_ownership"], 20)
        self.assertEqual(counts["topic_underwriting"], 5)
        self.assertEqual(sum(counts.values()), 70)

    def test_topic_definitions_keys(self):
        """测试各主题包含必填属性。"""
        for tid in TOPIC_KEYS:
            defn = get_topic_definition(tid)
            self.assertEqual(defn["id"], tid)
            self.assertIn("title", defn)
            self.assertIn("groups", defn)
            self.assertIn("expected_field_count", defn)
            self.assertIn("key_rules", defn)

    def test_field_to_topic_map(self):
        """测试字段映射的唯一性。"""
        mapping = get_field_to_topic_map(self.fields)
        self.assertEqual(len(mapping), 70)
        # 验证核心字段归属
        self.assertEqual(mapping["col_L"], "topic_offering")
        self.assertEqual(mapping["col_V"], "topic_financials")
        self.assertEqual(mapping["col_BA"], "topic_ownership")
        self.assertEqual(mapping["col_CJ"], "topic_underwriting")


if __name__ == "__main__":
    unittest.main()
