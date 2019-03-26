# app/familias/views.py
# coding: utf-8

from flask import abort, flash, jsonify
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func

from app.familias import familias
from app.familias.forms import FamiliaForm, DireccionModalForm

from app import db
from app.models import Familia, Direccion, Miembro, TipoFamilia


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@familias.route('/familias', methods=['GET', 'POST'])
@login_required
def ver_familias():
    """
    Ver una lista de todos las familias
    """
    check_admin()

    flag_accion = "Listar"

    nro_personas = db.session.query(Miembro.id_familia,
                                    func.count(Miembro.id_familia)
                                        .label('contar'))\
                             .group_by(Miembro.id_familia).subquery()

    query_familias = db.session.query(Familia)\
                               .join(Direccion,
                                     Familia.id_direccion ==
                                     Direccion.id)\
                               .join(TipoFamilia, Familia.id_tipofamilia ==
                                     TipoFamilia.id)\
                               .outerjoin(nro_personas,
                                          Familia.id ==
                                          nro_personas.c.id_familia)\
                               .add_columns(
                                        Familia.id,
                                        Familia.apellidos_familia,
                                        Familia.descripcion_familia,
                                        Familia.telefono_familia,
                                        TipoFamilia.tipo_familia,
                                        Direccion.tipo_via,
                                        Direccion.nombre_via,
                                        Direccion.nro_via,
                                        Direccion.portalescalotros_via,
                                        Direccion.cp_via,
                                        Direccion.ciudad_via,
                                        Direccion.provincia_via,
                                        Direccion.pais_via,
                                        nro_personas.c.contar)

    return render_template('familias/base_familias.html',
                           familias=query_familias,
                           flag_accion=flag_accion,
                           title=u'Gestión de Familias')


@familias.route('/familias/crear', methods=['GET', 'POST'])
@login_required
def crear_familia():
    """
    Agregar una Familia a la Base de Datos
    """
    check_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_accion = "Agregar"

    form = FamiliaForm()

    form.TipoFamilia.choices = [(row.id, row.tipo_familia)
                                for row in TipoFamilia.query.all()]

    if form.validate_on_submit():
        obj_fam = Familia(
                    apellidos_familia=form.apellidos_familia.data,
                    descripcion_familia=form.descripcion_familia.data,
                    telefono_familia=form.telefono_familia.data,
                    id_tipofamilia=form.TipoFamilia.data,
                    id_direccion=form.idDir.data)
        db.session.add(obj_fam)
        db.session.commit()
        url = url_for('familias.ver_familias')
        return jsonify(url=url)

    # load  template
    return render_template('familias/base_familias.html',
                           flag_accion=flag_accion,
                           form=form, title="Crear Familia")


@familias.route('/familias/crear/loadDir/<int:id>')
def crear_loaddir(id):
    check_admin()
    query = Direccion.query.get_or_404(id)
    form = DireccionModalForm(obj=query)
    return render_template('familias/_sub_direccion.html', form=form)


@familias.route('/familias/crear/nuevadir/loadForm')
def crear_nuevadir_load():
    check_admin()
    form = DireccionModalForm()
    return render_template('familias/_modal_direccion_agregar.html', form=form)


@familias.route('/familias/crear/usardir/loadForm')
def crear_usardir_load():
    check_admin()
    query = Direccion.query.all()
    return render_template('familias/_modal_direccion_editar.html', direcciones=query)


@familias.route('/familias/crear/nuevadir', methods=['POST'])
def crear_nuevadir():
    check_admin()

    form = DireccionModalForm()
    if form.validate_on_submit():
        print("submit")
        obj_dir = Direccion(
                    tipo_via=form.tipo_via.data,
                    nombre_via=form.nombre_via.data,
                    nro_via=form.nro_via.data,
                    portalescalotros_via=form.portalescalotros_via.data,
                    piso_nroletra_via=form.piso_nroletra_via.data,
                    cp_via=form.cp_via.data,
                    ciudad_via=form.ciudad_via.data,
                    provincia_via=form.provincia_via.data,
                    pais_via=form.pais_via.data)
        db.session.add(obj_dir)
        db.session.flush()
        dirid = obj_dir.id
        db.session.commit()
        return jsonify(status='ok', id=dirid)
    else:
        return jsonify(status='error')


@familias.route('/familias/crear/usardir/')
def crear_usardir():
    return render_template('familias/_modal_direccion_usar.html')


@familias.route('/familias/modificar/<int:id>',
                methods=['GET', 'POST'])
@login_required
def modif_familia(id):
    """
    Modificar una familia
    """
    check_admin()


@familias.route('/familias/borrar/<int:id>',
                methods=['GET', 'POST'])
@login_required
def borrar_familia(id):
    """
    Borrar un rol
    """
