# app/roles/views.py
# coding: utf-8

from flask import abort, flash
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.roles import roles
from app.roles.forms import RolForm

from app import db
from app.models import Rol


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# SECCION: ***** Rol: PASTOR, ANCIANO; DIACONO, LIDER GRUPO CASERO *****

@roles.route('/roles/<string:flag>', methods=['GET', 'POST'])
@login_required
def ver_roles(flag):
    """
    Ver una lista de todos los roles
     --- aunque es la misma tabla se mostrarán los distintos
     --- tipos de roles, misnitreros, clases, en distintas pantallas
    """
    check_admin()

    # si flag viene vacio ir por defecto a Roles
    if (flag == ''):
        flag = 'R'

    if (flag == 'R'):
        tit = 'Gestión de Roles de la Iglesia'

    elif (flag == 'M'):
        tit = 'Gestión de Ministerios de la Iglesia'

    elif (flag == 'C'):
        tit = 'Gestión de Clases de Escuela Dominical \
                                 y Talleres de la Iglesia'

    # de arranque carga el listado
    flag_listar = True

    query_roles = Rol.query.filter_by(tipo_rol=flag)

    return render_template('roles/base_roles.html',
                           roles=query_roles,
                           flag_listar=flag_listar,
                           flag_tiporol=flag,
                           title=tit)


@roles.route('/roles/crear/<string:flag>',
             methods=['GET', 'POST'])
@login_required
def crear_rol(flag):
    """
    Agregar un Rol a la Base de Datos
    """
    check_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False
    if (flag == 'R'):
        tit = 'Crear Rol'

    elif (flag == 'M'):
        tit = 'Crear Ministerio'

    elif (flag == 'C'):
        tit = 'Crear Clase'

    form = RolForm()

    if form.validate_on_submit():
        obj_rol = Rol(nombre_rol=form.nombre_rol.data,
                      descripcion_rol=form.descripcion_rol.data,
                      tipo_rol=flag)

        try:
            # add department to the database
            db.session.add(obj_rol)
            db.session.commit()
            flash('Has guardado los datos correctamente.', 'db')
        except Exception as e:
            # in case department name already exists
            flash('Error:', e)

        # redirect to departments page
        return redirect(url_for('roles.ver_roles', flag=flag))

    # load department template
    return render_template(
                'roles/base_roles.html',
                action="Crear", add_roles=flag_crear,
                flag_listar=flag_listar,
                flag_tiporol=flag,
                form=form, title=tit)


@roles.route('/roles/modificar/<int:id>/<string:flag>',
             methods=['GET', 'POST'])
@login_required
def modif_rol(id, flag):
    """
    Modificar un rol
    """
    check_admin()

    if (flag == 'R'):
        tit = 'Modificar Rol'

    elif (flag == 'M'):
        tit = 'Modificar Ministerio'

    elif (flag == 'C'):
        tit = 'Modificar Clase'

    flag_crear = False
    flag_listar = False

    obj_rol = Rol.query.get_or_404(id)
    form = RolForm(obj=obj_rol)
    if form.validate_on_submit():
        obj_rol.nombre_rol = form.nombre_rol.data
        obj_rol.descripcion_rol = form.descripcion_rol.data
        obj_rol.tipo_rol = flag
        db.session.commit()
        flash('Has modificado los datos correctamente.', 'db')

        # redirect to the ver page
        return redirect(url_for('roles.ver_roles', flag=flag))

    form.nombre_rol.data = obj_rol.nombre_rol
    form.descripcion_rol.data = obj_rol.descripcion_rol
    return render_template(
                'roles/base_roles.html',
                action="Modificar",
                add_roles=flag_crear, flag_listar=flag_listar,
                form=form, rol=obj_rol, flag_tiporol=flag, title=tit)


@roles.route('/roles/borrar/<int:id>/<string:flag>',
             methods=['GET', 'POST'])
@login_required
def borrar_rol(id, flag):
    """
    Borrar un rol
    """
    check_admin()

    if (flag == 'R'):
        tit = 'Borrar Rol'

    elif (flag == 'M'):
        tit = 'Borrar Ministerio'

    elif (flag == 'C'):
        tit = 'Borrar Clase'

    obj_rol = Rol.query.get_or_404(id)
    db.session.delete(obj_rol)
    db.session.commit()
    flash('Has borrado los datos correctamente.', 'db')

    # redirect to the departments page
    return redirect(url_for('roles.ver_roles', flag=flag))

    return render_template(title=tit)
