"""
CONSTANTS.py module

This module contains constants used in the PyWithingsAPI project.
"""

import os

STANDARD_SCOPE = "user.info,user.metrics,user.activity"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

TIMEOUT = 10

URL_AUTH = "https://account.withings.com/oauth2_user/authorize2"
URL_OAUTH2_V2 = "https://wbsapi.withings.net/v2/oauth2"