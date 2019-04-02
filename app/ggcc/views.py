# app/ggcc/views.py
# coding: utf-8

from flask import flash, jsonify
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func, or_

from app.ggcc import ggcc
from app.ggcc.forms import GGCCForm, DireccionModalForm, AsignacionMiembrosForm

from app import db
from app.models import GrupoCasero, Direccion, Miembro
from flask_paginate import Pagination, get_page_parameter


def check_edit_or_admin():
    """
    Si no es admin o editor lo manda al inicio
    """
    if not current_user.get_urole() >= 1:
        return redirect(url_for("home.hub"))


@ggcc.route('/ggcc', methods=['GET'])
@login_required
def ver_ggcc():
    """
    Ver una lista de todos los ggcc
    """
    check_edit_or_admin()

    flag_listar = True

    nro_personas = db.session.query(Miembro.id_grupocasero,
                                    func.count(Miembro.id_grupocasero)
                                        .label('contar'))\
                             .group_by(Miembro.id_grupocasero).subquery()

    query_ggcc = db.session.query(GrupoCasero)\
                           .join(Direccion,
                                 GrupoCasero.id_direccion ==
                                 Direccion.id)\
                           .outerjoin(nro_personas,
                                      GrupoCasero.id ==
                                      nro_personas.c.id_grupocasero)\
                           .add_columns(
                                        GrupoCasero.id,
                                        GrupoCasero.nombre_grupo,
                                        GrupoCasero.descripcion_grupo,
                                        Direccion.tipo_via,
                                        Direccion.nombre_via,
                                        Direccion.nro_via,
                                        Direccion.portalescalotros_via,
                                        Direccion.cp_via,
                                        Direccion.ciudad_via,
                                        Direccion.provincia_via,
                                        Direccion.pais_via,
                                        nro_personas.c.contar)

    return render_template('ggcc/base_ggcc.html',
                           ggcc=query_ggcc, flag_listar=flag_listar)


@ggcc.route('/ggcc/crear', methods=['GET', 'POST'])
@login_required
def crear_gc():
    """
    Agregar un GC a la Base de Datos
    """
    check_edit_or_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = GGCCForm()

    if form.validate_on_submit():
        obj_gc = GrupoCasero(nombre_grupo=form.nombre_grupo.data,
                             descripcion_grupo=form.descripcion_grupo.data,
                             id_direccion=form.id_direccion.data)
        try:
            db.session.add(obj_gc)
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
            status = 'ok'
        except Exception as e:
            flash('Error: ', e, 'danger')
            status = 'ko'

        url = url_for('ggcc.ver_ggcc')
        return jsonify(status=status, url=url)

    return render_template('ggcc/base_ggcc.html',
                           flag_crear=flag_crear,
                           flag_listar=flag_listar, form=form)


@ggcc.route('/ggcc/modificar/<int:id>',
            methods=['GET', 'POST'])
@login_required
def modif_gc(id):
    """
    Modificar un grupo casero
    """
    check_edit_or_admin()

    flag_crear = False
    flag_listar = False

    # lo hago por partes para actualizar más facil
    # la dir si se crea una nueva
    obj_gc = GrupoCasero.query.get_or_404(id)

    if request.method == 'GET':
        obj_dir = Direccion.query.get_or_404(obj_gc.id_direccion)
        form_dir = DireccionModalForm(obj=obj_dir)

    # Instancio el formulario si pasarle ningún dato para
    # luego contectarlo a mano
    form_gc = GGCCForm(obj=obj_gc)

    if form_gc.validate_on_submit():
        obj_gc.nombre_grupo = form_gc.nombre_grupo.data,
        obj_gc.descripcion_grupo = form_gc.descripcion_grupo.data
        obj_gc.id_direccion = form_gc.id_direccion.data

        try:
            # confirmo todos los datos en la db
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
            status = 'ok'
        except Exception as e:
            flash('Error: ', e, 'danger')
            status = 'ko'

        url = url_for('ggcc.ver_ggcc')
        return jsonify(status=status, url=url)

    return render_template(
                'ggcc/base_ggcc.html', flag_crear=flag_crear,
                flag_listar=flag_listar, form_gc=form_gc, form_dir=form_dir)


@ggcc.route('/ggcc/borrar/<int:id>',
            methods=['GET'])
@login_required
def borrar_gc(id):
    """
    Borrar un rol
    """
    check_edit_or_admin()

    obj_gc = GrupoCasero.query.get_or_404(id)
    db.session.delete(obj_gc)
    db.session.commit()
    flash('Has borrado los datos correctamente.', 'db')

    return redirect(url_for('ggcc.ver_ggcc'))


@ggcc.route('/ggcc/asignar/elegir-gc',
            methods=['GET', 'POST'])
