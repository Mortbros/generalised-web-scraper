from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time
import requests

import typing

# TODO: download all videos, grab transcript, add to HTML
# TODO: open iframe and grab content from it
# TODO: get transcript of all youtube videos https://pypi.org/project/youtube-transcript-api/
# TODO: add recording of actions
# TODO: add support for regular expression matching in element url field so it only works on urls that match the regex
# TODO: create "add element selector" wizard, checks if valid xpath or css selector in clipboard and adds it to object
# TODO: add exit condition (url contains "x", selector fails, specific selector exists, script has run for n mins)
# TODO: figure out a better way of passing the driver around, maybe via object inheritance?
# TODO: documentation

DEFAULT_TIMEOUT = 10
RESTART_DELAY = 2
ACTION_LIST = ["click", "validate", "capture", "click capture", "send", "send clear", "send click", "send clear click", "click capture", "send click capture", "send clear click capture", "ensure_absence"]


class ElementExistsError(Exception):
    """Raised if the element exists when it shouldn't"""
    pass

class ElementNotFoundError(Exception):
    """Raised if the element doesn't exist when it should"""
    pass


class WebScraper:
    def __init__(self, name, url, sign_in_url, sequences, sign_in_sequence, headless=False):
        self.name = name
        self.url = url
        self.status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}
        self.sign_in_url = sign_in_url
        
        if isinstance(sequences, list):
            if all(isinstance(i, ElementSequence) for i in sequences):
                self.sequences = sequences
            else:
                raise Exception("Invalid list of element sequence, all elements must be of type ElementSequence")
        elif isinstance(sequences, ElementSequence):
            self.sequences = [sequences]
        else:
            raise Exception(f"Invalid list of element sequences, must be of type list (currently {type(sequences)})")

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

    def write(self):
        open(f"{self.name}.html", "w", encoding="utf-8").write(self.html)

    def start(self):
        print(f"Starting scraper: {self.name}")
        self.driver.get(self.url)

    def iterate_sequence(self, iterations: int=1):
        if len(self.sequences) < self.sequence_index + iterations:
            raise Exception(f"Invalid iteration, list is of length {len(self.sequences)}, iteration would access index {self.sequence_index + iterations + 1}")
        for i in range(self.sequence_index, self.sequence_index + iterations):
            print(f"Running {self.name} scraper sequence {i}:")
            self.html += self.sequences[i].run(driver=self.driver)
        self.sequence_index += iterations

    def sign_in(self):
        print(f"Signing into scraper: {self.name}")
        self.driver.get(self.sign_in_url)
        self.sign_in_sequence.run(driver=self.driver)
        

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
    def __init__(self, name, elements=[], url=None, run_until_fail=False, restart_on_fail: int=1, restart_delay=RESTART_DELAY):
        self.html = ""
        
        self.name = name

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

        self.run_until_fail = run_until_fail
        self.restart_on_fail = restart_on_fail
        self.restart_delay = restart_delay

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
    
    # Runs iteration
    def run(self, driver):
        # This check is located here because an ElementSequence can be initialised with no elements, then populated later 
        if len(self.elements) != 0:
            # TODO: i'm not the biggest fan of moving over a block of code to a private function
            if self.run_until_fail:
                iteration = 0
                while True:
                    print(f"\tExcecuting sequence: {self.name}, iteration {iteration}")
                    if not self._excecute_iteration(driver):
                        break
            else:
                for r in range(self.restart_on_fail):
                    print(f"\tExcecuting sequence: {self.name}, attempt {r + 1}")
                    if self._excecute_iteration(driver):
                        break
                else:
                    raise Exception(f"Element sequence \"{self.name}\" failed to find and validate after {self.restart_on_fail} attempts")
            
            print("\t\tFinished after failing to find")
        else:
            raise Exception("Cannot run empty ElementSequence")
        return self.html
    
    def _excecute_iteration(self, driver):
        if self.url:
            self.driver.get(self.url)

        try:
            for element in self.elements:
                self.html += element.run(driver=driver)
            return True
        except ElementExistsError:
            time.sleep(self.restart_delay)
        except ElementNotFoundError as e:
            if self.run_until_fail:
                return False
            else:
                raise ElementNotFoundError(e)
        


