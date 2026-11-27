"""add content column to posts table

Revision ID: 2bf39e434cbc
Revises: 913683154275
Create Date: 2026-11-27 07:40:30.071865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bf39e434cbc'
down_revision: Union[str, Sequence[str], None] = '913683154275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    
    pass
