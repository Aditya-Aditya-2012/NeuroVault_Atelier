"""create_ai_tasks_table

Revision ID: e0b6bdd21e56
Revises: dd3663b2b9e6
Create Date: 2025-12-28 12:59:38.673599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e0b6bdd21e56'
down_revision: Union[str, Sequence[str], None] = 'dd3663b2b9e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# alembic/versions/e0b6bdd21e56_create_ai_tasks_table.py
from sqlalchemy.dialects import postgresql

ENUM_NAME = 'taskstatus'
ENUM_VALUES = ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')

def upgrade() -> None:
    # 1. Manually create the ENUM type in Postgres
    bind = op.get_bind()
    type_exists = bind.execute(
        sa.text(f"SELECT 1 FROM pg_type WHERE typname = '{ENUM_NAME}'")
    ).fetchone()

    if not type_exists:
        # Create it manually only if it's missing
        task_status = postgresql.ENUM(*ENUM_VALUES, name=ENUM_NAME)
        task_status.create(bind)

    # 2. Create the table
    op.create_table(
        'ai_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('prompt', sa.String(), nullable=True),
        sa.Column('input_image_ids', postgresql.ARRAY(sa.Integer()), nullable=False),
        # 🚩 FIX: Use sa.Enum with name and values, but set inherit_schema=True 
        # so Alembic doesn't try to "CREATE TYPE" inside "CREATE TABLE"
        sa.Column(
            'status', 
            postgresql.ENUM(*ENUM_VALUES, name=ENUM_NAME, create_type=False), 
            nullable=False
        ),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )

def downgrade() -> None:
    # 1. Drop table first
    op.drop_table('ai_tasks')

    # 2. Drop the ENUM type safely
    bind = op.get_bind()
    bind.execute(sa.text(f"DROP TYPE IF EXISTS {ENUM_NAME}"))