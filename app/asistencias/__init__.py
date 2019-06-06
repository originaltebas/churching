# app/extras/__init__.py

from flask import Blueprint

asistencias = Blueprint('asistencias', __name__)

from . import views