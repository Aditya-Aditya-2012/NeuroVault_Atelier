"""empty message

Revision ID: 9c2b79d7e9f4
Revises: 5a8e1e671790, f3a1b2c3d4e5
Create Date: 2025-12-29 17:27:02.395110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c2b79d7e9f4'
down_revision: Union[str, None] = '5a8e1e671790'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
