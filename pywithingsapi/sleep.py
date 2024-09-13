"""
sleep.py module

This module provides functions for retrieving sleep data from the Withings API.

It includes functionality for fetching high-frequency sleep data, sleep summaries, and handling
POST requests to the Withings API.
"""

from typing import List
import warnings

from pywithingsapi import CONSTANTS as CONST
from pywithingsapi import post_request
from pywithingsapi import utils
from pywithingsapi.withings_user import WithingsUser


def data_sleep_get(
        startdate: int,
        enddate: int,
        data_fields: List[str] = CONST.SLEEP_GET_DATA_FIELDS) -> dict:
    """
    Creates a data dictionary for making a POST request to get sleep data
    captured at high frequency, including sleep stages, from the
    Withings API. If the time difference between start and end datetime is
    greater than 24 hours, only data for the first 24 hours will be returned.
    By default, all data fields will be included in the response.

    Args:
        startdate (int): The start datetime of the sleep data retrieval
            period (Unix timestamp).
        enddate (int): The end datetime of the sleep data retrieval
            period (Unix timestamp).
        data_fields (list, optional): The data fields to be retrieved.
            Defaults to `CONST.SLEEP_GET_DATA_FIELDS`, which includes all available fields.

    Returns:
        dict: A dictionary containing the data for making the sleep
            data retrieval request, to be used in a POST request.

    Raises:
        ValueError: If required parameters are missing or invalid data fields are provided.
    """
    if startdate is None or enddate is None:
        raise ValueError("At least one parameter is missing.")
    elif enddate < startdate:
        warnings.warn(CONST.DATE_ORDER_WARNING_STR, Warning)
    elif startdate == enddate:
        warnings.warn(CONST.START_EQUALS_END_WARNING_STR, Warning)
    elif (enddate - startdate) / 3600 > 24:
        warnings.warn(CONST.TIME_DIFF_GREATER_24H_WARNING_STR, Warning)
    if not all(x in CONST.SLEEP_GET_DATA_FIELDS for x in data_fields):
        raise ValueError("At least one data field in the request does not exist.")
    return {'action': "get", 'startdate': startdate,
            'enddate': enddate, 'data_fields': ",".join(data_fields)}


def data_sleep_summary(
        startdate: int = None,
        enddate: int = None,
        lastupdate: int = None,
        offset: int = 0,
        data_fields: List[str] = CONST.SLEEP_SUMMARY_DATA_FIELDS
) -> dict:
    """
    Creates a data dictionary for retrieving a summary of sleep data from the
    Withings API based on start and end dates or last update timestamp.

    This function retrieves summary data for the specified date range or
    last updated timestamp, such as sleep stages and metrics. By default,
    it includes all available data fields.

    Either the parameter pair startdate and enddate, or the parameter lastupdate
    are required, but not both. These parameters will be handled in the utils.py module.

    Args:
        startdate (int, optional): The start date for the data summary (Unix timestamp).
        enddate (int, optional): The end date for the data summary (Unix timestamp).
        lastupdate (int, optional): The last update timestamp for the data (Unix timestamp).
        offset (int, optional): The offset for paginated data. Defaults to 0.
        data_fields (list, optional): A list of data fields to be included in the summary.
            Defaults to `CONST.SLEEP_SUMMARY_DATA_FIELDS`.

    Returns:
        dict: A dictionary containing the data for making the sleep summary
            request, to be used in a POST request.

    Raises:
        ValueError: If invalid data fields are provided, or if the parameter offset is not
            a non-negative integer.
    """
    startdateymd, enddateymd, lastupdate = \
        utils.handle_start_end_update_ymd(startdate, enddate, lastupdate)
    if not (isinstance(offset, int) and offset >= 0):
        raise ValueError("The parameter offset must be a non-negative integer.")
    if not all(x in CONST.SLEEP_SUMMARY_DATA_FIELDS for x in data_fields):
        raise ValueError("At least one data field in the request does not exist.")
    return {'action': "getsummary", 'startdateymd': startdateymd,
            'enddateymd': enddateymd, 'lastupdate': lastupdate,
            'offset': offset, 'data_fields': ",".join(data_fields)}


def post_request_sleep(data: dict, user: WithingsUser, to_json: bool = False) -> dict:
    """
    Sends a POST request to the Withings API to retrieve sleep data.

    This function sends a request with the provided data and user authentication.
    If `to_json` is set to True, the response is saved as a JSON file.

    Args:
        data (dict, required): A dictionary containing the request data
            (from `data_sleep_get` or `data_sleep_summary`).
        user (WithingsUser, required): An instance of `WithingsUser` containing the user credentials and headers.
        to_json (bool, optional): If set to True, the response is saved as a JSON file in the user's folder.
            Defaults to False.

    Returns:
        dict: The response from the API parsed as a dictionary.
    """
    return post_request.get_data_dict(data, CONST.URL_SLEEP_V2, user, to_json)
