"""Fix fbref_id column type from bigint to text

Revision ID: fix_fbref_id_type
Revises: 60c3c3c552bc
Create Date: 2026-04-03 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fix_fbref_id_type'
down_revision: Union[str, Sequence[str], None] = '60c3c3c552bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: convert fbref_id from bigint to text."""
    op.alter_column('players', 'fbref_id',
               existing_type=sa.BigInteger(),
               type_=sa.Text(),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema: convert fbref_id from text back to bigint."""
    op.alter_column('players', 'fbref_id',
               existing_type=sa.Text(),
               type_=sa.BigInteger(),
               existing_nullable=True)
