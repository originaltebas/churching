# app/informes/__init__.py

from flask import Blueprint

informes = Blueprint('informes', __name__)

from . import views