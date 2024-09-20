"""
sleep.py module

This module provides functions for retrieving sleep data from the Withings API.

It includes functionality for fetching high-frequency sleep data, sleep summaries, and handling
POST requests to the Withings API.
"""
import warnings

from pywithingsapi import CONSTANTS as CONST
from pywithingsapi import exceptions_warnings
from pywithingsapi import post_request
from pywithingsapi import utils
from pywithingsapi.withings_user import WithingsUser


def data_sleep_get(
        startdate: int,
        enddate: int,
        data_fields: list[str] = CONST.SLEEP_GET_DATA_FIELDS) -> dict:
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
    """
    utils.warn_if_end_before_start(startdate, enddate)
    utils.warn_if_start_equals_end(startdate, enddate)
    utils.warn_if_time_diff_greater_24h(startdate, enddate)

    for data_field in data_fields:
        if data_field not in CONST.SLEEP_GET_DATA_FIELDS:
            warnings.warn(exceptions_warnings.InvalidDataFieldWarning(data_sleep_get.__name__, data_field))
            data_fields.remove(data_field)

    if len(data_fields) == 0:  # if no valid data field remains after removing invalid data fields
        data_fields = CONST.SLEEP_GET_DATA_FIELDS

    return {'action': "get", 'startdate': startdate,
            'enddate': enddate, 'data_fields': ",".join(data_fields)}


def data_sleep_summary(
        startdate: int = None,
        enddate: int = None,
        lastupdate: int = None,
        offset: int = 0,
        data_fields: list[str] = CONST.SLEEP_SUMMARY_DATA_FIELDS
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
            Defaults to None.
        enddate (int, optional): The end date for the data summary (Unix timestamp).
            Defaults to None.
        lastupdate (int, optional): The last update timestamp for the data (Unix timestamp).
            Defaults to None.
        offset (int, optional): The offset for paginated data. Defaults to 0.
        data_fields (list, optional): A list of data fields to be included in the summary.
            Defaults to `CONST.SLEEP_SUMMARY_DATA_FIELDS`.

    Returns:
        dict: A dictionary containing the data for making the sleep summary
            request, to be used in a POST request.
    """
    startdateymd, enddateymd, lastupdate = \
        utils.handle_start_end_update_ymd(startdate, enddate, lastupdate)
    utils.ensure_non_negative_int_or_none(offset)

    for data_field in data_fields:
        if data_field not in CONST.SLEEP_SUMMARY_DATA_FIELDS:
            warnings.warn(exceptions_warnings.InvalidDataFieldWarning(data_sleep_summary.__name__, data_field))
            data_fields.remove(data_field)

    if len(data_fields) == 0:  # if no valid data field remains after removing invalid data fields
        data_fields = CONST.SLEEP_SUMMARY_DATA_FIELDS

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
