"""temp_migration

Revision ID: 43967bac186d
Revises: 0677ab0e59a9
Create Date: 2024-11-27 20:48:04.893767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43967bac186d'
down_revision: Union[str, None] = '0677ab0e59a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'price')
    # ### end Alembic commands ###