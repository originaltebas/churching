# app/miembros/__init__.py

from flask import Blueprint


miembros = Blueprint('miembros', __name__)

from . import views