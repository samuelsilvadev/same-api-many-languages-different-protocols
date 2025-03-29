"""update orders table to include updated_at

Revision ID: 3181920e3a95
Revises: 0efbfddc9d29
Create Date: 2025-03-29 07:22:37.374421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3181920e3a95"
down_revision: Union[str, None] = "0efbfddc9d29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "orders", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("orders", "updated_at")
    # ### end Alembic commands ###
