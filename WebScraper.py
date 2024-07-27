from ElementSequence import ElementSequence
from DownloadHandler import DownloadHandler

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


# The config class should not need to exist, all the scraper configuration should be set using function inputs.


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
        root_path=os.getcwd(),
    ):
        self.download_handler = DownloadHandler()
        self.name = "".join(l for l in name if l not in "\\/:*?\"<>',")
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

        # directory structure looks like this
        # Configured root path
        # └───Web Scraper output
        #     ├───Web Scraper 1 Name
        #     │   │    Web Scraper 1 HTML output
        #     │   └─── Downloads
        #     │           Downloaded files
        #     ├───Web Scraper 2 Name
        #     │   │    Web Scraper 2 HTML output
        #     │   └─── Downloads
        #     │           Downloaded files
        #     └───Web Scraper 3 Name
        #         │    Web Scraper 3 HTML output
        #         └─── Downloads
        #                 Downloaded files
        # we cd into the web scraper directory each time the scraper is ran, then cd out for repeatability

        # os.path.exists fails if input is None
        if root_path and not os.path.exists(root_path):
            raise Exception(f"Invalid root path '{root_path}'")

        self._current_scraper_path = os.path.join(
            root_path, "Web Scraper output", self.name
        )

        self.download_path = os.path.join(self._current_scraper_path, "Downloads")

        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path, exist_ok=True)

        self._original_path = os.getcwd()
        self._original_path = os.getcwd()

        options = Options()
        options.headless = headless

        # alternate option for setting download directory
        # prefs = {"download.default_directory": "C:\\Tutorial\\down"}
        # options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options)

        self.download_handler = DownloadHandler()

        self.unique_file_name = unique_file_name

        self.html = ""

        self.sequence_index = 0

        # self.status_row = StatusRow()

    def run(self):
        try:
            os.chdir(self._current_scraper_path)
            self.download_handler.set_download_path(self.driver, self.download_path)
            self.html = ""
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
