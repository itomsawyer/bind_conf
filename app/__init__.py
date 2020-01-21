# -*- coding:utf-8 -*-
from flask import Flask,Blueprint,session
from flask import url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin import helpers as admin_helpers
from flask_babelex import Babel
blp = Blueprint('main', __name__)

# local imports
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    Bootstrap(app)
    with app.app_context():
        db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        override = 'zh_CN'
        if override:
            session['lang'] = override
        return session.get('lang', 'en')



    from app import models, blp, action
    app.register_blueprint(blp)

    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    # Create admin
    ad = admin.Admin(app,
            name=u'BIND配置管理',
            base_template='my_master.html',
            template_mode='bootstrap3')

    from app import view
    ad.add_view(view.UserView(models.User,db.session,name=u'用户管理',roles_accepted=["superuser"]))
    ad.add_view(view.DnsForwardZoneGrpView(models.DnsForwardZoneGrp,db.session,name=u'域名组',roles_accepted=["user"]))
    ad.add_view(view.DnsForwardZoneView(models.DnsForwardZone,db.session,name=u'域名',roles_accepted=["user"]))
    ad.add_view(view.DnsForwardIpnetGrpView(models.DnsForwardIpnetGrp,db.session,name=u'源地址组',roles_accepted=["user"]))
    ad.add_view(view.DnsForwardIpnetView(models.DnsForwardIpnet,db.session,name=u'源地址',roles_accepted=["user"]))
    ad.add_view(view.DnsForwarderView(models.DnsForwarder,db.session,name=u'转发表',roles_accepted=["user"]))
    ad.add_view(view.LdnsView(models.Ldns,db.session,name=u'DNS表',roles_accepted=["user"]))
    ad.add_view(view.SubmitView(endpoint='submit',name=u'应用配置',roles_accepted=["user"]))

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=ad.base_template,
            admin_view=ad.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    return app
