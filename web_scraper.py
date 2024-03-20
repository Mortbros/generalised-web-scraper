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

import typing

# TODO: add first iteration support
# TODO: add recording of actions
# TODO: add support for regular expression matching in element url field so it only works on urls that match the regex
# TODO: create "add element selector" wizard, checks if valid xpath or css selector in clipboard and adds it to object
# TODO: add exit condition (url contains "x", selector fails, specific selector exists, script has run for n mins)
# TODO: get transcript of all youtube videos https://pypi.org/project/youtube-transcript-api/
# TODO: add WebScraper method that excecutes the next sequence, almost like a pop from the start of the sequence list
# This is so i can run python conditional statements in between the sequences
# TODO: open iframe and grab content from it

DEFAULT_TIMEOUT = 5
ACTION_LIST = ["capture", "click", "validate", "click capture", "send keys", "send keys click"]


class WebScraper:
    def __init__(self, name, url, sign_in_url, sequences: list[ElementSequence], sign_in_sequence: ElementSequence, headless=False):
        self.name = name
        self.url = url
        self.elements = elements
        self.status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}
        self.sign_in_url = sign_in_url
        
        if isinstance(sequences, list):
            if all(isinstance(i, ElementSequence) for i in sequences):
                self.sequences = sequences
            else:
                raise Exception("Invalid list of element sequence, all elements must be of type ElementSequence")
        else:
            raise Exception(f"Invalid list of element sequences, must be of type list (currently {type(sequence)})")

        if isinstance(sequences, ElementSequence):
            self.sign_in_sequence = sign_in_sequence
        else:
            raise Exception(f"Invalid sign in element sequence, must be of ElementSequence (currently {type(sequence)})")

        self.options = Options()
        self.options.headless = headless
        self.driver = webdriver.Chrome(options=self.options)

        self.html = ""

        self.sequence_index = 0

        # self.status_row = StatusRow()

    def write():
        open(f"{self.name}.html", "w", encoding="utf-8").write(self.html)

    def start():
        self.driver.get(url)

    def iterate(iterations: int=1):
        if len(self.sequences) < self.sequence_index + iterations + 1:
            raise Exception(f"Invalid iteration, list is of length {len(self.sequences)}, iteration would access index {sequence_index + iterations + 1}")
        for i in range(self.sequence_index + 1, self.sequence_index + iterations):
            self.sequences[i].run()
        self.sequence_index += iterations

    def sign_in():
        self.driver.get(self.sign_in_url)
        self.sign_in_sequence.run()
        


# class StatusRow:
#     def __init__(self, status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}):
#         vars(self)['status_row'] = status_row

#     def __setattr__(self, attr, value):
#         super.__setattr__(attr, value)
#         print(self)

#     def __str__(self):
#         return "status_row"
#         # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())

class ElementSequence:
    def __init__(self, driver, elements=[], url=None):
        self.driver = driver

        if isinstance(elements, list):
            if len(elements) == 0:
                self.elements = elements
            elif all(isinstance(i, Element) for i in elements):
                self.elements = elements
            else:
                raise Exception("Invalid element sequence, all elements must be of type Element")
        else:
            raise Exception(f"Invalid element sequence must be of type list (currently {type(sequence)})")
        
        self.elements = elements
        self.url = url

    def __add__(self, element):
        if isinstance(element, list):
            for elem in element:
                if isinstance(elem, Element):
                    self.elements.append(element)
                else:
                    raise Exception(f"Invalid element type {type(elem)}")
        else:
            if isinstance(element, Element):
                self.elements.append(element)
    
    def __sub__(self, element):
        if element in self.elements:
            self.elements.remove(element)
        # else:
        #     raise Exception("Element {element} not in sequence")
    
    def run():
        if len(self.elements) != 0:
            if self.url:
                self.driver.get(self.url)
            
            html_out = ""
            for element in self.elements:
                html_out += element.run()
            
            return html_out
        else:
            raise Exception("Cannot run empty ElementSequence")
# An object representing an element, including all possible methods of locating it (xpath, css selector)
class Element:
    def __init__(self, name, selectors: list[Selector]=[], action="click", timeout=DEFAULT_TIMEOUT):
        self.name = name

        if not all(isinstance(sel, Selector) for sel in selectors):
            raise Exception("Invalid selector")

        self.selectors = selectors
        # self.status_row = StatusRow()
        self.status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}
        
        if not isinstance(action, list):
            raise Exception("Actions must be a list")
        
        if action in ACTION_LIST:
            self.action = action
        else:
            raise Exception("Invalid action found")
        
    def run():
        # It is left to the user to manage superfluous actions
        html_out = ""
        if self.action == "click":
            self.find(click=True)
        elif self.action == "validate":
            self.find()
        elif self.action == "capture":
            html_out = self.find().get_attribute("innerHTML")
        elif self.action == "click capture":
            html_out = self.find(click=True).get_attribute("innerHTML")
        elif self.action == "send":
            html_out = self.find(click=True).get_attribute("innerHTML")
        elif self.action == "click capture":
            html_out = self.find(click=True).get_attribute("innerHTML")

        if not html_out:
            html_out = ""
        
        return html_out
        

    def find(self, click=False, timeout=self.timeout):
        for index, selector in enumerate(self.selectors):
            sel_value = selector.sel_value
            sel_type = selector.sel_type
            
            status_row["status"] = f"Trying selector {index}"
            # print_row(status_row)
            # Wait for pageload on first selector, do all others as quick as possible
            # This shouldn't need to be modified by the user, as you can't run selectors when the page hasnt been loaded
            if index == 0: 
                timeout = 0
            if element := wait_for_elem(sel_value, sel_type, click, timeout):
                status_row["status"] = "Element found"
                # print_row(status_row)
                return element
        status_row["status"] = "Element not found"
        # print_row(status_row)
        return False

    # Add selector to list at index
    # (depending on priority e.g one selector should be tried first because it has a higher chance at succeeding)
    def add_selector(self, selector: Selector, index=-1):
        types = {"xpath": By.XPATH, "css": By.CSS_SELECTOR}
        self.selectors.insert(index, [selector, types[sel_type]])


    def __wait_for_elem(self, selector, sel_type, click=False, timeout = 10):
        try:
            elem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((sel_type, selector)))
            if self.click:
                elem.click()
            return elem
        except TimeoutException:
            return False


    def __str__(self):
        print(self.selectors)
        return "none"
        # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())

class Selector:
    def __init__(self, sel_value: str, sel_type=None):
        self.sel_value = sel_value

        if sel_type:
            self.sel_type = sel_type
        else:
            # Auto-detect the selector type
            if sel_value[0] == "/":
                self.sel_type = By.XPATH
            else: #TODO: this is fragile
                self.sel_type = By.CSS_SELECTOR

    
    def __iter__(self):
        return iter([sel_value, sel_type])