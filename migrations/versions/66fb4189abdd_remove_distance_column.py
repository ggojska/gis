"""remove distance column

Revision ID: 66fb4189abdd
Revises: acdf11381983
Create Date: 2022-12-31 10:41:30.763252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66fb4189abdd'
down_revision = 'acdf11381983'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gas_stations', schema=None) as batch_op:
        batch_op.drop_column('distance')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gas_stations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('distance', sa.FLOAT(), nullable=True))

    # ### end Alembic commands ###
