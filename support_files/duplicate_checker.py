# Check if the quotes_file has any duplicate quotes
# quotes_dict = {}
# with open(quotes_file, 'r', encoding='utf-8') as f:
#     data = json.load(f)
#     for quote in data:
#         if quote['quote'] in quotes_dict:
#             existing_quote = quotes_dict[quote['quote']]
#             existing_quote['tags'] = list(
#                 set(existing_quote['tags'] + quote['tags']))
#         else:
#             quotes_dict[quote['quote']] = quote

# with open(quotes_file, 'w', encoding="utf-8") as f:
#     json.dump(list(quotes_dict.values()), f)
