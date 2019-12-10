"""workouts table

Revision ID: 6d09ee7208de
Revises: 90d3067d121d
Create Date: 2019-10-02 13:58:13.030702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d09ee7208de'
down_revision = '90d3067d121d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('what', sa.String(length=128), nullable=True),
    sa.Column('when', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('who', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['who'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workout_when'), 'workout', ['when'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workout_when'), table_name='workout')
    op.drop_table('workout')
    # ### end Alembic commands ###
