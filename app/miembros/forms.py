# app/ggcc/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms import DateField
from wtforms.validators import InputRequired, Length, Optional


class MiembroForm(FlaskForm):
    """
    Formulario para familias
    """

    id = HiddenField("id")
    id_direccion = HiddenField("idDir")

    # Modelo Familia
    nombres = StringField(u'Nombres',
                          validators=[InputRequired(),
                                      Length(min=1, max=100)])
    apellidos = StringField(u'Nombres',
                            validators=[InputRequired(),
                                        Length(min=1, max=100)])
    dni_doc = StringField(u'DNI/Doc.',
                          validators=[InputRequired(),
                                      Length(min=0, max=20)])
    email = StringField(u'Email',
                        validators=[InputRequired(),
                                    Length(min=0, max=60)])
    telefono_movil = StringField(u'Móvil',
                                 validators=[InputRequired(),
                                             Length(min=0, max=15)])
    telefono_fijo = StringField(u'Fijo',
                                validators=[InputRequired(),
                                            Length(min=0, max=15)])
    fecha_nac = DateField(u'Fecha de Nacimiento', validators=[InputRequired()]
    fecha_inicio_icecha = DateField(u'Fecha de Inicio en Iglesia',
                                    validators=[Optional()]
    fecha_miembro = DateField(u'Fecha de Membresía', validators=[Optional()]
    fecha_bautismo = DateField(u'Fecha de Bautismo', validators=[Optional()]
    lugar_bautismo = StringField(u'Lugar de Bautismo',
                                 validators=[InputRequired(),
                                             Length(min=0, max=15)])
    observaciones = StringField(u'Observaciones',
                                validators=[InputRequired(),
                                            Length(min=0, max=15)])
    EstadoCivil = SelectField(u'Estado Civil', coerce=int)
    TipoMiembro = SelectField(u'Tipo de Miembro', coerce=int)
    RolFamiliar = SelectField(u'Rol Familiar', coerce=int)

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
