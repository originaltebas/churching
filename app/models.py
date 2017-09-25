# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


miembros_roles = db.Table('miembros_roles',
    db.Column('id_miembro', db.Integer, db.ForeignKey('miembros.id')),
    db.Column('id_rol', db.Integer, db.ForeignKey('roles.id'))
)


class Miembro(db.Model):
    """
    Crear una tabla de miembros
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'miembros'

    id = db.Column(db.Integer, primary_key=True)
    id_familia = db.Column(db.Integer, db.ForeignKey('familias.id'))
    nombres = db.Column(db.String(100), index=True)
    apellidos = db.Column(db.String(100), index=True)
    id_parentezco = db.Column(db.String(100), db.ForeignKey('parentezcos.id'))
    email = db.Column(db.String(60), index=True, unique=True)
    id_estado_civil = db.Column(db.String(100), db.ForeignKey('estados.id'))
    direccion = db.Column(db.String(200))
    telefono_1 = db.Column(db.String(15))
    telefono_2 = db.Column(db.String(15))
    fecha_nac = db.Column(db.DateTime)
    fecha_miembro = db.Column(db.DateTime)
    fecha_bautismo = db.Column(db.DateTime)
    asiste_regular = db.Column(db.Boolean, default=False)
    id_grupo_casero = db.Column(db.String(100), db.ForeignKey('gruposcaseros.id'))
    observaciones = db.Column(db.String(500))
    
    def __repr__(self):
        return '<>Miembro: {}>'.format(self.nombres, ' ', self.apellidos)


class GrupoCasero(db.Model):
    """
    Crear una tabla de grupos caseros
    """

    __tablename__ = 'gruposcaseros'

    id = db.Column(db.Integer, primary_key=True)
    nombre_grupo = db.Column(db.String(60), unique=True)
    descripcion_grupo = db.Column(db.String(200))
    miembros = db.relationship('Miembro', backref='grupocasero',
                                lazy='dynamic')

    def __repr__(self):
        return '<Grupo Casero: {}>'.format(self.nombre_grupo)


class Rol(db.Model):
    """
    Crea una tabla de funciones y roles
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True)
    descripcion = db.Column(db.String(200))
    miembros = db.relationship('Miembro', secondary=miembros_roles, 
                                backref=db.backref('roles', lazy='dynamic'))
                            

    def __repr__(self):
        return '<Rol: {}>'.format(self.nombre)


class Usuario(UserMixin, db.Model):
    """
    Crear una tabla de usuarios de la aplicacion
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'usuarios'

    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
