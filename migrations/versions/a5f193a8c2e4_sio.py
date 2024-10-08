"""sio

Revision ID: a5f193a8c2e4
Revises: 5c9310f877ad
Create Date: 2024-10-08 14:42:01.856880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a5f193a8c2e4'
down_revision = '5c9310f877ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('examen', schema=None) as batch_op:
        batch_op.alter_column('contenido',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('titulo',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)

    with op.batch_alter_table('nota', schema=None) as batch_op:
        batch_op.add_column(sa.Column('curso_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('nota_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'curso', ['curso_id'], ['id'])
        batch_op.drop_column('examen_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('nota', schema=None) as batch_op:
        batch_op.add_column(sa.Column('examen_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('nota_ibfk_2', 'examen', ['examen_id'], ['id'])
        batch_op.drop_column('curso_id')

    with op.batch_alter_table('examen', schema=None) as batch_op:
        batch_op.alter_column('titulo',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('contenido',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###
