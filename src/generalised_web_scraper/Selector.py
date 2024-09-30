from selenium.webdriver.common.by import By


class Selector:
    def __init__(self, sel_value: str, sel_type=None):
        self.sel_value = sel_value

        if sel_type:
            self.sel_type = sel_type
        else:
            # loosely auto-detect the selector type
            # TODO: this is fragile
            if sel_value[0] == "/":
                self.sel_type = By.XPATH
            else:
                self.sel_type = By.CSS_SELECTOR

    # Selector[0] = self.sel_value, Selector[1] = self.sel_type
    def __iter__(self):
        return iter([self.sel_value, self.sel_type])

    def __str__(self):
        return f'{self.sel_value} (type "{self.sel_type}")'
