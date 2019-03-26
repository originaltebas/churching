# app/ggcc/views.py
# coding: utf-8

from flask import abort, flash
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import func, or_

from app.ggcc import ggcc
from app.ggcc.forms import GGCCForm, ListaAsignacionMiembrosFrom

from app import db
from app.models import GrupoCasero, Direccion, Miembro


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@ggcc.route('/ggcc', methods=['GET', 'POST'])
@login_required
def ver_ggcc():
    """
    Ver una lista de todos los ggcc
    """
    check_admin()

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
                           ggcc=query_ggcc,
                           flag_listar=flag_listar,
                           title=u'Gestión de Grupos Caseros')


@ggcc.route('/ggcc/crear', methods=['GET', 'POST'])
@login_required
def crear_gc():
    """
    Agregar un GC a la Base de Datos
    """
    check_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    # Traer las direcciones existentes en la base de datos
    obj_dirall = Direccion.query.all()

    form = GGCCForm()

    if form.validate_on_submit():
        # Es nueva direccion --> hay que crearla
        if (form.NewDirFlag.data == "True"):
            obj_gc = GrupoCasero(nombre_grupo=form.nombre_grupo.data,
                                 descripcion_grupo=form.descripcion_grupo.data)
            obj_dir = Direccion(
                          tipo_via=form.tipo_via.data,
                          nombre_via=form.nombre_via.data,
                          nro_via=form.nro_via.data,
                          portalescalotros_via=form.portalescalotros_via.data,
                          cp_via=form.cp_via.data,
                          ciudad_via=form.ciudad_via.data,
                          provincia_via=form.provincia_via.data,
                          pais_via=form.pais_via.data
                               )
            try:
                # agrego registro de direccion
                db.session.add(obj_dir)
                # envio los cambios a la base de datos
                db.session.flush()
                # asigno el id recien creado para direccion
                # al grupo casero
                obj_gc.id_direccion = obj_dir.id

                # Agrego el registro de gc
                db.session.add(obj_gc)

                # confirmo todos los datos en la db
                db.session.commit()
                flash('Has guardado los datos correctamente.', 'db')
            except Exception as e:
                # in case department name already exists
                flash('Error:', e)
        # La direccion ya existe y ha sido asignada -->
        # solo guardo la direccion_id
        else:
            obj_gc = GrupoCasero(nombre_grupo=form.nombre_grupo.data,
                                 descripcion_grupo=form.descripcion_grupo.data,
                                 id_direccion=form.idDir.data)
            try:
                # add department to the database
                db.session.add(obj_gc)
                db.session.commit()
                flash('Has guardado los datos correctamente.', 'db')
            except Exception as e:
                # in case department name already exists
                flash('Error:', e)

        # redirect to  ver
        return redirect(url_for('ggcc.ver_ggcc'))

    # load  template
    return render_template('ggcc/base_ggcc.html',
                           action="Crear", add_ggcc=flag_crear,
                           flag_listar=flag_listar,
                           direcciones=obj_dirall,
                           form=form, title="Crear Grupo Casero")


@ggcc.route('/ggcc/modificar/<int:id>',
            methods=['GET', 'POST'])
