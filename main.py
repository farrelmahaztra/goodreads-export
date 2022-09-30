import csv
import json
import requests

csv_path = "export.csv"
json_path = "export.json"
ol_domain = "https://openlibrary.org"
ol_covers_domain = "https://covers.openlibrary.org"

def search_book(title, author):
    response = requests.get(
        f"{ol_domain}/search.json?title={title}&author={author}")

    if response.status_code != 200:
        return {}

    results = response.json()

    if results["num_found"] == 0:
        return {}

    return results["docs"][0]


def get_olid(book):
    if "key" not in book:
        return ""

    return book["key"].split("/")[-1]


def get_cover_id(book):
    if "cover_i" not in book:
        return ""

    return book["cover_i"]


def enhance_row(row):
    row["ISBN"] = row["ISBN"][2:-1]
    row["ISBN13"] = row["ISBN13"][2:-1]
    row["Open Library Link"] = ""
    row["Cover Image"] = ""

    # Try to search for the book, preferentially use OLID/cover ID to avoid rate limit
    book = search_book(row["Title"], row["Author"])
    olid = get_olid(book)
    cover_id = get_cover_id(book)
    isbn = row["ISBN"]
    
    if olid:
        row["Open Library Link"] = f"{ol_domain}/works/{olid}"
        row["Cover Image"] = f"{ol_covers_domain}/b/olid/{olid}-M.jpg?default=false"

    # Use cover_id if available since this seems more reliable for images
    if cover_id:
        row["Cover Image"] = f"{ol_covers_domain}/b/id/{cover_id}-M.jpg?default=false"
    
    # Use ISBN if available as a fallback, but the images get rate limited
    if not olid and isbn:
        row["Open Library Link"] = f"{ol_domain}/isbn/{isbn}"

    if (not olid and not cover_id) and isbn:    
        row["Cover Image"] = f"{ol_covers_domain}/b/isbn/{isbn}-M.jpg?default=false"

    return row


def filter_row(row, filter_keys=[]):
    if (len(filter_keys) == 0):
        return row

    return {key: row[key] for key in filter_keys}


def csv_to_json(filepath, filter_keys=[]):
    parsed = []

    with open(filepath) as export_csv:
        reader = csv.DictReader(export_csv)

        for row in reader:
            enhanced = enhance_row(row)
            filtered = filter_row(enhanced, filter_keys)
            parsed.append(filtered)

    return parsed


def write_json(data, filepath):
    with open(filepath, "w") as export_json:
        export_json.write(json.dumps(data))


parsed = csv_to_json(
    csv_path, ["Title", "Author", "Exclusive Shelf", "Cover Image", "Open Library Link"])

write_json(parsed, json_path)
