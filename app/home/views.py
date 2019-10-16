# app/home/views.py
# coding: utf-8


from flask_login import current_user, login_required, user_logged_in
from flask import redirect, url_for, render_template

from app.home import home
from app import db
from app.models import Miembro, Familia, GrupoCasero
from sqlalchemy import and_, func


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

    panel_p = datos_personas()
    panel_f = datos_familias()
    panel_gc = datos_gruposcaseros()
    return render_template('home/index_admin.html',
                           panel_p=panel_p, panel_f=panel_f,
                           panel_gc=panel_gc)


@home.route('/dashboard_editor')
@login_required
def dashboard_editor():
    """
    Pagina de panel de control de edicion
    restringe el acceso a cosas privadas de las personas como el seguimiento
    """

    if not current_user.get_urole() == 1:
        return redirect(url_for('home.noaccess'))

    panel_p = datos_personas()
    panel_f = datos_familias()
    panel_gc = datos_gruposcaseros()
    return render_template('home/index_editor.html',
                           panel_p=panel_p, panel_f=panel_f,
                           panel_gc=panel_gc)


def datos_personas():
    total_personas = db.session.query(Miembro).count()
    total_miembros = db.session.query(Miembro)\
                       .filter(Miembro.id_tipomiembro == 1).count()
    total_asistentes = db.session.query(Miembro)\
                         .filter(Miembro.id_tipomiembro == 2).count()
    total_otros = db.session.query(Miembro)\
                    .filter(and_(Miembro.id_tipomiembro != 1,
                                 Miembro.id_tipomiembro != 2)).count()

    return [total_personas, total_miembros, total_asistentes, total_otros]


def datos_familias():
    from datetime import date

    today = date.today()

    total_familias = db.session.query(Familia).count()

    total_adultos = db.session.query(Miembro)\
                      .filter(func.datediff(today, Miembro.fecha_nac) > 25)\
                      .count()

    total_jovenes = db.session.query(Miembro)\
                      .filter(and_(func.datediff(today, Miembro.fecha_nac) <= 25,
                                   func.datediff(today, Miembro.fecha_nac) >= 13))\
                      .count()
    total_ninios = db.session.query(Miembro)\
                     .filter(func.datediff(today, Miembro.fecha_nac) < 13)\
                     .count()

    return [total_familias, total_adultos, total_jovenes, total_ninios]


def datos_gruposcaseros():
    total_gc = db.session.query(GrupoCasero).count()
    total_personas = db.session.query(Miembro)\
                       .filter(Miembro.id_grupocasero.isnot(None)).count()

    grupos = db.session.query(GrupoCasero.nombre_grupo)\
                       .outerjoin(Miembro,
                                  GrupoCasero.id ==
                                  Miembro.id_grupocasero)\
                       .add_columns(func.count(Miembro.id))\
                       .group_by(GrupoCasero.nombre_grupo)\
                       .all()
    print("-----------", grupos)
    return [total_gc, total_personas, grupos]