@login_required
def modif_gc(id):
    """
    Modificar un grupo casero
    """
    check_admin()

    flag_crear = False
    flag_listar = False

    # lo hago por partes para actualizar más facil
    # la dir si se crea una nueva
    obj_gc = GrupoCasero.query.get_or_404(id)
    obj_dir = Direccion.query.get_or_404(obj_gc.id_direccion)
    obj_dirall = Direccion.query.all()

    # Instancio el formulario si pasarle ningún dato para
    # luego contectarlo a mano
    form = GGCCForm()

    if form.validate_on_submit():
        # la direccion es nueva o no se ha tocado
        if (form.NewDirFlag.data == 'True'):
            obj_gc.nombre_grupo = form.nombre_grupo.data,
            obj_gc.descripcion_grupo = form.descripcion_grupo.data

            obj_dir_nueva = Direccion(
                          tipo_via=form.tipo_via.data,
                          nombre_via=form.nombre_via.data,
                          nro_via=form.nro_via.data,
                          portalescalotros_via=form.portalescalotros_via.data,
                          cp_via=form.cp_via.data,
                          ciudad_via=form.ciudad_via.data,
                          provincia_via=form.provincia_via.data,
                          pais_via=form.pais_via.data
                               )
            try:
                # agrego registro de direccion
                db.session.add(obj_dir_nueva)
                # envio los cambios a la base de datos
                db.session.flush()
                # asigno el id recien creado para direccion
                # al grupo casero
                obj_gc.id_direccion = obj_dir_nueva.id
                # Agrego el registro de gc
                # confirmo todos los datos en la db
                db.session.commit()
                flash('Has guardado los datos correctamente.', 'db')
            except Exception as e:
                # in case department name already exists
                flash('Error:', e)

        # La direccion ya existe y ha sido asignada -->
        # solo guardo la direccion_id
        else:
            # la newdir es falsa -> entonces se seleccionó una o se modificó
            # la existente para saber si se modificó la existente uso el idDir
            # que es vacio si no se cambio.
            if (form.idDir.data == ''):
                obj_gc.nombre_grupo = form.nombre_grupo.data,
                obj_gc.descripcion_grupo = form.descripcion_grupo.data

                obj_dir.tipo_via = form.tipo_via.data
                obj_dir.nombre_via = form.nombre_via.data
                obj_dir.nro_via = form.nro_via.data
                obj_dir.portalescalotros_via = form.portalescalotros_via.data
                obj_dir.cp_via = form.cp_via.data
                obj_dir.ciudad_via = form.ciudad_via.data
                obj_dir.provincia_via = form.provincia_via.data
                obj_dir.pais_via = form.pais_via.data
                db.session.commit()
                flash('Has guardado los datos correctamente.', 'db')
            else:
                obj_gc.nombre_grupo = form.nombre_grupo.data,
                obj_gc.descripcion_grupo = form.descripcion_grupo.data
                obj_gc.id_direccion = form.idDir.data
                db.session.commit()
                flash('Has guardado los datos correctamente.', 'db')
        # redirect to  ver
        return redirect(url_for('ggcc.ver_ggcc'))
        # ## aqui se acaba el if->submit

    # asigno los datos de la base al formulario para que se vean en el template
    form.nombre_grupo.data = obj_gc.nombre_grupo
    form.descripcion_grupo.data = obj_gc.descripcion_grupo
    form.tipo_via.data = obj_dir.tipo_via
    form.nombre_via.data = obj_dir.nombre_via
    form.nro_via.data = obj_dir.nro_via
    form.portalescalotros_via.data = obj_dir.portalescalotros_via
    form.cp_via.data = obj_dir.cp_via
    form.ciudad_via.data = obj_dir.ciudad_via
    form.provincia_via.data = obj_dir.provincia_via
    form.pais_via.data = obj_dir.pais_via
    return render_template(
                'ggcc/base_ggcc.html',
                action="Modificar",
                add_ggcc=flag_crear, flag_listar=flag_listar,
                form=form, direcciones=obj_dirall,
                title="Modificar Grupo Casero")


@ggcc.route('/ggcc/borrar/<int:id>',
            methods=['GET', 'POST'])
@login_required
def borrar_gc(id):
    """
    Borrar un rol
    """
    check_admin()

    obj_gc = GrupoCasero.query.get_or_404(id)
    db.session.delete(obj_gc)
    db.session.commit()
    flash('Has borrado los datos correctamente.', 'db')

    # redirect to the departments page
    return redirect(url_for('ggcc.ver_ggcc'))

    return render_template(title='Borrar Grupo Casero')


@ggcc.route('/ggcc/asignar/elegir-gc',
            methods=['GET', 'POST'])
@login_required
def asignar_elegir():
    """
    Asignar miembros a un grupo casero
    """
    check_admin()

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
                           flag_listar=flag_listar,
                           title=u'Asignar Miembros - Elegir Grupos Caseros')


@ggcc.route('/ggcc/asignar/miembros/<int:id>',
            methods=['GET', 'POST'])
@login_required
def asignar_miembros(id):
    """
    Asignar miembros a un grupo casero
    """
    check_admin()

    flag_listar = False
    ids_miembros = ListaAsignacionMiembrosFrom()

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
                           ids_miembros=ids_miembros,
                           title=u'Asignar Miembros - Elegir Grupos Caseros')
