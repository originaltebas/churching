
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
            roles = db.session.query(Rol).join(
                                          relacion_miembros_roles,
                                          relacion_miembros_roles.c.id_rol ==
                                          Rol.id)\
                                         .join(
                                          Miembro,
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


@informes.route('/informes/pdf_personas',
                methods=['GET', 'POST'])
@login_required
def pdf_personas():  # flag de generar pdf
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

    from flask_weasyprint import HTML, render_pdf

    salida = render_template('informes/pdf_personas.html',
                             informes=query_miembros,
                             roles=roles)

    return render_pdf(HTML(string=salida))


@informes.route('/informes/familias',
                methods=['GET', 'POST'])
@login_required
def informe_familias():
    """
    Listado de familias
    """
    check_edit_or_admin()

    integrantes = db.session.query(Miembro)\
                            .join(Familia,
                                  Familia.id ==
                                  Miembro.id_familia)\
                            .join(RolFamiliar,
                                  RolFamiliar.id ==
                                  Miembro.id_rolfamiliar)\
                            .add_columns(
                                        Miembro.id_familia,
                                        Miembro.fullname,
                                        RolFamiliar.nombre_rolfam,
                                        Miembro.id_direccion
                                               .label('dir_miembro'),
                                        Familia.id_direccion
                                               .label('dir_familia')
                                    )

    query = db.session.query(Familia)\
                      .join(Direccion,
                            Familia.id_direccion ==
                            Direccion.id)\
                      .join(TipoFamilia,
                            Familia.id_tipofamilia ==
                            TipoFamilia.id)\
                      .add_columns(
                            Familia.id,
                            Familia.id_direccion,
                            Familia.apellidos_familia,
                            Familia.descripcion_familia,
                            Familia.telefono_familia,
                            Direccion.tipo_via,
                            Direccion.nombre_via,
                            Direccion.nro_via,
                            Direccion.portalescalotros_via,
                            Direccion.cp_via,
                            Direccion.ciudad_via,
                            Direccion.provincia_via,
                            Direccion.pais_via,
                            TipoFamilia.tipo_familia
                            )

    query_miembros = query.all()

    return render_template('informes/informe_familias.html',
                           informes=query_miembros, integrantes=integrantes)


@informes.route('/informes/pdf_familias',
                methods=['GET'])
@login_required
def pdf_familias():  # flag de generar pdf
    """
    Listado de familias
    """
    check_edit_or_admin()

    integrantes = db.session.query(Miembro)\
                            .join(Familia,
                                  Familia.id ==
                                  Miembro.id_familia)\
                            .join(RolFamiliar,
                                  RolFamiliar.id ==
                                  Miembro.id_rolfamiliar)\
                            .add_columns(
                                        Miembro.id_familia,
                                        Miembro.fullname,
                                        RolFamiliar.nombre_rolfam,
                                        Miembro.id_direccion
                                               .label('dir_miembro'),
                                        Familia.id_direccion
                                               .label('dir_familia')
                                    )

    query = db.session.query(Familia)\
                      .join(Direccion,
                            Familia.id_direccion ==
                            Direccion.id)\
                      .join(TipoFamilia,
                            Familia.id_tipofamilia ==
                            TipoFamilia.id)\
                      .add_columns(
                            Familia.id,
                            Familia.id_direccion,
                            Familia.apellidos_familia,
                            Familia.descripcion_familia,
                            Familia.telefono_familia,
                            Direccion.tipo_via,
                            Direccion.nombre_via,
                            Direccion.nro_via,
                            Direccion.portalescalotros_via,
                            Direccion.cp_via,
                            Direccion.ciudad_via,
                            Direccion.provincia_via,
                            Direccion.pais_via,
                            TipoFamilia.tipo_familia
                            )

    query_miembros = query.all()

    from flask_weasyprint import HTML, render_pdf

    salida = render_template('informes/pdf_familias.html',
                             informes=query_miembros, integrantes=integrantes)

    return render_pdf(HTML(string=salida))


@informes.route('/informes/ggcc',
                methods=['GET', 'POST'])
@login_required
def informe_ggcc():
    """
    Listado de ggcc
    """
    check_edit_or_admin()

    integrantes = db.session.query(Miembro)\
                            .join(GrupoCasero,
                                  GrupoCasero.id ==
                                  Miembro.id_grupocasero)\
                            .join(TipoMiembro,
                                  TipoMiembro.id ==
                                  Miembro.id_tipomiembro)\
                            .add_columns(
                                        Miembro.id_grupocasero,
                                        Miembro.id,
                                        Miembro.fullname,
                                        TipoMiembro.nombre_tipomiembro
                                    )

    query = db.session.query(GrupoCasero)\
                      .join(Direccion,
                            GrupoCasero.id_direccion ==
                            Direccion.id)\
                      .add_columns(
                            GrupoCasero.id,
                            GrupoCasero.id_direccion,
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
                            )

    query_miembros = query.all()

    return render_template('informes/informe_ggcc.html',
                           informes=query_miembros, integrantes=integrantes)


@informes.route('/informes/pdf_ggcc',
                methods=['GET'])
@login_required
def pdf_ggcc():  # flag de generar pdf
    """
    Listado de ggcc
    """
    check_edit_or_admin()

    integrantes = db.session.query(Miembro)\
                            .join(GrupoCasero,
                                  GrupoCasero.id ==
                                  Miembro.id_grupocasero)\
                            .join(TipoMiembro,
                                  TipoMiembro.id ==
                                  Miembro.id_tipomiembro)\
                            .add_columns(
                                        Miembro.id_grupocasero,
                                        Miembro.id,
                                        Miembro.fullname,
                                        TipoMiembro.nombre_tipomiembro
                                    )

    query = db.session.query(GrupoCasero)\
                      .join(Direccion,
                            GrupoCasero.id_direccion ==
                            Direccion.id)\
                      .add_columns(
                            GrupoCasero.id,
                            GrupoCasero.id_direccion,
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
                            )

    query_miembros = query.all()

    from flask_weasyprint import HTML, render_pdf

    salida = render_template('informes/pdf_ggcc.html',
                             informes=query_miembros, integrantes=integrantes)
    print(salida)
    return render_pdf(HTML(string=salida))


@informes.route('/informes/responsables',
                methods=['GET', 'POST'])
@login_required
def informe_responsables():
    """
    Listado de personas
    """

    check_edit_or_admin()

    roles = db.session.query(Rol).filter(Rol.tipo_rol == 'R')\
                                 .join(relacion_miembros_roles,
                                       relacion_miembros_roles.c.id_rol ==
                                       Rol.id)\
                                 .join(Miembro,
                                       Miembro.id ==
                                       relacion_miembros_roles.c.id_miembro)\
                                 .add_columns(
                                     Miembro.id,
                                     Rol.nombre_rol)

    query = db.session.query(Miembro)\
                      .outerjoin(relacion_miembros_roles,
                                 Miembro.id ==
                                 relacion_miembros_roles.c.id_miembro)\
                      .outerjoin(Rol,
                                 Rol.id ==
                                 relacion_miembros_roles.c.id_rol)\
                      .outerjoin(Direccion,
                                 Miembro.id_direccion ==
                                 Direccion.id)\
                      .outerjoin(TipoMiembro,
                                 Miembro.id_tipomiembro ==
                                 TipoMiembro.id)\
                      .outerjoin(EstadoCivil,
                                 Miembro.id_estadocivil ==
                                 EstadoCivil.id)\
                      .filter(Rol.tipo_rol == 'R')\
                      .add_columns(
                              Miembro.id,
                              Miembro.fullname,
                              Miembro.email,
                              Miembro.telefono_fijo,
                              Miembro.telefono_movil,
                              EstadoCivil.nombre_estado,
                              TipoMiembro.nombre_tipomiembro,
                              Direccion.tipo_via,
                              Direccion.nombre_via,
                              Direccion.nro_via,
                              Direccion.portalescalotros_via,
                              Direccion.cp_via,
                              Direccion.ciudad_via,
                              Direccion.provincia_via,
                              Direccion.pais_via)

    query_miembros = query.all()

    return render_template('informes/informe_responsables.html',
                           informes=query_miembros, roles=roles)


@informes.route('/informes/pdf_responsables',
                methods=['GET', 'POST'])
@login_required
def pdf_responsables():  # flag de generar pdf
    """
    Listado de personas
    """
    check_edit_or_admin()

    roles = db.session.query(Rol).filter(Rol.tipo_rol == 'R')\
                                 .join(relacion_miembros_roles,
                                       relacion_miembros_roles.c.id_rol ==
                                       Rol.id)\
                                 .join(Miembro,
                                       Miembro.id ==
                                       relacion_miembros_roles.c.id_miembro)\
                                 .add_columns(
                                     Miembro.id,
                                     Rol.nombre_rol)

    query = db.session.query(Miembro)\
                      .outerjoin(relacion_miembros_roles,
                                 Miembro.id ==
                                 relacion_miembros_roles.c.id_miembro)\
                      .outerjoin(Rol,
                                 Rol.id ==
                                 relacion_miembros_roles.c.id_rol)\
                      .outerjoin(Direccion,
                                 Miembro.id_direccion ==
                                 Direccion.id)\
                      .outerjoin(TipoMiembro,
                                 Miembro.id_tipomiembro ==
                                 TipoMiembro.id)\
                      .outerjoin(EstadoCivil,
                                 Miembro.id_estadocivil ==
                                 EstadoCivil.id)\
                      .filter(Rol.tipo_rol == 'R')\
                      .add_columns(
                              Miembro.id,
                              Miembro.fullname,
                              Miembro.email,
                              Miembro.telefono_fijo,
                              Miembro.telefono_movil,
                              EstadoCivil.nombre_estado,
                              TipoMiembro.nombre_tipomiembro,
                              Direccion.tipo_via,
                              Direccion.nombre_via,
                              Direccion.nro_via,
                              Direccion.portalescalotros_via,
                              Direccion.cp_via,
                              Direccion.ciudad_via,
                              Direccion.provincia_via,
                              Direccion.pais_via)

    query_miembros = query.all()

    from flask_weasyprint import HTML, render_pdf

    salida = render_template('informes/pdf_responsables.html',
                             informes=query_miembros,
                             roles=roles)

    return render_pdf(HTML(string=salida))


@informes.route('/informes/ministerios',
                methods=['GET', 'POST'])
@login_required
def informe_ministerios():
    """
    Listado de personas
    """

    check_edit_or_admin()

    roles = db.session.query(Rol).filter(Rol.tipo_rol == 'M')\
                                 .join(relacion_miembros_roles,
                                       relacion_miembros_roles.c.id_rol ==
                                       Rol.id)\
                                 .join(Miembro,
                                       Miembro.id ==
                                       relacion_miembros_roles.c.id_miembro)\
                                 .add_columns(
                                     Miembro.id,
                                     Rol.nombre_rol)

    query = db.session.query(Miembro)\
                      .outerjoin(relacion_miembros_roles,
                                 Miembro.id ==
                                 relacion_miembros_roles.c.id_miembro)\
                      .outerjoin(Rol,
                                 Rol.id ==
                                 relacion_miembros_roles.c.id_rol)\
                      .outerjoin(Direccion,
                                 Miembro.id_direccion ==
                                 Direccion.id)\
                      .outerjoin(TipoMiembro,
                                 Miembro.id_tipomiembro ==
                                 TipoMiembro.id)\
                      .outerjoin(EstadoCivil,
                                 Miembro.id_estadocivil ==
                                 EstadoCivil.id)\
                      .filter(Rol.tipo_rol == 'M')\
                      .add_columns(
                              Miembro.id,
                              Miembro.fullname,
                              Miembro.email,
                              Miembro.telefono_fijo,
                              Miembro.telefono_movil,
                              EstadoCivil.nombre_estado,
                              TipoMiembro.nombre_tipomiembro,
                              Direccion.tipo_via,
                              Direccion.nombre_via,
                              Direccion.nro_via,
                              Direccion.portalescalotros_via,
                              Direccion.cp_via,
                              Direccion.ciudad_via,
                              Direccion.provincia_via,
                              Direccion.pais_via)

    query_miembros = query.all()

    return render_template('informes/informe_ministerios.html',
                           informes=query_miembros, roles=roles)


@informes.route('/informes/pdf_ministerios',
                methods=['GET', 'POST'])
@login_required
def pdf_ministerios():  # flag de generar pdf
    """
    Listado de personas
    """
    check_edit_or_admin()

    roles = db.session.query(Rol).filter(Rol.tipo_rol == 'M')\
                                 .join(relacion_miembros_roles,
                                       relacion_miembros_roles.c.id_rol ==
                                       Rol.id)\
                                 .join(Miembro,
                                       Miembro.id ==
                                       relacion_miembros_roles.c.id_miembro)\
                                 .add_columns(
                                     Miembro.id,
                                     Rol.nombre_rol)

    query = db.session.query(Miembro)\
                      .outerjoin(relacion_miembros_roles,
                                 Miembro.id ==
                                 relacion_miembros_roles.c.id_miembro)\
                      .outerjoin(Rol,
                                 Rol.id ==
                                 relacion_miembros_roles.c.id_rol)\
                      .outerjoin(Direccion,
                                 Miembro.id_direccion ==
                                 Direccion.id)\
                      .outerjoin(TipoMiembro,
                                 Miembro.id_tipomiembro ==
                                 TipoMiembro.id)\
                      .outerjoin(EstadoCivil,
                                 Miembro.id_estadocivil ==
                                 EstadoCivil.id)\
                      .filter(Rol.tipo_rol == 'M')\
                      .add_columns(
                              Miembro.id,
                              Miembro.fullname,
                              Miembro.email,
                              Miembro.telefono_fijo,
                              Miembro.telefono_movil,
                              EstadoCivil.nombre_estado,
                              TipoMiembro.nombre_tipomiembro,
                              Direccion.tipo_via,
                              Direccion.nombre_via,
                              Direccion.nro_via,
                              Direccion.portalescalotros_via,
                              Direccion.cp_via,
                              Direccion.ciudad_via,
                              Direccion.provincia_via,
                              Direccion.pais_via)

    query_miembros = query.all()

    from flask_weasyprint import HTML, render_pdf

    salida = render_template('informes/pdf_ministerios.html',
                             informes=query_miembros,
                             roles=roles)

    return render_pdf(HTML(string=salida))


@informes.route('/informes/clases',
                methods=['GET', 'POST'])
@login_required
def informe_clases():
    """
    Listado de personas
    """
    check_edit_or_admin()

    roles = db.session.query(Rol).filter(Rol.tipo_rol == 'C')\
                                 .join(relacion_miembros_roles,
                                       relacion_miembros_roles.c.id_rol ==
                                       Rol.id)\
                                 .join(Miembro,
                                       Miembro.id ==
                                       relacion_miembros_roles.c.id_miembro)\
                                 .add_columns(
                                     Miembro.id,
                                     Rol.nombre_rol)

    query = db.session.query(Miembro)\
                      .outerjoin(relacion_miembros_roles,
                                 Miembro.id ==
                                 relacion_miembros_roles.c.id_miembro)\
                      .outerjoin(Rol,
                                 Rol.id ==
                                 relacion_miembros_roles.c.id_rol)\
                      .outerjoin(Direccion,
                                 Miembro.id_direccion ==
                                 Direccion.id)\
                      .outerjoin(TipoMiembro,
                                 Miembro.id_tipomiembro ==
                                 TipoMiembro.id)\
                      .outerjoin(EstadoCivil,
                                 Miembro.id_estadocivil ==
                                 EstadoCivil.id)\
                      .filter(Rol.tipo_rol == 'C')\
                      .add_columns(
                              Miembro.id,
                              Miembro.fullname,
                              Miembro.email,
                              Miembro.telefono_fijo,
                              Miembro.telefono_movil,
                              EstadoCivil.nombre_estado,
                              TipoMiembro.nombre_tipomiembro,
                              Direccion.tipo_via,
                              Direccion.nombre_via,
                              Direccion.nro_via,
                              Direccion.portalescalotros_via,
                              Direccion.cp_via,
                              Direccion.ciudad_via,
                              Direccion.provincia_via,
                              Direccion.pais_via)

    query_miembros = query.all()

    return render_template('informes/informe_clases.html',
                           informes=query_miembros, roles=roles)


@informes.route('/informes/pdf_clases',
                methods=['GET', 'POST'])
@login_required
def pdf_clases():  # flag de generar pdf
    """
    Listado de personas
    """
    check_edit_or_admin()

    roles = db.session.query(Rol).filter(Rol.tipo_rol == 'C')\
                                 .join(relacion_miembros_roles,
                                       relacion_miembros_roles.c.id_rol ==
                                       Rol.id)\
                                 .join(Miembro,
                                       Miembro.id ==
                                       relacion_miembros_roles.c.id_miembro)\
                                 .add_columns(
                                     Miembro.id,
                                     Rol.nombre_rol)

    query = db.session.query(Miembro)\
                      .outerjoin(relacion_miembros_roles,
                                 Miembro.id ==
                                 relacion_miembros_roles.c.id_miembro)\
                      .outerjoin(Rol,
                                 Rol.id ==
                                 relacion_miembros_roles.c.id_rol)\
                      .outerjoin(Direccion,
                                 Miembro.id_direccion ==
                                 Direccion.id)\
                      .outerjoin(TipoMiembro,
                                 Miembro.id_tipomiembro ==
                                 TipoMiembro.id)\
                      .outerjoin(EstadoCivil,
                                 Miembro.id_estadocivil ==
                                 EstadoCivil.id)\
                      .filter(Rol.tipo_rol == 'C')\
                      .add_columns(
                              Miembro.id,
                              Miembro.fullname,
                              Miembro.email,
                              Miembro.telefono_fijo,
                              Miembro.telefono_movil,
                              EstadoCivil.nombre_estado,
                              TipoMiembro.nombre_tipomiembro,
                              Direccion.tipo_via,
                              Direccion.nombre_via,
                              Direccion.nro_via,
                              Direccion.portalescalotros_via,
                              Direccion.cp_via,
                              Direccion.ciudad_via,
                              Direccion.provincia_via,
                              Direccion.pais_via)

    query_miembros = query.all()

    from flask_weasyprint import HTML, render_pdf

    salida = render_template('informes/pdf_clases.html',
                             informes=query_miembros,
                             roles=roles)

    return render_pdf(HTML(string=salida))
