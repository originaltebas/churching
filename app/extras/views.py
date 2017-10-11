# app/extras/views.py
# coding: utf-8

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import extras
from .. import db

from forms import FormGrupoCasero, FormRol
from ..models import GrupoCasero, Rol

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@extras.route('/gruposcaseros', methods=['GET', 'POST'])
@login_required
def listar_gruposcaseros():
    """
    Lista de todos los grupos caseros
    """
    check_admin()

    gruposcaseros = GrupoCasero.query.all()

    return render_template('extras/gruposcaseros/gruposcaseros.html', gruposcaseros=gruposcaseros, title="Grupos Caseros")

@extras.route('/gruposcaseros/add', methods=['GET', 'POST'])
@login_required
def add_grupocasero():
    """
    agregar un grupo casero
    """
    check_admin()

    add_grupocasero = True

    form = FormGrupoCasero()
    if form.validate_on_submit():
        gruposcasero = GrupoCasero(nombre_grupo=form.nombre_grupo.data,descripcion_grupo=form.descripcion_grupo.data,direccion_grupo=form.direccion_grupo.data)
        try:
            # add department to the database
            db.session.add(gruposcasero)
            db.session.commit()
            flash('Has agregado un nuevo grupo casero.')
        except:
            # in case department name already exists
            flash('Error.')

        # redirect to departments page
        return redirect(url_for('extras.listar_gruposcaseros'))

    # load department template
    return render_template('extras/gruposcaseros/grupocasero.html', action="Add", add_grupocasero=add_grupocasero, form=form, title="Agregar Grupo Casero")

@extras.route('/gruposcaseros/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_grupocasero(id):
    """
    Modificar grupo casero
    """
    check_admin()

    add_grupocasero = False

    grupocasero = GrupoCasero.query.get_or_404(id)
    form = FormGrupoCasero(obj=grupocasero)
    if form.validate_on_submit():
        grupocasero.nombre_grupo = form.nombre_grupo.data
        grupocasero.descripcion_grupo = form.descripcion_grupo.data
        grupocasero.direccion_grupo = form.direccion_grupo.data
        db.session.commit()
        flash('Has modificado el grupo casero.')

        # redirect to the departments page
        return redirect(url_for('extras.listar_gruposcaseros'))

    form.descripcion_grupo = grupocasero.descripcion_grupo
    form.nombre_grupo = grupocasero.nombre_grupo
    return render_template('extras/gruposcaseros/grupocasero.html', action="Edit",
                           add_grupocasero = add_grupocasero, form=form,
                           grupocasero = grupocasero, title="Modificar Grupo Casero")

@extras.route('/gruposcaseros/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_grupocasero(id):
    """
    Delete a department from the database
    """
    check_admin()

    grupocasero = GrupoCasero.query.get_or_404(id)
    db.session.delete(grupocasero)
    db.session.commit()
    flash('Has borrado el grupo casero.')

    # redirect to the departments page
    return redirect(url_for('extras.listar_gruposcaseros'))

    return render_template(title="Borrar Grupos Caseros")


"""
AQUI FINALIZA CODIGO GRUPOS CASEROS
-------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------
AQUI COMIENZA CODIGO ROLES
"""

@extras.route('/roles')
@login_required
def listar_roles():
    check_admin()
    """
    Listar todos los roles
    """
    roles = Rol.query.all()
    return render_template('extras/roles/roles.html', roles=roles, title='Roles o Responsabilidades')

@extras.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_rol():
    """
    Agregar un rol o responsabilidad a la base de datos
    """
    check_admin()

    add_rol = True

    form = FormRol()
    if form.validate_on_submit():
        rol = Rol(nombre=form.nombre.data, descripcion=form.descripcion.data)

        try:
            # add role to the database
            db.session.add(rol)
            db.session.commit()
            flash('Has agregado un rol a la base de datos.')
        except:
            # in case role name already exists
            flash('Error: el rol ya existe.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_roles'))

    # load role template
    return render_template('extras/roles/rol.html', add_rol=add_rol, form=form, title='Agregar Rol o Responsabilidad')

@extras.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_rol(id):
    """
    Modificar un Rol
    """
    check_admin()

    add_rol = False

    rol = Rol.query.get_or_404(id)
    form = FormRol(obj=rol)
    if form.validate_on_submit():
        rol.nombre = form.nombre.data
        rol.descripcion = form.descripcion.data
        db.session.add(rol)
        db.session.commit()
        flash('Has modificado el rol en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_roles'))

    form.descripcion.data = rol.descripcion
    form.nombre.data = rol.nombre
    return render_template('admin/roles/rol.html', add_rol=add_rol, form=form, title="Modificar Rol o Responsabilidad")

@extras.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_rol(id):
    """
    Borrar un rol de la base de datos
    """
    check_admin()

    rol = Rol.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    flash('Has borrado el rol de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_roles'))

    return render_template(title="Borrar Rol o Responsabilidad")