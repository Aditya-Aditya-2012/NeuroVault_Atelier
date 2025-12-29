"""empty message

Revision ID: e94759e74b4d
Revises: 9c2b79d7e9f4
Create Date: 2025-12-29 17:27:53.429994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e94759e74b4d'
down_revision: Union[str, Sequence[str], None] = '9c2b79d7e9f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
