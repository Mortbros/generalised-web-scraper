from Element import Element
from web_scraper_errors import ElementExistsError, ElementNotFoundError

import time

RESTART_DELAY = 2


class ElementSequence:
    def __init__(
        self,
        name,
        elements=[],
        url=None,
        run_until_fail=False,
        restart_on_fail: int = 1,
        restart_delay=RESTART_DELAY,
    ):
        self.html = ""

        self.name = name

        if isinstance(elements, list):
            if len(elements) == 0:
                self.elements = elements
            elif all(isinstance(i, Element) for i in elements):
                self.elements = elements
            else:
                raise Exception(
                    "Invalid element sequence, all elements must be of type Element"
                )
        else:
            raise Exception(
                f"Invalid element sequence must be of type list (currently {type(elements)})"
            )

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

    # runs iteration
    def run(self, driver):
        # this check is located here because an ElementSequence can be initialised with no elements, then populated later
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
                    raise Exception(
                        f'Element sequence "{self.name}" failed to find and validate after {self.restart_on_fail} attempts'
                    )

            print("\t\tFinished after failing to find")
        else:
            raise Exception("Cannot run empty ElementSequence")
        return self.html

    def reset(self):
        pass

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
