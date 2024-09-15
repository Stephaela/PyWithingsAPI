"""
measure.py module

This module provides functionality for interacting with the Withings API to
retrieve user measurement and activity data.
"""

import warnings

from pywithingsapi import CONSTANTS as CONST
from pywithingsapi import post_request
from pywithingsapi import utils
from pywithingsapi.withings_user import WithingsUser


def data_measure_get_activity(
        startdate: int = None,
        enddate: int = None,
        lastupdate: int = None,
        offset: int = 0,
        data_fields: str | list[str] = CONST.MEASURE_GET_ACTIVITY_DATA_FIELDS
) -> dict:
    """
        Creates a dictionary for retrieving activity data within a specified date range or after a specified
        last update time.
        Either the parameter pair startdate and enddate, or the parameter lastupdate are required,
        but not both. These parameters will be handled in the utils.py module.

        Users can also specify which fields to retrieve in the response by passing them in `data_fields`.
        Invalid fields will be removed from the request and a warning will be issued. If no valid fields remain,
        all fields will be requested by default.

        Args:
            startdate (int, optional): The start date for the data summary (Unix timestamp).
            enddate (int, optional): The end date for the data summary (Unix timestamp).
            lastupdate (int, optional): The last update timestamp for the data (Unix timestamp).
            offset (int, optional): The offset for paginated data. Defaults to 0.
            data_fields (str or list, optional): A list of data fields to be retrieved.
                Defaults to `CONST.MEASURE_GET_ACTIVITY_DATA_FIELDS`.

        Returns:
            dict: A dictionary containing the parameters for the `getactivity` action, including:
                - action (str): The action being performed (always "getactivity").
                - startdateymd (str): The start date in YYYY-MM-DD format.
                - enddateymd (str): The end date in YYYY-MM-DD format.
                - lastupdate (int): The last update timestamp in UNIX format.
                - offset (int): The offset for the request.
                - data_fields (str): A comma-separated string of valid data fields to retrieve.
    """
    startdateymd, enddateymd, lastupdate = \
        utils.handle_start_end_update_ymd(startdate, enddate, lastupdate)

    if isinstance(data_fields, str):
        data_fields = [data_fields]  # Normalize single value to list

    for data_field in data_fields:
        if data_field not in CONST.MEASURE_GET_ACTIVITY_DATA_FIELDS:
            warnings.warn(f"{data_field} is not a valid data field and will not be sent in the request.")
            data_fields.remove(data_field)

    if len(data_fields) == 0:
        data_fields = CONST.MEASURE_GET_ACTIVITY_DATA_FIELDS

    return {
        "action": "getactivity",
        "startdateymd": startdateymd,
        "enddateymd": enddateymd,
        "lastupdate": lastupdate,
        "offset": offset,
        "data_fields": ",".join(data_fields)
    }


def data_measure_get_intradayactivity(
        startdate: int = None,
        enddate: int = None,
        lastupdate: int = None,
        data_fields: str | list[str] = CONST.MEASURE_GET_INTRADAYACTIVITY_DATA_FIELDS
) -> dict:
    """
    Creates a dictionary for retrieving intraday activity data.
    At least one of the parameters startdate and enddate are required.

    Args:
        startdate (int): startdate in unix format, default is None
        enddate (int): enddate in unix format, default is None
        lastupdate (int, optional): date in unix format, default is None
        data_fields (str or list, optional): standard value is
            `INTRADAYACTIVITY_DATA_FIELDS` in `CONSTANTS.py`

    Returns:
        dict: a dictionary containing the action type and the
            request parameters. Use it as parameter in the
            `data_measure_getmeas`function in order to
            retrieve the desired data.

    Raises:
        ValueError: if neither startdate nor enddate are provided
    """
    if startdate is None and enddate is None:
        raise ValueError("At least one of the parameters startdate and enddate must be provided.")

    utils.warn_if_end_before_start(startdate, enddate)
    utils.warn_if_start_equals_end(startdate, enddate)
    utils.warn_if_time_diff_greater_24h(startdate, enddate)

    if isinstance(data_fields, str):
        data_fields = [data_fields]  # Normalize single value to list

    for data_field in data_fields:
        if data_field not in CONST.MEASURE_GET_ACTIVITY_DATA_FIELDS:
            warnings.warn(f"{data_field} is not a valid data field and will not be sent in the request.")
            data_fields.remove(data_field)

    if len(data_fields) == 0:
        data_fields = CONST.MEASURE_GET_ACTIVITY_DATA_FIELDS

    return {
        "action": "getintradayactivity",
        "startdate": startdate,
        "enddate": enddate,
        "lastupdate": lastupdate,
        "data_fields": ",".join(data_fields)
    }


