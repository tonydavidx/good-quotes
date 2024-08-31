import json

quotes_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data.json"

# Load the JSON file
with open(quotes_file, 'r', encoding='utf-8') as f:
    quotes = json.load(f)

# Sort the quotes by the number of likes in descending order
sorted_quotes = sorted(quotes, key=lambda x: x['likes'], reverse=True)

# Save the sorted quotes to a new JSON file
with open(quotes_file, 'w', encoding='utf-8') as f:
    json.dump(sorted_quotes, f, indent=4)
