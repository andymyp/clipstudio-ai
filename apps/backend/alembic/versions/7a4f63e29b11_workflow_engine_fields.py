"""workflow engine definitions and retry fields.

Revision ID: 7a4f63e29b11
Revises: 04dc1b8926aa
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "7a4f63e29b11"
down_revision: str | None = "04dc1b8926aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add persisted workflow definitions and task retry metadata."""
    op.add_column(
        "workflows",
        sa.Column(
            "definition", sa.JSON(), nullable=False, server_default=sa.text("'{}'")
        ),
    )
    op.add_column(
        "workflows",
        sa.Column("errors", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )
    op.add_column(
        "workflow_tasks",
        sa.Column("input", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )
    op.add_column(
        "workflow_tasks",
        sa.Column(
            "depends_on", sa.JSON(), nullable=False, server_default=sa.text("'[]'")
        ),
    )
    op.add_column(
        "workflow_tasks",
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "workflow_tasks",
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
    )


def downgrade() -> None:
    """Remove workflow engine metadata."""
    op.drop_column("workflow_tasks", "max_attempts")
    op.drop_column("workflow_tasks", "attempts")
    op.drop_column("workflow_tasks", "depends_on")
    op.drop_column("workflow_tasks", "input")
    op.drop_column("workflows", "errors")
    op.drop_column("workflows", "definition")
