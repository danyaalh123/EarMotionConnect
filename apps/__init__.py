# -*- encoding: utf-8 -*-
"""
Original source from AppSeed.us - adapted and modified for educational purposes.
"""

import os

# import Flask 
from flask import Flask

from .config import Config

# Create Flask app
app = Flask(__name__)

# load Configuration
app.config.from_object( Config ) 

# Import routing to render the pages
from apps import views
