# app/extras/views.py
# coding: utf-8

from flask import abort, flash
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.ggcc import ggcc
from app.ggcc.forms import GGCCForm

from app import db
from app.models import GrupoCasero, Direccion


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# SECCION: ***** Rol: PASTOR, ANCIANO; DIACONO, LIDER GRUPO CASERO *****

@ggcc.route('/ggcc', methods=['GET', 'POST'])
@login_required
def ver_ggcc():
    """
    Ver una lista de todos los ggcc
    """
    check_admin()

    flag_listar = True

    query_ggcc = GrupoCasero.query.join(
                        Direccion,
                        GrupoCasero.id_direccion == Direccion.id)

    return render_template('ggcc/base_ggcc.html',
                           ggcc=query_ggcc,
                           flag_listar=flag_listar,
                           title=u'Gestión de Grupos Caseros')


@ggcc.route('/ggcc/crear', methods=['GET', 'POST'])
@login_required
def crear_gc():
    """
    Agregar un GC a la Base de Datos
    """
    check_admin()


@ggcc.route('/ggcc/modificar/<int:id>',
            methods=['GET', 'POST'])
@login_required
def modif_gc(id):
    """
    Modificar un rol
    """
    check_admin()


@ggcc.route('/ggcc/borrar/<int:id>',
            methods=['GET', 'POST'])
@login_required
def borrar_rol(id):
    """
    Borrar un rol
    """
    check_admin()
