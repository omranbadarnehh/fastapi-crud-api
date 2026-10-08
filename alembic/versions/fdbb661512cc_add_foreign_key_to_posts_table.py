"""add foreign key to posts table

Revision ID: fdbb661512cc
Revises: 7fe304554637
Create Date: 2026-10-04 13:20:35.636640

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fdbb661512cc"
down_revision: Union[str, Sequence[str], None] = "7fe304554637"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk' , table_name='posts')
    op.drop_column('posts' , 'owner_id')
    pass
