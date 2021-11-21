"""add last few columns to posts table

Revision ID: 4ea3dd968957
Revises: 0cfdd7677c31
Create Date: 2021-11-21 09:40:13.592077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4ea3dd968957"
down_revision = "0cfdd7677c31"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
