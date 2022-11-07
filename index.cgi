#!/usr/bin/env python3

from wsgiref.handlers import CGIHandler
import os
from app import app
import sys
PIP_PACKAGES_DIR = "./pypackages"
sys.path.insert(0, PIP_PACKAGES_DIR)


# Sets the directory so urls all match up.
os.environ['SCRIPT_NAME'] = os.environ['SCRIPT_NAME'][:-
                                                      1 * len(os.path.basename(__file__))]


CGIHandler().run(app)
