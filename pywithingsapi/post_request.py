"""
post.request.py module

This module provides functions for making POST requests to the Withings API.
"""

import requests

from pywithingsapi import CONSTANTS as CONST


def post_request(url: str, data: dict, headers: dict = None) -> requests.Response:
    """
    Sends a POST request to a specified URL with the provided data and headers.

    Args:
        url (str): The URL to send the POST request to.
        data (dict): A dictionary containing the data to send in the POST request body.
        headers (dict, optional): A dictionary of HTTP headers to send with the request. Defaults to None.

    Returns:
        requests.Response: The response object from the POST request.

    Raises:
        requests.RequestException: If an error occurs during the POST request.
    """
    try:
        res = requests.post(url=url, headers=headers, data=data, timeout=CONST.TIMEOUT)
        print(res)
        res.raise_for_status()
        return res

    except requests.RequestException as e:
        print(f"Error during post request: {e}")
        print("Post request url:", url)
        print("Post request data:", data)
        raise
