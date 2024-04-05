from ElementSequence import ElementSequence

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException

from datetime import datetime


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

        self.options = Options()
        self.options.headless = headless
        self.driver = webdriver.Chrome(options=self.options)

        self.unique_file_name = unique_file_name

        self.html = ""

        self.sequence_index = 0

        # self.status_row = StatusRow()

    def run(self):
        try:
            self.sign_in()
            self.open_url()
            self.iterate_sequence()
            self.write()
        except NoSuchWindowException:
            # TODO: this doesn't do what i want it to. an empty html file is created
            print("Window closed, writing to file")
            self.write()

    def write(self):
        open(
            f"{self.name}{datetime.now().strftime(' %Y-%m-%d_%H-%M-%S') if self.unique_file_name else ''}.html",
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
