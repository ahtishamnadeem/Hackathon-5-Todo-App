"""Add priority and tags to todos table

Revision ID: 002
Revises: 001
Create Date: 2026-02-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add priority column (default: medium)
    op.add_column('todos', sa.Column('priority', sa.String(), nullable=False, server_default='medium'))

    # Add tags column (nullable, comma-separated)
    op.add_column('todos', sa.Column('tags', sa.String(), nullable=True))


def downgrade():
    # Remove the columns if rolling back
    op.drop_column('todos', 'tags')
    op.drop_column('todos', 'priority')
