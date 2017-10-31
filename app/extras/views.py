# app/extras/views.py
# coding: utf-8

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import extras
from .. import db

from forms import FormGrupoCasero, FormRol, FormEstadoCivil
from forms import FormParentezco, FormFamilia, FormTipoMiembro
from ..models import GrupoCasero, Rol, EstadoCivil, Parentezco, Familia, TipoMiembro

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@extras.route('/gruposcaseros', methods = ['GET', 'POST'])
@login_required
def listar_gruposcaseros():
    """
    Lista de todos los grupos caseros
    """
    check_admin()

    gruposcaseros = GrupoCasero.query.all()

    return render_template('extras/gruposcaseros/gruposcaseros.html', 
                            gruposcaseros = gruposcaseros, title = "Grupos Caseros")

@extras.route('/gruposcaseros/add', methods = ['GET', 'POST'])
@login_required
def add_grupocasero():
    """
    agregar un grupo casero
    """
    check_admin()

    add_grupocasero = True

    form = FormGrupoCasero()
    if form.validate_on_submit():
        gruposcasero = GrupoCasero(nombre_grupo = form.nombre_grupo.data, descripcion_grupo = form.descripcion_grupo.data,
                                   direccion_grupo = form.direccion_grupo.data)
        try:
            # add department to the database
            db.session.add(gruposcasero)
            db.session.commit()
            flash('Has agregado un nuevo grupo casero.')
        except:
            # in case department name already exists
            flash('Error.')

        # redirect to departments page
        return redirect(url_for('extras.listar_gruposcaseros'))

    # load department template
    return render_template('extras/gruposcaseros/grupocasero.html', action = "Add", add_grupocasero = add_grupocasero, 
                           form = form, title = "Agregar Grupo Casero")

@extras.route('/gruposcaseros/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_grupocasero(id):
    """
    Modificar grupo casero
    """
    check_admin()

    add_grupocasero = False

    grupocasero = GrupoCasero.query.get_or_404(id)
    form = FormGrupoCasero(obj = grupocasero)
    if form.validate_on_submit():
        grupocasero.nombre_grupo = form.nombre_grupo.data
        grupocasero.descripcion_grupo = form.descripcion_grupo.data
        grupocasero.direccion_grupo = form.direccion_grupo.data
        db.session.commit()
        flash('Has modificado el grupo casero.')

        # redirect to the departments page
        return redirect(url_for('extras.listar_gruposcaseros'))

    form.descripcion_grupo = grupocasero.descripcion_grupo
    form.nombre_grupo = grupocasero.nombre_grupo
    return render_template('extras/gruposcaseros/grupocasero.html', action="Edit",
                           add_grupocasero = add_grupocasero, form=form,
                           grupocasero = grupocasero, title="Modificar Grupo Casero")

@extras.route('/gruposcaseros/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_grupocasero(id):
    """
    Delete a department from the database
    """
    check_admin()

    grupocasero = GrupoCasero.query.get_or_404(id)
    db.session.delete(grupocasero)
    db.session.commit()
    flash('Has borrado el grupo casero.')

    # redirect to the departments page
    return redirect(url_for('extras.listar_gruposcaseros'))

    return render_template(title = "Borrar Grupos Caseros")


"""
AQUI FINALIZA CODIGO GRUPOS CASEROS
-------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------
AQUI COMIENZA CODIGO ROLES
"""

@extras.route('/roles')
@login_required
def listar_roles():
    check_admin()

    """
    Listar todos los roles
    """
    roles = Rol.query.all()
    return render_template('extras/roles/roles.html', roles=roles, title='Roles o Responsabilidades')

@extras.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_rol():
    """
    Agregar un rol o responsabilidad a la base de datos
    """
    check_admin()

    add_rol = True

    form = FormRol()
    if form.validate_on_submit():
        rol = Rol(nombre=form.nombre.data, descripcion=form.descripcion.data)

        try:
            # add role to the database
            db.session.add(rol)
            db.session.commit()
            flash('Has agregado un rol a la base de datos.')
        except:
            # in case role name already exists
            flash('Error: el rol ya existe.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_roles'))

    # load role template
    return render_template('extras/roles/rol.html', add_rol=add_rol, form=form, title='Agregar Rol o Responsabilidad')

@extras.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_rol(id):
    """
    Modificar un Rol
    """
    check_admin()

    add_rol = False

    rol = Rol.query.get_or_404(id)
    form = FormRol(obj=rol)
    if form.validate_on_submit():
        rol.nombre = form.nombre.data
        rol.descripcion = form.descripcion.data
        db.session.add(rol)
        db.session.commit()
        flash('Has modificado el rol en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_roles'))

    form.descripcion.data = rol.descripcion
    form.nombre.data = rol.nombre
    return render_template('admin/roles/rol.html', add_rol=add_rol, form=form, title="Modificar Rol o Responsabilidad")

