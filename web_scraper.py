from re import M
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import time

import typing

# TODO: download all videos, grab transcript, add to HTML
# TODO: open iframe and grab content from it
    # iframe_capture="all"|"extract body"|[ElementSequence]
    # run a sequence if a specific condition is met in the URL
    # Or just grab entire HTML and append
    # Or run a list of elementSequences until HTML is extracted, else just grab entire HTML
    # OPTIONAL: Flag for recursive iframe html extraction
# TODO: status row
# TODO: get transcript of all youtube videos https://pypi.org/project/youtube-transcript-api/
# TODO: add support for regular expression matching in element url field so it only works on urls that match the regex
# TODO: figure out a better way of passing the driver around, maybe via object inheritance?
# TODO: create "add element selector" wizard, checks if valid xpath or css selector in clipboard and adds it to object
# TODO: add exit condition (url contains "x", selector fails, specific selector exists, script has run for n mins)
# TODO: record successes for element selectors and reorder list depending on how likely each selector is to succeed
# TODO: documentation
# TODO: talk about return types (specifically the return type of the element object) and code strictness with xena
# TODO: replace all Exception("...") with actual errors


DEFAULT_TIMEOUT = 10
RESTART_DELAY = 2
IFRAME_ACTION_LIST = {"html", "body"}
ELEMENT_FIND_MODES = ["run for n time", "wait per selector"]
IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)



class ElementExistsError(Exception):
    """Raised if the element exists when it shouldn't"""
    pass

class ElementNotFoundError(Exception):
    """Raised if the element doesn't exist when it should"""
    pass


