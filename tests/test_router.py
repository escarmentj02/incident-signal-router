import unittest
from router import summarize


class RouterTests(unittest.TestCase):
    def test_groups_and_escalates_customer_facing_alerts(self):
        incidents = summarize([
            {"timestamp":"2026-08-06T12:01:00Z", "service":"api", "priority":"critical", "customer_impact":True},
            {"timestamp":"2026-08-06T12:05:00Z", "service":"api", "priority":"high", "customer_impact":False},
        ])
        self.assertEqual(incidents[0]["severity"], "SEV-1")
        self.assertEqual(incidents[0]["alert_count"], 2)


if __name__ == "__main__":
    unittest.main()
