"""add content column to posts table

Revision ID: 9b3ec72cdb44
Revises: 301f14f00603
Create Date: 2024-02-12 17:16:48.230187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b3ec72cdb44'
down_revision: Union[str, None] = '301f14f00603'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
