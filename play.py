# from time import sleep
# from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options

# # Specify the path to your custom profile directory
# profile_path = "C:/programs/Browerbots/wzxw2qjx.firefoxbot1"

# # Set up the options for Firefox
# options = Options()

# # Load the custom profile
# options.profile = webdriver.FirefoxProfile(profile_path)

# # Initialize the WebDriver for Firefox using the WebDriver Manager
# driver = webdriver.Firefox(
#     service=Service(GeckoDriverManager().install()), options=options
# )

# # Now you can navigate using the custom profile
# driver.get("https://www.goodreads.com")

# # Do any automation work
# print(driver.title)
# sleep(300)
# # Close the browser
# driver.quit()

import langid

my_list = ["one", "two-two", "three"]

for i, name in enumerate(my_list):
    li_li = name.split("-")
    if len(li_li) > 1:
        del my_list[i]

print(my_list)
