# app/miembros/views.py
# coding: utf-8

from flask import flash, jsonify
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func

from app.miembros import miembros
from app.miembros.forms import MiembroForm, DireccionModalForm

from app import db
from app.models import Miembro, Direccion, relacion_miembros_roles
from app.models import Rol, EstadoCivil, TipoMiembro, RolFamiliar
from app.models import Familia, GrupoCasero


def check_edit_or_admin():
    """
    Si no es admin o editor lo manda al inicio
    """
    if not current_user.get_urole() >= 1:
        return redirect(url_for("home.hub"))


@miembros.route('/miembros', methods=['GET'])
@login_required
def ver_miembros():
    """
    Ver una lista de todos los miembros
    """
    check_edit_or_admin()

    flag_listar = True

    nro_roles = db.session.query(Miembro.id,
                                 func.count(Rol.id).label('contar'))\
                          .outerjoin(relacion_miembros_roles,
                                     Miembro.id ==
                                     relacion_miembros_roles.c.id_miembro)\
                          .outerjoin(Rol,
                                     Rol.id ==
                                     relacion_miembros_roles.c.id_rol)\
                          .group_by(Miembro).subquery()

    query_miembros = db.session.query(Miembro)\
                               .outerjoin(Direccion,
                                          Miembro.id_direccion ==
                                          Direccion.id)\
                               .outerjoin(TipoMiembro,
                                          Miembro.id_tipomiembro ==
                                          TipoMiembro.id)\
                               .outerjoin(nro_roles,
                                          Miembro.id ==
                                          nro_roles.c.id)\
                               .add_columns(
                                            Miembro.id,
                                            Miembro.apellidos,
                                            Miembro.nombres,
                                            Miembro.email,
                                            Miembro.telefono_fijo,
                                            Miembro.telefono_movil,
                                            Miembro.id_familia,
                                            Miembro.id_grupocasero,
                                            TipoMiembro.nombre_tipomiembro,
                                            Direccion.tipo_via,
                                            Direccion.nombre_via,
                                            Direccion.nro_via,
                                            Direccion.portalescalotros_via,
                                            Direccion.cp_via,
                                            Direccion.ciudad_via,
                                            Direccion.provincia_via,
                                            Direccion.pais_via,
                                            nro_roles.c.contar)

    return render_template('miembros/base_miembros.html',
                           miembros=query_miembros,
                           flag_listar=flag_listar)


@miembros.route('/miembros/crear', methods=['GET', 'POST'])
@login_required
def crear_miembro():
    """
    Agregar un miembro a la Base de Datos
    """
    check_edit_or_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = MiembroForm()

    form.EstadoCivil.choices = [(row.id, row.nombre_estado)
                                for row in EstadoCivil.query.all()]
    form.TipoMiembro.choices = [(row.id, row.nombre_tipomiembro)
                                for row in TipoMiembro.query.all()]
    form.RolFamiliar.choices = [(row.id, row.nombre_rolfam)
                                for row in RolFamiliar.query.all()]
    form.Familia.choices = [(row.id, row.apellidos_familia)
                            for row in Familia.query.all()]
    form.GrupoCasero.choices = [(row.id, row.nombre_grupo)
                                for row in GrupoCasero.query.all()]

    if request.method == "POST":
        if form.validate_on_submit():
            obj_miembro = Miembro(nombres=form.nombres.data,
                                  apellidos=form.apellidos.data,
                                  dni_doc=form.dni_doc.data,
                                  email=form.email.data,
                                  telefono_movil=form.telefono_movil.data,
                                  telefono_fijo=form.telefono_fijo.data,
                                  fecha_nac=form.fecha_nac.data,
                                  fecha_inicio_icecha=form.fecha_inicio_icecha.data,
                                  fecha_miembro=form.fecha_miembro.data,
                                  fecha_bautismo=form.fecha_bautismo.data,
                                  lugar_bautismo=form.lugar_bautismo.data,
                                  hoja_firmada=form.hoja_firmada.data,
                                  nro_hoja=form.nro_hoja.data,
                                  observaciones=form.observaciones.data,
                                  id_estadocivil=form.EstadoCivil.data,
                                  id_tipomiembro=form.TipoMiembro.data,
                                  id_rolfamiliar=form.RolFamiliar.data,
                                  id_familia=form.Familia.data,
                                  id_grupocasero=form.GrupoCasero.data,
                                  id_direccion=form.id_direccion.data)
            try:
                db.session.add(obj_miembro)
                db.session.commit()
                flash('Has guardado los datos correctamente', 'success')
                status = 'ok'
            except Exception as e:
                flash('Error: ' + str(e), 'danger')
                status = 'ko'

            # return submited y validated
            url = url_for('miembros.ver_miembros')
            return jsonify(status=status, url=url)
        else:
            # validation error
            status = 'val'
            url = url_for('miembros.crear_miembro')
            er = ""
            for field, errors in form.errors.items():
                for error in errors:
                    er = er + "Campo: " +\
                         getattr(form, field).label.text +\
                         " - Error: " +\
                         error + "<br/>"

            return jsonify(status=status, url=url, errors=er)
    else:
        # get
        return render_template('miembros/base_miembros.html',
                               flag_crear=flag_crear,
                               flag_listar=flag_listar, form=form)


