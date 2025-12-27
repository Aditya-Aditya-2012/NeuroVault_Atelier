"""add_is_processed_to_images

Revision ID: dd3663b2b9e6
Revises: 
Create Date: 2025-12-27 17:56:43.658206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd3663b2b9e6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('images', sa.Column('is_processed', sa.Boolean(), nullable=False, server_default='false'))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('images', 'is_processed')
