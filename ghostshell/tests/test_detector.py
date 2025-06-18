import unittest
from ghostshell.detector import detect_suspicious

class TestDetector(unittest.TestCase):
    def detect_suspicious(conns, rules):
        flagged = []
        for conn in conns:
            conn["suspicious"] = False
            reasons = []

            if conn.get("country") in rules.get("high_risk_countries", []):
                conn["suspicious"] = True
                reasons.append("high-risk country")

            if conn.get("isp") in rules.get("blacklisted_isps", []):
                conn["suspicious"] = True
                reasons.append("blacklisted ISP")

            conn["reason"] = ", ".join(reasons)
            flagged.append(conn)

        return flagged


if __name__ == '__main__':
    unittest.main()
