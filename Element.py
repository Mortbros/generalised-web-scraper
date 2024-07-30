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
import os
import json


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


# an object representing an element, including all possible methods of locating it (xpath, css selector)
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
        download_files=False,
        iframe_capture="",
        banned_iframe_url_snippets=["about:blank"],
        retry_on_stale: int = 5,
    ):
        self.name = name

        if mode not in ELEMENT_FIND_MODES:
            raise ElementNotFoundError(
                f"Invalid Element mode type '{mode}', not found in '{ELEMENT_FIND_MODES}'"
            )
        else:
            self.mode = mode

        # if not all(isinstance(sel, Selector) for sel in selectors):
        #     raise ElementNotFoundError("Invalid selector")

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
                    raise ElementNotFoundError(f"Invalid selector type '{type(s)}'")
        else:
            raise ElementNotFoundError(f"Invalid selector type '{type(selectors)}'")

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

        self.download_files = download_files
        # we cannot initialise the downloaded_files variable here because the Element class can be instantiated outside of a WebScraper instance
        self._downloaded_files = None

        if (not iframe_capture) or (iframe_capture in IFRAME_ACTION_LIST):
            self.iframe_capture = iframe_capture
        else:
            raise ElementNotFoundError(
                f"Invalid iframe capture method, iframe_capture '{iframe_capture}' not present in '{IFRAME_ACTION_LIST}'"
            )

        if isinstance(banned_iframe_url_snippets, list):
            self.banned_iframe_url_snippets = banned_iframe_url_snippets
            if "about:blank" not in self.banned_iframe_url_snippets:
                self.banned_iframe_url_snippets.append("about:blank")
        else:
            raise TypeError("Invalid banned iframe url snippets, must be of type list")

        # the element may change in the time between finding it and using it,
        # causing a StaleElementReferenceException. Retry retry_on_stale times when this happens
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

        # try and find the element as many times as possible until the timeout
        # there is 0 timeout for the individual searches, instead a timeout overall
        if self.mode == ELEMENT_FIND_MODES[0]:
            self.timeout = 0
            end_time = time.time() + self._loop_timeout
            while time.time() < end_time and not out:
                out = self.find(driver)
                self._current_retry_on_stale = self.retry_on_stale
        # try and find the element once, with default timeouts
        elif self.mode == ELEMENT_FIND_MODES[1]:
            out = self.find(driver)

        # reset retry_on_stale attempts, for potential reruns of this element
        self._current_retry_on_stale = self.retry_on_stale

        return out

    def find(self, driver):
        attribute_catches = []
        return_status = False

        if self.download_files:
            self._downloaded_files = {"downloaded_files": []}
            # store links to downloaded files in a JSON file to prevent downloading a file mulitple times
            if not os.path.isfile("downloaded_files.json"):
                with open("downloaded_files.json", "w") as f:
                    json.dump(self._downloaded_files, f)
            else:
                with open("downloaded_files.json", "r") as f:
                    self._downloaded_files = json.load(f)

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
                        if (
                            self.content_contains
                            in element.get_attribute("innerHTML").lower()
                        ):
                            print(
                                f"\t\t\tSuccess: Element innerHTML contains content '{self.content_contains}'"
                            )
                        else:
                            print(
                                f"\t\t\tFailed: Element innerHTML doesn't contain content '{self.content_contains}'"
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
                            print("\t\t\tCapturing HTML")
                        else:
                            attribute_catches.append(attribute_value)
                    if self.download_files:
                        # the dot at the start of the xpath means that we only search for download links contained in the current element
                        download_link_elem = element.find_elements(
                            By.XPATH, ".//*[@download and @href]"
                        )
                        # TODO: wait for downloads to finish in order to quit
                        if len(download_link_elem) > 0:
                            for dl in [
                                dle.get_attribute("href")
                                for dle in download_link_elem
                                if dle.get_attribute("href")
                                not in self._downloaded_files["downloaded_files"]
                            ]:
                                driver.execute_script(f"window.open('{dl}','_blank');")
                                driver.switch_to.window(driver.window_handles[0])
                                self._downloaded_files["downloaded_files"].append(dl)

            except StaleElementReferenceException as e:
                if self._current_retry_on_stale <= 0:
                    raise e
                else:
                    print(
                        f"\t\t\tRetrying due to stale element ({self._current_retry_on_stale} tr{'ies' if self._current_retry_on_stale > 1 else 'y'} left)"
                    )
                    self._current_retry_on_stale -= 1
                    self.run(driver)

        if self.iframe_capture:
            # this is probably bad practice, but it works

            IFRAME_ELEMENT_SRC = Element(
                name="(Internal) Iframe capture URL source",
                selectors=Selector("iframe", By.TAG_NAME),
                timeout=5,
                capture_attribute="src",
                critical=False,
            )

            iframe_srcs = IFRAME_ELEMENT_SRC.run(driver)
            if iframe_srcs:
                # filter out invalid/banned iframe url snippets
                iframe_srcs = [
                    f
                    for f in iframe_srcs
                    if f and not any(b in f for b in self.banned_iframe_url_snippets)
                ]
                for iframe_src in iframe_srcs:
                    print(
                        f"\t\t\tOpening iframe url, extracting {self.iframe_capture} element: {iframe_src}"
                    )
                    driver.execute_script(f"window.open('{iframe_src}','_blank');")
                    driver.switch_to.window(driver.window_handles[1])

                    if (
                        new_tab_html := WebDriverWait(driver, DEFAULT_TIMEOUT)
                        .until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        .get_attribute("innerHTML")
                    ):
                        if isinstance(attribute_catches, list):
                            attribute_catches = "".join(attribute_catches)
                        attribute_catches += (
                            "BEGIN IFRAME HTML INSERTION"
                            + new_tab_html
                            + "END IFRAME HTML INSERTION"
                        )

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        # write list of links that have been downloaded to file
        if self.download_files:
            with open("downloaded_files.json", "w") as f:
                json.dump(self._downloaded_files, f)

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

    # # add selector to list at index
    # # (depending on priority e.g one selector should be tried first because it has a higher chance at succeeding)
    # def add_selector(self, selector, index=-1):
    #     types = {"xpath": By.XPATH, "css": By.CSS_SELECTOR}
    #     self.selectors.insert(index, [selector, types[sel_type]])

    def reset(self):
        pass

    def __str__(self):
        return str(self.selectors)
        # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())