# st is used with numbers ending in 1
# nd is used with numbers ending in 2
# rd is used with numbers ending in 3
# As an exception to the above rules, numbers ending with 11, 12, and 13 use -th (e.g. 11th, pronounced eleventh, 112th, pronounced one hundred [and] twelfth)
# th is used for all other numbers (e.g. 9th, pronounced ninth)
def ordinal_suffix(i):
    i = str(i)
    if i[-1] == "1" and not i[-2:] == "11":
        return "st"
    elif i[-1] == "2" and not i[-2:] == "12":
        return "nd"
    elif i[-1] == "3" and not i[-2:] == "13":
        return "rd"
    else:
        return "th"
    


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
            raise Exception(f"Invalid sign in element sequence, must be of ElementSequence (currently {type(sequences)})")

        self.options = Options()
        self.options.headless = headless
        self.driver = webdriver.Chrome(options=self.options)

        self.html = ""

        self.sequence_index = 0

        # self.status_row = StatusRow()

    def run(self):
        self.sign_in()
        self.start()
        self.iterate_sequence()
        self.write()
    
    def write(self):
        open(f"{self.name}.html", "w", encoding="utf-8").write(self.html)

    # TODO: rename this function or combine it with something else
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
            raise Exception(f"Invalid element sequence must be of type list (currently {type(elements)})")
        
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
            # TODO: i'm not the biggest fan of moving over a block of code to the _excecute_iteration private function
            if self.run_until_fail:
                iteration = 1
                while True:
                    print(f"\tExcecuting sequence: {self.name}, iteration {iteration}")
                    if not self._excecute_iteration(driver):
                        break
                    iteration += 1
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
            driver.get(self.url)

        try:
            for element in self.elements:
                element_out = element.run(driver=driver)
                if element.capture_attribute == "innerHTML":
                    self.html += element_out
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
    def __init__(self, name, selectors=[], mode="run for n time", capture_attribute="", click=False, return_on_click=False, send_values=None, clear=True, ensure_absence=False, critical=True, timeout=DEFAULT_TIMEOUT, pageload_wait=0, url=None, iframe_capture="", retry_on_stale: int=5):
        self.name = name

        if mode not in ELEMENT_FIND_MODES:
            raise Exception(f"Invalid Element mode type: {mode}")
        else:
            self.mode = mode

        # if not all(isinstance(sel, Selector) for sel in selectors):
        #     raise Exception("Invalid selector")

        # selectors could be a string, Selector, or list of a combination of strings or selectors
        if isinstance(selectors, str):
            self.selectors = [Selector(selectors)]
        elif isinstance(selectors, Selector):
            self.selectors = [selectors]
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
        
        self.capture_attribute = capture_attribute
        self.click = click
        self.return_on_click = return_on_click
        self.send_values = send_values
        self.clear = clear
        self.ensure_absence = ensure_absence

        self.critical = critical

        self.send_values = send_values

        self.timeout = timeout
        self._loop_timeout = timeout

        # this only exists because, in some cases, a Element can grab the wrong html element before the page is fully loaded.
        # the element's selector will succeed in matching, but it won't be what we are looking for
        self.pageload_wait = pageload_wait
        self._last_url = None
        
        self.url = url

        # Brackets for readability
        if (not iframe_capture) or (iframe_capture in IFRAME_ACTION_LIST):
            self.iframe_capture = iframe_capture
        else:
            raise Exception("Invalid iframe capture method")
        
        self.retry_on_stale = retry_on_stale
        self._current_retry_on_stale = retry_on_stale

        # self.status_row = StatusRow()
        
    def run(self, driver):
        out = None
        current_url = driver.current_url
        if self.pageload_wait > 0 and current_url != self._last_url:
            print(f"\t\tWaiting for pageload ({self.pageload_wait}s)")
            self._last_url = current_url
            time.sleep(self.pageload_wait)
        
        if self.mode == ELEMENT_FIND_MODES[0]:
            self.timeout = 0
            end_time = time.time() + self._loop_timeout
            while time.time() < end_time and not out:
                out = self.find(driver)
                self._current_retry_on_stale = self.retry_on_stale
        
        elif self.mode == ELEMENT_FIND_MODES[1]:
            out = self.find(driver)

        self._current_retry_on_stale = self.retry_on_stale

        return out
    
    
    def find(self, driver):
        
        attribute_catches = []
        return_status = False

        for i, selector in enumerate(self.selectors):
            print(f"\t\tFinding element: {self.name}, selector {selector} ")
            
            try:
                elements = []
                try:
                    elements = WebDriverWait(driver, self.timeout, ignored_exceptions=IGNORED_EXCEPTIONS).until(EC.presence_of_all_elements_located((selector.sel_type, selector.sel_value)))
                except TimeoutException:
                    print(f"\t\t\tFailed to find element with {i + 1}{ordinal_suffix(i + 1)} selector")

                if len(elements) > 0:
                    print("\t\t\tSuccess: Element found")
                    return_status = True
                
                for element in elements:
                    if self.ensure_absence:
                        raise ElementExistsError(f"Element '{self.name}' found when it shouldn't exist, selector '{selector}'")
                    
                    if self.click:
                        element.click()
                        if self.return_on_click:
                            return True
                    if self.send_values:
                        if self.clear:
                            element.clear()
                        element.send_keys(self.send_values)
                    
                        
                    if self.capture_attribute:
                        attribute_value = element.get_attribute(self.capture_attribute)
                        if self.capture_attribute == "innerHTML":
                            if isinstance(attribute_catches, list):
                                attribute_catches = "".join(attribute_catches)
                            attribute_catches += attribute_value
                        else:
                            attribute_catches.append(attribute_value)
                
                # TODO: untested
                if self.iframe_capture:
                    # This is probably bad practice, but it works(?)

                    IFRAME_ELEMENT_SRC = Element(name="(Internal) Iframe capture URL source", selectors=Selector("iframe", By.TAG_NAME), timeout=5, capture_attribute="src", critical=False)

                    iframe_srcs = IFRAME_ELEMENT_SRC.run(driver)
                    if iframe_srcs:
                        
                        BODY_ELEMENT_HTML = Element(name="(Internal) Iframe capture innerHTML", selectors=Selector("body", By.TAG_NAME), iframe_capture="body", timeout=5, capture_attribute="innerHTML", critical=False)
                        
                        for iframe_src in iframe_srcs:
                            # TODO: mac support with Keys.COMMAND?
                            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

                            driver.get(iframe_src)
                            if new_tab_html := BODY_ELEMENT_HTML.run(driver):
                                attribute_catches = attribute_catches + new_tab_html

                            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
        
            except StaleElementReferenceException as e:
                if self._current_retry_on_stale <= 0:
                    raise e
                else:
                    print(f"\t\t\tRetrying due to stale element ({self._current_retry_on_stale} tr{'ies' if self._current_retry_on_stale > 1 else 'y'} left)")
                    self._current_retry_on_stale -= 1
                    self.run(driver)
            
        if self.ensure_absence:  # exit if the element must appear
            print("\t\t\tSuccess: Element not found (yes really)")
            return True
        elif self.critical and not return_status:
            raise ElementNotFoundError(f"Element '{self.name}' not found")
        elif self.capture_attribute:
            return attribute_catches
        else:
            if not return_status:
                print("\t\t\tFailed: Element not found")
            return return_status

    # # Add selector to list at index
    # # (depending on priority e.g one selector should be tried first because it has a higher chance at succeeding)
    # def add_selector(self, selector, index=-1):
    #     types = {"xpath": By.XPATH, "css": By.CSS_SELECTOR}
    #     self.selectors.insert(index, [selector, types[sel_type]])


    def __str__(self):
        return str(self.selectors)
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

    # Selector[0] = self.sel_value, Selector[1] = self.sel_type
    def __iter__(self):
        return iter([self.sel_value, self.sel_type])
    
    def __str__(self):
        return f"{self.sel_value} (type \"{self.sel_type}\")"