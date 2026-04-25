import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from services.core.models.mixins import ID
from shared.models.base import Base


class Lead(Base, ID):
    __tablename__ = "leads"

    lead_id: Mapped[str] = mapped_column(sa.String(36), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(sa.String(20), nullable=False)
    offer_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("offers.id"), nullable=False
    )
    affiliate_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("affiliates.id"), nullable=False
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC)
    )


class Offer(Base, ID):
    __tablename__ = "offers"

    name: Mapped[str] = mapped_column(sa.String(255), unique=True)


class Affiliate(Base, ID):
    __tablename__ = "affiliates"

    name: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False)
