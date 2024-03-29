from Selector import Selector
from web_scraper_errors import ElementExistsError, ElementNotFoundError

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import time



DEFAULT_TIMEOUT = 10
IFRAME_ACTION_LIST = {"html", "body"}
ELEMENT_FIND_MODES = ["run for n time", "wait per selector"]
IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

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

# An object representing an element, including all possible methods of locating it (xpath, css selector)
class Element:
    def __init__(
        self,
        name,
        selectors=[],
        mode="run for n time",
        capture_attribute="",
        content_contains="",
        click=False,
        return_on_click=False,
        send_values=None,
        clear=True,
        ensure_absence=False,
        critical=True,
        timeout=DEFAULT_TIMEOUT,
        pageload_wait=0,
        url=None,
        iframe_capture="",
        retry_on_stale: int = 5,
    ):
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
        self.content_contains = content_contains.lower()
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
                    elements = WebDriverWait(
                        driver, self.timeout, ignored_exceptions=IGNORED_EXCEPTIONS
                    ).until(
                        EC.presence_of_all_elements_located(
                            (selector.sel_type, selector.sel_value)
                        )
                    )
                except TimeoutException:
                    print(
                        f"\t\t\tFailed to find element with {i + 1}{ordinal_suffix(i + 1)} selector"
                    )

                if len(elements) > 0:
                    print("\t\t\tSuccess: Element found")
                    return_status = True

                for element in elements:
                    if self.ensure_absence:
                        raise ElementExistsError(
                            f"Element '{self.name}' found when it shouldn't exist, selector '{selector}'"
                        )

                    if self.content_contains:
                        if self.content_contains in element.get_attribute("innerHTML").lower():
                            print(
                                f"\t\t\tSuccess: Element innerHTML contains content '{self.content_contains}'"
                            )
                        else:
                            print(
                                f"\t\t\tFailed:Element innerHTML doesn't contain content '{self.content_contains}'"
                            )
                            return_status = False
                            continue

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

                    IFRAME_ELEMENT_SRC = Element(
                        name="(Internal) Iframe capture URL source",
                        selectors=Selector("iframe", By.TAG_NAME),
                        timeout=5,
                        capture_attribute="src",
                        critical=False,
                    )

                    iframe_srcs = IFRAME_ELEMENT_SRC.run(driver)
                    if iframe_srcs:

                        BODY_ELEMENT_HTML = Element(
                            name="(Internal) Iframe capture innerHTML",
                            selectors=Selector("body", By.TAG_NAME),
                            iframe_capture="body",
                            timeout=5,
                            capture_attribute="innerHTML",
                            critical=False,
                        )

                        for iframe_src in iframe_srcs:
                            # TODO: mac support with Keys.COMMAND?
                            driver.find_element_by_tag_name("body").send_keys(
                                Keys.CONTROL + "t"
                            )

                            driver.get(iframe_src)
                            if new_tab_html := BODY_ELEMENT_HTML.run(driver):
                                attribute_catches = attribute_catches + new_tab_html

                            driver.find_element_by_tag_name("body").send_keys(
                                Keys.CONTROL + "w"
                            )

            except StaleElementReferenceException as e:
                if self._current_retry_on_stale <= 0:
                    raise e
                else:
                    print(
                        f"\t\t\tRetrying due to stale element ({self._current_retry_on_stale} tr{'ies' if self._current_retry_on_stale > 1 else 'y'} left)"
                    )
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
    
    def reset(self):
        pass

    def __str__(self):
        return str(self.selectors)
        # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())