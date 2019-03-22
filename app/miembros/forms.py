# app/miembros/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import Usuario


class RegistrationForm(FlaskForm):
    """
    Formulario para registrar usuarios
    """
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    username = StringField(u'Nombre de usuario', validators=[DataRequired()])
    first_name = StringField(u'Nombres', validators=[DataRequired()])
    last_name = StringField(u'Apellidos', validators=[DataRequired()])
    password = PasswordField(u'Contraseña', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField(u'Confirma contraseña')
    submit = SubmitField(u'Crear usuario')

    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError(u'El email ya existe en la BD.')

    def validate_username(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError(u'El usuario ya existe en la BD.')


class LoginForm(FlaskForm):
    """
    Formulario para logarse en el sistema
    """
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    password = PasswordField(u'Contraseña', validators=[DataRequired()])
    submit = SubmitField(u'Aceptar')
