"""make email column unique for users

Revision ID: 19a64bfe9dd3
Revises: 04045e54ddb5
Create Date: 2024-11-22 20:00:48.577204

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "19a64bfe9dd3"
down_revision: Union[str, None] = "04045e54ddb5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
