"""Initial migration

Revision ID: 74098beb7223
Revises: f76974c6c1ff
Create Date: 2024-07-25 23:13:59.855850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74098beb7223'
down_revision: Union[str, None] = 'f76974c6c1ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('player_level', 'score',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10, asdecimal=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('player_level', 'score',
               existing_type=sa.Float(precision=10, asdecimal=2),
               type_=sa.REAL(),
               existing_nullable=True)
    # ### end Alembic commands ###
