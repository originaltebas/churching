# app/extras/views.py
# coding: utf-8

from app.extras import extras
from app import db

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extras.forms import FormMiembro
# ,

# FormTipoMiembro, FormEstadoCivil
# from forms import FormRol, FormFamilia, FormTipoFamilia
# from forms import FormRolFamiliar, FormDireccion, FormTelefono
# from forms import FormAsistencia, FormSeguimiento, FormGrupoCasero

# from ..models import GrupoCasero, Rol, EstadoCivil
# from ..models import Familia, TipoMiembro, TipoParentezco
from app.models import Miembro


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


"""
 VISTAS DE MIEMBROS
"""
# LISTAR MIEMBROS
@extras.route('/miembros')
@login_required
def listar_miembros():
    check_admin()

    new_miembros = Miembro.query.all()
    return render_template('extras/miembros/listar_miembros.html',
                           miembros=new_miembros, title='Miembros')

# AGREGAR UN MIEMBRO
@extras.route('/miembros/add', methods=['GET', 'POST'])
@login_required
def add_miembro():
    check_admin()

    add_miembro = True

    form = FormMiembro()
    new_miembro = Miembro()

    try:
        # add estado to the database
        db.session.add(new_miembro)
        db.session.commit()
        flash('Has agregado un miembro a la base de datos.')
    except:
        # in case role name already exists
        flash('Error: El miembro ya existe.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_miembros'))

    # load role template
    return render_template('extras/miembros/miembro.html',
                           add_miembro=add_miembro, form=form,
                           title='Agregar un Miembro')


"""
@extras.route('/miembros/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_miembro(id):
    check_admin()

    add_miembro = False

    miembro = Miembro.query.get_or_404(id)
    form = FormMiembro(obj=miembro)

    if form.validate_on_submit():
        miembro.nombres = form.nombres.data
        miembro.apellidos = form.apellidos.data
        miembro.email = form.email.data
        miembro.direccion = form.direccion.data
        miembro.telefono_1 = form.telefono_1.data
        miembro.telefono_2 = form.telefono_2.data

        miembro.fecha_nac = form.fecha_nac.data
        miembro.fecha_bautismo = form.fecha_bautismo.data
        miembro.fecha_miembro = form.fecha_miembro.data

        miembro.id_familia = form.familia.data
        miembro.id_parentezco = form.parentezco.data
        miembro.id_estadocivil = form.estadocivil.data
        miembro.id_tipo_miembro = form.tipomiembro.data
        miembro.id_grupo_casero = form.grupocasero.data
        miembro.miembros_roles.id_rol = form.rol.data
        miembro.miembros_roles.id_miembro = form.id.data

        db.session.add(miembro)
        db.session.commit()
        flash('Has modificado el miembro en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_miembros'))

    form.nombres.data= miembro.nombres
    form.apellidos.data = miembro.apellidos
    form.email.data = miembro.email
    form.direccion.data = miembro.direccion
    form.telefono_1.data = miembro.telefono_1
    form.telefono_2.data = miembro.telefono_2

    form.fecha_nac.data = miembro.fecha_nac
    form.fecha_bautismo.data = miembro.fecha_bautismo
    form.fecha_miembro.data = miembro.fecha_miembro

    form.familia.data = miembro.id_familia
    form.parentezco.data = miembro.id_parentezco
    form.estadocivil.data = miembro.id_estadocivil
    form.tipomiembro.data = miembro.id_tipo_miembro
    form.grupocasero.data = miembro.id_grupo_casero
    form.rol.data = miembro.miembros_roles.id_rol
    form.id.data = miembro.miembros_roles.id_miembro

    return render_template('extras/miembros/miembro.html',
                           add_miembro=add_miembro,
                           form=form, title="Modificar Miembro")


@extras.route('/miembros/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_miembro(id):
    check_admin()

    miembro = Miembro.query.get_or_404(id)

    db.session.delete(miembro)
    db.session.commit()
    flash('Has borrado un miembro de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_miembros'))

    return render_template(title="Borrar Miembro")
"""
