"""
withings_client.py module

This module provides the WithingsClient class for managing Withings API client parameters.
It includes functionality to initialize the client, load parameters from a dictionary,
and store them in a JSON file.
"""

import json
import os
import urllib.parse as urlparse

from pywithingsapi import CONSTANTS as CONST


class WithingsClient:
    """
    A client for interacting with the Withings API.

    This class manages the parameters needed for API interaction and provides methods
    to initialize the client, load parameters from a dictionary, and store them in a file.

    Attributes:
        client_id (str): The client ID for the Withings API.
        client_secret (str): The client secret for the Withings API.
        redirect_uri (str): The redirect URI for OAuth2 authentication.
        state (str): A string to maintain state between the request and callback.
        scope (str): The scope of the API access.
        demo (bool): A flag indicating whether the client is in demo mode.
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, state: str,
                 scope: str = CONST.STANDARD_SCOPE, demo: bool = False):
        """
        Initializes a WithingsClient instance and stores the parameters in a JSON file.

        Args:
            client_id (str): The client ID for the Withings API.
            client_secret (str): The client secret for the Withings API.
            redirect_uri (str): The redirect URI for OAuth2 authentication.
            state (str): A string to maintain state between the request and callback.
            scope (str, optional): The scope of the API access. Defaults to CONST.STANDARD_SCOPE.
            demo (bool, optional): A flag indicating whether the client is in demo mode. Defaults to False.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state
        self.scope = scope
        self.demo = demo

        self.store_client_params()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a WithingsClient instance from a dictionary.

        Args:
            data (dict): A dictionary containing the parameters needed to create a WithingsClient instance.
                Must include "client_id", "client_secret", "redirect_uri", "state", "scope", and "demo".

        Returns:
            WithingsClient: A new instance of WithingsClient.

        Raises:
            TypeError: If the input data is not a dictionary.
            KeyError: If any of the required keys are missing from the dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary.")
        if not all(key in data for key in ["client_id", "client_secret", "redirect_uri", "state", "scope", "demo"]):
            raise KeyError("At least one key is missing in the dictionary.")
        return cls(**data)

    def store_client_params(self):
        """
        Stores the client parameters in a JSON file.

        The file name depends on whether the client is in demo mode or not.
        Creates the data directory if it does not exist and handles file writing errors.

        Raises:
            OSError: If an error occurs while accessing or creating the dictionary or while writing the file.
        """
        try:
            if not os.path.exists(CONST.DATA_DIR):
                os.makedirs(CONST.DATA_DIR)

            client_params = {
                key: getattr(self, key)
                for key in ["client_id", "client_secret", "redirect_uri", "state", "scope", "demo"]
            }

            client_params_file_name = 'client_params_demo.json' if self.demo else 'client_params.json'

            try:
                with open(os.path.join(CONST.DATA_DIR, client_params_file_name), 'w') as file:
                    json.dump(client_params, file, indent=4)
            except OSError as e:
                print(f"An error occurred while writing the file ({e}, {type(e).__name__}).")

        except OSError as e:
            print(f"An error occurred while accessing or creating the directory ({e}, {type(e).__name__}).")

    def create_auth_url(self) -> str:
        """
        Generates the authentication URL for user authorization in the Withings API.

        This method constructs a URL for initiating an OAuth authorization request
        and returns it as a string. It includes the required parameters such as
        `response_type`, `client_id`, `scope`, `redirect_uri`, and `state`. If the
        `demo` flag is enabled, a `mode=demo` parameter is appended to the URL.

        Returns:
            str: The full authentication URL with encoded parameters for user authorization.
        """
        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
            "state": self.state
        }
        if self.demo:
            auth_params["mode"] = "demo"
        return CONST.URL_AUTH + "?" + urlparse.urlencode(auth_params)
