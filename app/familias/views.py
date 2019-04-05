# app/familias/views.py
# coding: utf-8

from flask import flash, jsonify
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func, or_

from app.familias import familias
from app.familias.forms import FamiliasForm
from app.familias.forms import DireccionModalForm, AsignacionMiembrosForm

from app import db
from app.models import Familia, Direccion, Miembro, TipoFamilia


def check_edit_or_admin():
    """
    Si no es admin o editor lo manda al inicio
    """
    if not current_user.get_urole() >= 1:
        return redirect(url_for("home.hub"))


@familias.route('/familias', methods=['GET'])
@login_required
def ver_familias():
    """
    Ver una lista de todos los familias
    """
    check_edit_or_admin()

    flag_listar = True

    nro_personas = db.session.query(Miembro.id_familia,
                                    func.count(Miembro.id_familia)
                                        .label('contar'))\
                             .group_by(Miembro.id_familia).subquery()

    query_familias = db.session.query(Familia)\
                               .join(Direccion,
                                     Familia.id_direccion ==
                                     Direccion.id)\
                               .outerjoin(nro_personas,
                                          Familia.id ==
                                          nro_personas.c.id_familia)\
                               .outerjoin(TipoFamilia,
                                          Familia.id_tipofamilia ==
                                          TipoFamilia.id)\
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
                           familias=query_familias, flag_listar=flag_listar)


@familias.route('/familias/crear', methods=['GET', 'POST'])
@login_required
def crear_familia():
    """
    Agregar un familia a la Base de Datos
    """
    check_edit_or_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = FamiliasForm()

    form.TipoFamilia.choices = [(row.id, row.tipo_familia)
                                for row in TipoFamilia.query.all()]

    if form.validate_on_submit():
        obj_familia = Familia(
                        apellidos_familia=form.apellidos_familia.data,
                        descripcion_familia=form.descripcion_familia.data,
                        telefono_familia=form.telefono_familia.data,
                        id_tipofamilia=form.TipoFamilia.data,
                        id_direccion=form.id_direccion.data)
        try:
            db.session.add(obj_familia)
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
            status = 'ok'
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
            status = 'ko'

        url = url_for('familias.ver_familias')
        return jsonify(status=status, url=url)

    return render_template('familias/base_familias.html',
                           flag_crear=flag_crear,
                           flag_listar=flag_listar, form=form)


@familias.route('/familias/modificar/<int:id>',
                methods=['GET', 'POST'])
@login_required
def modif_familia(id):
    """
    Modificar un familia
    """
    check_edit_or_admin()

    flag_crear = False
    flag_listar = False

    # lo hago por partes para actualizar más facil
    # la dir si se crea una nueva
    obj_familia = Familia.query.get_or_404(id)

    form_familia = FamiliasForm(obj=obj_familia)
    form_familia.TipoFamilia.choices = [(row.id, row.tipo_familia)
                                        for row in TipoFamilia.query.all()]

    if request.method == 'GET':
        obj_dir = Direccion.query.get_or_404(obj_familia.id_direccion)
        form_dir = DireccionModalForm(obj=obj_dir)
        form_familia.TipoFamilia.data = obj_familia.id_tipofamilia
        form_familia.id_direccion.data = obj_familia.id_direccion

    if form_familia.validate_on_submit():
        obj_familia.apellidos_familia = form_familia.apellidos_familia.data
        obj_familia.descripcion_familia = form_familia.descripcion_familia.data
        obj_familia.telefono_familia = form_familia.telefono_familia.data
        obj_familia.id_tipofamilia = form_familia.TipoFamilia.data
        obj_familia.id_direccion = form_familia.id_direccion.data
        try:
            # confirmo todos los datos en la db
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
            status = 'ok'
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
            status = 'ko'

        url = url_for('familias.ver_familias')
        return jsonify(status=status, url=url)

    return render_template('familias/base_familias.html',
                           flag_crear=flag_crear,
                           flag_listar=flag_listar,
                           form_familia=form_familia,
                           form_dir=form_dir)


@familias.route('/familias/borrar/<int:id>',
                methods=['GET'])
