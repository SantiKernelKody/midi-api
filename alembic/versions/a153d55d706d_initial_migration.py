"""Initial migration

Revision ID: a153d55d706d
Revises: e1a8fbc10d40
Create Date: 2024-07-26 00:19:04.283798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a153d55d706d'
down_revision: Union[str, None] = 'e1a8fbc10d40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('special_need', sa.Boolean(), nullable=True))
    op.drop_constraint('player_special_need_id_fkey', 'player', type_='foreignkey')
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
    op.create_foreign_key('player_special_need_id_fkey', 'player', 'special_need', ['special_need_id'], ['id'])
    op.drop_column('player', 'special_need')
    # ### end Alembic commands ###
