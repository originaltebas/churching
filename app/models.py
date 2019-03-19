# -*- coding: UTF-8 -*-
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# Tablas intemedias para Relaciones N:N
# Miembros con Roles (1 miembro->varios roles, 1 rol -> varios miembros)
relacion_miembros_roles = db.Table('relacion_miembros_roles',
                                   db.Column('id_miembro',
                                             db.Integer,
                                             db.ForeignKey('miembros.id'),
                                             primary_key=True),
                                   db.Column('id_rol',
                                             db.Integer,
                                             db.ForeignKey('roles.id'),
                                             primary_key=True)
                                   )


class Miembro(db.Model):
    "TABLA BASE DEL MODELO - MIEMBROS DE LA IGLESIA"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'miembros'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombres = db.Column(db.String(100), index=True, nullable=False)
    apellidos = db.Column(db.String(100), index=True, nullable=False)
    dni_doc = db.Column(db.String(20))
    email = db.Column(db.String(60), index=True, unique=True)
    telefono_movil = db.Column(db.String(15))
    telefono_fijo = db.Column(db.String(15))
    fecha_nac = db.Column(db.DateTime, nullable=False)
    fecha_inicio_icecha = db.Column(db.DateTime)
    fecha_miembro = db.Column(db.DateTime)
    fecha_bautismo = db.Column(db.DateTime)
    lugar_bautismo = db.Column(db.String(50))
    observaciones = db.Column(db.String(500))

    # RELACIONES N:1 [FOREINGKEYS]
    # Direccion (1 direccion para N miembros [la familia])
    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    # Estado Civil (1 estado civil para muchos miembros)
    id_estadoscivil = db.Column(db.Integer, db.ForeignKey('estadosciviles.id'),
                                nullable=False)
    # Tipo de Miembro (1 tipo de miembro para muchos miembros)
    id_tipomiembro = db.Column(db.Integer, db.ForeignKey('tiposmiembros.id'),
                               nullable=False)
    # Grupo Casero (1 grupo casero, muchos miembros)
    id_grupocasero = db.Column(db.Integer, db.ForeignKey('gruposcaseros.id'))
    # Rol Familiar (1 rol, muchos miembros)
    id_rolfamiliar = db.Column(db.Integer, db.ForeignKey('rolesfamiliares.id'),
                               nullable=False)
    # Familia (1 familia, muchos miembros)
    id_familia = db.Column(db.Integer, db.ForeignKey('familias.id'),
                           nullable=False)

    # RELACIONES N:1 [BACKREF]
    # Asistencia (1 miembro, muchas asistencias)
    asistencias = db.relationship('Asistencia', backref='miembro', lazy=True)
    # Seguimiento (1 miembro, muchos Seguimientos)
    seguimientos = db.relationship('Seguimiento', backref='miembro', lazy=True)

    # RELACIONES N:N [TABLA INTERMEDIA]
    # Roles (1 miembros puede tener varios roles: ej: anciano, tesorero,
    # ministerio alabanza, etc)
    roles = db.relationship("Rol", secondary=relacion_miembros_roles,
                            back_populates="miembros")

    def __repr__(self):
        return '<Miembro: %s ' ' %s>' % (self.nombres, self.apellidos)


class Direccion(db.Model):
    "TABLA GENERAL DE DIRECCIONES DE MIEMBROS / FAMILIAS / GRUPOS CASEROS"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'direcciones'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    tipo_via = db.Column(db.String(20), nullable=False)
    nombre_via = db.Column(db.String(100), nullable=False)
    nro_via = db.Column(db.String(10), nullable=False)
    portalescalotros_via = db.Column(db.String(20))
    cp_via = db.Column(db.String(10), nullable=False)
    ciudad_via = db.Column(db.String(20), nullable=False)
    provincia_via = db.Column(db.String(20), nullable=False)
    pais_via = db.Column(db.String(20), nullable=False)

    # RELACIONES 1:N [BACKREF]
    miembros = db.relationship('Miembro', backref='direccion', lazy=True)

    gruposcaseros = db.relationship('GrupoCasero', backref='direccion',
                                    lazy=True)

    familias = db.relationship('Familia', backref='direccion', lazy=True)

    def __repr__(self):
        return '<Direccion: %s ' ' %s ' ' %s>' % (self.tipo_via,
                                                  self.nombre_via,
                                                  self.nro_via)


class EstadoCivil(db.Model):
    "TABLA TIPO DE ESTADO CIVIL"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'estadosciviles'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombre_estado = db.Column(db.String(60), nullable=False)
    descripcion_estado = db.Column(db.String(200))

    # RELACIONES 1:N [BACKREF]
    miembros = db.relationship('Miembro', backref='estadocivil', lazy=True)

    def __repr__(self):
        return '<Estado Civil: {}>'.format(self.nombre_estado)


class TipoMiembro(db.Model):
    "TABLA TIPO DE MIEMBRO. EJ. ASISTENTE REGULAR, MIEMBRO, VISITANTE, ETC."

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'tiposmiembros'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombre_tipomiembro = db.Column(db.String(60), nullable=False)
    descripcion_tipomiembro = db.Column(db.String(200))

    # RELACIONES 1:N [BACKREF]
    miembros = db.relationship('Miembro', backref='tipomiembro', lazy=True)

    def __repr__(self):
        return '<Tipo de Miembro: {}>'.format(self.nombre)


