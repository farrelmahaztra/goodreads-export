import csv
import json

csv_path = "export.csv"
json_path = "export.json"

def csv_to_json(filepath):
  parsed = []

  with open(filepath) as export_csv:
    reader = csv.DictReader(export_csv)

    for row in reader:
      parsed.append(row)

  return parsed


def write_json(data, filepath):
  with open(filepath, "w") as export_json:
    export_json.write(json.dumps(data))

parsed = csv_to_json(csv_path)
write_json(parsed, json_path)