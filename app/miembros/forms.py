# app/ggcc/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms import DateField, BooleanField
from wtforms.validators import InputRequired, Length, Optional, DataRequired


class MiembroForm(FlaskForm):
    """
    Formulario para familias
    """

    id = HiddenField("id")
    id_direccion = HiddenField("idDir")

    # Modelo Familia
    nombres = StringField(u'Nombre/s',
                          validators=[DataRequired(),
                                      Length(min=1, max=100)])
    apellidos = StringField(u'Apellido/s',
                            validators=[DataRequired(),
                                        Length(min=1, max=100)])
    dni_doc = StringField(u'DNI/Doc.',
                          validators=[Length(min=0, max=20)])
    email = StringField(u'Email (si son niños poner el email\
                          de alguno de los padres/tutores)',
                        validators=[DataRequired(),
                                    Length(min=0, max=60)])
    telefono_movil = StringField(u'Móvil',
                                 validators=[Length(min=0, max=15)])
    telefono_fijo = StringField(u'Fijo',
                                validators=[Length(min=0, max=15)])
    fecha_nac = DateField(u'Fecha de Nacimiento', validators=[DataRequired()])
    fecha_inicio_icecha = DateField(u'Fecha de Inicio en Iglesia',
                                    validators=[Optional()])
    fecha_miembro = DateField(u'Fecha de Membresía', validators=[Optional()])
    fecha_bautismo = DateField(u'Fecha de Bautismo', validators=[Optional()])
    lugar_bautismo = StringField(u'Lugar de Bautismo',
                                 validators=[Length(min=0, max=15)])
    hoja_firmada = BooleanField(u'¿Tiene firmada la hoja de membresía?')
    nro_hoja = StringField(u'# de Hoja de Membresía (formato AAAA-NRO)')
    observaciones = StringField(u'Observaciones',
                                validators=[Length(min=0, max=15)])
    EstadoCivil = SelectField(u'Estado Civil', coerce=int)
    TipoMiembro = SelectField(u'Tipo de Miembro', coerce=int)
    RolFamiliar = SelectField(u'Rol Familiar', coerce=int)

    Familia = SelectField(u'Familia', coerce=int)
    GrupoCasero = SelectField(u'Grupo Casero', coerce=int)

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
