"""empty message

Revision ID: d25f2c5ab0ae
Revises: ec1acb6af04d
Create Date: 2019-05-17 20:48:26.132411

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd25f2c5ab0ae'
down_revision = 'ec1acb6af04d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('asistencias', 'asistio',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    op.alter_column('miembros', 'hoja_firmada',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.drop_index('ix_miembros_email', table_name='miembros')
    op.create_index(op.f('ix_miembros_email'), 'miembros', ['email'], unique=False)
    op.alter_column('seguimientos', 'comentarios_seg',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seguimientos', 'comentarios_seg',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    op.drop_index(op.f('ix_miembros_email'), table_name='miembros')
    op.create_index('ix_miembros_email', 'miembros', ['email'], unique=True)
    op.alter_column('miembros', 'hoja_firmada',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('asistencias', 'asistio',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False)
    # ### end Alembic commands ###