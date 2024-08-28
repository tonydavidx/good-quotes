from langdetect import detect
import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import json

from get_user_agent import get_user_agent

with open('D:/Documents/Python/Scrapping Projects/goodquotes/scrappedQuotePages.csv', 'r', encoding="utf-8") as f:
    scrapped_pages = f.readlines()
with open("D:/Documents/Python/Scrapping Projects/goodquotes/urls.csv", 'r', encoding="utf-8") as f:
    urls = f.readlines()

my_agent = {"User-Agent": get_user_agent()}

for url in urls:
    if url in scrapped_pages:
        print(f'url already scrapped\n {url}')
        continue
    url_res = requests.get(url, headers=my_agent)
    html = url_res.content
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    pages = soup.find('a', {'class': 'next_page'})
    last_page = pages.find_previous_sibling().text
    # Number of pages to scrape
    num_pages = int(last_page)

    # Load existing quotes from JSON file
    with open('D:/Documents/Python/Scrapping Projects/goodquotes/data/scrappedquotes.json', 'r', encoding='utf-8') as f:
        existing_quotes = json.load(f)

    # List to store new quotes
    new_quotes = []
    print(f"scraping {url} ...")
    # Loop through each page and scrape quotes
    for i in range(1, num_pages+1):
        print(f"scrapping page {i} ...", end='\r')
        page_url = f'{url}?page={i}'
        response = requests.get(page_url, headers=my_agent)
        soup = BeautifulSoup(response.content, 'html.parser')
        # with open('quotepage.txt', "w", encoding="utf-8") as f:
        #      f.write(soup.prettify())

        # Find all quote containers on the page
        quote_containers = soup.find_all('div', {'class': 'quote'})

        # Extract data from each quote container
        for container in quote_containers:
            quote = container.find(
                'div', {'class': 'quoteText'}).text.strip()
            quote = quote.split('―')[0]
            author = container.find(
                'span', {'class': 'authorOrTitle'}).text.strip().replace(',', '')
            # Check if the quote is less than 300 characters before adding it to the new quotes list
            if len(quote) < 280:
                # Check if the quote already exists in the existing quotes list
                if not any(q['quote'] == quote for q in existing_quotes):
                    try:
                        language = detect(quote)
                        if language == 'en':
                            # Create a dictionary for the quote data and append to the new quotes list
                            quote_data = {
                                'quote': quote,
                                'author': author,
                            }
                            new_quotes.append(quote_data)
                    except Exception as e:
                        print(e)
        # print(new_quotes)
        sleep(randint(3, 15))

    print(f"completed scrapping: {url}")
    # Append new quotes to existing quotes list
    existing_quotes += new_quotes

    # Save quotes to the JSON file
    with open('D:/Documents/Python/Scrapping Projects/goodquotes/data/scrappedquotes.json', 'w', encoding="utf-8") as f:
        json.dump(existing_quotes, f)

    with open('D:/Documents/Software-Projects/my-newtab/public/assets/quotes.json', 'w', encoding="utf-8") as f:
        json.dump(existing_quotes, f)

    with open('D:/Documents/Software-Projects/my-newtab/dist/assets/quotes.json', 'w', encoding="utf-8") as f:
        json.dump(existing_quotes, f)

    scrapped_pages.append(url)

    with open("D:/Documents/Python/Scrapping Projects/goodquotes/scrappedQuotePages.csv", "w", encoding='utf-8') as f:
        f.writelines(scrapped_pages)

    sleep(randint(30, 60))
