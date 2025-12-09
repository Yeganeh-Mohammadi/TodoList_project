"""Add closed_at to tasks table

Revision ID: a1b2c3d4e5f6
Revises: f7e5bcaaf966
Create Date: 2025-12-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f7e5bcaaf966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add closed_at column to tasks table."""
    op.add_column('tasks', sa.Column('closed_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Remove closed_at column from tasks table."""
    op.drop_column('tasks', 'closed_at')

