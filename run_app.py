#!/usr/bin/env python
"""Entry point script that runs the correct Flask app based on environment"""

import os
import sys

app_type = os.environ.get('APP_TYPE', 'main')

if app_type == 'admin':
    from admin_app import admin_app
    if __name__ == '__main__':
        admin_app.run()
else:
    from app import app
    if __name__ == '__main__':
        app.run()
