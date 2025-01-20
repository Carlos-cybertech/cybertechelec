"""test43

Revision ID: fdefe8f05ca6
Revises: 52ce37e5928f
Create Date: 2025-01-20 09:34:34.480957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'fdefe8f05ca6'
down_revision: Union[str, None] = '52ce37e5928f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('test', mysql.VARCHAR(length=32), nullable=True))
    # ### end Alembic commands ###
