# app/extras/__init__.py

from flask import Blueprint

roles = Blueprint('roles', __name__)

from . import views