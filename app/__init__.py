# third-party imports
from flask import Flask,redirect,Blueprint
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

blp = Blueprint('main', __name__)

# local imports
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    #app.config.from_pyfile('config.py')

    #app.config['SECRET_KEY'] = '123456790'
    ## Create in-memory database
    #app.config['DATABASE_FILE'] = 'iwg'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/' + app.config['DATABASE_FILE']

    Bootstrap(app)
    with app.app_context():
        db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from app import models

    @app.route('/')
    def index():
        return redirect("/admin/",code=301)

    from . import action
    app.register_blueprint(blp)

    # Create admin
    ad = admin.Admin(app, name='IWG', template_mode='bootstrap3')

    from app import view
    ad.add_view(view.DnsForwardZoneView(db.session))

    return app
