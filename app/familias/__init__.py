# app/familias/__init__.py

from flask import Blueprint


familias = Blueprint('familias', __name__)

from . import views