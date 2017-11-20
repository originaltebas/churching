# app/extras/forms.py
#coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField
from wtforms.validators import DataRequired, Email, Optional, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


from ..models import Familia, Parentezco, TipoMiembro
from ..models import Rol, GrupoCasero, EstadoCivil

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


class FormAsignacionMiembro(FlaskForm):
    """
    Form for admin to para asignar Familia, Parentezco, GrupoCasero, TipoMiembro y EstadoCivil
    """
    id = HiddenField('id') 

    familia = QuerySelectField(query_factory=lambda: Familia.query.all(),
                               get_label="apellidos_familia")

    parentezco = QuerySelectField(query_factory=lambda: Parentezco.query.all(),
                                  get_label="nombre")

    grupocasero = QuerySelectField(query_factory=lambda: GrupoCasero.query.all(),
                                   get_label="nombre_grupo")

    tipomiembro = QuerySelectField(query_factory=lambda: TipoMiembro.query.all(),
                                   get_label="nombre")

    estadocivil = QuerySelectField(query_factory=lambda: EstadoCivil.query.all(),
                                   get_label="nombre")

    rol = QuerySelectMultipleField(query_factory=lambda: Rol.query.all(),
                                   get_label="nombre")

    submit = SubmitField(u'Guardar')    


class FormMiembro(FlaskForm):
    """
    Formulario para agregar y editar tipos de miembros de la iglesia (miembro, asistente regular, no viene, etc)
    """
    
    
    nombres = StringField(u'Nombre(s)', validators = [DataRequired()])
    apellidos = StringField(u'Apellidos(s)', validators = [DataRequired()])
    email = StringField(u'Email', validators = [Optional(), Email()])
    direccion = StringField(u'Dirección', validators = [DataRequired()])
    telefono_1 = StringField(u'Teléfono Fijo', validators = [Optional(), NumberRange(min=80000000, max=99999999, message=u'Escriba un nro. de teléfono válido')])
    telefono_2 = StringField(u'Teléfono Móvil', validators = [Optional(), NumberRange(min=80000000, max=99999999, message=u'Escriba un nro. de teléfono válido')])
    
    fecha_nac = DateField(u'Fecha de Nacimiento', validators = [DataRequired()])
    fecha_bautismo = DateField(u'Fecha de Bautismo', validators = [Optional()])   
    fecha_miembro = DateField(u'Fecha Membresía', validators = [Optional()])

    observaciones = StringField(u'Observaciones', validators = [Optional()])

    familia = QuerySelectField(query_factory = lambda: Familia.query.all(),
                               get_label = "apellidos_familia")

    parentezco = QuerySelectField(query_factory = lambda: Parentezco.query.all(),
                                  get_label = "nombre")

    grupocasero = QuerySelectField(query_factory = lambda: GrupoCasero.query.all(),
                                   get_label = "nombre_grupo")

    tipomiembro = QuerySelectField(query_factory = lambda: TipoMiembro.query.all(),
                                   get_label = "nombre")

    estadocivil = QuerySelectField(query_factory = lambda: EstadoCivil.query.all(),
                                   get_label = "nombre")

    rol = QuerySelectMultipleField(query_factory = lambda: Rol.query.all(),
                                   get_label = "nombre")

    submit = SubmitField(u'Guardar')
'''
    id_familia = db.Column(db.Integer, db.ForeignKey('familias.id'),nullable=False)
    id_parentezco = db.Column(db.Integer, db.ForeignKey('parentezcos.id'),nullable=False)
    id_estado_civil = db.Column(db.Integer, db.ForeignKey('estadosciviles.id'),nullable=False)
    id_tipo_miembro = db.Column(db.Integer, db.ForeignKey('tiposmiembros.id'),nullable=False)
    id_grupo_casero = db.Column(db.Integer, db.ForeignKey('gruposcaseros.id'),nullable=False)
    ->Rol
'''

