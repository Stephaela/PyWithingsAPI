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

START_EQUALS_END_WARNING_STR = (
        "Start and end are equal. No data will be returned."
)
DATE_ORDER_WARNING_STR = (
    "Start and end are in the wrong order. No data will be returned."
)
TIME_DIFF_GREATER_24H_WARNING_STR = (
        "Time difference between start and end greater than 24h. "
        + "Only data for first 24h after startdate will be returned."
)

SLEEP_GET_DATA_FIELDS = [
    "hr",
    "rr",
    "snoring",
    "sdnn_1",
    "rmssd",
    "mvt_score"
]

SLEEP_SUMMARY_DATA_FIELDS = [
    "nb_rem_episodes",
    "sleep_efficiency",
    "sleep_latency",
    "total_sleep_time",
    "total_timeinbed",
    "wakeup_latency",
    "waso",
    "apnea_hypopnea_index",
    "breathing_disturbances_intensity",
    "asleepduration",
    "deepsleepduration",
    "durationtosleep",
    "durationtowakeup",
    "hr_average",
    "hr_max",
    "hr_min",
    "lightsleepduration",
    "mvt_active_duration",
    "mvt_score_avg",
    "night_events",
    "out_of_bed_count",
    "remsleepduration",
    "rr_average",
    "rr_max",
    "rr_min",
    "sleep_score",
    "snoring",
    "snoringepisodecount",
    "wakeupcount",
    "wakeupduration",
    "withings_index"
]
