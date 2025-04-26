"""add content column in post table

Revision ID: 669a2dfe4c3e
Revises: c8e6cdf624f6
Create Date: 2025-04-23 20:09:06.340152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '669a2dfe4c3e'
down_revision: Union[str, None] = 'c8e6cdf624f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
