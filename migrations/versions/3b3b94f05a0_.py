"""empty message

Revision ID: 3b3b94f05a0
Revises: None
Create Date: 2015-11-14 17:37:48.709779

"""

# revision identifiers, used by Alembic.
revision = '3b3b94f05a0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('investment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('symbol', sa.String(length=64), nullable=True),
    sa.Column('shares', sa.Float(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('symbol')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('investment')
    op.drop_table('accounts')
    ### end Alembic commands ###
