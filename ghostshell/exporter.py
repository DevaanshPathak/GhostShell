import json
import csv

FIELDS = [
    "time", "proto", "local", "remote", "status",
    "pid", "country", "isp", "suspicious", "reason"
]

def export_to_json(data, path):
    # Convert tuple rows to dictionaries
    dict_rows = [dict(zip(FIELDS, row)) for row in data]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict_rows, f, indent=4)

def export_to_csv(data, path):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in data:
            writer.writerow(dict(zip(FIELDS, row)))
