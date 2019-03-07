# app/home/views.py
# coding: utf-8

from flask import render_template, abort
from flask_login import current_user, login_required

from . import home


@home.route('/')
def homepage():
    """
    Pagina de Inicio / Bienvenida
    """
    return render_template('home/index.html', title="Bienvenido")


@home.route('/homenoadmin')
@login_required
def dashboard():
    """
    Pagina de Usuario NO ADMIN logado. Por ahora no muestra nada.
    Solo un mensaje diciendo que no es admin
    """
    return render_template('home/home_no_admin.html',
                           title="Panel de Control - No Admin")


@home.route('/dashboard')
@login_required
def admin_dashboard():
    """
    Pagina de panel de control de administracion
    Esta es la pagina principal de donde se va a todos lados
    """
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html',
                           title="Panel de Control Administración")
