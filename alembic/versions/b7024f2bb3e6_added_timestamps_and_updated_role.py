"""added timestamps and updated Role

Revision ID: b7024f2bb3e6
Revises: 2a7fd3a71a27
Create Date: 2026-07-19 17:36:44.920501
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7024f2bb3e6"
down_revision: Union[str, Sequence[str], None] = "2a7fd3a71a27"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "employees",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "employees",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("employees", "updated_at")
    op.drop_column("employees", "created_at")