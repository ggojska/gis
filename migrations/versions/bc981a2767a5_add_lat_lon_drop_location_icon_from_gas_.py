"""add lat, lon, drop location, icon from gas_stations

Revision ID: bc981a2767a5
Revises: 0587edfae7ec
Create Date: 2022-12-09 12:38:14.858209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc981a2767a5'
down_revision = '0587edfae7ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gas_stations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lat', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('lon', sa.Float(), nullable=True))
        batch_op.create_index(batch_op.f('ix_gas_stations_lat'), ['lat'], unique=False)
        batch_op.create_index(batch_op.f('ix_gas_stations_lon'), ['lon'], unique=False)
        batch_op.drop_column('icon')
        batch_op.drop_column('location')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gas_stations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('icon', sa.TEXT(), nullable=True))
        batch_op.drop_index(batch_op.f('ix_gas_stations_lon'))
        batch_op.drop_index(batch_op.f('ix_gas_stations_lat'))
        batch_op.drop_column('lon')
        batch_op.drop_column('lat')

    # ### end Alembic commands ###
