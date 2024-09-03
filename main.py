from operator import contains
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random
import langid
from unidecode import unidecode
from time import sleep
from random import randint
import json
from get_user_agent import get_user_agent
from support_files import process_urls, last_run_time

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

total_pages_scrapped = 0
profile = "C:/programs/chrome_bot"

driver_options = Options()
driver_options.add_argument("--disable-gpu")
driver_options.add_argument("--start-maximized")
prefs = {"profile.managed_default_content_settings.images": 2}
driver_options.add_experimental_option("prefs", prefs)
driver_options.add_argument(f"--user-data-dir={profile}")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=driver_options
)


while total_pages_scrapped < 50:
    with open(scrapped_pages_file, "r", encoding="utf-8") as f:
        scrapped_pages = f.readlines()
    with open(quotes_toScrap_file, "r", encoding="utf-8") as f:
        urls = f.readlines()

    # with open(quotes_iwant, "r", encoding="utf-8") as f:
    #     quotes_want = f.readlines()
    my_agent = {"User-Agent": get_user_agent()}

    while True:
        # url = random.choice(quotes_want)
        url = random.choice(urls)
        if url not in scrapped_pages:
            break
    driver.get(url)
    last_page = 1
    try:
        navigation = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.CLASS_NAME,
                    "mainContent ",
                )
            )
        )
        all_links = navigation.find_elements(By.TAG_NAME, "a")
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
    tag_links_got = []
    pages_got = 0
    for i in range(1, num_pages + 1):
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

            tags_div = container.find_element(By.CLASS_NAME, "quoteFooter")
            tag_links = tags_div.find_elements(By.TAG_NAME, "a")
            tags = [tag.text for tag in tag_links][:-1]

            likes = [tag.text for tag in tag_links][-1].strip(" likes")

            # Filtering out tags that contain the words "quote" or "quotes"
            tag_names = [tag for tag in tags if "quote" not in tag.lower()]
            tag_links = [tag.get_attribute("href") for tag in tag_links][:-1]

            quote_book_link = None
            try:
                quote_book_link = container.find_elements(
                    By.CLASS_NAME, "authorOrTitle"
                )[1].get_attribute("href")
                # print(quote_book_link)
                if quote_book_link:
                    tag_links.append(quote_book_link)
            except Exception as e:
                pass

            for link in tag_links:
                if link + "\n" not in urls and link + "\n" not in scrapped_pages:
                    urls.append(link + "\n")
            # print(tags_names, likes)
            #         # sleep(15)

            # Check if the quote already exists in the existing quotes list
            if not any(ext_quote["quote"] == quote for ext_quote in existing_quotes):
                try:
                    language, confidence = langid.classify(quote)
                    if language == "en":
                        # Create a dictionary for the quote data and append to the new quotes list
                        quote_data = {
                            "quote": quote,
                            "author": author,
                            "likes": int(likes),
                            "tags": tag_names,
                            "work": quote_book_link if quote_book_link else "",
                        }
                        new_quotes.append(quote_data)

                except Exception as e:
                    print(e)

        total_pages_scrapped += 1
        pages_got += 1
        # print(new_quotes)
        try:
            next_page = driver.find_element(By.CLASS_NAME, "next_page").click()
        except Exception as e:
            pass
        sleep(randint(60, 180)) if total_pages_scrapped == 50 else sleep(randint(3, 10))

    print(f"\ntotal pages scrapped: {total_pages_scrapped}")

    print(f"completed scrapping: {url}")
    # Append new quotes to existing quotes list
    existing_quotes += new_quotes

    if pages_got >= num_pages:
        urls.remove(url)
        # quotes_want.remove(url)
        with open(quotes_toScrap_file, "w", encoding="utf-8") as f:
            f.writelines(urls)

        # with open(quotes_iwant, "w", encoding="utf-8") as f:
        #     f.writelines(quotes_want)

        # Save quotes to the JSON file
        with open(quotes_file, "w", encoding="utf-8") as f:
            json.dump(existing_quotes, f)

        scrapped_pages.append(url)

        with open(scrapped_pages_file, "w", encoding="utf-8") as f:
            f.writelines(scrapped_pages)

        process_urls.process_urls(quotes_toScrap_file)
