"""empty message

Revision ID: 170ec599e68
Revises: 3b3b94f05a0
Create Date: 2015-11-15 13:16:21.665190

"""

# revision identifiers, used by Alembic.
revision = '170ec599e68'
down_revision = '3b3b94f05a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('investments', sa.Column('price', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('investments', 'price')
    ### end Alembic commands ###
