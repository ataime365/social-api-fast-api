"""rename column

Revision ID: b1904a26ab4b
Revises: 5b0defd96ea4
Create Date: 2024-02-13 09:22:56.050585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1904a26ab4b'
down_revision: Union[str, None] = '5b0defd96ea4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('posts', 'titile',
                    new_column_name='title')

def downgrade():
    op.alter_column('posts', 'title',
                    new_column_name='titile')