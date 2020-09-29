"""Fixed camara pasillo relation

Revision ID: af26fd67fea9
Revises: 65ce0c9c14c6
Create Date: 2020-07-16 23:23:12.306955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af26fd67fea9'
down_revision = '65ce0c9c14c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('camaras', sa.Column('path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('camaras', 'path')
    # ### end Alembic commands ###
