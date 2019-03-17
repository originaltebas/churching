# app/extras/forms.oy
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RolForm(FlaskForm):
    """
    Form para agregar o modificar un rol, ministerio o clase
    """
    nombre_rol = StringField(u'Nombre', validators=[DataRequired()])
    descripcion_rol = StringField(u'Descripción')
    tipo_rol = StringField(u'Tipo')
    submit = SubmitField(u'Aceptar')
