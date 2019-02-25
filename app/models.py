# -*- coding: UTF-8 -*-
# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


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
    fecha_nac = db.Column(db.DateTime, nullable=False)
    fecha_inicio_icecha = db.Column(db.DateTime)
    fecha_miembro = db.Column(db.DateTime)
    fecha_bautismo = db.Column(db.DateTime)
    lugar_bautismo = db.Column(db.String(50))
    observaciones = db.Column(db.String(500))

    # RELACIONES 1:1 [FOREINGKEYS]
    # Direccion
    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    direccion = db.relationship("Direccion", back_populates="miembro")

    # Estado Civil
    id_estadoscivil = db.Column(db.Integer, db.ForeignKey('estadosciviles.id'),
                                nullable=False)
    estadocivil = db.relationship("EstadoCivil", back_populates="miembro")

    # Tipo de Miembro
    id_tipomiembro = db.Column(db.Integer, db.ForeignKey('tiposmiembros.id'),
                               nullable=False)
    tipomiembro = db.relationship("TipoMiembro", back_populates="miembro")

    # Grupo Casero
    id_grupocasero = db.Column(db.Integer, db.ForeignKey('gruposcaseros.id'),
                               nullable=False)
    grupocasero = db.relationship("GrupoCasero", back_populates="miembro")

    # Grupo Casero
    id_rolfamiliar = db.Column(db.Integer, db.ForeignKey('rolesfamiliares.id'),
                               nullable=False)
    rolfamiliar = db.relationship("RolFamiliar", back_populates="miembro")

    # RELACIONES 0:N // 1:N // N:N
    # FAMILIAS  1:N
    familias = db.relationship("Familia", back_populates="miembro")

    # TELEFONOS 1:N
    telefonos = db.relationship("Telefono", back_populates="miembro")

    # ROLES 1:N
    roles = db.relationship("Rol", back_populates="miembro")

    # ASISTENCIAS 1:N
    asistencias = db.relationship("Asistencia", back_populates="miembro")

    # SEGUIMIENTOS 1:N
    seguimientos = db.relationship("Seguimiento", back_populates="miembro")

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

    # RELACIONES 1:1 [BACKPOPULATES]
    miembro = db.relationship('Miembro', uselist=False,
                              back_populates='direccion')
    familia = db.relationship('Familia', uselist=False,
                              back_populates='direccion')
    grupocasero = db.relationship('GrupoCasero', uselist=False,
                                  back_populates='direccion')

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

    # RELACIONES 1:1 [BACKPOPULATE]
    miembro = db.relationship('Miembro', uselist=False,
                              back_populates='estadocivil')

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

    # RELACIONES 1:1 [BACKPOPULATE]
    miembro = db.relationship('Miembro', uselist=False,
                              back_populates='tipomiembro')

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

    # RELACIONES 1:1 [FOREINGKEYS]
    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    direccion = db.relationship("Direccion", back_populates="GrupoCasero")

    # RELACIONES 1:1 [BACKPOPULATE]
    miembro = db.relationship('Miembro', uselist=False,
                              back_populates='grupocasero')

    def __repr__(self):
        return '<Grupo Casero: {}>'.format(self.nombre_grupo)


class Familia(db.Model):
    "TABLA DE FAMILIAS"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'familias'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    apellidos_familia = db.Column(db.String(60), nullable=False)
    descripcion_familia = db.Column(db.String(200))

    # RELACIONES 1:1 [FOREINGKEYS]
    # Direccion
    id_direccion = db.Column(db.Integer, db.ForeignKey('direcciones.id'),
                             nullable=False)
    direccion = db.relationship("Direccion", back_populates="familia")

    # Tipo Familia
    id_tipofamilia = db.Column(db.Integer, db.ForeignKey('tiposfamilias.id'),
                               nullable=False)
    tipofamilia = db.relationship("TipoFamilia", back_populates="familia")

    # RELACIONES 0:N // 1:N // N:N
    # MIEMBROS  N:1
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'))
    miembro = db.relationship('Miembro', back_populates='familias')

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

    # RELACIONES 1:1 [BACKPOPULATE]
    familia = db.relationship('Familia', uselist=False,
                              back_populates='tipofamilia')

    def __repr__(self):
        return '<Tipo Familia: {}>'.format(self.tipo_familia)


class Telefono(db.Model):
    "TABLA DE TELEFONOS FIJOS Y MOVILES"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'telefonos'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    numero_tel = db.Column(db.String(20), nullable=False)
    tipo_tel = db.Column(db.String(20), nullable=False)  # movil,casa,trabajo

    # RELACIONES 0:N // 1:N // N:N
    # MIEMBROS  N:1
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'))
    miembro = db.relationship('Miembro', back_populates='telefonos')

    def __repr__(self):
        return '<Telefono: {}>'.format(self.numero)


class Rol(db.Model):
    "TABLA DE ROL DENTRO DE LA IGLESIA"
    "EJ. PASTOR, ANCIANO; DIACONO, LIDER GRUPO CASERO"
    "PARTICIPA EN: OBRA SOCIAL, MUSICA; SONIDO; UJIERES"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'roles'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    nombre_rol = db.Column(db.String(60), nullable=False)
    descripcion_rol = db.Column(db.String(200))

    # RELACIONES 0:N // 1:N // N:N
    # MIEMBROS  N:1
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'))
    miembro = db.relationship('Miembro', back_populates='roles')

    def __repr__(self):
        return '<Rol: {}>'.format(self.nombre)


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

    # RELACIONES 1:1 [BACKPOPULATE]
    # Miembro
    miembro = db.relationship('Miembro', uselist=False,
                              back_populates='rolfamiliar')

    def __repr__(self):
        return '<Rol Familiar: {}>'.format(self.nombre_rolfam)


class Asistencia(db.Model):
    "TABLA DE ASISTENCIAS - PARA SABER QUIEN FALTA Y PODER CONTACTARLO"

    # NOMBRE DE TABLA EN MYSQL
    __tablename__ = 'asistencias'

    # CLAVE PRIMARIA
    id = db.Column(db.Integer, primary_key=True)

    # CAMPOS DESCRIPTIVOS
    fecha_culto = db.Column(db.DateTime, nullable=False)
    asistio = db.Column(db.Boolean, nullable=False)

    # MIEMBROS  N:1
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'))
    miembro = db.relationship('Miembro', back_populates='asistencias')

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

    # MIEMBROS  N:1
    id_miembro = db.Column(db.Integer, db.ForeignKey('miembros.id'))
    miembro = db.relationship('Miembro', back_populates='seguimientos')

    def __repr__(self):
        return '<Seguimiento: %s>' '%s' % (self.fecha_seg,
                                           self.comentarios_seg)


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
