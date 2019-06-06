# app/seguimientos/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms import DateField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class SeguimientoForm(FlaskForm):
    """
    Formulario para seguimientos
    """

    id_miembro = HiddenField("idDir")
    nomyape = StringField(u'Nombres y Apellidos Miembro:')

    # Modelo Familia
    fecha_seg = DateField(u'Fecha de la entrada',
                          validators=[DataRequired()])
    tipo_seg = SelectField(u'Tipo de Contacto',
                           coerce=int,
                           choices=[(0, 'LLAMADA'),
                                    (1, 'MENSAJE'),
                                    (2, 'PRESENCIAL'),
                                    (3, 'OTRO')])

    comentarios_seg = StringField(u'Comentarios',
                                  widget=TextArea())

    submit = SubmitField(u'Aceptar')
