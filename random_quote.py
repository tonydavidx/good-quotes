import json
import os
import random, textwrap
import time

quote_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data.json"
moved_quotes_file = (
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/moved_quotes.json"
)

with open(quote_file, "r", encoding="utf-8") as f:
    quotes = json.load(f)

with open(moved_quotes_file, "r", encoding="utf-8") as f:
    moved_quotes = json.load(f)


keys = ["s", "q", "m", "sa"]


def random_quote():
    quote = random.choice(quotes)
    quote_text, author, work = quote["quote"], quote["author"], quote["work"]
    wrapped_quote = textwrap.fill(quote_text, width=100)
    print(f"{wrapped_quote}\n\n- {author} {work if len(work) > 0 else ''}")
    return quote_text, author, work


def quote_slides():
    print("keys [s]: to run slides, [q]: quit, [m]: move quote  [any]: to quit")
    while True:
        random_quote()
        time.sleep(10)


def move_quote(quote_t):
    for i, q in enumerate(quotes):
        if q["quote"] == quote_t:
            quotes.pop(i)
            moved_quotes.append(q)
            with open(quote_file, "w", encoding="utf-8") as f:
                json.dump(quotes, f, indent=4)
            with open(moved_quotes_file, "w", encoding="utf-8") as f:
                json.dump(moved_quotes, f, indent=4)
            break


def same_author(author):
    print(f"same author: {author}")
    for q in quotes:
        if q["author"] == author:
            print(q["quote"])


while True:
    quote, author, work = random_quote()
    ans = input("")
    os.system("cls")

    if len(ans) > 0 and ans not in keys:
        break

    if ans == "s":
        quote_slides()

    if ans == "m":
        move_quote(quote)

    if ans == "sa":
        same_author(author)
