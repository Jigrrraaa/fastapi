"""add user table

Revision ID: 6ebb83f1af2f
Revises: 669a2dfe4c3e
Create Date: 2025-04-23 20:15:34.678184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ebb83f1af2f'
down_revision: Union[str, None] = '669a2dfe4c3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable= False),
                    sa.Column('email', sa.String(), nullable= False),
                    sa.Column('password', sa.String(), nullable= False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable= False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
