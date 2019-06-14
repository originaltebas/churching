# app/asistencias/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms import DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class ReunionForm(FlaskForm):
    """
    Formulario para reunion
    """

    id = HiddenField(u'id')
    nombre_reunion = StringField(u'Nombre de la reunión')

    # Modelo Familia
    fecha_reunion = DateField(u'Fecha de la reunión',
                              validators=[DataRequired()])

    comentarios_reunion = StringField(u'Comentarios',
                                      widget=TextArea())

    submit = SubmitField(u'Aceptar')


class AsistenciaForm(FlaskForm):
    """
    Consulta de asistencias
    """

    id_miembros = HiddenField(u'idMiembros')
    id_reunion = HiddenField(u'idReunion')
    submit = SubmitField(u'Buscar')


class ConsultaAsistenciasForm(FlaskForm):
    """
    Consulta de asistencias
    """

    id_miembro = HiddenField(u'idMiembro')
    nomyape = StringField(u'Nombres y Apellidos de la Persona:')
    submit = SubmitField(u'Buscar')
