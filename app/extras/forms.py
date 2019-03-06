# -*- coding: UTF-8 -*-
# app/extras/forms.py

from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, HiddenField, DateField
# from wtforms.validators import DataRequired, Email, Optional, NumberRange
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from ..models import Miembro, TipoMiembro, EstadoCivil, Rol
from ..models import Familia, TipoFamilia, RolFamiliar
from ..models import Direccion, Telefono, Asistencia, Seguimiento
from ..models import GrupoCasero


class FormMiembro(FlaskForm):
    class Meta:
        model = Miembro
        include_foreign_keys = True


class FormTipoMiembro(FlaskForm):
    class Meta:
        model = TipoMiembro
        include_foreign_keys = True


class FormEstadoCivil(FlaskForm):
    class Meta:
        model = EstadoCivil
        include_foreign_keys = True


class FormRol(FlaskForm):
    class Meta:
        model = Rol
        include_foreign_keys = True


class FormFamilia(FlaskForm):
    class Meta:
        model = Familia
        include_foreign_keys = True


class FormTipoFamilia(FlaskForm):
    class Meta:
        model = TipoFamilia
        include_foreign_keys = True


class FormRolFamiliar(FlaskForm):
    class Meta:
        model = RolFamiliar
        include_foreign_keys = True


class FormDireccion(FlaskForm):
    class Meta:
        model = Direccion
        include_foreign_keys = True


class FormTelefono(FlaskForm):
    class Meta:
        model = Telefono
        include_foreign_keys = True


class FormAsistencia(FlaskForm):
    class Meta:
        model = Asistencia
        include_foreign_keys = True


class FormSeguimiento(FlaskForm):
    class Meta:
        model = Seguimiento
        include_foreign_keys = True


class FormGrupoCasero(FlaskForm):
    class Meta:
        model = GrupoCasero
        include_foreign_keys = True
