import csv
import json
import requests

csv_path = "export.csv"
json_path = "export.json"

def get_olid(title, author):
  response = requests.get(f"http://openlibrary.org/search.json?title={title}&author={author}")
  
  if response.status_code != 200:
    return ""

  results = response.json()

  if results["num_found"] == 0:
    return ""

  return results["docs"][0]["key"].split("/")[-1]
    

def csv_to_json(filepath):
  parsed = []

  with open(filepath) as export_csv:
    reader = csv.DictReader(export_csv)

    for row in reader:
      row["ISBN"] = row["ISBN"][2:-1]
      row["ISBN13"] = row["ISBN13"][2:-1]

      if (row["ISBN"] != ""):
        row["Open Library Link"] = f"https://openlibrary.org/isbn/{row['ISBN']}"
        row["Cover Image"] = f"https://covers.openlibrary.org/b/isbn/{row['ISBN']}-M.jpg" 
      else:
        olid = get_olid(row["Title"], row["Author"])
        row["Open Library Link"] = f"https://openlibrary.org/works/{olid}"
        row["Cover Image"] = f"https://covers.openlibrary.org/b/olid/{olid}-M.jpg"
       
      parsed.append(row)

  return parsed


def write_json(data, filepath):
  with open(filepath, "w") as export_json:
    export_json.write(json.dumps(data))

parsed = csv_to_json(csv_path)
write_json(parsed, json_path)