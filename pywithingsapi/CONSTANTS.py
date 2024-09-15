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

MEASURE_GET_ACTIVITY_DATA_FIELDS = [
    "steps",
    "distance",
    "elevation",
    "soft",
    "moderate",
    "intense",
    "active",
    "calories",
    "totalcalories",
    "hr_average",
    "hr_min",
    "hr_max",
    "hr_zone_0",
    "hr_zone_1",
    "hr_zone_2",
    "hr_zone_3"
]

MEASURE_GET_INTRADAYACTIVITY_DATA_FIELDS = [
    "steps",
    "elevation",
    "calories",
    "distance",
    "stroke",
    "pool_lap",
    "duration",
    "heart_rate",
    "spo2_auto",
]

MEASURE_GET_MEAS_DATA_FIELDS_INT_TO_STR = {
    1: "weight",
    4: "height",
    5: "fat_free_mass",
    6: "fat_ratio",
    8: "fat_mass_weight",
    9: "diastolic_bp",
    10: "systolic_bp",
    11: "heart_pulse",
    12: "temperature",
    54: "spo2",
    71: "body_temperature",
    73: "skin_temperature",
    76: "muscle_mass",
    77: "hydration",
    88: "bone_mass",
    91: "pulse_wave_velocity",
    123: "vo2_max",
    130: "afib",
    135: "qrs_duration",
    136: "pr_duration",
    137: "qt_duration",
    138: "qtc_duration",
    139: "afib_ppg",
    155: "vascular_age",
    167: "nerve_health",
    168: "extracellular_water",
    169: "intracellular_water",
    170: "visceral_fat",
    174: "fat_mass_segments",
    175: "muscle_mass_segments",
    196: "electrodermal_activity",
}

MEASURE_GET_MEAS_DATA_FIELDS_INT = list(MEASURE_GET_MEAS_DATA_FIELDS_INT_TO_STR.keys())
MEASURE_GET_MEAS_DATA_FIELDS_STR = list(MEASURE_GET_MEAS_DATA_FIELDS_INT_TO_STR.values())

MEASURE_GET_MEAS_DATA_FIELDS_STR_TO_INT = {value: key for key, value in MEASURE_GET_MEAS_DATA_FIELDS_INT_TO_STR.items()}

MEASURE_GET_WORKOUTS_DATA_FIELDS = [
    "calories",
    "intensity",
    "manual_distance",
    "manual_calories",
    "hr_average",
    "hr_min",
    "hr_max",
    "hr_zone_0",
    "hr_zone_1",
    "hr_zone_2",
    "hr_zone_3",
    "pause_duration",
    "algo_pause_duration",
    "spo2_average",
    "steps",
    "distance",
    "elevation",
    "pool_laps",
    "strokes",
    "pool_length",
]

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
