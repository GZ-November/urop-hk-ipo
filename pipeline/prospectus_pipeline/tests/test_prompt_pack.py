"""prompt_pack：harness 无关 prompt 生成器的契约测试。"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from prompt_pack import (  # noqa: E402
    MANUAL_RULES,
    build_prompt,
    shared_prefix,
)

PACKET = "## 唯一输出契约\n...（模拟的抽取包内容）...\n"


class PromptPackTests(unittest.TestCase):
    def test_extract_and_review_share_byte_identical_prefix(self):
        ex = build_prompt("extract", "0001.HK", "Test Co", PACKET, out_path="out/x.json")
        rv = build_prompt("review", "0001.HK", "Test Co", PACKET, out_path="out/x.json")
        shared = shared_prefix(ex, rv)
        # 共享前缀必须覆盖整个包内联段 + 手册规则（到阶段任务才分叉）
        self.assertGreater(len(shared), len(PACKET))
        self.assertTrue(ex.startswith(shared))
        self.assertTrue(rv.startswith(shared))
        self.assertIn("任务：抽取", ex[len(shared):])
        self.assertIn("任务：独立复核", rv[len(shared):])

    def test_manual_rules_present(self):
        prompt = build_prompt("extract", "0001.HK", "Test Co", PACKET)
        for marker in ("合并报表唯一原则", "Pre-IPO VC/PE 十个字段", "绝对不要猜"):
            self.assertIn(marker, prompt)

    def test_escalate_carries_only_fields(self):
        prompt = build_prompt("escalate", "0001.HK", "Test Co", PACKET,
                              only_fields=["col_U", "col_DP"])
        self.assertIn("col_U", prompt)
        self.assertIn("col_DP", prompt)
        self.assertIn("任务：定向重抽", prompt)

    def test_unknown_phase_rejected(self):
        with self.assertRaises(ValueError):
            build_prompt("nope", "0001.HK", "T", PACKET)

    def test_escalate_smaller_than_extract_on_same_packet(self):
        big_packet = "招股书正文" * 20000
        ex = build_prompt("extract", "0001.HK", "T", big_packet)
        es = build_prompt("escalate", "0001.HK", "T", big_packet[:len(big_packet) // 5],
                          only_fields=["col_U"])
        self.assertLess(len(es), len(ex) // 2)


if __name__ == "__main__":
    unittest.main()
