from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import pandas as pd

url = "https://www.goodreads.com/work/quotes/1858012"
PAGES = 5
profile = 'D:/Documents/python/Twitter_Bot/profiles/common'
opt = Options()

opt.add_argument(f"user-data-dir={profile}")


driver = webdriver.Chrome(
    options=opt, executable_path="C:/programs/chromedriver.exe")
driver.get(url)


author_name = driver.find_elements(By.CLASS_NAME, "authorOrTitle")[0].text
book_name = driver.find_elements(By.CLASS_NAME, "authorOrTitle")[1].text

quote_texts = []
page = 0

while page < PAGES:
    sleep(1)
    page += 1
    quotes = driver.find_elements(By.CLASS_NAME, "quoteText")
    for q in quotes:
        quote_texts.append(q.text)
    sleep(1)
    driver.find_element(By.CLASS_NAME, "next_page").click()
    if page == 2:
        break

pd.DataFrame(quote_texts).to_csv(
    f'D:/Documents/python/Twitter_Bot/book-wisdom-twt/quotes-data/{book_name}.csv', index=False, header=False, encoding='utf-8-sig')

# qdict = {
#     'author': author_name,
#     'title': book_name,
#     'quotes': []
# }

# for i in range(len(quote_texts)):
#     qtext = quote_texts[i]
#     qt_list = qtext.splitlines()[:-1]
#     print(qt_list)
#     qdict['quotes'].append("\n".join(qt_list))

# with open(f'{book_name}.json', 'w') as f:
#     json.dump(qdict, f, indent=4)
#     # convert dictionary to json

driver.quit()
