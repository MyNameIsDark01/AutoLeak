class Error(Exception):
    """Return a simple error"""


class NoDigit(Error):
    """Raise if the string is not digit"""

    def __init__(self, message='No numbers provided') -> None:
        self.message = message
        super().__init__(self.message)
