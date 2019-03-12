# app/extras/forms.oy
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EstadoCivilForm(FlaskForm):
    """
    Form para agregar o modificar EstadoCivil
    """
    nombre_ec = StringField(u'Nombre', validators=[DataRequired()])
    descripcion_ec = StringField(u'Descripción')
    submit = SubmitField(u'Aceptar')