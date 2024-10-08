"""migracion sigma + english or spaniosh

Revision ID: dfd93eb84323
Revises: 6da40fab2d2a
Create Date: 2024-10-07 09:47:15.513945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfd93eb84323'
down_revision = '6da40fab2d2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contenido', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_creacion', sa.DateTime(), nullable=True))

    with op.batch_alter_table('curso', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_creacion', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('fecha_actualizacion', sa.DateTime(), nullable=True))

    with op.batch_alter_table('examen', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_creacion', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('examen', schema=None) as batch_op:
        batch_op.drop_column('fecha_creacion')

    with op.batch_alter_table('curso', schema=None) as batch_op:
        batch_op.drop_column('fecha_actualizacion')
        batch_op.drop_column('fecha_creacion')

    with op.batch_alter_table('contenido', schema=None) as batch_op:
        batch_op.drop_column('fecha_creacion')

    # ### end Alembic commands ###
