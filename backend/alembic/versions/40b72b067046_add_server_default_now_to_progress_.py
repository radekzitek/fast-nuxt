"""Add server_default now() to progress_updates.created_at

Revision ID: 40b72b067046
Revises: 39115286c23a
Create Date: 2025-05-11 18:22:55.619195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40b72b067046'
down_revision: Union[str, None] = '39115286c23a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'progress_updates',
        'created_at',
        server_default=sa.text('now()'),
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )
    op.alter_column(
        'progress_updates',
        'updated_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=True
    )

def downgrade():
    op.alter_column(
        'progress_updates',
        'created_at',
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )
    op.alter_column(
        'progress_updates',
        'updated_at',
        existing_type=sa.DateTime(timezone=False),
        nullable=False
    )