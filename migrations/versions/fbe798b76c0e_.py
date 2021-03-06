"""empty message

Revision ID: fbe798b76c0e
Revises: 0aa8e0442999
Create Date: 2021-12-27 21:54:43.051050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbe798b76c0e'
down_revision = '0aa8e0442999'
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
