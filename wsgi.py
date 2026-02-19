#!/usr/bin/env python
"""
WSGI application wrapper that loads the correct Flask app based on APP_TYPE environment variable.
This allows a single Procfile to serve both the main website and admin dashboard.
"""

import os
from app import app as main_app
from admin_app import admin_app

# Determine which app to run based on environment variable
app_type = os.environ.get('APP_TYPE', 'main')

if app_type == 'admin':
    application = admin_app
else:
    application = main_app
