"""Add pending to datto enum

Revision ID: feaa0f85db58
Revises: fdefe8f05ca6
Create Date: 2025-01-20 09:38:43.975503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feaa0f85db58'
down_revision: Union[str, None] = 'fdefe8f05ca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a new enum type with the additional value
    op.execute("ALTER TABLE projects MODIFY COLUMN datto ENUM('completed', 'in_progress', 'pending') NOT NULL")


def downgrade() -> None:
    pass
