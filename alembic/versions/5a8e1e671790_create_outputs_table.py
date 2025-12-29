"""5a8e1e671790_create_outputs_table

Revision ID: replace_with_new_uuid
Revises: e0b6bdd21e56
Create Date: 2025-12-29

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5a8e1e671790' 
down_revision: Union[str, None] = 'e0b6bdd21e56'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create the outputs table
    op.create_table(
        'outputs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('gen_file_path', sa.String(), nullable=False),
        sa.Column('source_filenames', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['ai_tasks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_outputs_id'), 'outputs', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_outputs_id'), table_name='outputs')
    op.drop_table('outputs')