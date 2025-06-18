import json
import os

RULES_FILE = os.path.join(os.path.dirname(__file__), "suspicious_rules.json")

def load_rules():
    try:
        with open(RULES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[!] Failed to load rules: {e}")
        return {
            "high_risk_countries": [],
            "blacklisted_isps": []
        }
