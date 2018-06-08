"""empty message

Revision ID: 396698708af2
Revises: 
Create Date: 2017-10-27 20:46:29.778299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396698708af2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('estadosciviles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=60), nullable=True),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('familias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('apellidos_familia', sa.String(length=60), nullable=True),
    sa.Column('comentarios', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gruposcaseros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_grupo', sa.String(length=60), nullable=False),
    sa.Column('descripcion_grupo', sa.String(length=200), nullable=False),
    sa.Column('direccion_grupo', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parentezcos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=60), nullable=True),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=60), nullable=True),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tiposmiembros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=60), nullable=True),
    sa.Column('descripcion', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_username'), 'usuarios', ['username'], unique=True)
    op.create_table('miembros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_familia', sa.Integer(), nullable=False),
    sa.Column('nombres', sa.String(length=100), nullable=True),
    sa.Column('apellidos', sa.String(length=100), nullable=True),
    sa.Column('id_parentezco', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('id_estado_civil', sa.Integer(), nullable=False),
    sa.Column('direccion', sa.String(length=200), nullable=True),
    sa.Column('telefono_1', sa.String(length=15), nullable=True),
    sa.Column('telefono_2', sa.String(length=15), nullable=True),
    sa.Column('fecha_nac', sa.DateTime(), nullable=True),
    sa.Column('fecha_miembro', sa.DateTime(), nullable=True),
    sa.Column('fecha_bautismo', sa.DateTime(), nullable=True),
    sa.Column('id_tipo_miembro', sa.Integer(), nullable=False),
    sa.Column('asiste_regular', sa.Boolean(), nullable=True),
    sa.Column('id_grupo_casero', sa.Integer(), nullable=False),
    sa.Column('observaciones', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['id_estado_civil'], ['estadosciviles.id'], ),
    sa.ForeignKeyConstraint(['id_familia'], ['familias.id'], ),
    sa.ForeignKeyConstraint(['id_grupo_casero'], ['gruposcaseros.id'], ),
    sa.ForeignKeyConstraint(['id_parentezco'], ['parentezcos.id'], ),
    sa.ForeignKeyConstraint(['id_tipo_miembro'], ['tiposmiembros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_miembros_apellidos'), 'miembros', ['apellidos'], unique=False)
    op.create_index(op.f('ix_miembros_email'), 'miembros', ['email'], unique=True)
    op.create_index(op.f('ix_miembros_nombres'), 'miembros', ['nombres'], unique=False)
    op.create_table('miembros_roles',
    sa.Column('id_miembro', sa.Integer(), nullable=False),
    sa.Column('id_rol', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_miembro'], ['miembros.id'], ),
    sa.ForeignKeyConstraint(['id_rol'], ['roles.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('miembros_roles')
    op.drop_index(op.f('ix_miembros_nombres'), table_name='miembros')
    op.drop_index(op.f('ix_miembros_email'), table_name='miembros')
    op.drop_index(op.f('ix_miembros_apellidos'), table_name='miembros')
    op.drop_table('miembros')
    op.drop_index(op.f('ix_usuarios_username'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
    op.drop_table('tiposmiembros')
    op.drop_table('roles')
    op.drop_table('parentezcos')
    op.drop_table('gruposcaseros')
    op.drop_table('familias')
    op.drop_table('estadosciviles')
    # ### end Alembic commands ###