"""add content column to posts table

Revision ID: 0c9f9af9fb13
Revises: 8430eb911af5
Create Date: 2021-11-21 09:18:12.874109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0c9f9af9fb13"
down_revision = "8430eb911af5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
