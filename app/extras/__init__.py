# app/extras/__init__.py

from flask import Blueprint

extras = Blueprint('extras', __name__)

from . import views