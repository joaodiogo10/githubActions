"""user table

Revision ID: 955a626d6058
Revises: 
Create Date: 2022-10-18 20:53:41.870530

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '955a626d6058'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), nullable=False, unique=True),
        sa.Column('address', sa.String(100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
     op.drop_table('users')
