# app/familias/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import HiddenField, SelectField
from wtforms.validators import InputRequired, Length


class FamiliaForm(FlaskForm):
    """
    Formulario para familias
    """
    idDir = HiddenField("idDir")
    apellidos_familia = StringField(
                            u'Apellidos de la Familia',
                            validators=[InputRequired(),
                                        Length(min=1, max=60)])

    descripcion_familia = StringField(u'Descripción de la Familia')
    telefono_familia = StringField(u'Teléfono Familiar')
    TipoFamilia = SelectField(u'Tipo de Familia', coerce=int)
    submit = SubmitField(u'Crear Familia')


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


class AsignacionMiembrosFrom(FlaskForm):
    """
    Formulario para la asignacion de personas a las
    familias. Las personas tienen que ser miembros creados
    """
    ids_in = HiddenField('Ids IN')
    ids_out = HiddenField('Ids OUT')
    modifFlag = HiddenField("modifFlag", default=False)
    submit = SubmitField(u'Aceptar')
