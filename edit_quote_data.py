import json

data_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data - Copy.json"
# Read the JSON file into a list
with open(
    data_file, "r"
) as f:
    data = json.load(f)

# Modify the list by deleting the "work" key if its value is empty
for item in data:
    if item.get("work", "") == "":
        del item["work"]

# Write the modified list back to the file
with open(
    data_file, "w"
) as f:
    json.dump(data, f, indent=4)
