# app/ggcc/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length


class GGCCForm(FlaskForm):
    """
    Formulario para gruposcaseros
    """
    id = HiddenField("id")
    id_direccion = HiddenField("idDir")
    # Modelo GGCC
    nombre_grupo = StringField(u'Nombre del Grupo Casero',
                               validators=[InputRequired(),
                                           Length(min=1, max=60)])
    descripcion_grupo = StringField(u'Descripción del Grupo Casero',
                                    validators=[InputRequired(),
                                                Length(min=0, max=200)])
    submit = SubmitField(u'Aceptar')


class DireccionModalForm(FlaskForm):
    # Modelo Direccion
    tipo_via = StringField(u'Tipo de vía',
                           validators=[InputRequired(),
                                       Length(min=1, max=20)])

    nombre_via = StringField(u'Nombre de la vía',
                             validators=[InputRequired(),
                                         Length(min=1, max=100)])

    nro_via = StringField(u'Nro',
                          validators=[InputRequired(),
                                      Length(min=1, max=10)])

    portalescalotros_via = StringField(u'Portal/Esc/Otro')
    piso_nroletra_via = StringField(u'Nro/Letra del Piso')
    cp_via = StringField(u'CP',
                         validators=[InputRequired(),
                                     Length(min=1, max=10)])

    ciudad_via = StringField(u'Ciudad',
                             validators=[InputRequired(),
                                         Length(min=1, max=50)])

    provincia_via = StringField(u'Provincia',
                                validators=[InputRequired(),
                                            Length(min=1, max=50)])

    pais_via = StringField(u'País',
                           validators=[InputRequired(),
                                       Length(min=1, max=50)])

    submit = SubmitField(u'Crear Dirección')


class AsignacionMiembrosForm(FlaskForm):
    """
    Formulario para la asignacion de personas a las
    ggcc. Las personas tienen que ser miembros creados
    """
    ids_in = HiddenField('Ids IN')
    ids_out = HiddenField('Ids OUT')
    submit = SubmitField(u'Aceptar')
