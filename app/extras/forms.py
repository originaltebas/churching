# app/extras/forms.py
#coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class FormGrupoCasero(FlaskForm):
    """
    Formulario para agregar o editar un grupo casero
    """
    nombre_grupo = StringField(u'Nombre del Grupo', validators=[DataRequired()])
    descripcion_grupo = StringField(u'Día y Hora de reunión', validators=[DataRequired()])
    direccion_grupo = StringField(u'Dirección del Grupo', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')

class FormRol(FlaskForm):
    """
    Formulario para agregar y editar roles (pastor, anciano, diacono, líder GC, )
    """
    nombre = StringField(u'Nombre', validators=[DataRequired()])
    descripcion = StringField(u'Descripción', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')

class FormEstadoCivil(FlaskForm):
    """
    Formulario para agregar y editar estados civiles (casado, soltero, viudo, divorciado, etc)
    """
    nombre = StringField(u'Nombre', validators=[DataRequired()])
    descripcion = StringField(u'Descripción', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')


class FormParentezco(FlaskForm):
    """
    Formulario para agregar y editar parentezco (padre,madre,hijo,etc)
    """
    nombre = StringField(u'Nombre', validators=[DataRequired()])
    descripcion = StringField(u'Descripción', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')


class FormFamilia(FlaskForm):
    """
    Formulario para agregar y editar familia 
    (Datos generales de la familia. Por Ejemplo Perez Perez)
    """
    apellidos_familia = StringField(u'Apellidos de la Familia', validators=[DataRequired()])
    comentarios = StringField(u'Comentarios', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')

class FormTipoMiembro(FlaskForm):
    """
    Formulario para agregar y editar tipos de miembros de la iglesia (miembro, asistente regular, no viene, etc)
    """
    nombre = StringField(u'Nombre', validators=[DataRequired()])
    descripcion = StringField(u'Descripción', validators=[DataRequired()])
    submit = SubmitField(u'Guardar')
    