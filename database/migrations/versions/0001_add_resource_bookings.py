"""Add resource bookings table

Revision ID: 0001_add_resource_bookings
Revises: 
Create Date: 2026-07-12 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_add_resource_bookings"
down_revision = None
branch_labels = None
deployments = None


def upgrade() -> None:
    op.create_table(
        "resource_bookings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id"), nullable=False),
        sa.Column("booked_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("departments.id"), nullable=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", postgresql.ENUM("Upcoming", "Ongoing", "Completed", "Cancelled", name="booking_status"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f("ix_resource_bookings_asset_id"), "resource_bookings", ["asset_id"])
    op.create_index(op.f("ix_resource_bookings_booked_by"), "resource_bookings", ["booked_by"])
    op.create_index(op.f("ix_resource_bookings_department_id"), "resource_bookings", ["department_id"])
    op.create_index(op.f("ix_resource_bookings_start_datetime"), "resource_bookings", ["start_datetime"])
    op.create_index(op.f("ix_resource_bookings_status"), "resource_bookings", ["status"])


def downgrade() -> None:
    op.drop_index(op.f("ix_resource_bookings_status"), table_name="resource_bookings")
    op.drop_index(op.f("ix_resource_bookings_start_datetime"), table_name="resource_bookings")
    op.drop_index(op.f("ix_resource_bookings_department_id"), table_name="resource_bookings")
    op.drop_index(op.f("ix_resource_bookings_booked_by"), table_name="resource_bookings")
    op.drop_index(op.f("ix_resource_bookings_asset_id"), table_name="resource_bookings")
    op.drop_table("resource_bookings")
    postgresql.ENUM("Upcoming", "Ongoing", "Completed", "Cancelled", name="booking_status").drop(op.get_bind())
