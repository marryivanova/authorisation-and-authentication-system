"""add_new_tablue_users

Revision ID: 0873a5547aff
Revises:
Create Date: 2025-03-21 13:29:17.284566

"""

from alembic import op
import sqlalchemy as sa

revision = "0873a5547aff"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("role", sa.String, default="user"),
    )


def downgrade():
    op.drop_table("users")
