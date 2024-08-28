from langdetect import detect
import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import json
from get_user_agent import get_user_agent

scrapped_pages_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/scrapped_links.csv"
quotes_toScrap_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/links_toScrap.csv"
quotes_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data.json"

with open(scrapped_pages_file, 'r', encoding="utf-8") as f:
    scrapped_pages = f.readlines()
with open(quotes_toScrap_file, 'r', encoding="utf-8") as f:
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
    with open(quotes_file, 'r', encoding='utf-8') as f:
        existing_quotes = json.load(f)

    # List to store new quotes
    new_quotes = []
    print(f"scraping {url} ...")
    # Loop through each page and scrape quotes
    for i in range(2):
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

            tags_div = container.find('div', {'class': 'quoteFooter'})
            tags = tags_div.find_all('a')

            tag_names = [tag.get_text(strip=True) for tag in tags[:-1]]
            tag_links = ["https://www.goodreads.com"+tag['href']
                         for tag in tags[:-1]]
            likes = int(tags[-1].get_text(strip=True).replace(" likes", ""))

            try:
                quote_book_link = container.find(
                    'span', id=lambda x: x and x.startswith("quote_book_link"))
                quote_book_link = quote_book_link.find('a')['href']
                tag_links.append("https://www.goodreads.com"+quote_book_link)
                print("https://www.goodreads.com"+quote_book_link)
                # sleep(15)
            except Exception as e:
                pass

            # print(tags_names, likes)
            # print(tags_links)
            # sleep(15)

            # Check if the quote already exists in the existing quotes list
            if not any(q['quote'] == quote for q in existing_quotes):
                try:
                    language = detect(quote)
                    if language == 'en':
                        # Create a dictionary for the quote data and append to the new quotes list
                        quote_data = {
                            'quote': quote,
                            'author': author,
                            'likes': likes,
                            'tags': tag_names,
                            'tag_links': tag_links
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
    with open(quotes_file, 'w', encoding="utf-8") as f:
        json.dump(existing_quotes, f)

    scrapped_pages.append(url)

    with open(scrapped_pages_file, "w", encoding='utf-8') as f:
        f.writelines(scrapped_pages)

    sleep(randint(30, 60))