@miembros.route('/miembros/modificar/<int:id>',
                methods=['GET', 'POST'])
@login_required
def modif_miembro(id):
    """
    Modificar un miembro
    """
    check_edit_or_admin()

    flag_crear = False
    flag_listar = False

    # lo hago por partes para actualizar más facil
    # la dir si se crea una nueva
    obj_miembro = Miembro.query.get_or_404(id)
    form_miembro = MiembroForm(obj=obj_miembro)

    form_miembro.EstadoCivil.choices = [(row.id, row.nombre_estado)
                                        for row in EstadoCivil.query.all()]
    form_miembro.TipoMiembro.choices = [(row.id, row.nombre_tipomiembro)
                                        for row in TipoMiembro.query.all()]
    form_miembro.RolFamiliar.choices = [(row.id, row.nombre_rolfam)
                                        for row in RolFamiliar.query.all()]
    form_miembro.Familia.choices = [(row.id, row.apellidos_familia)
                                    for row in Familia.query.all()]
    form_miembro.GrupoCasero.choices = [(row.id, row.nombre_grupo)
                                        for row in GrupoCasero.query.all()]

    if request.method == 'GET':
        obj_dir = Direccion.query.get_or_404(obj_miembro.id_direccion)
        form_dir = DireccionModalForm(obj=obj_dir)
        form_miembro.id_direccion.data = obj_miembro.id_direccion

        form_miembro.EstadoCivil.data = obj_miembro.id_estadocivil
        form_miembro.TipoMiembro.data = obj_miembro.id_tipomiembro
        form_miembro.RolFamiliar.data = obj_miembro.id_rolfamiliar
        form_miembro.Familia.data = obj_miembro.id_familia
        form_miembro.GrupoCasero.data = obj_miembro.id_grupocasero

        return render_template('miembros/base_miembros.html',
                               flag_crear=flag_crear,
                               flag_listar=flag_listar,
                               form=form_miembro,
                               form_dir=form_dir)

    elif request.method == "POST":
        if form_miembro.validate_on_submit():
            obj_miembro.nombres = form_miembro.nombres.data
            obj_miembro.apellidos = form_miembro.apellidos.data
            obj_miembro.dni_doc = form_miembro.dni_doc.data
            obj_miembro.email = form_miembro.email.data
            obj_miembro.telefono_movil = form_miembro.telefono_movil.data
            obj_miembro.telefono_fijo = form_miembro.telefono_fijo.data
            obj_miembro.fecha_nac = form_miembro.fecha_nac.data
            obj_miembro.fecha_inicio_icecha = form_miembro.fecha_inicio_icecha.data
            obj_miembro.fecha_miembro = form_miembro.fecha_miembro.data
            obj_miembro.fecha_bautismo = form_miembro.fecha_bautismo.data
            obj_miembro.lugar_bautismo = form_miembro.lugar_bautismo.data
            obj_miembro.hoja_firmada = form_miembro.hoja_firmada.data
            obj_miembro.nro_hoja = form_miembro.nro_hoja.data
            obj_miembro.observaciones = form_miembro.observaciones.data
            obj_miembro.id_estadocivil = form_miembro.EstadoCivil.data
            obj_miembro.id_tipomiembro = form_miembro.TipoMiembro.data
            obj_miembro.id_rolfamiliar = form_miembro.RolFamiliar.data
            obj_miembro.id_familia = form_miembro.Familia.data
            obj_miembro.id_grupocasero = form_miembro.GrupoCasero.data
            obj_miembro.id_direccion = form_miembro.id_direccion.data

            try:
                # confirmo todos los datos en la db
                db.session.commit()
                flash('Has guardado los datos correctamente', 'success')
                status = 'ok'
            except Exception as e:
                flash('Error: ' + str(e), 'danger')
                status = 'ko'
                # return submited y validated

            url = url_for('miembros.ver_miembros')
            return jsonify(status=status, url=url)
        else:
            # validation error
            status = 'val'
            url = url_for('miembros.ver_miembros')
            er = ""
            for field, errors in form_miembro.errors.items():
                for error in errors:
                    er = er + "Campo: " +\
                         getattr(form_miembro, field).label.text +\
                         " - Error: " +\
                         error + "<br/>"

            return jsonify(status=status, url=url, errors=er)


@miembros.route('/miembros/borrar/<int:id>',
                methods=['GET'])
@login_required
def borrar_miembro(id):
    """
    Borrar una miembro
    """
    check_edit_or_admin()

    obj_miembro = Miembro.query.get_or_404(id)
    try:
        db.session.delete(obj_miembro)
        db.session.commit()
        flash('Has borrado los datos correctamente.', 'success')
    except Exception as e:
        flash('Error: ' + str(e), 'danger')

    return redirect(url_for('miembros.ver_miembros'))