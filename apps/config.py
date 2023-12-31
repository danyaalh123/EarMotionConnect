# -*- encoding: utf-8 -*-
"""
Original source from AppSeed.us - adapted and modified for educational purposes.
"""

import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
    # App Config - the minimal footprint
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_9999')
    # Spotify API Config
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URL = os.getenv('SPOTIFY_REDIRECT_URL')
