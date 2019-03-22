# app/ggcc/__init__.py

from flask import Blueprint


ggcc = Blueprint('ggcc', __name__)

from . import views