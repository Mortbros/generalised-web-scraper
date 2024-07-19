class ElementExistsError(Exception):
    """Raised if the element exists when it shouldn't"""

    pass


class ElementNotFoundError(Exception):
    """Raised if the element doesn't exist when it should"""

    pass