@extras.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_rol(id):
    """
    Borrar un rol de la base de datos
    """
    check_admin()

    rol = Rol.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    flash('Has borrado el rol de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_roles'))

    return render_template(title="Borrar Rol o Responsabilidad")


"""
AQUI FINALIZA CODIGO ROLES
-------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------
AQUI COMIENZA CODIGO ESTADO CIVILES
"""

@extras.route('/estadosciviles')
@login_required
def listar_estadosciviles():
    check_admin()

    """
    Listar todos los estados civiles
    """
    estadosciviles = EstadoCivil.query.all()
    return render_template('extras/estadosciviles/estadosciviles.html', estadosciviles=estadosciviles, title='Estados Civiles')

@extras.route('/estadosciviles/add', methods=['GET', 'POST'])
@login_required
def add_estadocivil():
    """
    Agregar un estado civile a la base de datos
    """
    check_admin()

    add_estadocivil = True

    form = FormEstadoCivil()
    if form.validate_on_submit():
        estadocivil = EstadoCivil(nombre=form.nombre.data, descripcion=form.descripcion.data)

        try:
            # add estado to the database
            db.session.add(estadocivil)
            db.session.commit()
            flash('Has agregado un estado civil a la base de datos.')
        except:
            # in case role name already exists
            flash('Error: el estado civil ya existe.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_estadosciviles'))

    # load role template
    return render_template('extras/estadosciviles/estadocivil.html', add_estadocivil=add_estadocivil, form=form, title='Agregar Estado Civil')

@extras.route('/estadosciviles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_estadocivil(id):
    """
    Modificar un Estado Civil
    """
    check_admin()

    add_estadocivil = False

    estadocivil = EstadoCivil.query.get_or_404(id)
    form = FormEstadoCivil(obj=estadocivil)
    if form.validate_on_submit():
        estadocivil.nombre = form.nombre.data
        estadocivil.descripcion = form.descripcion.data
        db.session.add(estadocivil)
        db.session.commit()
        flash('Has modificado el estado civil en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_estadosciviles'))

    form.descripcion.data = estadocivil.descripcion
    form.nombre.data = estadocivil.nombre
    return render_template('admin/estadosciviles/estadocivil.html', add_estadocivil=add_estadocivil, form=form, title="Modificar Estado Civil")

@extras.route('/estadosciviles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_estadocivil(id):
    """
    Borrar un estado civil de la base de datos
    """
    check_admin()

    estadocivil = EstadoCivil.query.get_or_404(id)
    db.session.delete(estadocivil)
    db.session.commit()
    flash('Has borrado el estado civil de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_estadosciviles'))

    return render_template(title="Borrar Estado Civil")

