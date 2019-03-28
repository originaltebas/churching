# app/auth/views.py
# coding: utf-8

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app import db
from app.models import Usuario


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Agrega el usuario a la base de datos
    -- Actualmente todas las funciones están hechas para administradores
    -- y solo se puede poner la marca de admin por base de datos
    -- está creado en el modelo el flag de editor para dar permiso a
    -- todo excepto a datos de seguimiento de gente por privacidad
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                          username=form.username.data,
                          first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          password=form.password.data)

        try:
            # agregar usuario a la BD
            db.session.add(usuario)
            db.session.commit()
            flash(u'Se ha creado correctamente el usuario.', 'success')
        except Exception as e:
            # error
            flash('Error:', e, 'danger')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gestiona las solicitudes de login
    Loguea un usuario
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario is not None and usuario.verify_password(form.password.data):
            login_user(usuario)
            # redirect to the appropriate dashboard page
            if usuario.is_admin:
                return redirect(url_for('home.dashboard_admin'))
            elif usuario.is_editor:
                return redirect(url_for('home.dashboard_editor'))
            else:
                return redirect(url_for('home.noaccess'))

        # when login details are incorrect
        else:
            flash(u'Email o contraseña invalidos.', 'danger')

    # load login template
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Gestiona los logouts
    """
    logout_user()
    flash(u'Has salido correctamente.', 'success')

    # redirect to the login page
    return redirect(url_for('auth.login'))
