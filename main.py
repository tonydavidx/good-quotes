import json
import os
import random
from random import randint
from time import sleep

import langid
from selenium import webdriver

# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unidecode import unidecode
from webdriver_manager.firefox import GeckoDriverManager

from get_user_agent import get_user_agent
from support_files import (
    detect_language,
    last_run_time,
    process_urls,
    save_newtab_quotes,
)

os.chdir("D:/Documents/Python/Scrapping Projects/goodquotes")
quotes_iwant = (
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/quotes_iwant.csv"
)
scrapped_pages_file = (
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/scrapped_links.csv"
)
quotes_toScrap_file = (
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/csv/links_toScrap.csv"
)
quotes_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/quote_data.json"

rejected_quotes_file = (
    "D:/Documents/Python/Scrapping Projects/goodquotes/data/moved_quotes.json"
)
# profile = "C:/programs/chrome_bot"
profile_path = "C:/programs/Browerbots/wzxw2qjx.firefoxbot1"

# driver_options = Options()

firefox_options = FirefoxOptions()
firefox_options.set_preference("general.useragent.override", get_user_agent())
firefox_options.set_preference("permissions.default.image", 2)
# firefox_options.add_argument("--headless")
firefox_options.profile = webdriver.FirefoxProfile(profile_path)


driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()), options=firefox_options
)
# driver = webdriver.Chrome(
#     service=ChromeService(ChromeDriverManager().install()), options=driver_options
# )


with open(scrapped_pages_file, "r", encoding="utf-8") as f:
    scrapped_pages = f.readlines()

with open(quotes_toScrap_file, "r", encoding="utf-8") as f:
    urls = f.readlines()

with open(quotes_iwant, "r", encoding="utf-8") as f:
    quotes_want_links = f.readlines()

my_agent = {"User-Agent": get_user_agent()}

while True:
    if len(quotes_want_links) > 0:
        url = random.choice(quotes_want_links)
    else:
        url = random.choice(urls)

    if url not in scrapped_pages:
        break
driver.get(url)
last_page = 1

try:
    maincontent = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (
                By.CLASS_NAME,
                "mainContent ",
            )
        )
    )
    all_links = maincontent.find_elements(By.TAG_NAME, "a")
    all_links = [link.get_attribute("href") for link in all_links]
    page_links = []
    for link in all_links:
        if "page=" in link:
            page_links.append(link)
    # print(page_links)
    last_page = page_links[-2].split("=")[-1]
except Exception as e:
    print(e)

num_pages = int(last_page)
print(f"total pages: {num_pages}")
# Load existing quotes from JSON file
with open(quotes_file, "r", encoding="utf-8") as f:
    existing_quotes = json.load(f)

with open(rejected_quotes_file, "r", encoding="utf-8") as f:
    rejected_quotes = json.load(f)

# List to store new quotes
new_quotes = []
# print(f"scraping {url}")
# Loop through each page and scrape quotes
pages_got = 0
for i in range(num_pages):
    # print(f"scrapping page {i} ... out of {num_pages}", end="\r")
    page_url = driver.current_url
    print(page_url + "\n", end="\r")
    # driver.get(page_url)
    # Find all quote containers on the page
    quote_containers = WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "quote"))
    )
    # Extract data from each quote container, the enumerate in the loop is used to get the index of container
    for idx, container in enumerate(quote_containers):
        quote = container.find_element(By.CLASS_NAME, "quoteText").text
        quote = unidecode(quote.split("―")[0].replace("”", "").replace("“", ""))
        author = container.find_element(By.CLASS_NAME, "authorOrTitle").text
        # print(quote, author)

        tags_div = container.find_element(By.CLASS_NAME, "quoteFooter")
        tag_links = tags_div.find_elements(By.TAG_NAME, "a")
        likes = [tag.text for tag in tag_links][-1].strip(" likes")

        # Filtering out tags that contain the words "quote" or "quotes"
        tag_names = [tag.text for tag in tag_links][:-1]
        tag_links = [tag.get_attribute("href") for tag in tag_links][:-1]

        for idx, tag in enumerate(tag_names):
            try:
                language = detect_language.check_char_lang(tag)
                if language == False:
                    del tag_names[idx]
                    del tag_links[idx]
                    print("deleted tag for language", tag)
            except Exception as e:
                print(e)

                if len(tag_names) > 1:
                    tag_split = tag.split("-")
                    if (
                        "quote" in tag.lower()
                        or "quotes" in tag.lower()
                        or len(tag_split) > 3
                    ):
                        del tag_names[idx]
                        print("deleted tag for quote or length", tag)
                    # print(tag_split, len(tag_split))

        tag_names = tag_names[:5] if len(tag_names) > 5 else tag_names
        tag_links = tag_links[:5] if len(tag_links) > 5 else tag_links

        quote_book_link = None
        try:
            quote_book_link = container.find_elements(By.CLASS_NAME, "authorOrTitle")[
                1
            ].get_attribute("href")
            # print(quote_book_link)
            if quote_book_link:
                tag_links.append(quote_book_link)
        except Exception as e:
            pass

        for link in tag_links:
            if link + "\n" not in urls and link + "\n" not in scrapped_pages:
                urls.append(link + "\n")

        # Check if the quote already exists in the existing quotes list
        if not any(
            ext_quote["quote"] == quote for ext_quote in existing_quotes
        ) and not any(rej_quote["quote"] == quote for rej_quote in rejected_quotes):
            try:
                language, confidence = langid.classify(quote)
                if language == "en":
                    quote_data = {
                        "quote": quote,
                        "author": author,
                        "likes": int(likes),
                    }
                    if len(tag_names) > 0:
                        quote_data["tags"] = tag_names
                    if quote_book_link is not None:
                        quote_data["work"] = quote_book_link
                    new_quotes.append(quote_data)

            except Exception as e:  # pylance:ignore
                print(e)

    pages_got += 1
    # print(new_quotes)
    try:
        next_page = driver.find_element(By.CLASS_NAME, "next_page").click()
    except Exception as e:
        break

    sleep(randint(3, 10))


print(f"completed scrapping: {url}")
# Append new quotes to existing quotes list
existing_quotes += new_quotes

if pages_got >= num_pages:
    if len(quotes_want_links) > 0:
        quotes_want_links.remove(url)
        with open(quotes_iwant, "w", encoding="utf-8") as f:
            f.writelines(quotes_want_links)
        # save_newtab_quotes.save_and_process_quotes(new_quotes)
        with open(quotes_toScrap_file, "w", encoding="utf-8") as f:
            f.writelines(urls)
    else:
        urls.remove(url)
        with open(quotes_toScrap_file, "w", encoding="utf-8") as f:
            f.writelines(urls)
    # Save quotes to the JSON file
    with open(quotes_file, "w", encoding="utf-8") as f:
        json.dump(existing_quotes, f)

    scrapped_pages.append(url)

    with open(scrapped_pages_file, "w", encoding="utf-8") as f:
        f.writelines(scrapped_pages)

    process_urls.process_urls(quotes_toScrap_file)


driver.quit()
