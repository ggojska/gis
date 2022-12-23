"""add comments

Revision ID: 8e31628ea937
Revises: 9f02c46c1875
Create Date: 2022-12-23 18:52:46.592925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e31628ea937'
down_revision = '9f02c46c1875'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('rate', sa.Numeric(precision=2, scale=1), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('gas_station_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gas_station_id'], ['gas_stations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###
