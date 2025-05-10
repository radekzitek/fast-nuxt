"""add team_member_id to user

Revision ID: 70c6f7ff50d3
Revises: 9b7304d6873c
Create Date: 2025-05-09 17:54:52.189815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70c6f7ff50d3'
down_revision: Union[str, None] = '9b7304d6873c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('team_member_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_users_team_member_id_team_members',
        'users',
        'team_members',
        ['team_member_id'],
        ['id'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_users_team_member_id_team_members', 'users', type_='foreignkey')
    op.drop_column('users', 'team_member_id')
