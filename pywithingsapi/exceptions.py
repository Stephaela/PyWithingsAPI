"""
exceptions.py module

This module provides custom exceptions for the PyWithingsAPI project.
"""


class WithingsStatusNotZeroError(Exception):
    """Exception raised when a Withings API response has a status of 200 but the Withings status is not 0."""
    def __init__(self, data: dict, url: str, dct: dict):
        """Initialize the WithingsStatusNotZeroError exception with a detailed message.

        Args:
            data (dict): The data sent in the post request.
            url (str): The URL to which the post request was sent.
            dct (dict): The dictionary containing the response details, including status code and error message.
        """
        self.message = (
            f"The post request response status is 200, i.e. the post request was successful, "
            f"but the Withings status is not 0.\n"
            f"Withings status code: {dct['status']}\n"
            f"Withings error message: {dct['error']}\n"
            f"URL: {url}\n"
            f"Data: {data}"
        )
        super().__init__(self.message)
