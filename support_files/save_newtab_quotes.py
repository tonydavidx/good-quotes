import json


def save_and_process_quotes(quotes_data):
    """
    Process quotes data and save it to the JSON files. to save to the newtab data
    """

    with open(
        "D:/Documents/Python/Scrapping Projects/goodquotes/data/newtab_data/newtab_quotes.json",
        "r",
        encoding="utf-8",
    ) as f:
        existing_ntquots = json.load(f)

    new_quotes = existing_ntquots + quotes_data

    seen = set()
    duplicates = []
    for quote in new_quotes[:]:
        if quote["quote"] in seen:
            duplicates.append(quote)
        else:
            seen.add(quote["quote"])
    if duplicates:
        print("The following quotes are duplicated:")
        for quote in duplicates:
            print(quote["quote"])
        for quote in duplicates:
            new_quotes.remove(quote)

    with open(
        "D:/Documents/Python/Scrapping Projects/goodquotes/data/newtab_data/newtab_quotes.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(new_quotes, f)

    with open(
        "D:/Documents/Python/Scrapping Projects/goodquotes/data/newtab_data/newtab_quotes.json",
        "r",
        encoding="utf-8",
    ) as f:
        newtab_quotes = json.load(f)

    modified_data = [
        {"quote": item["quote"], "author": item["author"]}
        for item in newtab_quotes
        if len(item["quote"]) < 300
    ]

    with open(
        "D:/Documents/Software-Projects/my-newtab/public/assets/quotes.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(modified_data, f)

    with open(
        "D:/Documents/Software-Projects/my-newtab/dist/assets/quotes.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(modified_data, f)


# save_and_process_quotes(
#     [
#         {
#             "quote": "Nature always has its way of showing its power and might. Majestic, full of life, and passionate; yet graceful, calm, and not forceful.\n",
#             "author": "Felisa Tan,",
#             "likes": 0,
#             "tags": [
#                 "gentleness",
#                 "laws-of-nature",
#                 "learn-from-nature",
#                 "mother-nature",
#                 "nature",
#                 "power",
#                 "spirituality",
#                 "wisdom",
#             ],
#             "work": "https://www.goodreads.com/work/quotes/110685991",
#         }
#     ]
# )
