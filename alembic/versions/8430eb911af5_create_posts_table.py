"""create posts table

Revision ID: 8430eb911af5
Revises: 
Create Date: 2021-11-21 09:00:44.660973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8430eb911af5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False, primary_key=False),
    )


def downgrade():
    op.drop_table("posts")
