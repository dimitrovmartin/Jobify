"""empty message

Revision ID: b0a4c1638901
Revises: 3e30730cc551
Create Date: 2021-12-26 18:04:43.662761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0a4c1638901'
down_revision = '3e30730cc551'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('advertisements_company_user_id_fkey', 'advertisements', type_='foreignkey')
    op.create_foreign_key(None, 'advertisements', 'company_users', ['company_user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'advertisements', type_='foreignkey')
    op.create_foreign_key('advertisements_company_user_id_fkey', 'advertisements', 'company_users', ['company_user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
