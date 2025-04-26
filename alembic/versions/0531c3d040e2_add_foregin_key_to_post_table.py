"""add foregin key to post Table

Revision ID: 0531c3d040e2
Revises: 6ebb83f1af2f
Create Date: 2025-04-23 20:25:57.777890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0531c3d040e2'
down_revision: Union[str, None] = '6ebb83f1af2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('who_created_user',sa.Integer(), nullable = False ))
    op.create_foreign_key('fk_post_who_created_user', source_table = 'posts', 
                          referent_table = 'users', 
                          local_cols = ['who_created_user'], 
                          remote_cols = ['id'], 
                          ondelete = 'CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_post_who_created_user', table_name = 'posts')
    op.drop_column('posts', 'who_created_user')
    pass
