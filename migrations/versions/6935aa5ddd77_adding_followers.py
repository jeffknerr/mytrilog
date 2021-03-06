"""adding followers

Revision ID: 6935aa5ddd77
Revises: a4e364816e04
Create Date: 2019-10-08 14:46:26.610374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6935aa5ddd77'
down_revision = 'a4e364816e04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
