"""Add pending to project_status enum

Revision ID: 52ce37e5928f
Revises: e3825fa78392
Create Date: 2025-01-20 09:27:59.594144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52ce37e5928f'
down_revision: Union[str, None] = 'e3825fa78392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a new enum type with the additional value
    op.execute("ALTER TABLE projects MODIFY COLUMN project_status ENUM('completed', 'in_progress', 'pending', 'on_hold') NOT NULL")


def downgrade() -> None:
    # Revert to the old enum type if necessary
    op.execute("ALTER TABLE projects MODIFY COLUMN project_status ENUM('completed', 'in_progress', 'on_hold') NOT NULL")
