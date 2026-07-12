"""Initial AssetFlow organization setup schema.

Revision ID: 0001_organization_setup
Revises:
Create Date: 2026-07-12
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0001_organization_setup"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the initial AssetFlow platform tables."""

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=False)
    op.create_index(op.f("ix_roles_name"), "roles", ["name"], unique=False)

    op.create_table(
        "departments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("parent_department_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("department_head_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["parent_department_id"], ["departments.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_departments_id"), "departments", ["id"], unique=False)
    op.create_index(op.f("ix_departments_name"), "departments", ["name"], unique=False)
    op.create_index(op.f("ix_departments_code"), "departments", ["code"], unique=False)
    op.create_index(op.f("ix_departments_parent_department_id"), "departments", ["parent_department_id"], unique=False)
    op.create_index(op.f("ix_departments_department_head_id"), "departments", ["department_head_id"], unique=False)
    op.create_index(op.f("ix_departments_status"), "departments", ["status"], unique=False)

    op.create_table(
        "asset_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("default_warranty_months", sa.Integer(), nullable=False),
        sa.Column("is_bookable", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_asset_categories_id"), "asset_categories", ["id"], unique=False)
    op.create_index(op.f("ix_asset_categories_name"), "asset_categories", ["name"], unique=False)
    op.create_index(op.f("ix_asset_categories_code"), "asset_categories", ["code"], unique=False)
    op.create_index(op.f("ix_asset_categories_status"), "asset_categories", ["status"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("employee_code", sa.String(length=50), nullable=True),
        sa.Column("designation", sa.String(length=150), nullable=True),
        sa.Column("joining_date", sa.Date(), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("profile_image", sa.String(length=500), nullable=True),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("employee_code"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_employee_code"), "users", ["employee_code"], unique=False)
    op.create_index(op.f("ix_users_department_id"), "users", ["department_id"], unique=False)
    op.create_index(op.f("ix_users_role_id"), "users", ["role_id"], unique=False)

    op.create_foreign_key(
        "fk_departments_department_head_id_users",
        "departments",
        "users",
        ["department_head_id"],
        ["id"],
    )


def downgrade() -> None:
    """Drop the initial AssetFlow platform tables."""

    op.drop_constraint("fk_departments_department_head_id_users", "departments", type_="foreignkey")
    op.drop_index(op.f("ix_users_role_id"), table_name="users")
    op.drop_index(op.f("ix_users_department_id"), table_name="users")
    op.drop_index(op.f("ix_users_employee_code"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_asset_categories_status"), table_name="asset_categories")
    op.drop_index(op.f("ix_asset_categories_code"), table_name="asset_categories")
    op.drop_index(op.f("ix_asset_categories_name"), table_name="asset_categories")
    op.drop_index(op.f("ix_asset_categories_id"), table_name="asset_categories")
    op.drop_table("asset_categories")

    op.drop_index(op.f("ix_departments_status"), table_name="departments")
    op.drop_index(op.f("ix_departments_department_head_id"), table_name="departments")
    op.drop_index(op.f("ix_departments_parent_department_id"), table_name="departments")
    op.drop_index(op.f("ix_departments_code"), table_name="departments")
    op.drop_index(op.f("ix_departments_name"), table_name="departments")
    op.drop_index(op.f("ix_departments_id"), table_name="departments")
    op.drop_table("departments")

    op.drop_index(op.f("ix_roles_name"), table_name="roles")
    op.drop_index(op.f("ix_roles_id"), table_name="roles")
    op.drop_table("roles")
