"""create orders products table

Revision ID: 0efbfddc9d29
Revises: 28249da3a75a
Create Date: 2025-03-26 22:04:18.480291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0efbfddc9d29'
down_revision: Union[str, None] = '28249da3a75a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_products_id'), 'orders_products', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_products_id'), table_name='orders_products')
    op.drop_table('orders_products')
    # ### end Alembic commands ###