"""
AQUI FINALIZA CODIGO ESTADOS CIVILES
-------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------
AQUI COMIENZA CODIGO PARENTEZCOS

EL CONCEPTO SE ESCAPA UN POCO PERO LA IDEA ES DEFINIR SU POSICION DENTRO DEL GRUPO FAMILIAR. POR EJEMPLO FAMILIA 1, PEREZ-PEREZ, HABRÁ ALGUNO
QUE SEA EL PADRE, OTRO MADRE, OTRO HIJO, OTRO ABUELA, SIEMPRE DENTRO DEL GRUPO FAMILIAR.

"""

@extras.route('/parentezcos')
@login_required
def listar_parentezcos():
    check_admin()

    """
    Listar todos los parentezcos
    """
    parentezcos = Parentezco.query.all()
    return render_template('extras/parentezcos/parentezcos.html', parentezcos=parentezcos, title='Parentezcos')

@extras.route('/parentezcos/add', methods=['GET', 'POST'])
@login_required
def add_parentezco():
    """
    Agregar un parentezco a la base de datos
    """
    check_admin()

    add_parentezco = True

    form = FormParentezco()
    if form.validate_on_submit():
        parentezco = Parentezco(nombre=form.nombre.data, descripcion=form.descripcion.data)

        try:
            # add estado to the database
            db.session.add(parentezco)
            db.session.commit()
            flash('Has agregado un parentezco a la base de datos.')
        except:
            # in case role name already exists
            flash('Error: el parentezco ya existe.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_parentezcos'))

    # load role template
    return render_template('extras/parentezcos/parentezco.html', add_parentezco=add_parentezco, form=form, title='Agregar Parentezco')

@extras.route('/parentezcos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_parentezco(id):
    """
    Modificar un Parentezcos
    """
    check_admin()

    add_parentezco = False

    parentezco = Parentezco.query.get_or_404(id)
    form = FormParentezco(obj=parentezco)
    if form.validate_on_submit():
        parentezco.nombre = form.nombre.data
        parentezco.descripcion = form.descripcion.data
        db.session.add(parentezco)
        db.session.commit()
        flash('Has modificado el parentezco en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_parentezcos'))

    form.descripcion.data = parentezco.descripcion
    form.nombre.data = parentezco.nombre
    return render_template('admin/parentezcos/parentezco.html', add_parentezco=add_parentezco, form=form, title="Modificar Parentezco")

@extras.route('/parentezcos/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_parentezco(id):
    """
    Borrar un parentezco de la base de datos
    """
    check_admin()

    parentezco = Parentezco.query.get_or_404(id)
    db.session.delete(parentezco)
    db.session.commit()
    flash('Has borrado el parentezco de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_parentezcos'))

    return render_template(title="Borrar Parentezco")


"""
AQUI FINALIZA CODIGO PARENTEZCOS
-------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------
AQUI COMIENZA CODIGO FAMILIAS

EL CONCEPTO DE FAMILIA ES EL DE GRUPO FAMILIAR. DEFINICION DE LOS QUE VIVEN JUNTOS BAJO LA MISMA CASA Y TIENEN RELACION FILIAL.
"""

@extras.route('/familias')
@login_required
def listar_familias():
    check_admin()

    """
    Listar todos las familias
    """
    familias = Familia.query.all()
    return render_template('extras/familias/familias.html', familias=familias, title='Familias')

@extras.route('/familias/add', methods=['GET', 'POST'])
@login_required
def add_familia():
    """
    Agregar un familias a la base de datos
    """
    check_admin()

    add_familia = True

    form = FormFamilia()
    if form.validate_on_submit():
        familia = Familia(apellidos_familia=form.apellidos_familia.data, comentarios=form.comentarios.data)

        try:
            # add estado to the database
            db.session.add(familia)
            db.session.commit()
            flash('Has agregado una familia a la base de datos.')
        except:
            # in case role name already exists
            flash('Error: la familia ya existe.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_familias'))

    # load role template
    return render_template('extras/familias/familia.html', add_familia=add_familia, form=form, title='Agregar Familia')

