from ElementSequence import ElementSequence

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException

from datetime import datetime

import os

# TODO: status row
# TODO: figure out a better way of passing the driver around, maybe via object inheritance?
# TODO: create "add element selector" wizard, checks if valid xpath or css selector in clipboard and adds it to object
# TODO: documentation
# TODO: replace all Exception("...") with actual errors
# TODO: add Ctrl + D to force stop the page loading if the page is taking forever to load (and i mean forever, like 30 seconds)


class WebScraper:
    def __init__(
        self,
        name,
        url,
        sign_in_url,
        sequences,
        sign_in_sequence,
        headless=False,
        unique_file_name=True,
    ):
        self.name = name
        self.url = url
        self.status_row = {
            "iter_num": 0,
            "action": "Adding body to string",
            "status": None,
            "ID": None,
        }
        self.sign_in_url = sign_in_url

        if isinstance(sequences, list):
            if all(isinstance(i, ElementSequence) for i in sequences):
                self.sequences = sequences
            else:
                raise Exception(
                    "Invalid list of element sequence, all elements must be of type ElementSequence"
                )
        elif isinstance(sequences, ElementSequence):
            self.sequences = [sequences]
        else:
            raise Exception(
                f"Invalid list of element sequences, must be of type list (currently {type(sequences)})"
            )

        if isinstance(sequences, ElementSequence):
            self.sign_in_sequence = sign_in_sequence
        else:
            raise Exception(
                f"Invalid sign in element sequence, must be of ElementSequence (currently {type(sequences)})"
            )

        # Directory structure looks like this
        # │ Code Files here
        # └───Web Scraper downloads
        #     ├───Web Scraper 1 Name
        #     │       Web Scraper 1 Files
        #     ├───Web Scraper 2 Name
        #     │       Web Scraper 2 Files
        #     └───Web Scraper 3 Name
        #             Web Scraper 3 Files
        # We cd into the web scraper directory each time the scraper is ran, then cd out for repeatability
        downloads_path = os.path.join(os.getcwd(), "WebScraper downloads")
        self._original_path = os.getcwd()
        self._current_scraper_path = os.path.join(downloads_path, self.name)
        # TODO: name validation, make the name a valid path
        if not os.path.exists(downloads_path):
            os.mkdir(downloads_path)
        if not os.path.exists(self._current_scraper_path):
            os.mkdir(self._current_scraper_path)

        options = Options()
        options.headless = headless
        # Doesn't work
        options.add_argument(f"download.default_directory={self._current_scraper_path}")
        self.driver = webdriver.Chrome(options=options)

        self.unique_file_name = unique_file_name

        self.html = ""

        self.sequence_index = 0

        # self.status_row = StatusRow()

    def run(self):
        try:
            os.chdir(self._current_scraper_path)
            self.sign_in()
            self.open_url()
            self.iterate_sequence()
            self.write()
            os.chdir(self._original_path)
        except NoSuchWindowException:
            # TODO: this doesn't do what i want it to. an empty html file is created
            print("Window closed, writing to file")
            self.write()

    def write(self):
        filename = f"{self.name}{datetime.now().strftime(' %Y-%m-%d_%H-%M-%S') if self.unique_file_name else ''}.html"
        print(f"Writing to file {filename}")
        print(len(self.html))
        print(self.html)
        open(
            filename,
            "w",
            encoding="utf-8",
        ).write(self.html)

    # TODO: rename this function or combine it with something else
    def open_url(self):
        print(f"Starting scraper: {self.name}")
        self.driver.get(self.url)

    def iterate_sequence(self, iterations: int = 1):
        if len(self.sequences) < self.sequence_index + iterations:
            raise Exception(
                f"Invalid iteration, list is of length {len(self.sequences)}, iteration would access index {self.sequence_index + iterations + 1}"
            )
        for i in range(self.sequence_index, self.sequence_index + iterations):
            print(f"Running {self.name} scraper sequence {i}:")
            self.html += self.sequences[i].run(driver=self.driver)
        self.sequence_index += iterations

    def sign_in(self):
        print(f"Signing into scraper: {self.name}")
        self.driver.get(self.sign_in_url)
        self.sign_in_sequence.run(driver=self.driver)

    def reset(self):
        pass
