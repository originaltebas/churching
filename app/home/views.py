# app/home/views.py
# coding: utf-8


from flask_login import current_user, login_required, user_logged_in
from flask import redirect, url_for, render_template, request

from app.home import home

from app.home.forms import BusquedaForm


@home.route('/')
def homepage():
    """
    Pagina de Inicio / Bienvenida
    """

    # si no está logado mandar a login
    if not user_logged_in:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('home.hub'))


@home.route('/noaccess')
@login_required
def noaccess():
    """
    Pagina de Usuario NO ADMIN & NO EDITOR logado. Por ahora no muestra nada.
    Solo un mensaje diciendo que no es admin
    """
    return render_template('home/index_noaccess.html')


@home.route('/hub')
@login_required
def hub():
    """
    Redirige al dashboard correcto segun rol
    """

    if (current_user.get_urole() == 2):
        return redirect(url_for('home.dashboard_admin'))
    elif (current_user.get_urole() == 1):
        return redirect(url_for('home.dashboard_editor'))
    else:
        return redirect(url_for('home.noaccess'))


@home.route('/dashboard_admin', methods=['GET', 'POST'])
@login_required
def dashboard_admin():
    """
    Pagina de panel de control de administracion
    Esta es la pagina principal de donde se va a todos lados
    """
    # prevent non-admins from accessing the page
    if not current_user.is_admin():
        return redirect(url_for('home.noaccess'))

    form = BusquedaForm()
    return render_template('home/index_admin.html', form=form)


@home.route('/dashboard_editor')
@login_required
def dashboard_editor():
    """
    Pagina de panel de control de edicion
    restringe el acceso a cosas privadas de las personas como el seguimiento
    """

    if not current_user.get_urole() == 1:
        return redirect(url_for('home.noaccess'))

    return render_template('home/index_editor.html')


@home.route('/busqueda', methods=['POST'])
@login_required
def busqueda_rapida():
    form = BusquedaForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            if form.cadena.data != "":
                return redirect(url_for('miembros.ver_miembros',
                                        cadena=form.cadena.data))
