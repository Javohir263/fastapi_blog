"""rating ustun qo'shildi

Revision ID: 298b1a84b879
Revises: d242a8ae34e0
Create Date: 2026-05-12 22:50:14.045231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '298b1a84b879'
down_revision: Union[str, Sequence[str], None] = 'd242a8ae34e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'posts',
        'content',      # Eski nom
        new_column_name='body'   # Yangi nom
    )

def downgrade() -> None:
    op.alter_column(
        'posts',
        'body',
        new_column_name='content'
    )