"""Add AssetFlow asset inventory tables.

Revision ID: 0002_assets
Revises: 0001_organization_setup
Create Date: 2026-07-12
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0002_assets"
down_revision = "0001_organization_setup"
branch_labels = None
depends_on = None


asset_status = sa.Enum(
    "Available",
    "Allocated",
    "Reserved",
    "Under Maintenance",
    "Lost",
    "Retired",
    "Disposed",
    name="asset_status",
)

asset_condition = sa.Enum(
    "Excellent",
    "Good",
    "Fair",
    "Poor",
    "Damaged",
    name="asset_condition",
)


def upgrade() -> None:
    """Create asset inventory tables and enum types."""

    asset_status.create(op.get_bind(), checkfirst=True)
    asset_condition.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_tag", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("serial_number", sa.String(length=100), nullable=False),
        sa.Column("manufacturer", sa.String(length=150), nullable=True),
        sa.Column("model_number", sa.String(length=150), nullable=True),
        sa.Column("purchase_date", sa.Date(), nullable=True),
        sa.Column("purchase_cost", sa.Numeric(14, 2), nullable=False),
        sa.Column("warranty_expiry", sa.Date(), nullable=True),
        sa.Column("condition", asset_condition, nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("status", asset_status, nullable=False),
        sa.Column("is_bookable", sa.Boolean(), nullable=False),
        sa.Column("photo_url", sa.String(length=500), nullable=True),
        sa.Column("document_url", sa.String(length=500), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["asset_categories.id"]),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["updated_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asset_tag"),
        sa.UniqueConstraint("serial_number"),
    )
    op.create_index(op.f("ix_assets_id"), "assets", ["id"], unique=False)
    op.create_index(op.f("ix_assets_asset_tag"), "assets", ["asset_tag"], unique=False)
    op.create_index(op.f("ix_assets_name"), "assets", ["name"], unique=False)
    op.create_index(op.f("ix_assets_category_id"), "assets", ["category_id"], unique=False)
    op.create_index(op.f("ix_assets_department_id"), "assets", ["department_id"], unique=False)
    op.create_index(op.f("ix_assets_serial_number"), "assets", ["serial_number"], unique=False)
    op.create_index(op.f("ix_assets_manufacturer"), "assets", ["manufacturer"], unique=False)
    op.create_index(op.f("ix_assets_model_number"), "assets", ["model_number"], unique=False)
    op.create_index(op.f("ix_assets_location"), "assets", ["location"], unique=False)
    op.create_index(op.f("ix_assets_status"), "assets", ["status"], unique=False)
    op.create_index(op.f("ix_assets_created_by"), "assets", ["created_by"], unique=False)
    op.create_index(op.f("ix_assets_updated_by"), "assets", ["updated_by"], unique=False)


def downgrade() -> None:
    """Drop asset inventory tables and enum types."""

    op.drop_index(op.f("ix_assets_updated_by"), table_name="assets")
    op.drop_index(op.f("ix_assets_created_by"), table_name="assets")
    op.drop_index(op.f("ix_assets_status"), table_name="assets")
    op.drop_index(op.f("ix_assets_location"), table_name="assets")
    op.drop_index(op.f("ix_assets_model_number"), table_name="assets")
    op.drop_index(op.f("ix_assets_manufacturer"), table_name="assets")
    op.drop_index(op.f("ix_assets_serial_number"), table_name="assets")
    op.drop_index(op.f("ix_assets_department_id"), table_name="assets")
    op.drop_index(op.f("ix_assets_category_id"), table_name="assets")
    op.drop_index(op.f("ix_assets_name"), table_name="assets")
    op.drop_index(op.f("ix_assets_asset_tag"), table_name="assets")
    op.drop_index(op.f("ix_assets_id"), table_name="assets")
    op.drop_table("assets")

    asset_status.drop(op.get_bind(), checkfirst=True)
    asset_condition.drop(op.get_bind(), checkfirst=True)
