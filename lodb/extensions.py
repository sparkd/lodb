# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory function in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flaskext.csrf import csrf

csrf = csrf
cache = Cache()
debug_toolbar = DebugToolbarExtension()
