"""Update player table

Revision ID: e53116613489
Revises: 1b877df7737b
Create Date: 2024-07-17 17:47:45.566022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e53116613489'
down_revision: Union[str, None] = '1b877df7737b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('full_name', sa.String(length=128), nullable=False))
    op.create_foreign_key(None, 'player', 'special_need', ['special_need_id'], ['id'])
    op.create_foreign_key(None, 'player', 'educational_entity', ['school_id'], ['id'])
    op.drop_column('player', 'last_name')
    op.drop_column('player', 'special_need')
    op.drop_column('player', 'avatar_id')
    op.drop_column('player', 'name')
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
    op.add_column('player', sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('player', sa.Column('avatar_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('player', sa.Column('special_need', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('player', sa.Column('last_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'player', type_='foreignkey')
    op.drop_constraint(None, 'player', type_='foreignkey')
    op.drop_column('player', 'full_name')
    # ### end Alembic commands ###
