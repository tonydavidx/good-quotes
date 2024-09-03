import os
import random
import langid
import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import json
from get_user_agent import get_user_agent
from support_files import process_urls, last_run_time

os.chdir("D:/Documents/Python/Scrapping Projects/goodquotes")
quotes_iwant = "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/quotes_iwant.csv"
scrapped_pages_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/scrapped_links.csv"
quotes_toScrap_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/links_toScrap.csv"
quotes_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data.json"

total_pages_scrapped = 0

while total_pages_scrapped < 50:
    with open(scrapped_pages_file, 'r', encoding="utf-8") as f:
        scrapped_pages = f.readlines()
    with open(quotes_toScrap_file, 'r', encoding="utf-8") as f:
        urls = f.readlines()

    with open(quotes_iwant, 'r', encoding="utf-8") as f:
        quotes_want = f.readlines()

    my_agent = {"User-Agent": get_user_agent()}
    while True:
        url = random.choice(quotes_want)
        # url = random.choice(urls)
        if url not in scrapped_pages:
            break

    url_res = requests.get(url, headers=my_agent)
    html = url_res.content
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    try:
        pages = soup.find('a', {'class': 'next_page'})
        last_page = pages.find_previous_sibling().text
        last_page = int(last_page)
    except Exception as e:
        print(e)
        last_page = 1
    # Number of pages to scrape
    num_pages = last_page
    print(f"total pages: {num_pages}")
    # Load existing quotes from JSON file
    with open(quotes_file, 'r', encoding='utf-8') as f:
        existing_quotes = json.load(f)

    # List to store new quotes
    new_quotes = []
    print(f"scraping {url}")
    # Loop through each page and scrape quotes
    tag_links_got = []
    pages_got = 0
    for i in range(1, num_pages+1):
        print(f"scrapping page {i} ... out of {num_pages}", end='\r')
        page_url = f'{url}?page={i}'
        print(page_url)
        response = requests.get(page_url, headers=my_agent)
        soup = BeautifulSoup(response.content, 'html.parser')
        with open('quotepage.txt', "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        # Find all quote containers on the page
        quote_containers = soup.find_all('div', {'class': 'quote'})
        print("quotes on page: ", len(quote_containers))

        if len(quote_containers) == 0:
            print("No quotes found on page")
            break

        # Extract data from each quote container, the enumerate in the loop is used to get the index of container
        for idx, container in enumerate(quote_containers):
            quote = container.find(
                'div', {'class': 'quoteText'}).text.strip()
            quote = quote.split('―')[0]
            author = container.find(
                'span', {'class': 'authorOrTitle'}).text.strip().replace(',', '')

            tags_div = container.find('div', {'class': 'quoteFooter'})
            tags = tags_div.find_all('a')

            # Filtering out tags that contain the words "quote" or "quotes"
            tag_names = [tag.get_text(strip=True) for tag in tags[:-1]
                         if 'quote' not in tag.get_text(strip=True).lower()]

            tag_links = ["https://www.goodreads.com" + tag['href'] for tag in tags[:-1]
                         if 'quote' not in tag.get_text(strip=True).lower()]

            likes = int(tags[-1].get_text(strip=True).replace(" likes", ""))

            try:
                quote_book_link = container.find(
                    'span', id=lambda x: x and x.startswith("quote_book_link"))
                quote_book_link = "https://www.goodreads.com" + \
                    quote_book_link.find('a')['href']
                tag_links.append(quote_book_link)
                # print("https://www.goodreads.com"+quote_book_link)
                # sleep(15)
            except Exception as e:
                pass

            for link in tag_links:
                if link+"\n" not in urls and link+"\n" not in scrapped_pages:
                    urls.append(link+"\n")
            # print(tags_names, likes)
            # sleep(15)

            # Check if the quote already exists in the existing quotes list
            if not any(ext_quote['quote'] == quote for ext_quote in existing_quotes):
                try:
                    language, confidence = langid.classify(quote)
                    if language == 'en':
                        # Create a dictionary for the quote data and append to the new quotes list
                        quote_data = {
                            'quote': quote,
                            'author': author,
                            'likes': likes,
                            'tags': tag_names,
                            'work': quote_book_link if quote_book_link else '',
                        }
                        new_quotes.append(quote_data)

                except Exception as e:
                    print(e)

        total_pages_scrapped += 1
        pages_got += 1
        # print(new_quotes)
        sleep(randint(3, 15))

    print(f"\ntotal pages scrapped: {total_pages_scrapped}")

    print(f"completed scrapping: {url}")
    # Append new quotes to existing quotes list
    existing_quotes += new_quotes

    if pages_got == num_pages:
        # urls.remove(url)
        quotes_want.remove(url)
        with open(quotes_toScrap_file, 'w', encoding="utf-8") as f:
            f.writelines(urls)

        with open(quotes_iwant, 'w', encoding="utf-8") as f:
            f.writelines(quotes_want)

        # Save quotes to the JSON file
        with open(quotes_file, 'w', encoding="utf-8") as f:
            json.dump(existing_quotes, f)

        scrapped_pages.append(url)

        with open(scrapped_pages_file, "w", encoding='utf-8') as f:
            f.writelines(scrapped_pages)

        process_urls.process_urls(quotes_toScrap_file)
