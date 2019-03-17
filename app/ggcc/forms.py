# app/auth/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class GGCCForm(FlaskForm):
    """
    Formulario para gruposcaseros
    """
    NewDirFlag = HiddenField("NewDirFlag")
    idDir = HiddenField("idDir")
    # Modelo GGCC
    nombre_grupo = StringField(u'Nombre', validators=[DataRequired()])
    descripcion_grupo = StringField(u'Descripción')
    # Modelo Direccion
    tipo_via = StringField(u'Tipo vía', validators=[DataRequired()])
    nombre_via = StringField(u'Nombre vía', validators=[DataRequired()])
    nro_via = StringField(u'Nro', validators=[DataRequired()])
    portalescalotros_via = StringField(u'Portal/Esc/Otro')
    cp_via = StringField(u'CP', validators=[DataRequired()])
    ciudad_via = StringField(u'Ciudad', validators=[DataRequired()])
    provincia_via = StringField(u'Provincia', validators=[DataRequired()])
    pais_via = StringField(u'País', validators=[DataRequired()])
    submit = SubmitField(u'Aceptar')

