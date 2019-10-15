# app/home/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class BusquedaForm(FlaskForm):
    """
    Formulario de busqueda rapida
    """

    cadena = StringField(u'cadena de busqueda',
                         validators=[InputRequired(),
                                     Length(min=3, max=100)])
    submit = SubmitField(u'Aceptar')
