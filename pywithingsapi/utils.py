"""
utils.py module

This module provides utility functions for the PyWithingsAPI project.
"""

import datetime as dt
import warnings

from pywithingsapi import CONSTANTS as CONST


def handle_start_end_update_ymd(startdate: int = None,
                                enddate: int = None,
                                lastupdate: int = None) -> (dt.date, dt.date, int):
    """
    Handles the parameters startdate, enddate and lastupdate for some of the functions of the
    sleep.py and measure.py module.

    Some of the functions for retrieving data in the sleep.py and measure.py module require the
    parameters startdate, enddate and lastupdate to be handled in the same way: either the pair
    startdate and enddate, or the parameter lastupdate are required, but not both. If the pair
    startdate and enddate are used, they must be converted from unix timestamps to dt.date YMD
    format, i.e. the time of the day will be removed. If the parameter lastupdate is used, it
    must stay in the unix timestamp format.

    This function handles the three parameters in this way.

    Args:
        startdate (int, optional): The start date in Unix timestamp format. Defaults to None.
        enddate (int, optional): The end date in Unix timestamp format. Defaults to None.
        lastupdate (int, optional): The last update timestamp in Unix format. Defaults to None.

    Returns:
        tuple: A tuple containing:
            - startdateymd (dt.date or None): The start date in YMD format, or None if lastupdate is provided.
            - enddateymd (dt.date or None): The end date in YMD format, or None if lastupdate is provided.
            - lastupdate (int or None): The last update timestamp, or None if start and end dates are provided.

    Raises:
        ValueError: If neither `startdate`/`enddate` nor `lastupdate` are provided,
                    or if all parameters are provided.
        Warning: If the end date is earlier than the start date, a warning is issued.
    """
    if (startdate is None or enddate is None) and lastupdate is None:
        # Neither both startdate and enddate, nor lastupdate were provided
        raise ValueError("At least one required parameter is missing")
    elif (startdate is not None or enddate is not None) and lastupdate is not None:
        # All three parameters were provided
        raise ValueError("The provided parameters are incompatible")

    if startdate is not None and enddate is not None:
        # Both startdate and enddate were provided, but not lastupdate
        if enddate < startdate:
            warnings.warn(CONST.DATE_ORDER_WARNING_STR, Warning)
        startdateymd = dt.date.fromtimestamp(startdate)
        enddateymd = dt.date.fromtimestamp(enddate)
    else:
        # Only the parameter lastupdate was provided
        startdateymd = None
        enddateymd = None

    return startdateymd, enddateymd, lastupdate
