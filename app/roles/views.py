# app/roles/views.py
# coding: utf-8

from flask import flash
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.roles import roles
from app.roles.forms import RolForm

from app import db
from app.models import Rol


def check_edit_or_admin():
    """
    Si no es admin o editor lo manda al inicio
    """
    if not current_user.get_urole() >= 1:
        return redirect(url_for("home.hub"))


# SECCION: ***** Rol: PASTOR, ANCIANO; DIACONO, LIDER GRUPO CASERO *****

@roles.route('/roles/<string:flag>', methods=['GET'])
@login_required
def ver_roles(flag):
    """
    Ver una lista de todos los roles
     --- aunque es la misma tabla se mostrarán los distintos
     --- tipos de roles, misnitreros, clases, en distintas pantallas
    """
    check_edit_or_admin()

    # si flag viene vacio ir por defecto a Roles
    if (flag == ''):
        flag = 'R'

    # de arranque carga el listado
    flag_listar = True

    query_roles = Rol.query.filter_by(tipo_rol=flag)

    return render_template('roles/base_roles.html',
                           roles=query_roles,
                           flag_listar=flag_listar,
                           flag_tiporol=flag)


@roles.route('/roles/crear/<string:flag>',
             methods=['GET', 'POST'])
@login_required
def crear_rol(flag):
    """
    Agregar un Rol a la Base de Datos
    """
    check_edit_or_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = RolForm()

    if form.validate_on_submit():
        obj_rol = Rol(nombre_rol=form.nombre_rol.data,
                      descripcion_rol=form.descripcion_rol.data,
                      tipo_rol=flag)
        try:
            db.session.add(obj_rol)
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
        except Exception as e:
            flash('Error: ', e, ' danger')

        return redirect(url_for('roles.ver_roles', flag=flag))

    return render_template(
                'roles/base_roles.html',
                add_roles=flag_crear, flag_listar=flag_listar,
                flag_tiporol=flag, form=form)


@roles.route('/roles/modificar/<int:id>/<string:flag>',
             methods=['GET', 'POST'])
@login_required
def modif_rol(id, flag):
    """
    Modificar un rol
    """
    check_edit_or_admin()

    flag_crear = False
    flag_listar = False

    obj_rol = Rol.query.get_or_404(id)
    form = RolForm(obj=obj_rol)
    if form.validate_on_submit():
        obj_rol.nombre_rol = form.nombre_rol.data
        obj_rol.descripcion_rol = form.descripcion_rol.data
        obj_rol.tipo_rol = flag
        try:
            db.session.commit()
            flash('Has modificado los datos correctamente', 'success')
        except Exception as e:
            flash('Error: ' + str(e), 'danger')

        return redirect(url_for('roles.ver_roles', flag=flag))

    form.nombre_rol.data = obj_rol.nombre_rol
    form.descripcion_rol.data = obj_rol.descripcion_rol
    return render_template(
                'roles/base_roles.html',
                add_roles=flag_crear, flag_listar=flag_listar,
                form=form, rol=obj_rol, flag_tiporol=flag)


@roles.route('/roles/borrar/<int:id>/<string:flag>',
             methods=['GET'])
@login_required
def borrar_rol(id, flag):
    """
    Borrar un rol
    """
    check_edit_or_admin()

    obj_rol = Rol.query.get_or_404(id)
    db.session.delete(obj_rol)
    try:
        db.session.commit()
        flash('Has borrado los datos correctamente', 'success')
    except Exception as e:
        flash('Error: ' + str(e), 'danger')

    return redirect(url_for('roles.ver_roles', flag=flag))


