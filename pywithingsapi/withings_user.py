"""
withings_user.py module

This module defines the `WithingsUser` class, which handles user-related operations
such as token storage, user folder creation, API request authorization and refreshing
an existing access token.
"""

import json
import os
import time

import requests

from pywithingsapi import CONSTANTS as CONST
from pywithingsapi import post_request
from pywithingsapi import withings_client


class WithingsUser:
    """
    Represents a Withings user and manages user-specific data such as access tokens,
    refresh_token, folder storage, and headers for API requests.

    This class interacts with an API client to manage authentication tokens and stores
    user-related data locally in a directory structure.

    Attributes:
        api_client (withings_client.WithingsClient): The corresponding Withings API client
        userid (str): The Withings user ID
        access_token (str): The access token for this user
        refresh_token (str): The refresh token for this user
        scope (str): The scope of the API access.
        token_type (str): The type of the access and refresh token
        expiration_time (int): The time the access token expires
        user_folder (str): The name of the folder where the token and user data are saved

    """

    def __init__(self, api_client: withings_client.WithingsClient, data: dict = None):
        """
        Initializes a WithingsUser instance, either from provided data or by requesting a new token.

        Args:
            api_client: An instance of the API client to manage token requests.
            data (dict, optional): A dictionary containing user information such as access tokens and user ID.
                If no data is provided, the function will request a new token from the API.

        Raises:
            KeyError: If any expected keys are missing from the provided data or the token response.
        """
        self.api_client = api_client

        keys = ["userid", "access_token", "refresh_token", "scope", "token_type", "expiration_time"]

        if data is not None:
            for key in keys:
                try:
                    setattr(self, key, data[key])
                except KeyError:
                    raise KeyError(f"Key '{key}' is missing from the provided data.")

            if self.expiration_time < int(time.time()):
                self.user_folder = self.create_user_folder()
                self.refresh_existing_token()

        else:
            token_data = self.api_client.access_new_token()["body"]
            print(token_data)

            for key in keys:
                try:
                    setattr(self, key, token_data[key])
                except KeyError:
                    raise KeyError(f"Key '{key}' is missing from the token data.")

            self.expiration_time = int(time.time()) + token_data["expires_in"]

        self.user_folder = self.create_user_folder()
        self.store_user_params()

    @classmethod
    def from_dict(cls, api: withings_client.WithingsClient, data: dict):
        """
        Creates a `WithingsUser` instance from a dictionary.

        Args:
            api (withings_client.WithingsClient): An instance of the API client to manage token requests.
            data (dict): A dictionary containing user-specific information like access tokens, user ID, and scope.

        Returns:
            WithingsUser: A new instance of `WithingsUser`.

        Raises:
            TypeError: If the provided data is not a dictionary.
            KeyError: If any expected keys are missing from the dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary.")
        if not all(key in data for key in ["userid", "access_token", "refresh_token", "scope", "token_type",
                                           "expiration_time"]):
            raise KeyError("At least one key is missing in the dictionary.")
        return cls(api, data)

    def create_user_folder(self):
        """
        Creates a directory for storing user-specific data.

        The directory is named `user_<userid>` and is created inside the `data` folder defined
        in the CONSTANTS.py module.

        Returns:
            str: The name of the created user folder.

        Raises:
            OSError: If an error occurs during the creation of the directory.
        """
        try:
            user_folder = f"user_{self.userid}"
            if not os.path.exists(os.path.join(CONST.DATA_DIR, user_folder)):
                os.makedirs(os.path.join(CONST.DATA_DIR, user_folder))
            return user_folder
        except OSError as e:
            print(f"An error occurred while accessing or creating the directory ({e}, {type(e).__name__}).")

    def store_user_params(self):
        """
        Stores user parameters such as access tokens and user ID in a JSON file.

        The file is saved in the user's folder and contains user data including the demo status.

        Raises:
            OSError: If an error occurs during the writing of the file.
        """
        user_params_file_path = os.path.join(CONST.DATA_DIR, self.user_folder, 'user_params.json')

        user_data = {
            key: getattr(self, key)
            for key in ["userid", "access_token", "refresh_token", "scope", "token_type", "expiration_time"]
        }

        user_data["demo"] = self.api_client.demo

        try:
            with open(user_params_file_path, 'w') as file:
                json.dump(user_data, file, indent=4)
        except OSError as e:
            print(f"An error occurred while writing the file ({e}, {type(e).__name__}).")

    def create_headers(self) -> dict:
        """
        Creates the authorization headers required for making API requests.

        This method constructs an authorization header using the token type and access token.

        Returns:
            dict: A dictionary containing the authorization header and content type.
        """
        auth = " ".join([self.token_type, self.access_token])
        return {
            "Authorization": auth,
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def post_request_refresh(self) -> requests.Response:
        """
        Sends a POST request to obtain a new access token by using the refresh token.

        This function sends a POST request to the OAuth2 endpoint to exchange the refresh
        token for a fresh access token. The necessary client credentials and refresh token are included
        in the request body.

        Returns:
            requests.Response: The response object from the POST request, which contains the fresh access
             and refresh tokens if the request is successful.
        """
        url = CONST.URL_OAUTH2_V2
        data = {
            "action": "requesttoken",
            "grant_type": "refresh_token",
            "client_id": self.api_client.client_id,
            "client_secret": self.api_client.client_secret,
            "refresh_token": self.refresh_token,
        }
        return post_request.post_request(url, data)

    def refresh_existing_token(self):
        """
        This method guides the user through refreshing the access token.

        It retrieves the updated tokens and stores them in a JSON file.
        """
        res = json.loads(self.post_request_refresh().content)["body"]

        self.access_token = res["access_token"]
        self.refresh_token = res["refresh_token"]
        self.expiration_time = int(time.time()) + res["expires_in"]

        self.store_user_params()
