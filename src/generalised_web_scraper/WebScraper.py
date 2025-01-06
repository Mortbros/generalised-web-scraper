from .ElementSequence import ElementSequence
from .DownloadHandler import DownloadHandler

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException

from document_merger import DocumentMerger, DocumentMergerConfig
import os

from datetime import datetime

import os

# Sorted from most to least relevant
# TODO: documentation
# TODO: figure out a better way of passing the driver around, maybe via object inheritance?
# TODO: move the web_scraper_data.json file from each directory into a single global file in the a directory
# TODO: keep track of the following in the web_scraper_data.json file:
#           last link processed
#           list of all links processed
#           last datetime this scraper was ran
#           location of all combined HTML outputs
# "scraper name": {
#     "downloaded_files": [abs_path_to_downloaded_files],
#     "last_processed_url": "",
#     "processed_urls": [{"url": "", "datetime": ""}],
#     "last_processed_time": unix,
#     "outputs": [],
# }
# TODO: flag to reprocess all pages every n time, using the last datetime this scraper was ran in the json file
# TODO: grab last html output and append to the end when not entirely reprocessing
# TODO: add Ctrl + D to force stop the page loading if the page is taking ages to load (and i mean ages, like 30 seconds)
# TODO: catch errors when there is no internet
# TODO: reuse the same browser window, check for accessibility to given url and sign in only if needed
# TODO: parameter in Element that takes another Element object as the "flag" that tells us when the page has loaded
# TODO: create "add element selector" wizard, checks if valid xpath or css selector in clipboard and adds it to object
# TODO: status row

# The config class should not need to exist, all the scraper configuration should be set using function inputs.


class WebScraper:

    def __init__(
        self,
        name: str,
        url: str,
        sign_in_url: str,
        sequences: list[ElementSequence],
        sign_in_sequence: ElementSequence,
        headless: bool = False,
        unique_file_name: bool = True,
        root_path: str = os.getcwd(),
        document_merger_config: DocumentMergerConfig | None = None,
        export_html: bool = True,
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
        # ├───Web Scraper 1 Name
        # │   │    Web Scraper 1 HTML output
        # │   └─── Web Scraper Downloads
        # │           Downloaded files
        # ├───Web Scraper 2 Name
        # │   │    Web Scraper 2 HTML output
        # │   └─── Web Scraper Downloads
        # │           Downloaded files
        # └───Web Scraper 3 Name
        #     │    Web Scraper 3 HTML output
        #     └─── Web Scraper Downloads
        #             Downloaded files
        # we cd into the web scraper directory each time the scraper is ran, then cd out for repeatability

        # os.path.exists fails if input is None
        if root_path and not os.path.exists(root_path):
            raise Exception(f"Invalid root path '{root_path}'")

        self._current_scraper_path = os.path.join(root_path, self.name)

        self.download_path = os.path.join(
            self._current_scraper_path, "Web Scraper Downloads"
        )
        # create all directories in download path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path, exist_ok=True)

        self._original_path = os.getcwd()

        options = Options()

        if headless:
            options.add_argument("--headless=new")

        # alternate option for setting download directory
        # prefs = {"download.default_directory": "C:\\Tutorial\\down"}
        # options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options)

        self.download_handler = DownloadHandler()

        self.unique_file_name = unique_file_name

        self.html = ""

        self.sequence_index = 0

        # self.status_row = StatusRow()
        self.document_merger_config = document_merger_config

        self.export_html = export_html

    def run(self):
        try:
            os.chdir(self._current_scraper_path)
            self.download_handler.set_download_path(self.driver, self.download_path)
            self.html = ""
            self.sign_in()
            self.open_url()
            self.iterate_sequence()
            if self.export_html:
                self.write()
            os.chdir(self._original_path)

            # run document merger
            if self.document_merger_config:
                if isinstance(self.document_merger_config, DocumentMergerConfig):
                    self.document_merger_config.analysis_path = (
                        self._current_scraper_path
                    )
                    DocumentMerger(self.document_merger_config).start()
                else:
                    raise TypeError("Invalid document_merger_config type")

        except NoSuchWindowException:
            # TODO: this doesn't do what i want it to. an empty html file is created
            print("Window closed, writing to file")
            if self.export_html:
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
