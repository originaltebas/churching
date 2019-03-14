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


class TipoMiembroForm(FlaskForm):
    """
    Form para agregar o modificar Tipo de Miembro
    """
    nombre_tm = StringField(u'Nombre', validators=[DataRequired()])
    descripcion_tm = StringField(u'Descripción')
    submit = SubmitField(u'Aceptar')


class RolFamiliarForm(FlaskForm):
    """
    Form para agregar o modificar Tipo de Miembro
    """
    nombre_rf = StringField(u'Nombre', validators=[DataRequired()])
    descripcion_rf = StringField(u'Descripción')
    submit = SubmitField(u'Aceptar')