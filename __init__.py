from flask import Flask, redirect, url_for, Blueprint
from flask_login import LoginManager

from models import User

from init_db import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    setup_login_manager(login_manager)

    from routes import main
    from api import apiBp
    app.register_blueprint(main)
    app.register_blueprint(apiBp)

    return app


def setup_login_manager(login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('main.login'))
