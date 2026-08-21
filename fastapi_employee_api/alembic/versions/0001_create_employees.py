"""create employees table

Revision ID: 0001_create_employees
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_employees"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("salary", sa.Integer(), nullable=False),
    )
    op.create_index("ix_employees_id", "employees", ["id"])
    op.create_index("ix_employees_email", "employees", ["email"], unique=True)


def downgrade():
    op.drop_index("ix_employees_email", table_name="employees")
    op.drop_index("ix_employees_id", table_name="employees")
    op.drop_table("employees")
