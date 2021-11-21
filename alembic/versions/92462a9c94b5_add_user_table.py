"""add user table

Revision ID: 92462a9c94b5
Revises: 0c9f9af9fb13
Create Date: 2021-11-21 09:23:01.002369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "92462a9c94b5"
down_revision = "0c9f9af9fb13"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
