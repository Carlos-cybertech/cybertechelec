"""test42

Revision ID: e3825fa78392
Revises: 59cd7e750591
Create Date: 2025-01-20 09:23:52.302871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3825fa78392'
down_revision: Union[str, None] = '59cd7e750591'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('test', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'test')
    # ### end Alembic commands ###
