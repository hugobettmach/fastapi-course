"""add foreign key to posts table

Revision ID: 0cfdd7677c31
Revises: 92462a9c94b5
Create Date: 2021-11-21 09:34:03.664642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cfdd7677c31"
down_revision = "92462a9c94b5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
