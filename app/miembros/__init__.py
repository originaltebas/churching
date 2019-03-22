# app/miembros/__init__.py

from flask import Blueprint


auth = Blueprint('miembros', __name__)

from . import views