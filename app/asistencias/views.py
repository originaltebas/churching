# app/asistencias/views.py
# coding: utf-8

from flask import flash, jsonify
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required

from app.asistencias import asistencias
from app.asistencias.forms import ReunionForm
from app.asistencias.forms import AsistenciaForm, ConsultaAsistenciasForm
from app import db
from sqlalchemy import desc
from app.models import Reunion, Miembro, relacion_asistencias


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


@asistencias.route('/asistencias', methods=['GET'])
@login_required
def ver_asistencias():
    """
    Lista de los reuniones para seguimiento de asistencias
    """
    check_edit_or_admin()

    # de arranque carga el listado
    flag_listar = True
    # flag_crear = False
    # flag_consultar = False

    query_asistencias = db.session.query(Reunion)\
                                  .order_by(desc(Reunion.fecha_reunion)).all()

    return render_template('asistencias/base_asistencias.html',
                           reuniones=query_asistencias,
                           flag_listar=flag_listar)


@asistencias.route('/asistencias/reunion/crear', methods=['GET', 'POST'])
@login_required
def crear_reunion():
    """
    Crear una entrada de seguimiento
    """
    check_edit_or_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_listar = False
    flag_crear = True
    # flag_consultar = False

    form = ReunionForm()

    if form.validate_on_submit():
        obj_reu = Reunion(nombre_reunion=form.nombre_reunion.data,
                          fecha_reunion=form.fecha_reunion.data,
                          comentarios_reunion=form.comentarios_reunion.data)
        try:
            db.session.add(obj_reu)
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
        except Exception as e:
            flash('Error:' + str(e), 'danger')

        return redirect(url_for('asistencias.ver_asistencias'))

    return render_template(
                'asistencias/base_asistencias.html',
                add_asistencias=flag_crear, flag_listar=flag_listar, form=form)


@asistencias.route('/asistencias/reunion/modif/<int:id>',
                   methods=['GET', 'POST'])
@login_required
def modif_reunion(id):
    """
    Modificar una reunion para dar seguimiento
    """
    check_edit_or_admin()

    flag_crear = False
    flag_listar = False
    # flag_consultar = False

    obj = Reunion.query.get_or_404(id)

    form = ReunionForm(obj=obj)

    # print('req: ', request.method)
    # print('sub: ', form.is_submitted())
    # print('val: ', form.validate())
    # er = ""
    # for field, errors in form.errors.items():
    #     for error in errors:
    #         er = er + "Campo: " +\
    #              getattr(form, field).label.text +\
    #              " - Error: " +\
    #              error + "<br/>"
    # print(er)

    if request.method == 'GET':
        form.nombre_reunion.data = obj.nombre_reunion
        form.fecha_reunion.data = obj.fecha_reunion
        form.comentarios_reunion.data = obj.comentarios_reunion

    if request.method == 'POST':
        if form.validate_on_submit():
            obj.nombre_reunion = form.nombre_reunion.data
            obj.fecha_reunion = form.fecha_reunion.data
            obj.comentarios_reunion = form.comentarios_reunion.data
            try:
                db.session.commit()
                flash('Has modificado los datos correctamente', 'success')
            except Exception as e:
                flash('Error: ' + str(e), 'danger')

            return redirect(url_for('asistencias.ver_asistencias'))

    return render_template(
                'asistencias/base_asistencias.html',
                add_asistencias=flag_crear, flag_listar=flag_listar, form=form)


@asistencias.route('/asistencias/reunion/borrar/<int:id>',
                   methods=['GET'])
@login_required
def borrar_reunion(id):
    """
    Borrar una reunion de seguimiento de asistencias
    """
    check_edit_or_admin()

    obj = Reunion.query.get_or_404(id)

    try:
        db.session.delete(obj)
        db.session.commit()
        flash('Has borrado los datos correctamente', 'success')
    except Exception as e:
        flash('Error: ' + str(e), 'danger')

    return redirect(url_for('asistencias.ver_asistencias'))


