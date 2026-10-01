"""Margin snapshot timing: an article is usable before the deadline only if demonstrably published before it."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from tools.external.margin_reference import availability  # noqa: E402


class AvailabilityTests(unittest.TestCase):
    def test_earlier_calendar_day_is_public_before_the_deadline(self):
        self.assertEqual(availability("2026-07-03", "2026-07-03T20:06+08:00", "2026-07-06", "12:00"),
                         "yes_published_before_closing_day")

    def test_closing_day_evening_article_is_after_the_deadline(self):
        self.assertEqual(availability("2026-07-06", "2026-07-06T19:04+08:00", "2026-07-06", "12:00"), "no_after_deadline")

    def test_closing_day_morning_article_is_before_a_documented_deadline(self):
        self.assertEqual(availability("2026-07-06", "2026-07-06T09:30+08:00", "2026-07-06", "12:00"), "yes_before_deadline")

    def test_closing_day_with_unknown_time_or_deadline_stays_unknown(self):
        self.assertEqual(availability("2026-07-06", "", "2026-07-06", "12:00"), "unknown_closing_day_time_missing")
        self.assertEqual(availability("2026-07-06", "2026-07-06T09:30+08:00", "2026-07-06", ""),
                         "unknown_closing_day_time_missing")

    def test_publication_after_the_closing_day_is_never_available(self):
        self.assertEqual(availability("2026-07-06", "2026-07-08T11:15+08:00", "2026-07-06", "12:00"),
                         "no_published_after_closing_day")


if __name__ == "__main__":
    unittest.main()
