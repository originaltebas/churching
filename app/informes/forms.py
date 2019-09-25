# app/informes/forms.py
# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class FiltroInformePersonas(FlaskForm):
    EstadoCivil = SelectField(u'Estado Civil', coerce=int)
    TipoMiembro = SelectField(u'Tipo de Miembro', coerce=int)
    RolFamiliar = SelectField(u'Rol Familiar', coerce=int)

    TipoFamilia = SelectField(u'Tipo Familia', coerce=int)
    GrupoCasero = SelectField(u'Grupo Casero', coerce=int)

    submit = SubmitField(u'Aceptar')


class FiltroInformeFamilias(FlaskForm):
    TipoFamilia = SelectField(u'Tipo Familia', coerce=int)
    GrupoCasero = SelectField(u'Grupo Casero', coerce=int)

    submit = SubmitField(u'Aceptar')