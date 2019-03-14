# app/extras/views.py
# coding: utf-8

from flask import abort, flash
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extras import extras
from app.extras.forms import EstadoCivilForm, TipoMiembroForm, RolFamiliarForm
from app import db
from app.models import EstadoCivil, TipoMiembro, RolFamiliar


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# SECCION: *****ESTADOS CIVILES*****

@extras.route('/extras/estadosciviles', methods=['GET', 'POST'])
@login_required
def ver_estadosciviles():
    """
    Ver una lista de todos los estados civiles
    con la opción de modificar, borrar o agregar uno nuevo
    """
    check_admin()

    # de arranque carga el listado
    flag_listar = True

    query_ecivil = EstadoCivil.query.all()

    return render_template('extras/estadosciviles/base_estadosciviles.html',
                           estadosciviles=query_ecivil,
                           flag_listar=flag_listar,
                           title=u"Gestión de Estados Civiles")


@extras.route('/extras/estadosciviles/crear', methods=['GET', 'POST'])
@login_required
def crear_estadocivil():
    """
    Agregar un Estado Civil a la Base de Datos
    """
    check_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = EstadoCivilForm()
    if form.validate_on_submit():
        obj_ecivil = EstadoCivil(nombre_estado=form.nombre_ec.data,
                                 descripcion_estado=form.descripcion_ec.data)
        try:
            # add department to the database
            db.session.add(obj_ecivil)
            db.session.commit()
            flash('Has guardado los datos correctamente.', 'db')
        except Exception as e:
            # in case department name already exists
            flash('Error:', e)

        # redirect to departments page
        return redirect(url_for('extras.ver_estadosciviles'))

    # load department template
    return render_template(
                'extras/estadosciviles/base_estadosciviles.html',
                action="Crear", add_estadocivil=flag_crear,
                flag_listar=flag_listar,
                form=form, title="Crear Estado Civil")


@extras.route('/extras/estadosciviles/modif/<int:id>', methods=['GET', 'POST'])
@login_required
def modif_estadocivil(id):
    """
    Modificar un estado civil
    """
    check_admin()

    flag_crear = False
    flag_listar = False

    obj_ecivil = EstadoCivil.query.get_or_404(id)
    form = EstadoCivilForm(obj=obj_ecivil)
    if form.validate_on_submit():
        obj_ecivil.nombre_estado = form.nombre_ec.data
        obj_ecivil.descripcion_estado = form.descripcion_ec.data
        db.session.commit()
        flash('Has modificado los datos correctamente.', 'db')

        # redirect to the departments page
        return redirect(url_for('extras.ver_estadosciviles'))

    form.nombre_ec.data = obj_ecivil.nombre_estado
    form.descripcion_ec.data = obj_ecivil.descripcion_estado
    return render_template(
                'extras/estadosciviles/base_estadosciviles.html',
                action="Modificar",
                add_estadocivil=flag_crear, flag_listar=flag_listar,
                form=form, estadocivil=obj_ecivil,
                title="Modificar Estado Civil")


@extras.route('/extras/estadosciviles/borrar/<int:id>',
              methods=['GET', 'POST'])
@login_required
def borrar_estadocivil(id):
    """
    Borrar un estado civil
    """
    check_admin()

    obj_ecivil = EstadoCivil.query.get_or_404(id)
    db.session.delete(obj_ecivil)
    db.session.commit()
    flash('Has borrado los datos correctamente.', 'db')

    # redirect to the departments page
    return redirect(url_for('extras.ver_estadosciviles'))

    return render_template(title="Borrar Estado Civil")


# SECCION: *****TIPOS DE MIEMBROS*****

@extras.route('/extras/tiposmiembros', methods=['GET', 'POST'])
@login_required
def ver_tiposmiembros():
    """
    Ver una lista de todos los tipos de miembros de la iglesia
    con la opción de modificar, borrar o agregar uno nuevo
    """
    check_admin()

    # de arranque carga el listado
    flag_listar = True

    query_tmiembro = TipoMiembro.query.all()

    return render_template('extras/tiposmiembros/base_tiposmiembros.html',
                           tiposmiembros=query_tmiembro,
                           flag_listar=flag_listar,
                           title=u"Gestión de Tipos de Miembros")


@extras.route('/extras/tiposmiembros/crear', methods=['GET', 'POST'])
@login_required
def crear_tipomiembro():
    """
    Agregar un Tipo de Miembro a la Base de Datos
    """
    check_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = TipoMiembroForm()
    if form.validate_on_submit():
        obj_tmiembro = TipoMiembro(
                            nombre_tipomiembro=form.nombre_tm.data,
                            descripcion_tipomiembro=form.descripcion_tm.data)
        try:
            # add department to the database
            db.session.add(obj_tmiembro)
            db.session.commit()
            flash('Has guardado los datos correctamente.', 'db')
        except Exception as e:
            # in case department name already exists
            flash('Error:', e)

        # redirect to departments page
        return redirect(url_for('extras.ver_tiposmiembros'))

    # load department template
    return render_template(
                'extras/tiposmiembros/base_tiposmiembros.html',
                action="Crear", add_tipomiembro=flag_crear,
                flag_listar=flag_listar,
                form=form, title="Crear Tipo de Miembro")


