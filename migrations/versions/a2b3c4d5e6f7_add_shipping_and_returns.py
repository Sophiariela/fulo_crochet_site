"""add shipping_and_returns to products

Revision ID: a2b3c4d5e6f7
Revises: d1a4d34c86df
Create Date: 2026-07-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2b3c4d5e6f7'
down_revision = 'd1a4d34c86df'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('products', sa.Column('shipping_and_returns', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('products', 'shipping_and_returns')