# An object representing an element, including all possible methods of locating it (xpath, css selector)
class Element:
    def __init__(self, name, selectors=[], action="click", critical=True, send_values=None, timeout=DEFAULT_TIMEOUT, url=None):
        self.name = name

        # if not all(isinstance(sel, Selector) for sel in selectors):
        #     raise Exception("Invalid selector")

        # selectors could be a string, Selector, or list of a combination of strings or selectors
        if isinstance(selectors, str):
            self.selectors = [Selector(selectors)]
        elif isinstance(selectors, list):
            self.selectors = []
            for s in selectors:
                if isinstance(s, str):
                    self.selectors.append(Selector(s))
                elif isinstance(s, Selector):
                    self.selectors.append(s)
                else:
                    raise Exception(f"Invalid selector type '{type(s)}'")
        else:
            raise Exception(f"Invalid selector type '{type(selectors)}'")

        if action in ACTION_LIST:
            self.action = action
        else:
            raise Exception(f"Invalid action found: '{action}' not in list of actions")
        
        self.critical = critical
        
        self.send_values = send_values

        self.timeout = timeout

        self.url = url
        
        # self.status_row = StatusRow()
        self.status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}
        
    def run(self, driver):
        # It is left to the user to manage superfluous actions
        
        if self.url:
            driver.get(self.url)

        # TODO: This is poorly written, i need a better way to initialise the run type/self.action on object instantiation 
        html_out = ""
        if self.action == "click":
            self.find(driver=driver, click=True)
        elif self.action == "validate":
            self.find(driver=driver)
        elif self.action == "capture":
            elem_out = self.find(driver=driver)
        elif self.action == "click capture":
            elem_out = self.find(driver=driver, click=True)
        elif self.action == "send":
            elem_out = self.find(driver=driver, send_values=self.send_values)
        elif self.action == "send noclear":
            elem_out = self.find(driver=driver, send_values=self.send_values, clear=False)
        elif self.action == "send click":
            elem_out = self.find(driver=driver, click=True, send_values=self.send_values)
        elif self.action == "send noclear click":
            elem_out = self.find(driver=driver, click=True, send_values=self.send_values, clear=False)
        elif self.action == "click capture":
            elem_out = self.find(driver=driver, click=True)
        elif self.action == "send click capture":
            elem_out = self.find(driver=driver, click=True, send_values=self.send_values)
        elif self.action == "send noclear click capture":
            elem_out = self.find(driver=driver, click=True, send_values=self.send_values, clear=False)
        elif self.action == "ensure_absence":
            self.find(driver=driver, ensure_absence=True)


        if "capture" in self.action:
            html_out = elem_out.get_attribute("innerHTML")

        if not html_out:
            html_out = ""
        
        return html_out
        

    def find(self, driver, click=False, clear=True, send_values=None, timeout=None, ensure_absence=False):
        if not timeout:
            if self.timeout:
                timeout = self.timeout
            else:
                timeout = DEFAULT_TIMEOUT
        
        for index, selector in enumerate(self.selectors):
            print(f"\t\tFinding element: {self.name}, selector {selector} ")
            sel_value = selector.sel_value
            sel_type = selector.sel_type
            # status_row["status"] = f"Trying selector {index}"
            
            # Wait for pageload on first selector, do all others as quick as possible
            # This shouldn't need to be modified by the user, as you can't run selectors when the page hasn't been loaded
            if index == 0: 
                timeout = 0
            if element := self._wait_for_elem(driver, sel_value, sel_type, click, timeout):
                if ensure_absence:
                    raise ElementExistsError(f"Element '{self.name}' found when it shouldn't exist")

                # status_row["status"] = "Element found"
                # print_row(status_row)
                if send_values:
                    if clear:
                        element.clear()
                    element.send_keys(send_values)
                print("\t\t\tSuccess: Element found")
                return element
        # status_row["status"] = "Element not found"
        # print_row(status_row)

        # exit if the element must appear
        if ensure_absence:
            print("\t\t\tSuccess: Element not found (yes really)")
            return True
        elif self.critical:
            raise ElementNotFoundError(f"Element '{self.name}' not found")
        else:
            print("\t\t\tFailed: Element not found")


    # # Add selector to list at index
    # # (depending on priority e.g one selector should be tried first because it has a higher chance at succeeding)
    # def add_selector(self, selector, index=-1):
    #     types = {"xpath": By.XPATH, "css": By.CSS_SELECTOR}
    #     self.selectors.insert(index, [selector, types[sel_type]])


    def _wait_for_elem(self, driver, selector, sel_type, click=False, timeout=DEFAULT_TIMEOUT):
        try:
            elem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((sel_type, selector)))
            if click:
                elem.click()
            return elem
        except TimeoutException:
            return False


    def __str__(self):
        return self.selectors
        # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())

class Selector:
    def __init__(self, sel_value: str, sel_type=None):
        self.sel_value = sel_value

        if sel_type:
            self.sel_type = sel_type
        else:
            # Auto-detect the selector type
            #TODO: this is fragile
            if sel_value[0] == "/":
                self.sel_type = By.XPATH
            else:
                self.sel_type = By.CSS_SELECTOR

    
    def __iter__(self):
        return iter([sel_value, sel_type])
    
    def __str__(self):
        return f"{self.sel_value} (type \"{self.sel_type}\")"