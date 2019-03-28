# app/home/views.py
# coding: utf-8


from flask_login import current_user, login_required, user_logged_in
from flask import redirect, url_for, render_template, abort

from . import home


@home.route('/')
def homepage():
    """
    Pagina de Inicio / Bienvenida
    """
    user = current_user

    # si no está logado mandar a login
    if not user_logged_in:
        return redirect(url_for('auth.login'))
    elif user.is_admin:
        return redirect(url_for('home.dashboard_admin'))
    elif user.is_editor:
        return redirect(url_for('home.dashboard_editor'))
    else:
        return redirect(url_for('home.noaccess'))


@home.route('/noaccess')
@login_required
def noaccess():
    """
    Pagina de Usuario NO ADMIN & NO EDITOR logado. Por ahora no muestra nada.
    Solo un mensaje diciendo que no es admin
    """
    return render_template('home/index_noaccess.html')


@home.route('/dashboard_admin')
@login_required
def dashboard_admin():
    """
    Pagina de panel de control de administracion
    Esta es la pagina principal de donde se va a todos lados
    """
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/index_admin.html')


@home.route('/dashboard_editor')
@login_required
def dashboard_editor():
    """
    Pagina de panel de control de edicion
    restringe el acceso a cosas privadas de las personas como el seguimiento
    """

    if not current_user.is_editor:
        abort(403)

    return render_template('home/index_editor.html')
