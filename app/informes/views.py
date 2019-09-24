# app/informes/views.py
# coding: utf-8

from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required

from app.informes import informes
from app.informes.forms import FiltroInformePersonas
from app import db
from app.models import Miembro, EstadoCivil, TipoFamilia, Familia
from app.models import relacion_miembros_roles, Direccion
from app.models import TipoMiembro, GrupoCasero, Rol, RolFamiliar

from sqlalchemy import func
from sqlalchemy_filters import apply_filters

# Dentro de los informes hay algunos que tienen acceso
# de editor y otros que tienen solo administrador (Seg y Asis)


def check_edit_or_admin():
    """
    Si no es admin o editor lo manda al inicio
    """
    if not current_user.get_urole() >= 1:
        return redirect(url_for("home.hub"))


def check_only_admin():
    """
    Si no es admin o editor lo manda al inicio
    """
    if not current_user.get_urole() == 2:
        return redirect(url_for("home.hub"))


@informes.route('/informes/personas',
                methods=['GET', 'POST'])
@login_required
def informe_personas():
    """
    Listado de personas
    """
    check_edit_or_admin()

    form = FiltroInformePersonas()

    form.EstadoCivil.choices = [(0, "Sin Filtros")] +\
                               [(row.id, row.nombre_estado)
                                for row in EstadoCivil.query.all()]
    form.TipoMiembro.choices = [(0, "Sin Filtros")] +\
                               [(row.id, row.nombre_tipomiembro)
                                for row in TipoMiembro.query.all()]
    form.RolFamiliar.choices = [(0, "Sin Filtros")] +\
                               [(row.id, row.nombre_rolfam)
                                for row in RolFamiliar.query.all()]
    form.TipoFamilia.choices = [(0, "Sin Filtros")] +\
                               [(row.id, row.tipo_familia)
                                for row in TipoFamilia.query.all()]
    form.GrupoCasero.choices = [(0, "Sin Filtros")] +\
                               [(row.id, row.nombre_grupo)
                                for row in GrupoCasero.query.all()]

    if request.method == "POST":
        if form.validate_on_submit():
            '''
            cuando entrar filtros
            '''
            roles = db.session.query(Rol).join(relacion_miembros_roles,
                                               relacion_miembros_roles.c.id_rol ==
                                               Rol.id)\
                                         .join(Miembro,
                                               Miembro.id ==
                                               relacion_miembros_roles.c.id_miembro)\
                                         .add_columns(
                                             Miembro.id,
                                             Rol.nombre_rol
                                        )

            nro_roles = db.session.query(Miembro.id,
                                         func.count(Rol.id).label('contar'))\
                                  .join(relacion_miembros_roles,
                                        Miembro.id ==
                                        relacion_miembros_roles.c.id_miembro)\
                                  .join(Rol,
                                        Rol.id ==
                                        relacion_miembros_roles.c.id_rol)\
                                  .group_by(Miembro).subquery()

            query = db.session.query(Miembro)\
                              .outerjoin(Direccion,
                                         Miembro.id_direccion ==
                                         Direccion.id)\
                              .outerjoin(TipoMiembro,
                                         Miembro.id_tipomiembro ==
                                         TipoMiembro.id)\
                              .outerjoin(nro_roles,
                                         Miembro.id ==
                                         nro_roles.c.id)\
                              .outerjoin(Familia,
                                         Miembro.id_familia ==
                                         Familia.id)\
                              .outerjoin(GrupoCasero,
                                         Miembro.id_grupocasero ==
                                         GrupoCasero.id)\
                              .outerjoin(EstadoCivil,
                                         Miembro.id_estadocivil ==
                                         EstadoCivil.id)\
                              .outerjoin(RolFamiliar,
                                         Miembro.id_rolfamiliar ==
                                         RolFamiliar.id)\
                              .add_columns(
                                Miembro.id,
                                Miembro.fullname,
                                Miembro.email,
                                Miembro.telefono_fijo,
                                Miembro.telefono_movil,
                                Miembro.fecha_nac,
                                Miembro.fecha_inicio_icecha,
                                Miembro.fecha_miembro,
                                Miembro.fecha_bautismo,
                                EstadoCivil.nombre_estado,
                                RolFamiliar.nombre_rolfam,
                                Familia.apellidos_familia,
                                GrupoCasero.nombre_grupo,
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

            if form.EstadoCivil.data != 0:
                user_attribute = getattr(Miembro, 'id_estadocivil')
                user_filter = user_attribute == form.EstadoCivil.data
                query = query.filter(user_filter)

            if form.TipoFamilia.data != 0:
                user_attribute = getattr(Familia, 'id_tipofamilia')
                user_filter = user_attribute == form.TipoFamilia.data
                query = query.filter(user_filter)

            if form.RolFamiliar.data != 0:
                user_attribute = getattr(Miembro, 'id_rolfamiliar')
                user_filter = user_attribute == form.RolFamiliar.data
                query = query.filter(user_filter)

            if form.TipoMiembro.data != 0:
                user_attribute = getattr(Miembro, 'id_tipomiembro')
                user_filter = user_attribute == form.TipoMiembro.data
                query = query.filter(user_filter)

            if form.GrupoCasero.data != 0:
                user_attribute = getattr(Miembro, 'id_grupocasero')
                user_filter = user_attribute == form.GrupoCasero.data

        query_miembros = query.all()

    else:
        # get

        roles = db.session.query(Rol).join(relacion_miembros_roles,
                                           relacion_miembros_roles.c.id_rol ==
                                           Rol.id)\
                                     .join(Miembro,
                                           Miembro.id ==
                                           relacion_miembros_roles.c.id_miembro)\
                                     .add_columns(
                                         Miembro.id,
                                         Rol.nombre_rol
                                     )

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
                                   .outerjoin(Familia,
                                              Miembro.id_familia ==
                                              Familia.id)\
                                   .outerjoin(GrupoCasero,
                                              Miembro.id_grupocasero ==
                                              GrupoCasero.id)\
                                   .outerjoin(EstadoCivil,
                                              Miembro.id_estadocivil ==
                                              EstadoCivil.id)\
                                   .outerjoin(RolFamiliar,
                                              Miembro.id_rolfamiliar ==
                                              RolFamiliar.id)\
                                   .add_columns(
                                        Miembro.id,
                                        Miembro.fullname,
                                        Miembro.email,
                                        Miembro.telefono_fijo,
                                        Miembro.telefono_movil,
                                        Miembro.fecha_nac,
                                        Miembro.fecha_inicio_icecha,
                                        Miembro.fecha_miembro,
                                        Miembro.fecha_bautismo,
                                        EstadoCivil.nombre_estado,
                                        RolFamiliar.nombre_rolfam,
                                        Familia.apellidos_familia,
                                        GrupoCasero.nombre_grupo,
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

    return render_template('informes/informe_personas.html',
                           form=form, informes=query_miembros, roles=roles)


@informes.route('/informes/generar_pdf',
                methods=['GET', 'POST'])
@login_required
def generar_pdf():
    """
    Listado de personas
    """
    check_edit_or_admin()
