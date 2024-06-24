import os
from . import create_app

from init_db import db

config_name = os.getenv('FLASK_CONFIG') or 'config.DevelopmentConfig'
app = create_app(config_name)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
