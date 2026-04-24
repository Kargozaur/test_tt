import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class ID:
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
