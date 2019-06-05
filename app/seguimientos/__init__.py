# app/extras/__init__.py

from flask import Blueprint

seguimientos = Blueprint('seguimientos', __name__)

from . import views