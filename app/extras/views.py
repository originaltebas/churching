# app/extras/views.py
# coding: utf-8

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import extras
from forms import FormGrupoCasero
from .. import db
from ..models import GrupoCasero

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

    return render_template('extras/gruposcaseros/gruposcaseros.html', departments=gruposcaseros, title="Grupos Caseros")

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
        gruposcasero = GrupoCasero(name=form.name.data,description=form.description.data)
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
    return render_template('extras/gruposcaseros/gruposcasero.html', action="Add", add_grupocasero=add_grupocasero, form=form, title="Agregar Grupo Casero")

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
        grupocasero.descricion_grupo = form.descripcion_grupo.data
        grupocasero.direccion_grupo = form.direccion_grupo.data
        db.session.commit()
        flash('Has modificado el grupo casero.')

        # redirect to the departments page
        return redirect(url_for('extras.listar_gruposcaseros'))

    form.descripcion_grupo = grupocasero.descricion_grupo
    form.nombre_grupo = grupocasero.nombre_grupo
    return render_template('extras/gruposcaseros/gruposcasero.html', action="Edit",
                           add_grupocasero = add_grupocasero, form=form,
                           grupocasero = grupocasero, title="Modificar Grupo Casero")

@extras.route('/gruposcaseros/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
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