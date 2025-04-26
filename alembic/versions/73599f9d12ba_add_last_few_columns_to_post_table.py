"""add last few columns to post Table

Revision ID: 73599f9d12ba
Revises: 0531c3d040e2
Create Date: 2025-04-26 10:34:52.107388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73599f9d12ba'
down_revision: Union[str, None] = '0531c3d040e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable= False, server_default= 'TRUE'))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_default= sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

    pass
