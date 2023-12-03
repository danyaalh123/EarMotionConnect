# -*- encoding: utf-8 -*-
"""
Original source from AppSeed.us - adapted and modified for educational purposes.
"""

from flask_minify  import Minify

from apps import app

DEBUG = app.config['DEBUG'] 

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

app.logger.info('DEBUG            = ' + str( DEBUG )                 )
app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
app.logger.info('ASSETS_ROOT      = ' + app.config['ASSETS_ROOT']    )

if __name__ == "__main__":
    app.run()