@login_required
def borrar_familia(id):
    """
    Borrar una familia
    """
    check_edit_or_admin()

    obj_familia = Familia.query.get_or_404(id)
    try:
        db.session.delete(obj_familia)
        db.session.commit()
        flash('Has borrado los datos correctamente.', 'success')
    except Exception as e:
        flash('Error: ' + str(e), 'danger')

    return redirect(url_for('familias.ver_familias'))


@familias.route('/familias/asignar', methods=['GET'])
@login_required
def ver_familias_asignar():
    """
    Asignar miembros a un familia
    """
    check_edit_or_admin()

    flag_listar = True

    nro_personas = db.session.query(Miembro.id_familia,
                                    func.count(Miembro.id_familia)
                                        .label('contar'))\
                             .group_by(Miembro.id_familia).subquery()

    query_familias = db.session.query(Familia)\
                               .join(Direccion,
                                     Familia.id_direccion ==
                                     Direccion.id)\
                               .outerjoin(nro_personas,
                                          Familia.id ==
                                          nro_personas.c.id_familia)\
                               .outerjoin(TipoFamilia,
                                          Familia.id_tipofamilia ==
                                          TipoFamilia.id)\
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

    return render_template('familias/base_familias_asignar.html',
                           familias=query_familias,
                           flag_listar=flag_listar)


@familias.route('/familias/asignar/miembros/<int:id>',
                methods=['GET', 'POST'])
@login_required
def asignar_miembros(id):
    """
    Asignar miembros a una Familia
    """
    check_edit_or_admin()

    flag_listar = False
    FormMiembros = AsignacionMiembrosForm()

    if request.method == 'GET':
        obj_familia = Familia.query.get_or_404(id)
        form_familia = FamiliasForm(obj=obj_familia)

        obj_miembros_in = db.session.query(Miembro.id, Miembro.nombres,
                                           Miembro.apellidos)\
                                    .filter(Miembro.id_familia == id)\
                                    .all()

        obj_miembros_out = db.session.query(Miembro.id, Miembro.nombres,
                                            Miembro.apellidos)\
                                     .filter(or_(
                                          Miembro.id_familia == 0,
                                          Miembro.id_familia.is_(None)))\
                                     .all()

        # genero una cadena de ids con los datos de los miembros
        # incluídos para guardarlos en un Hidden Field
        FormMiembros.ids_in.data = ""
        for idm in obj_miembros_in:
            FormMiembros.ids_in.data = str(FormMiembros.ids_in.data
                                           ) + str(idm.id) + ","
        # genero una cadena de ids con los datos de los miembros
        # incluídos para guardarlos en un Hidden Field
        FormMiembros.ids_out.data = ""
        for idm in obj_miembros_out:
            FormMiembros.ids_out.data = str(FormMiembros.ids_out.data)\
                                      + str(idm.id) + ","

        return render_template('familias/base_familias_asignar.html',
                               form_familia=form_familia,
                               miembros_in=obj_miembros_in,
                               miembros_out=obj_miembros_out,
                               flag_listar=flag_listar,
                               FormMiembros=FormMiembros)

    elif FormMiembros.validate_on_submit():
        ids_in = FormMiembros.ids_in.data[:-1].split(",")
        ids_out = FormMiembros.ids_out.data[:-1].split(",")

        obj_in = Miembro.query.filter(Miembro.id.in_(ids_in))
        obj_out = Miembro.query.filter(
                                or_(Miembro.id.in_(ids_out),
                                    Miembro.id.is_(None)))

        # Para borrar las relaciones de los antiguos
        for o in obj_out:
            o.id_familia = None

        # Para agregar a los recien asignados
        for m in obj_in:
            m.id_familia = id

        try:
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
        except Exception as e:
            flash('Error: ', e, 'danger')

        url = url_for('familias.ver_familias_asignar')
        return jsonify(url=url)
    else:
        # Es Post pero no pasa el validate.
        flash('Los datos de miembros no han podido modificarse', 'danger')
        return redirect(url_for('familias.ver_familias_asignar'))
        url = url_for('familias.ver_familias_asignar')
        return jsonify(url=url)