@extras.route('/familias/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_familia(id):
    """
    Modificar una Familia
    """
    check_admin()

    add_familia = False

    familia = Familia.query.get_or_404(id)
    form = FormFamilia(obj=familia)
    if form.validate_on_submit():
        familia.apellidos_familia = form.apellidos_familia.data
        familia.comentarios = form.comentarios.data
        db.session.add(familia)
        db.session.commit()
        flash('Has modificado la familia en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.familias'))

    form.comentarios.data = familia.comentarios
    form.apellidos_familia.data = familia.apellidos_familia
    return render_template('admin/familias/familia.html', add_familia=add_familia, form=form, title="Modificar Familia")

@extras.route('/familias/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_familia(id):
    """
    Borrar una familia de la base de datos
    """
    check_admin()

    familia = Familia.query.get_or_404(id)
    db.session.delete(familia)
    db.session.commit()
    flash('Has borrado la familia de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_familias'))

    return render_template(title="Borrar Familia")

"""
AQUI FINALIZA CODIGO FAMILIAS
-------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------
AQUI COMIENZA CODIGO TIPOS DE MIEMBROS
SER REFIERE A ESTADOS DE LOS MIEMBROS EN LA IGLESIA: MIEMBROS, ASISTENTE REGULAR, NO ASISTE, ETC
"""

@extras.route('/tiposmiembros')
@login_required
def listar_tiposmiembros():
    check_admin()

    """
    Listar todos los tipos de miembros
    """
    tiposmiembros = TipoMiembro.query.all()
    return render_template('extras/tiposmiembros/tiposmiembros.html', tiposmiembros=tiposmiembros, title='Tipos de Miembros')

@extras.route('/tiposmiembros/add', methods=['GET', 'POST'])
@login_required
def add_tipomiembro():
    """
    Agregar un tipo de miembro a la base de datos
    """
    check_admin()

    add_tipomiembro = True

    form = FormTipoMiembro()
    if form.validate_on_submit():
        tipomiembro = TipoMiembro(nombre=form.nombre.data, descripcion=form.descripcion.data)

        try:
            # add estado to the database
            db.session.add(tipomiembro)
            db.session.commit()
            flash('Has agregado un tipo de miembro a la base de datos.')
        except:
            # in case role name already exists
            flash('Error: el tipo de miembto ya existe.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_tiposmiembros'))

    # load role template
    return render_template('extras/tiposmiembros/tipomiembro.html', add_tipomiembro=add_tipomiembro, form=form, title='Agregar un Tipo de Miembro')

@extras.route('/tiposmiembros/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tipomiembro(id):
    """
    Modificar un Tipo de Miembro
    """
    check_admin()

    add_tipomiembro = False

    tipomiembro = TipoMiembro.query.get_or_404(id)
    form = FormTipoMiembro(obj=tipomiembro)
    if form.validate_on_submit():
        tipomiembro.nombre = form.nombre.data
        tipomiembro.descripcion = form.descripcion.data
        db.session.add(tipomiembro)
        db.session.commit()
        flash('Has modificado el tipo de miembro en la base de datos.')

        # redirect to the roles page
        return redirect(url_for('extras.listar_tiposmiembros'))

    form.descripcion.data = tipomiembro.descripcion
    form.nombre.data = tipomiembro.nombre
    return render_template('admin/tiposmiembros/tipomiembro.html', add_tipomiembro=add_tipomiembro, form=form, title="Modificar Tipo de Miembro")

@extras.route('/tiposmiembros/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_tipomiembro(id):
    """
    Borrar un tipo de miembro de la base de datos
    """
    check_admin()

    tipomiembro = TipoMiembro.query.get_or_404(id)
    db.session.delete(tipomiembro)
    db.session.commit()
    flash('Has borrado un tipo de miembro de la base de datos.')

    # redirect to the roles page
    return redirect(url_for('extras.listar_tiposmiembros'))

    return render_template(title="Borrar Tipo de Miembro")