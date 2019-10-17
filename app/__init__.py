# -*- coding: UTF-8 -*-
# app/__init__.py

# third-party imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
# after the db variable initialization
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # en prod app.static_folder = os.path.abspath("./churching/app/static/")
    app._static_folder = os.path.abspath("app/static/")

    Bootstrap(app)
    db.init_app(app)

    app.config['PAGE_SIZE'] = 20
    app.config['VISIBLE_PAGE_COUNT'] = 10

    login_manager.init_app(app)
    login_manager.login_message = "Debes estar logado para ver esta pagina"
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    from app import models

    from .miembros import miembros as miembros_blueprint
    app.register_blueprint(miembros_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .ggcc import ggcc as ggcc_blueprint
    app.register_blueprint(ggcc_blueprint)

    from .familias import familias as familias_blueprint
    app.register_blueprint(familias_blueprint)

    from .roles import roles as roles_blueprint
    app.register_blueprint(roles_blueprint)

    from .extras import extras as extras_blueprint
    app.register_blueprint(extras_blueprint)

    from .seguimientos import seguimientos as seguimientos_blueprint
    app.register_blueprint(seguimientos_blueprint)

    from .asistencias import asistencias as asistencias_blueprint
    app.register_blueprint(asistencias_blueprint)

    from .informes import informes as informes_blueprint
    app.register_blueprint(informes_blueprint)

    return app
