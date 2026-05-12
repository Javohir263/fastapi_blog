"""rename_content_to_body_in_posts

Revision ID: a264428db863
Revises: fe6598ebd469
Create Date: 2026-05-12 23:13:16.623315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a264428db863'
down_revision: Union[str, Sequence[str], None] = 'fe6598ebd469'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
