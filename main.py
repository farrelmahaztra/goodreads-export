import csv
import json

csv_path = "export.csv"
json_path = "export.json"

def csv_to_json(filepath):
  parsed = []

  with open(filepath) as export_csv:
    reader = csv.DictReader(export_csv)

    for row in reader:
      row["ISBN"] = row["ISBN"][2:-1]
      row["ISBN13"] = row["ISBN13"][2:-1]

      if (row["ISBN"] != ""):
        row["Cover Image"] = f"https://covers.openlibrary.org/b/isbn/{row['ISBN']}-M.jpg" 
      else:
        row["Cover Image"] = ""
       
      parsed.append(row)

  return parsed


def write_json(data, filepath):
  with open(filepath, "w") as export_json:
    export_json.write(json.dumps(data))

parsed = csv_to_json(csv_path)
write_json(parsed, json_path)