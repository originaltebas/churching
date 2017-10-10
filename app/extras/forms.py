# app/extras/forms.py
#coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FormGrupoCasero(FlaskForm):
    """
    Formulario para agregar o editar un grupo casero
    """
    nombre_grupo = StringField(u'Nombre del Grupo', validators=[DataRequired()])
    descripcion_grupo = StringField(u'Descripción del Grupo', validators=[DataRequired()])
    direccion_grupo = StringField(u'Dirección del Grupo', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')
