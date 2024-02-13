"""create posts table

Revision ID: 301f14f00603
Revises: 
Create Date: 2024-02-12 15:59:26.586542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '301f14f00603'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                                sa.Column('titile', sa.String(), nullable=False) )
    pass


def downgrade(): #for rollback
    op.drop_table('posts')
    pass