class GrupoCasero(db.Model):
    "TABLA DE GRUPOS CASEROS / GRUPOS CELULA / GRUPOS PEQUEÑOS / SMALL GROUPS"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'gruposcaseros'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombre_grupo = db.Column(db.String(60), nullable=False)
    descripcion_grupo = db.Column(db.String(200))

    # RELACIONES N:1 [FOREINGKEYS] (1 direccion, varios grupos)
    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    # RELACIONES 1:N [BACKREF] (1 grupo muchos miembros)
    miembros = db.relationship('Miembro', backref='grupocasero', lazy=True)

    def __repr__(self):
        return '<Grupo Casero: {}>'.format(self.nombre_grupo)


class RolFamiliar(db.Model):
    "TABLA DE TIPOS DE ROLES FAM (padre, madre, hijo, abuelo, amigo)"
    "En lugar de pasar por familia directamente relaciono con miembros"
    "ya que un miembro solo podrá tener 1 rol familiar"
    "En el caso que vivan Padres, hijos y nietos se relaciona así"
    "Abuelos --> Padres --> Hijos --> Amigos --> Otros"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'rolesfamiliares'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombre_rolfam = db.Column(db.String(60), nullable=False)
    descripcion_rolfam = db.Column(db.String(200))

    # RELACIONES 1:N [BACKREF] (1 rolfamiliar muchos miembros)
    miembros = db.relationship('Miembro', backref='rolfamiliar', lazy=True)

    def __repr__(self):
        return '<Rol Familiar: {}>'.format(self.nombre_rolfam)


class Familia(db.Model):
    "TABLA DE FAMILIAS"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'familias'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    apellidos_familia = db.Column(db.String(60), nullable=False)
    descripcion_familia = db.Column(db.String(200))
    telefono_familia = db.Column(db.String(15))

    # RELACIONES 1:n [FOREINGKEYS]
    # Direccion
    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    # Tipo Familia
    id_tipofamilia = db.Column(db.Integer, db.ForeignKey('tiposfamilias.id'),
                               nullable=False)

    # RELACIONES 1:N [BACKREF] (1 familia muchos miembros)
    miembros = db.relationship('Miembro', backref='familia', lazy=True)

    def __repr__(self):
        return '<Familia: {}>'.format(self.apellidos_familia)


class TipoFamilia(db.Model):
    "TIPO DE FAMILIA.EJ: ESTANDAR, MONOPARENTAL,"
    "MULTIFAMILIAR, SOLTERO/SOLO/VIUDO, NO SABE"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'tiposfamilias'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    tipo_familia = db.Column(db.String(60), nullable=False)
    descripcion_tipo_familia = db.Column(db.String(200))

    # RELACIONES 1:N [BACKREF] (1 familia muchos miembros)
    familias = db.relationship('Familia', backref='tipofamilia', lazy=True)

    def __repr__(self):
        return '<Tipo Familia: {}>'.format(self.tipo_familia)


class Asistencia(db.Model):
    "TABLA DE ASISTENCIAS - PARA SABER QUIEN FALTA Y PODER CONTACTARLO"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'asistencias'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    fecha_culto = db.Column(db.DateTime, nullable=False)
    asistio = db.Column(db.Boolean, nullable=False)

    # 1 miembro muchas asistencias
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'),
                           nullable=False)

    def __repr__(self):
        return '<Asistencia: %s>' '%s' % (self.fecha_culto,
                                          self.asistio)


class Seguimiento(db.Model):
    "TABLA DE SEGUIMIENTO - COMENTARIOS SOBRE LLAMADAS "
    "Y COSAS QUE PUEDE SER BUENO SABER"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'seguimientos'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    fecha_seg = db.Column(db.DateTime, nullable=False)
    comentarios_seg = db.Column(db.Boolean, nullable=False)

    # 1 miembro muchos seguimientos
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'),
                           nullable=False)

    def __repr__(self):
        return '<Seguimiento: %s>' '%s' % (self.fecha_seg,
                                           self.comentarios_seg)


class Rol(db.Model):
    """
    TABLA DE ROL DENTRO DE LA IGLESIA
    EJ. PASTOR, ANCIANO; DIACONO, LIDER GRUPO CASERO
    PARTICIPA EN: OBRA SOCIAL, MUSICA; SONIDO; UJIERES
    CREO QUE PUEDO HACER ALGO TIPO: TAGS, es decir agrego por ejemplo
    ministerio de alabaza, pero tambien guitarrista ministerio de alabanza,
    sonidista, etc
    y los roles serían como las veces de etiquetas.
    """

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'roles'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombre_rol = db.Column(db.String(60), nullable=False)
    # tipo rol (ej. pastor) o tipo ministerio (ej. obra social),
    # o clase (ej. 3-5años)
    # si es rol es un cargo, si es un ministerio es que participa en...
    tipo_rol = db.Column(db.String(60), nullable=False)
    descripcion_rol = db.Column(db.String(200))

    # RELACIONES N:N [TABLA INTERMEDIA]
    # Miembro (1 miembros puede tener varios roles: ej: anciano, tesorero,
    # ministerio alabanza, etc)
    miembros = db.relationship("Miembro", secondary=relacion_miembros_roles,
                               back_populates="roles")

    def __repr__(self):
        return '<Rol: {}>'.format(self.nombre)


class Usuario(UserMixin, db.Model):
    "tabla de usuarios de la aplicacion -- no tiene relacion con el modelo"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'usuarios'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Para evitar que se acceda a la contraseña
        """
        raise AttributeError('La contraseña no es un atributo de lectura.')

    @password.setter
    def password(self, password):
        """
        Establecer la contraseña a hash
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Controlar si la contraseña coincide
        """
        return check_password_hash(self.password_hash, password)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
