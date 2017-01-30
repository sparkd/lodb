# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory function in app.py."""

from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_pymongo import PyMongo

extensions = [
    # Cache(),
    DebugToolbarExtension(),
    PyMongo(),
]