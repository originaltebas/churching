# app/familias/views.py
# coding: utf-8

from flask import abort, jsonify, flash, redirect
from flask import render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func
from flask_paginate import Pagination, get_page_parameter


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


@familias.route('/familias/modificar/<int:id>', methods=['GET', 'POST'])
@login_required
def modif_familia(id):
    """
    Modificar una familia
    """
    check_admin()

    flag_accion = "Modificar"

    query_familia = Familia.query.get_or_404(id)
    query_domicilio = Direccion.query.get_or_404(query_familia.id_direccion)

    form = FamiliaForm(obj=query_familia)
    form.TipoFamilia.choices = [(row.id, row.tipo_familia)
                                for row in TipoFamilia.query.all()]
    if (request.method == 'GET'):
        form.TipoFamilia.data = query_familia.id_tipofamilia
        form.idDir.data = query_familia.id_direccion

    if form.validate_on_submit():
        query_familia.apellidos_familia = form.apellidos_familia.data
        query_familia.descripcion_familia = form.descripcion_familia.data
        query_familia.telefono_familia = form.telefono_familia.data
        query_familia.id_tipofamilia = form.TipoFamilia.data
        query_familia.id_direccion = form.idDir.data

        db.session.commit()
        url = url_for('familias.ver_familias')
        return jsonify(status='ok', url=url)
    else:
        # load  template
        return render_template('familias/base_familias.html',
                               flag_accion=flag_accion,
                               domicilio=query_domicilio,
                               form=form, title="Modificar Familia")


@familias.route('/familias/modificar/actualizarDir/<int:id>',
                methods=['POST'])
@login_required
def modif_familia_update_dir(id):

    check_admin()

    obj_dir = Direccion.query.get_or_404(id)

    form = DireccionModalForm(obj=obj_dir)

    if form.validate_on_submit():
        obj_dir.tipo_via = form.tipo_via.data
        obj_dir.nombre_via = form.nombre_via.data
        obj_dir.nro_via = form.nro_via.data
        obj_dir.portalescalotros_via = form.portalescalotros_via.data
        obj_dir.piso_nroletra_via = form.piso_nroletra_via.data
        obj_dir.ciudad_via = form.ciudad_via.data
        obj_dir.cp_via = form.cp_via.data
        obj_dir.provincia_via = form.provincia_via.data
        obj_dir.pais_via = form.pais_via.data

        db.session.commit()
        return jsonify(status='ok')
    else:
        return jsonify(status="error")


@familias.route('/familias/borrar/<int:id>', methods=['GET'])
@login_required
def borrar_familia(id):
    """
    Borrar un rol
    """
    check_admin()

    obj_fam = Familia.query.get_or_404(id)
    try:
        db.session.delete(obj_fam)
        db.session.commit()
        flash(u'Registro borrado correctamente', 'success')
    except Exception as e:
        flash('Error:', e, 'danger')

    return redirect(url_for('familias.ver_familias'))


@familias.route('/familias/loadDir/<int:id>')
@login_required
def cargar_DireccionActual(id):
    check_admin()
    query = Direccion.query.get_or_404(id)
    form = DireccionModalForm(obj=query)
    return render_template('familias/_sub_direccion.html', form=form)


@familias.route('/familias/nuevadir/loadForm')
@login_required
def cargarForm_direccionblanco():
    check_admin()
    form = DireccionModalForm()
    return render_template('familias/_modal_direccion_agregar.html', form=form)


@familias.route('/familias/usardir/loadForm')
@login_required
def cargarForm_direcciones():
    check_admin()
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    nro_dirs = db.session.query(Direccion).count()

    query_dir = Direccion.query.offset(((page-1)*10)).limit(10)

    pagination = Pagination(page=page, total=nro_dirs,
                            search=search, record_name='query_dir',
                            css_framework='bootstrap4')

    return render_template('familias/_modal_direccion_usar.html',
                           direcciones=query_dir,
                           pagination=pagination)


@familias.route('/familias/nuevadir', methods=['POST'])
@login_required
def crear_nuevadir():
    check_admin()

    form = DireccionModalForm()
    if form.validate_on_submit():
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


@familias.route('/familias/usardir/')
@login_required
def usar_direccionactual():
    return render_template('familias/_modal_direccion_usar.html')


@familias.route('/familias/cambiar',
                methods=['GET', 'POST'])
@login_required
def cambiar_composicion():
    """
    Modificar los integrantes de una familia
    --> Funciones: Agregar o quitar miembros
    """

    check_admin()

    flag_accion = "ListarCompo"

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
                           title=u'Cambiar Composición de Familias')


@familias.route('/familias/cambiar/edicion/<int:id>',
                methods=['GET', 'POST'])
@login_required
def cambiar_composicion_edicion(id):
    """
    Edicion de la composición de la familia
    """
    check_admin()