@extras.route('/extras/tiposmiembros/modif/<int:id>', methods=['GET', 'POST'])
@login_required
def modif_tipomiembro(id):
    """
    Modificar un tipo de miembro
    """
    check_admin()

    flag_crear = False
    flag_listar = False

    obj_tmiembro = TipoMiembro.query.get_or_404(id)
    form = TipoMiembroForm(obj=obj_tmiembro)
    if form.validate_on_submit():
        obj_tmiembro.nombre_tipomiembro = form.nombre_tm.data
        obj_tmiembro.descripcion_tipomiembro = form.descripcion_tm.data
        db.session.commit()
        flash('Has modificado los datos correctamente.', 'db')

        # redirect to the departments page
        return redirect(url_for('extras.ver_tiposmiembros'))

    form.nombre_tm.data = obj_tmiembro.nombre_tipomiembro
    form.descripcion_tm.data = obj_tmiembro.descripcion_tipomiembro
    return render_template(
                'extras/tiposmiembros/base_tiposmiembros.html',
                action="Modificar",
                add_tipomiembro=flag_crear, flag_listar=flag_listar,
                form=form, tipomiembro=obj_tmiembro,
                title="Modificar Tipo de Miembro")


@extras.route('/extras/tiposmiembros/borrar/<int:id>', methods=['GET', 'POST'])
@login_required
def borrar_tipomiembro(id):
    """
    Borrar un tipo de miembros
    """
    check_admin()

    obj_tmiembro = TipoMiembro.query.get_or_404(id)
    db.session.delete(obj_tmiembro)
    db.session.commit()
    flash('Has borrado los datos correctamente.', 'db')

    # redirect to the departments page
    return redirect(url_for('extras.ver_tiposmiembros'))

    return render_template(title="Borrar Tipo de Miembro")


# SECCION: ***** ROLES FAMILIARES *****

@extras.route('/extras/rolesfamiliares', methods=['GET', 'POST'])
@login_required
def ver_rolesfamiliares():
    """
    Ver una lista de todos los roles familiares de la iglesia
    con la opción de modificar, borrar o agregar uno nuevo
    """
    check_admin()

    # de arranque carga el listado
    flag_listar = True

    query_rfamiliar = RolFamiliar.query.all()

    return render_template('extras/rolesfamiliares/base_rolesfamiliares.html',
                           rolesfamiliares=query_rfamiliar,
                           flag_listar=flag_listar,
                           title=u"Gestión de Roles Familiares")


@extras.route('/extras/rolesfamiliares/crear', methods=['GET', 'POST'])
@login_required
def crear_rolfamiliar():
    """
    Agregar un Rol Familiar a la Base de Datos
    """
    check_admin()

    # Variable para el template. Para decirle si es Alta o Modif
    flag_crear = True
    flag_listar = False

    form = RolFamiliarForm()
    if form.validate_on_submit():
        obj_rfamiliar = RolFamiliar(
                            nombre_rolfam=form.nombre_rf.data,
                            descripcion_rolfam=form.descripcion_rf.data)
        try:
            # add department to the database
            db.session.add(obj_rfamiliar)
            db.session.commit()
            flash('Has guardado los datos correctamente.', 'db')
        except Exception as e:
            # in case department name already exists
            flash('Error:', e)

        # redirect to departments page
        return redirect(url_for('extras.ver_rolesfamiliares'))

    # load department template
    return render_template(
                'extras/rolesfamiliares/base_rolesfamiliares.html',
                action="Crear", add_rolfamiliar=flag_crear,
                flag_listar=flag_listar,
                form=form, title="Crear Rol Familiar")


@extras.route('/extras/rolesfamiliares/modif/<int:id>',
              methods=['GET', 'POST'])
@login_required
def modif_rolfamiliar(id):
    """
    Modificar un rol familiar
    """
    check_admin()

    flag_crear = False
    flag_listar = False

    obj_rfamiliar = RolFamiliar.query.get_or_404(id)
    form = RolFamiliarForm(obj=obj_rfamiliar)
    if form.validate_on_submit():
        obj_rfamiliar.nombre_rolfam = form.nombre_rf.data
        obj_rfamiliar.descripcion_rolfam = form.descripcion_rf.data
        db.session.commit()
        flash('Has modificado los datos correctamente.', 'db')

        # redirect to the departments page
        return redirect(url_for('extras.ver_rolesfamiliares'))

    form.nombre_rf.data = obj_rfamiliar.nombre_rolfam
    form.descripcion_rf.data = obj_rfamiliar.descripcion_rolfam
    return render_template(
                'extras/rolesfamiliares/base_rolesfamiliares.html',
                action="Modificar",
                add_tipomiebro=flag_crear, flag_listar=flag_listar,
                form=form, rolfamiliar=obj_rfamiliar,
                title="Modificar Tipo de Miembro")


@extras.route('/extras/rolesfamiliares/borrar/<int:id>',
              methods=['GET', 'POST'])
@login_required
def borrar_rolfamiliar(id):
    """
    Borrar un rol familiar
    """
    check_admin()

    obj_rfamiliar = RolFamiliar.query.get_or_404(id)
    db.session.delete(obj_rfamiliar)
    db.session.commit()
    flash('Has borrado los datos correctamente.', 'db')

    # redirect to the departments page
    return redirect(url_for('extras.ver_rolesfamiliares'))

    return render_template(title="Borrar Rol Familiar")
