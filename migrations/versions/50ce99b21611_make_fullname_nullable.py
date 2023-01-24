"""make fullname nullable

Revision ID: 50ce99b21611
Revises: 85db3b1768d3
Create Date: 2023-01-23 22:38:04.929021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50ce99b21611'
down_revision = '85db3b1768d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'full_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'full_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
