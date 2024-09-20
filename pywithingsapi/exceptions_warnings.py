"""
exceptions_warnings.py module

This module provides custom exceptions and custom warnings for the PyWithingsAPI project.
"""

import warnings


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


class InvalidDataFieldWarning(Warning):
    def __init__(self, fct_name, data_field):
        # Format the message dynamically with the parameter
        message = f"{data_field} is not a valid data field for {fct_name.removeprefix("data_")} " + \
            "and will not be used in the request."
        # Initialize the base Warning class with the constructed message
        super().__init__(message)
