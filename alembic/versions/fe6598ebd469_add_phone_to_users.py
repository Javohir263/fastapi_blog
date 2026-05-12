"""add_phone_to_users

Revision ID: fe6598ebd469
Revises: 298b1a84b879
Create Date: 2026-05-12 22:56:06.925662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe6598ebd469'
down_revision: Union[str, Sequence[str], None] = '298b1a84b879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
