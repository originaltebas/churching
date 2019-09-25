"""empty message

Revision ID: 22450008e9ee
Revises: 7263a24da5fd
Create Date: 2019-06-11 12:13:41.161340

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '22450008e9ee'
down_revision = '7263a24da5fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('miembros', 'hoja_firmada',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.add_column('reuniones', sa.Column('comentarios_reunion', sa.String(length=100), nullable=True))
    op.add_column('reuniones', sa.Column('fecha_reunion', sa.Date(), nullable=False))
    op.add_column('reuniones', sa.Column('nombre_reunion', sa.String(length=20), nullable=False))
    op.drop_column('reuniones', 'comentarios_culto')
    op.drop_column('reuniones', 'fecha_culto')
    op.drop_column('reuniones', 'nombre_culto')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reuniones', sa.Column('nombre_culto', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('reuniones', sa.Column('fecha_culto', sa.DATE(), nullable=False))
    op.add_column('reuniones', sa.Column('comentarios_culto', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('reuniones', 'nombre_reunion')
    op.drop_column('reuniones', 'fecha_reunion')
    op.drop_column('reuniones', 'comentarios_reunion')
    op.alter_column('miembros', 'hoja_firmada',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    # ### end Alembic commands ###