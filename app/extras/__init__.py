#app/__init__.py

#third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# after existing third-party imports
from flask_login import LoginManager
from flask_migrate import Migrate

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
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "Debes estar logado para acceder a esta pagina"
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models
    
    return app