@login_required
def asignar_elegir():
    """
    Asignar miembros a un grupo casero
    """
    check_edit_or_admin()

    flag_listar = True

    nro_personas = db.session.query(Miembro.id_grupocasero,
                                    func.count(Miembro.id_grupocasero)
                                        .label('contar'))\
                             .group_by(Miembro.id_grupocasero).subquery()

    query_ggcc = db.session.query(GrupoCasero)\
                           .join(Direccion,
                                 GrupoCasero.id_direccion ==
                                 Direccion.id)\
                           .outerjoin(nro_personas,
                                      GrupoCasero.id ==
                                      nro_personas.c.id_grupocasero)\
                           .add_columns(
                                        GrupoCasero.id,
                                        GrupoCasero.nombre_grupo,
                                        GrupoCasero.descripcion_grupo,
                                        Direccion.tipo_via,
                                        Direccion.nombre_via,
                                        Direccion.nro_via,
                                        Direccion.portalescalotros_via,
                                        Direccion.cp_via,
                                        Direccion.ciudad_via,
                                        Direccion.provincia_via,
                                        Direccion.pais_via,
                                        nro_personas.c.contar)

    return render_template('ggcc/base_asignar.html',
                           ggcc=query_ggcc,
                           flag_listar=flag_listar)


@ggcc.route('/ggcc/asignar/miembros/<int:id>',
            methods=['GET', 'POST'])
@login_required
def asignar_miembros(id):
    """
    Asignar miembros a un grupo casero
    """
    check_edit_or_admin()

    flag_listar = False
    ids_miembros = AsignacionMiembrosForm()

    if request.method == 'GET':
        obj_gc = GrupoCasero.query.get_or_404(id)
        obj_miembros_incluidos = Miembro.query\
                                        .filter(Miembro.id_grupocasero == id)

        obj_miembros_todos = Miembro.query\
                                    .filter(or_(
                                         Miembro.id_grupocasero != id,
                                         Miembro.id_grupocasero.is_(None)))

        ids_miembros.ids.data = ""
        for idm in obj_miembros_incluidos:
            ids_miembros.ids.data = str(ids_miembros.ids.data)\
                                  + str(idm.id) + ","

        ids_miembros.ids_totales.data = ""
        for idm in obj_miembros_todos:
            ids_miembros.ids_totales.data = str(ids_miembros.ids_totales.data)\
                                            + str(idm.id) + ","

    if ids_miembros.validate_on_submit():
        # los miembros SÍ se han tocado -- hay que grabar de nuevo
        if (ids_miembros.modifFlag.data == 'True'):
            # Hay que hacer 2 cosas. Quitar a los que
            # se han ido y agregar los nuevos

            ids_inc = ids_miembros.ids.data[:-1].split(",")
            ids_no_inc = ids_miembros.ids_totales.data[:-1].split(",")
            obj_inc = Miembro.query\
                             .filter(Miembro.id.in_(ids_inc))
            obj_no_inc = Miembro.query\
                                .filter(or_(Miembro.id.in_(ids_no_inc),
                                            Miembro.id.is_(None)))

            # Para borrar las relaciones de los antiguos
            for o in obj_no_inc:
                o.id_grupocasero = None

            # Para agregar a los recien asignados
            for m in obj_inc:
                m.id_grupocasero = id

            db.session.commit()
            flash('Has guardado los datos correctamente.', 'db')
        else:
            # los miembros no se han tocado. no hacer nada.
            flash('Has guardado los datos correctamente.', 'db')

        return redirect(url_for('ggcc.asignar_elegir'))

    return render_template('ggcc/base_asignar.html',
                           gc=obj_gc,
                           miembros_in=obj_miembros_incluidos,
                           miembros_all=obj_miembros_todos,
                           flag_listar=flag_listar,
                           ids_miembros=ids_miembros)


@ggcc.route('/direcciones/loadFormNueva')
@login_required
def cargarForm_direccionblanco():
    check_edit_or_admin()
    form = DireccionModalForm(prefix="m_")
    return render_template('ggcc/_modal_direccion_agregar.html', form=form)


@ggcc.route('/direcciones/loadFormUsar')
@login_required
def cargarForm_direcciones():
    check_edit_or_admin()
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

    return render_template('ggcc/_modal_direccion_usar.html',
                           direcciones=query_dir,
                           pagination=pagination)


@ggcc.route('/direcciones/loadDir/<int:id>')
@login_required
def cargar_Direccion(id):
    check_edit_or_admin()
    query = Direccion.query.get_or_404(id)
    form = DireccionModalForm(obj=query)
    return render_template('ggcc/_sub_direccion.html', form=form)


@ggcc.route('/direcciones/creardireccion', methods=['POST'])
@login_required
def crear_nuevadir():
    check_edit_or_admin()

    form = DireccionModalForm(prefix="m_")

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
        try:
            db.session.add(obj_dir)
            db.session.flush()
            dirid = obj_dir.id
            db.session.commit()
            return jsonify(status='ok', id=dirid)
        except Exception as e:
            return jsonify(status='ko'+str(e))
    else:
        errores = []
        # no se ha validado correctamente
        for field, errors in form.errors.items():
            for error in errors:
                errores.append((getattr(form, field).name))
        return jsonify(status='v_error', errores=errores)
