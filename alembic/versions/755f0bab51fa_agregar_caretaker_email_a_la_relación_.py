"""Agregar caretaker_email a la relación entre player y caretaker

Revision ID: 755f0bab51fa
Revises: 63f6cd676221
Create Date: 2024-08-18 23:16:49.722232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '755f0bab51fa'
down_revision: Union[str, None] = '63f6cd676221'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_dashboard_user_email', table_name='dashboard_user')
    op.create_index(op.f('ix_dashboard_user_email'), 'dashboard_user', ['email'], unique=False)
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
    op.drop_index(op.f('ix_dashboard_user_email'), table_name='dashboard_user')
    op.create_index('ix_dashboard_user_email', 'dashboard_user', ['email'], unique=True)
    # ### end Alembic commands ###
