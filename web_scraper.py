# import selenium
# from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

import re
import time
import requests
import pickle

#TODO: add first iteration support

#TODO: add recording of actions
#TODO: add support for regular expression matching in element url field so it only works on urls that match the regex
#TODO: create "add element selector" wizard, checks if valid xpath or css selector in clipboard and adds it to object
#TODO: add exit condition (url contains "x", selector fails, specific selector exists, script has run for n mins)
#TODO: get transcript of all youtube videos https://pypi.org/project/youtube-transcript-api/

class Scraper:
    def __init__(self, name, url, sign_in_url, elements={}):
        self.url = url
        self.elements = elements
        self.status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}
        self.sign_in_url = sign_in_url


# An object representing an element, including all possible methods of locating it (xpath, css selector)
class ElementQuery:
    #  selectors=[[selector, type], [selector, type]]
    def __init__(self, selectors=[]):
        self.selectors = selectors
        self.status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}

    def find(selectors, click=False, timeout=5):
        for index, selector, sel_type in enumerate(selectors):
            status_row["status"] = f"Trying selector {index}"
            # print_row(status_row)
            if index != 0: # Wait for pageload on first selector, do all others as quick as possible
                timeout = 0
            if element := wait_for_elem(selector, sel_type, click, timeout):
                status_row["status"] = "Success"
                # print_row(status_row)
                return element
        status_row["status"] = f"Failed"
        # print_row(status_row)
        return False

    # Add selector to list at index
    # (depending on priority e.g one selector should be tried first because it has a higher chance at succeeding)
    def add_selector(self, selector, sel_type, index=0):
        # By.CSS_SELECTOR
        # By.XPATH
        types = {"xpath": By.XPATH, "css": By.CSS_SELECTOR}
        self.selectors.insert(index, [selector, types[sel_type]])


    def __wait_for_elem(self, selector, sel_type, click=False, timeout = 10):
        try:
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((sel_type, selector)))
            if click:
                element.click()
            return element
        except TimeoutException:
            return False


    def __str__(self):
        print(self.selectors)
        return "none"
        # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())



# s = Service(ChromeDriverManager().install())
# s = webdriver.Chrome(executable_path=ChromeDriverManager(version="115.0.5790.110").install())
# driver = webdriver.Chrome(service=s)



print(f"| Iter Num |        Action         |     Status     | ID")


next_button = ElementQuery([['//*[@id="wiki_page_show"]', "xpath"]])

next_button.add_selector("test", "css", 0)

print(next_button)

# with open("FOAIFS.html", "w", encoding="utf-8") as f:
    # f.write(final_string)