def data_measure_get_meas(
        startdate: int = None,
        enddate: int = None,
        lastupdate: int = None,
        offset: int = 0,
        category: int = 1,
        data_fields: int | str | list[int | str] = CONST.MEASURE_GET_MEAS_DATA_FIELDS_INT
) -> dict:
    """
    Prepares a dictionary of parameters for the Withings API 'getmeas' action.

    The function validates and organizes the input parameters required to
    retrieve measurements from the Withings API, ensuring they conform to the
    expected format. It also provides warning messages if inputs are invalid
    or unexpected.

    Args:
        startdate (int, optional): Unix timestamp representing the start date of measurements.
            Defaults to None.
        enddate (int, optional): Unix timestamp representing the end date of measurements.
            Defaults to None.
        lastupdate (int, optional): Unix timestamp representing the last update of measurements.
            Defaults to None.
        offset (int, optional): The number of measurements to skip in the response.
            Defaults to 0.
        category (int, optional): Category of the measures, either 1 (real measures) or 2 (user objectives).
            Defaults to 1.
        data_fields (int | str | list[int | str], optional): The fields to retrieve, as integers, strings, or a list
            of integers and strings. Defaults to CONST.MEASURE_GET_MEAS_DATA_FIELDS_INT.

    Returns:
        dict: A dictionary with the necessary parameters to send to the Withings API.

    Raises:
        ValueError: If the category is not 1 (real measures) or 2 (user objectives).
    """

    utils.ensure_non_negative_int_or_none(startdate, enddate, lastupdate, offset)
    utils.warn_if_end_before_start(startdate, enddate)
    utils.warn_if_start_equals_end(startdate, enddate)

    meastypes_list = []

    if isinstance(data_fields, (int, str)):
        data_fields = [data_fields]  # Normalize single value to list

    for data_field in data_fields:
        if isinstance(data_field, int) and data_field in CONST.MEASURE_GET_MEAS_DATA_FIELDS_INT:
            meastypes_list.append(data_field)
        elif isinstance(data_field, str) and data_field in CONST.MEASURE_GET_MEAS_DATA_FIELDS_STR:
            meastypes_list.append(CONST.MEASURE_GET_MEAS_DATA_FIELDS_STR_TO_INT[data_field])
        else:
            warnings.warn(f"{data_field} is not a valid data field and will not be sent in the request.")

    if len(meastypes_list) == 0:
        meastypes = ",".join(map(str, CONST.MEASURE_GET_MEAS_DATA_FIELDS_INT))
    elif len(meastypes_list) == 1:
        meastype = meastypes_list[0]
        meastypes = None
    else:
        meastype = None
        meastypes = ",".join(map(str, meastypes_list))

    if category not in (1, 2):
        raise ValueError("The parameter 'category' must be 1 for real measures or 2 for user objectives.")

    return {
        "action": "getmeas",
        "meastype": meastype,
        "meastypes": meastypes,
        "category": category,
        "startdate": startdate,
        "enddate": enddate,
        "lastupdate": lastupdate,
        "offset": offset,
    }


def data_measure_get_workouts(
    startdate: int = None,
    enddate: int = None,
    lastupdate: int = None,
    offset: int = 0,
    data_fields: list[str] = CONST.MEASURE_GET_WORKOUTS_DATA_FIELDS
) -> dict:

    startdateymd, enddateymd, lastupdate = \
        utils.handle_start_end_update_ymd(startdate, enddate, lastupdate)

    for data_field in data_fields:
        if data_field not in CONST.MEASURE_GET_WORKOUTS_DATA_FIELDS:
            warnings.warn(f"{data_field} is not a valid data field and will not be sent in the request.")
            data_fields.remove(data_field)

    return {
        "action": "getworkouts",
        "startdateymd": startdateymd,
        "enddateymd": enddateymd,
        "lastupdate": lastupdate,
        "offset": offset,
        "data_fields": ",".join(data_fields)
    }


def post_request_measure(data: dict, user: WithingsUser, to_json: bool = False) -> dict:
    """
    Sends a POST request to the Withings API to retrieve measurements, activity or workout data.

    This function sends a request with the provided data and user authentication.
    If `to_json` is set to True, the response is saved as a JSON file.

    Args:
        data (dict, required): A dictionary containing the request data.
        user (WithingsUser, required): An instance of `WithingsUser` containing the user credentials and headers.
        to_json (bool, optional): If set to True, the response is saved as a JSON file in the user's folder.
            Defaults to False.

    Returns:
        dict: The response from the API parsed as a dictionary.
    """
    if dict["action"] == "getmeas":
        url = CONST.URL_MEASURE
    else:
        url = CONST.URL_MEASURE_V2
    return post_request.get_data_dict(data, url, user, to_json)
