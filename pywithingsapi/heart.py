"""
heart.py module

This module provides functions to interact with the Withings API for heart data.

It includes functions to retrieve a heart signal (`data_heart_get`), list heart signals
within a date range (`data_heart_list`), and make POST requests to fetch heart data (`post_request_heart`).
"""
import warnings

from pywithingsapi import CONSTANTS as CONST
from pywithingsapi import post_request
from pywithingsapi.withings_user import WithingsUser


def data_heart_get(signalid: int) -> dict:
    """
    Creates a dictionary for retrieving a specific heart signal (with the specified signal ID)
    from the Withings API.

    Args:
        signalid (int, required): The ID of the heart signal to be retrieved.

    Returns:
        dict: A dictionary for making the API request.

    Raises:
        ValueError: If signalid is not a positive integer.
    """
    if not (isinstance(signalid, int) and signalid > 0):
        raise ValueError("All parameters must be positive integers.")
    return {"action": "get", "signalid": signalid}


def data_heart_list(startdate: int = None, enddate: int = None, offset: int = 0) -> dict:
    """
    Creates a dictionary for listing heart signals within a date range from the Withings API.
    If there is more data available than the chunk limit, the newest data will be returned first.

    Args:
        startdate (int, optional): The start datetime for the heart signal listing (in Unix timestamp format).
            Defaults to None.
        enddate (int, optional): The end datetime for the heart signal listing (in Unix timestamp format).
            Defaults to None.
        offset (int, optional): The offset for paginated results. Defaults to 0.

    Returns:
        dict: A dictionary containing the action, start date, end date, and offset for the API request.

    Raises:
        ValueError: If there is at least one parameter which is not either None or a non-negative integer.
    """
    if not all(((isinstance(param, int) and param >= 0) or param is None for param in list(locals().values()))):
        raise ValueError("All parameters must be either None or non-negative integers.")
    if startdate is not None and enddate is not None:
        if enddate < startdate:
            warnings.warn(CONST.DATE_ORDER_WARNING_STR, Warning)
        elif startdate == enddate:
            warnings.warn(CONST.START_EQUALS_END_WARNING_STR, Warning)
    return {"action": "list", "startdate": startdate, "enddate": enddate, "offset": offset}


def post_request_heart(data: dict, user: WithingsUser, to_json: bool = False) -> dict:
    """
    Sends a POST request to the Withings API to retrieve heart data.

    This function sends a request with the provided data and user authentication.
    If `to_json` is set to True, the response is saved as a JSON file.

    Args:
        data (dict, required): A dictionary containing the request data ( from `data_heart_get` or `data_heart_list`).
        user (WithingsUser, required): An instance of `WithingsUser` containing the user credentials and headers.
        to_json (bool, optional): If set to True, the response is saved as a JSON file in the user's folder.
            Defaults to False.

    Returns:
        dict: The response from the API parsed as a dictionary.
    """
    return post_request.get_data_dict(data, CONST.URL_HEART_V2, user, to_json)
