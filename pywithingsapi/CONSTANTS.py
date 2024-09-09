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
URL_MEASURE = "https://wbsapi.withings.net/measure"
URL_MEASURE_V2 = "https://wbsapi.withings.net/v2/measure"
URL_HEART_V2 = "https://wbsapi.withings.net/v2/heart"
URL_SLEEP_V2 = "https://wbsapi.withings.net/v2/sleep"
