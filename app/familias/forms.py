# app/familias/forms.py
# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class FamiliaForm(FlaskForm):
    """
    Formulario para familias
    """


    apellidos_familia = db.Column(db.String(60), nullable=False)
    descripcion_familia = db.Column(db.String(200))
    telefono_familia = db.Column(db.String(15))

    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    id_tipofamilia = db.Column(db.Integer, db.ForeignKey('tiposfamilias.id'),
                               nullable=False)



class AsignacionMiembrosFrom(FlaskForm):
    """
    Formulario para la asignacion de personas a las
    familias. Las personas tienen que ser miembros creados
    """
    ids_in = HiddenField('Ids IN')
    ids_out = HiddenField('Ids OUT')
    modifFlag = HiddenField("modifFlag", default=False)