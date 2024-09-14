"""
post.request.py module

This module provides functions for making POST requests to the Withings API.
"""

import json
import requests
import os
import time

from pywithingsapi import CONSTANTS as CONST
from pywithingsapi import exceptions
from pywithingsapi.withings_user import WithingsUser


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
        res.raise_for_status()
        return res

    except requests.RequestException as e:
        print(f"Error during post request: {e}")
        print("Post request url:", url)
        print("Post request data:", data)
        raise


def get_data_dict(data: dict, url: str, user: WithingsUser, to_json: bool = False) -> dict:
    """
    Sends a POST request with the provided data and returns the response as a dictionary.

    This function sends a POST request to the given URL with the specified data and user authentication headers.
    If the `to_json` flag is set to True, the response is saved as a JSON file in the user's directory.

    Args:
        data (dict): The data to be sent in the POST request.
        url (str): The URL to send the POST request to.
        user (WithingsUser): An instance of `WithingsUser` which is necessary to create the headers
        to_json (bool, optional): If set to True, the response is saved as a JSON file in the user's folder.
            Defaults to False.

    Returns:
        dict: The response content parsed as a dictionary.

    Raises:
        OSError: If an error occurs while accessing the directory or writing the file.
    """
    if user.expiration_time < int(time.time()):
        user.refresh_existing_token()

    headers = user.create_headers()
    response = post_request(url, data, headers)
    dct = json.loads(response.content)

    if dct["status"] != 0:
        raise exceptions.WithingsStatusNotZeroError(data, url, dct)

    if to_json:
        user_folder = f"user_{user.userid}"
        filename = url.split('/')[-1] + "_" + data["action"] + ".json"

        try:
            with open(os.path.join(CONST.DATA_DIR, user_folder, filename), "w",
                      encoding="utf-8") as f:
                json.dump(dct["body"], f, indent=4)
        except OSError as e:
            print(f"An error occurred while accessing the directory or writing the file ({e}, {type(e).__name__}).")

    return dct["body"]
