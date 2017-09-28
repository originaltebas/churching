# app/auth/views.py
# coding: utf-8

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Usuario

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Gestiona los pedidos de registro
    Agrega el usuario a la base de datos
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        usuario = Usuario(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add usuario to the database
        db.session.add(usuario)
        db.session.commit()
        flash(u'Se ha creado correctamente el usuario.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title=u'Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    GEstiona las solicitudes de login
    Loguea un usuario
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario is not None and usuario.verify_password(form.password.data):
            login_user(usuario)

            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash(u'Email o contrase&ntilde;a invalidos.')

    # load login template
    return render_template('auth/login.html', form=form, title=u'Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Gestiona los logouts
    """
    logout_user()
    flash(u'Has salido correctamente.')

    # redirect to the login page
    return redirect(url_for('auth.login'))