# app/extras/views.py
# coding: utf-8

from flask import abort, flash
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extras import extras
from app.extras.forms import EstadoCivilForm
from app import db
from app.models import EstadoCivil


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
            flash('Se han guardado los datos correctamente.','db')
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
        flash('Has modificado el estado civil correctamente.', 'db')

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


@extras.route('/extras/estadosciviles/borrar/<int:id>', methods=['GET', 'POST'])
@login_required
def borrar_estadocivil(id):
    """
    Borrar un estado civil
    """
    check_admin()

    obj_ecivil = EstadoCivil.query.get_or_404(id)
    db.session.delete(obj_ecivil)
    db.session.commit()
    flash('Has borrado el Estado Civil correctamente.', 'db')

    # redirect to the departments page
    return redirect(url_for('extras.ver_estadosciviles'))

    return render_template(title="Borrar Estado Civil")
