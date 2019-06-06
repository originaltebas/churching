# app/seguimientos/views.py
# coding: utf-8

from flask import flash, jsonify
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required

from app.seguimientos import seguimientos
from app.seguimientos.forms import SeguimientoForm, ConsultaSegForm
from app import db
from sqlalchemy import desc, false
from app.models import Seguimiento, Miembro


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


@seguimientos.route('/seguimientos', methods=['GET'])
@login_required
def ver_seguimientos():
    """
    Lista de los seguimientos realizados a las personas
    SOLO ACCESIBLE A ADMINISTRADORES
    """
    check_only_admin()

    # de arranque carga el listado
    flag_listar = True
    # flag_crear = False
    # flag_consultar = False

    query_seguimientos = db.session.query(Seguimiento)\
                                   .join(Miembro,
                                         Seguimiento.id_miembro ==
                                         Miembro.id)\
                                   .add_columns(Seguimiento.fecha_seg,
                                                Seguimiento.comentarios_seg,
                                                Seguimiento.tipo_seg,
                                                Seguimiento.id,
                                                Seguimiento.id_miembro,
                                                Miembro.fullname)\
                                   .order_by(desc(Seguimiento.fecha_seg))

    return render_template('seguimientos/base_seguimientos.html',
                           seguimientos=query_seguimientos,
                           flag_listar=flag_listar)


@seguimientos.route('/seguimientos/crear', methods=['GET', 'POST'])
@login_required
def crear_seguimiento():
    """
    Crear una entrada de seguimiento
    """
    check_edit_or_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_listar = False
    flag_crear = True
    # flag_consultar = False

    form = SeguimientoForm()

    if form.validate_on_submit():
        obj_seg = Seguimiento(fecha_seg=form.fecha_seg.data,
                              comentarios_seg=form.comentarios_seg.data,
                              id_miembro=form.id_miembro.data,
                              tipo_seg=form.tipo_seg.data)
        try:
            db.session.add(obj_seg)
            db.session.commit()
            flash('Has guardado los datos correctamente', 'success')
        except Exception as e:
            flash('Error:' + str(e), 'danger')

        return redirect(url_for('seguimientos.ver_seguimientos'))

    return render_template(
                'seguimientos/base_seguimientos.html',
                add_seguimiento=flag_crear, flag_listar=flag_listar, form=form)


@seguimientos.route('/seguimientos/modif/<int:id>',
                    methods=['GET', 'POST'])
@login_required
def modif_seguimiento(id):
    """
    Modificar un seguimiento
    """
    check_only_admin()

    flag_crear = False
    flag_listar = False
    # flag_consultar = False

    obj_seg = Seguimiento.query.get_or_404(id)

    miembro = Miembro.query.get_or_404(obj_seg.id_miembro)

    form = SeguimientoForm(obj=obj_seg)

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
        form.fecha_seg.data = obj_seg.fecha_seg
        form.comentarios_seg.data = obj_seg.comentarios_seg
        form.tipo_seg.data = obj_seg.tipo_seg
        form.id_miembro.data = obj_seg.id_miembro

    if request.method == 'POST':
        if form.validate_on_submit():
            obj_seg.fecha_seg = form.fecha_seg.data
            obj_seg.comentarios_seg = form.comentarios_seg.data
            obj_seg.tipo_seg = form.tipo_seg.data
            obj_seg.id_miembro = form.id_miembro.data
            try:
                db.session.commit()
                flash('Has modificado los datos correctamente', 'success')
            except Exception as e:
                flash('Error: ' + str(e), 'danger')

            return redirect(url_for('seguimientos.ver_seguimientos'))

    return render_template(
                'seguimientos/base_seguimientos.html', miembro=miembro,
                add_seguimiento=flag_crear, flag_listar=flag_listar, form=form)


@seguimientos.route('/seguimientos/borrar/<int:id>',
                    methods=['GET'])
@login_required
def borrar_seguimiento(id):
    """
    Borrar una entrada de seguimiento
    """
    check_only_admin()

    obj_seg = Seguimiento.query.get_or_404(id)
    try:
        db.session.delete(obj_seg)
        db.session.commit()
        flash('Has borrado los datos correctamente', 'success')
    except Exception as e:
        flash('Error: ' + str(e), 'danger')

    return redirect(url_for('seguimientos.ver_seguimientos'))


@seguimientos.route('/seguimientos/consultas',
                    methods=['GET', 'POST'])
@login_required
def consulta_seguimientos():
    """
    Consultar los seguimientos de una persona
    """
    check_only_admin()

    # flag_crear = False
    # flag_listar = False
    flag_consultar = True

    form = ConsultaSegForm()

    if form.validate_on_submit():
        listado_segs = Seguimiento.query.filter(Seguimiento.id_miembro ==
                                                form.id_miembro.data).all()
        return render_template(
                'seguimientos/base_seguimientos.html',
                flag_consultar=flag_consultar, form=form,
                seguimientos=listado_segs, flag_seguimientos=True)

    return render_template(
                'seguimientos/base_seguimientos.html',
                flag_consultar=flag_consultar, form=form)


def Convert(tup, di):
    for a, b in tup:
        di.setdefault("id", a)
        di.setdefault("name", b)
    return di


@seguimientos.route('/seguimientos/autocomplete', methods=['GET'])
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
