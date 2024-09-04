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
from support_files import last_run_time, process_urls

os.chdir("D:/Documents/Python/Scrapping Projects/goodquotes")

scrapped_pages_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/newtab_data/nscrapped_quots_link.csv"
quotes_toScrap_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/newtab_data/nquotes_links.csv"

quotes_file = "D:/Documents/Python/Scrapping Projects/goodquotes/data/newtab_data/newtab_quotes.json"

# profile = "C:/programs/chrome_bot"
profile_path = "C:/programs/Browerbots/wzxw2qjx.firefoxbot1"

# driver_options = Options()

firefox_options = FirefoxOptions()
firefox_options.set_preference("general.useragent.override", get_user_agent())
firefox_options.set_preference("permissions.default.image", 2)
# firefox_options.add_argument('--headless')
firefox_options.profile = webdriver.FirefoxProfile(profile_path)


driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()), options=firefox_options
)


with open(scrapped_pages_file, "r", encoding="utf-8") as f:
    scrapped_pages = f.readlines()

with open(quotes_toScrap_file, "r", encoding="utf-8") as f:
    urls = f.readlines()

my_agent = {"User-Agent": get_user_agent()}

while True:
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

# List to store new quotes
new_quotes = []
print(f"scraping {url}")
# Loop through each page and scrape quotes
pages_got = 0
for i in range(num_pages):
    print(f"scrapping page {i} ... out of {num_pages}", end="\r")
    page_url = driver.current_url
    print(page_url)
    # driver.get(page_url)
    # Find all quote containers on the page
    # quote_containers = driver.find_elements(By.CLASS_NAME, "quote")
    quote_containers = WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "quote"))
    )
    # Extract data from each quote container, the enumerate in the loop is used to get the index of container
    for idx, container in enumerate(quote_containers):
        quote = container.find_element(By.CLASS_NAME, "quoteText").text
        quote = unidecode(quote.split("―")[0].replace("”", "").replace("“", ""))
        author = container.find_element(By.CLASS_NAME, "authorOrTitle").text
        # print(quote, author)
        # Check if the quote already exists in the existing quotes list
        if not any(ext_quote["quote"] == quote for ext_quote in existing_quotes):
            try:
                language, confidence = langid.classify(quote)
                if language == "en" and len(quote) > 300:
                    # Create a dictionary for the quote data and append to the new quotes list
                    quote_data = {
                        "quote": quote,
                        "author": author,
                    }
                    new_quotes.append(quote_data)

            except Exception as e:  # pylint:ignore
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
    urls.remove(url)
    with open(quotes_toScrap_file, "w", encoding="utf-8") as f:
        f.writelines(urls)

    scrapped_pages.append(url)

    with open(scrapped_pages_file, "w", encoding="utf-8") as f:
        f.writelines(scrapped_pages)
    # Save quotes to the JSON file
    with open(quotes_file, "w", encoding="utf-8") as f:
        json.dump(existing_quotes, f)

    with open(
        "D:/Documents/Software-Projects/my-newtab/public/assets/quotes.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(existing_quotes, f)

    with open(
        "D:/Documents/Software-Projects/my-newtab/dist/assets/quotes.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(existing_quotes, f)

driver.quit()
