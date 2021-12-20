"""empty message

Revision ID: 547a68bccc62
Revises: be425f9f2e31
Create Date: 2021-12-20 00:35:18.008829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '547a68bccc62'
down_revision = 'be425f9f2e31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applied_advertisements',
    sa.Column('applicant_user_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('sent', 'approved', 'rejected', name='status'), nullable=False),
    sa.ForeignKeyConstraint(['applicant_user_id'], ['applicant_users.id'], ),
    sa.ForeignKeyConstraint(['skill_id'], ['advertisements.id'], ),
    sa.PrimaryKeyConstraint('applicant_user_id', 'skill_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('applied_advertisements')
    # ### end Alembic commands ###