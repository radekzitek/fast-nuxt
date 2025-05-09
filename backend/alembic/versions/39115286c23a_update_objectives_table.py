"""Update objectives table

Revision ID: 39115286c23a
Revises: 8e595d257e90
Create Date: 2025-05-10 18:54:54.764805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39115286c23a'
down_revision: Union[str, None] = '8e595d257e90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('objectives', 'level',
               existing_type=sa.VARCHAR(length=14),
               nullable=True)
    op.alter_column('objectives', 'last_updated_date',
               existing_type=sa.DATETIME(),
               nullable=True)
    op.drop_column('objectives', 'creation_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('objectives', sa.Column('creation_date', sa.DATETIME(), nullable=False))
    op.alter_column('objectives', 'last_updated_date',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.alter_column('objectives', 'level',
               existing_type=sa.VARCHAR(length=14),
               nullable=False)
    # ### end Alembic commands ###
