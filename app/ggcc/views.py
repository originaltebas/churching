# app/extras/views.py
# coding: utf-8

from flask import abort, flash
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.ggcc import ggcc
from app.ggcc.forms import GGCCForm

from app import db
from app.models import GrupoCasero, Direccion


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# SECCION: ***** Rol: PASTOR, ANCIANO; DIACONO, LIDER GRUPO CASERO *****

@ggcc.route('/ggcc', methods=['GET', 'POST'])
@login_required
def ver_ggcc():
    """
    Ver una lista de todos los ggcc
    """
    check_admin()

    flag_listar = True

    query_ggcc = db.session.query(GrupoCasero).join(
                        Direccion,
                        GrupoCasero.id_direccion == Direccion.id).add_columns(
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
                                        Direccion.pais_via)

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
            obj_dir = Direccion(tipo_via=form.tipo_via.data,
                                nombre_via=form.nombre_via.data,
                                nro_via=form.nro_via.data,
                                portalescalotro=form.portalescalotro_via.data,
                                cp_via=form.cp_via.data,
                                ciudad_via=form.ciudad_via.data,
                                provincia_via=form.provincia_via.data,
                                pais_via=form.pais_via.data)
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
    Modificar un rol
    """
    check_admin()


@ggcc.route('/ggcc/borrar/<int:id>',
            methods=['GET', 'POST'])
@login_required
def borrar_gc(id):
    """
    Borrar un rol
    """
    check_admin()
