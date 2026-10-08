"""add new columns

Revision ID: 256e190283e7
Revises: fdbb661512cc
Create Date: 2026-10-07 18:29:59.077591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '256e190283e7'
down_revision: Union[str, Sequence[str], None] = 'fdbb661512cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column("posts",sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
