"""empty message

Revision ID: d8b28d7a629b
Revises: 8cfdefa75766
Create Date: 2025-04-18 15:54:59.579790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8b28d7a629b'
down_revision: Union[str, None] = '8cfdefa75766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Tasks', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Tasks', 'UserProfiles', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Tasks', type_='foreignkey')
    op.drop_column('Tasks', 'user_id')
    # ### end Alembic commands ###
