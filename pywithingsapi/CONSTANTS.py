"""
CONSTANTS.py module

This module contains constants used in the PyWithingsAPI project.
"""

import os

STANDARD_SCOPE = "user.info,user.metrics,user.activity"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

TIMEOUT = 10
