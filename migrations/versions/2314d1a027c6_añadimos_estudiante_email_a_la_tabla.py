"""añadimos estudiante.email a la tabla

Revision ID: 2314d1a027c6
Revises: de8e0ef08c42
Create Date: 2024-10-03 10:35:32.303518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2314d1a027c6'
down_revision = 'de8e0ef08c42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estudiante', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estudiante', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