@asistencias.route('/asistencias/registrar/<int:id>',
                   methods=['GET', 'POST'])
@login_required
def registrar_asistencias(id):
    """
    Registrar asistencia a una reunion
    """
    check_edit_or_admin()

    # flag_crear = False
    # flag_listar = False
    # flag_consultar = False
    flag_registrar = True

    form = AsistenciaForm()

    if request.method == 'GET':
        query_reunion = Reunion.query.get_or_404(id)

        m_sel = db.session.query(Miembro.id,
                                 relacion_asistencias.c.id_miembro
                                 .label('seleccionado'))\
                          .outerjoin(relacion_asistencias,
                                     Miembro.id ==
                                     relacion_asistencias.c.id_miembro)\
                          .filter(relacion_asistencias.c.id_reunion == id)\
                          .subquery()

        query_miembros = db.session.query(Miembro)\
                                   .outerjoin(m_sel,
                                              m_sel.c.id == Miembro.id)\
                                   .add_columns(Miembro.id,
                                                Miembro.fullname,
                                                Miembro.email,
                                                Miembro.telefono_movil,
                                                m_sel.c.seleccionado
                                                )

        return render_template(
                'asistencias/base_asistencias.html',
                reunion=query_reunion, miembros=query_miembros,
                flag_registrar=flag_registrar, form=form)

    if request.method == 'POST':
        if form.validate_on_submit():

            id_ms = form.id_miembros.data[:].split(",")
            id_r = form.id_reunion.data

            # Traigo el objeto reunion
            reunion = db.session.query(Reunion).filter(Reunion.id == id_r)\
                                .first()

            # Cojo los actuales para eliminarlos
            obj_del = db.session.query(Miembro)\
                                .join(relacion_asistencias,
                                      Miembro.id ==
                                      relacion_asistencias.c.id_miembro)\
                                .filter(relacion_asistencias.c.id_reunion
                                        == id_r).all()

            # Cojo los nuevos para agregarlos
            obj_add = db.session.query(Miembro)\
                                .filter(Miembro.id.in_(id_ms))\
                                .all()

            for o in obj_del:
                reunion.miembros.remove(o)
                db.session.delete(reunion)

            for i in obj_add:
                reunion.miembros.append(i)
                db.session.add(reunion)

            try:
                db.session.commit()

                flash(u'Se ha registrado la asistencia correctamente.',
                      'success')
            except Exception as e:
                # error
                flash('Error:', e, 'danger')

        url = url_for('asistencias.ver_asistencias')
        return jsonify(url=url)

@asistencias.route('/asistencias/consultas',
                   methods=['GET', 'POST'])
@login_required
def consulta_asistencias():
    """
    Consultar los asistencias de una persona
    """
    check_only_admin()

    # flag_crear = False
    # flag_listar = False
    flag_consultar = True

    # solo
    form = ConsultaAsistenciasForm()

    if form.validate_on_submit():
        listado_miembros = relacion_asistencias.query\
                                      .filter(relacion_asistencias.id_miembro
                                              == form.id_miembro.data).all()
        return render_template(
                'asistencias/base_asistencias.html',
                flag_consultar=flag_consultar, form=form,
                asistencias=listado_miembros, flag_asistencias=True)

    return render_template(
                'asistencias/base_asistencias.html',
                flag_asistencias=flag_consultar, form=form)


def Convert(tup, di):
    for a, b in tup:
        di.setdefault("id", a)
        di.setdefault("name", b)
    return di


@asistencias.route('/asistencias/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    # query = db.session.query(Miembro)\
    #   .filter(Miembro.fullname.like('%' + str(search) + '%'))
    # results = [mv[0] for mv in query.all()]
    results = [(row.id, row.fullname)
               for row in Miembro.query
                                 .filter(
                Miembro.fullname.like('%' + str(search) + '%')).all()]

    resdic = {}
    Convert(results, resdic)
    print(resdic)

    return jsonify(matching_results=resdic)
