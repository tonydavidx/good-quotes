# Load existing data from a JSON file
import json


with open(
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data.json", "r"
) as file:
    existing_data = json.load(file)

renamed_data = []

for item in existing_data:
    renamed_item = {
        "q": item["quote"],
        "a": item["author"],
        "l": item["likes"],
        "t": item["tags"],
        "w": item["work"],
    }
    renamed_data.append(renamed_item)

# Save to a new JSON file
with open(
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/renmaedd_quotes.json", "w"
) as json_file:
    json.dump(renamed_data, json_file, indent=4)
