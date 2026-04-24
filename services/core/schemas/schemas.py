from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Period(BaseModel):
    date_from: str
    date_to: str


class Base(BaseModel):
    affiliate_id: str | UUID
    group_by: str
    period: Period

    model_config = ConfigDict(from_attributes=True)


class OfferDataItem(BaseModel):
    offer_id: int
    offer_name: str
    count: int
    leads: list[str]


class OfferStats(Base):
    affiliate_id: str | UUID
    group_by: Literal["offer"]
    period: Period
    data: list[OfferDataItem]


class DateDataItem(BaseModel):
    date: str
    count: int
    leads: list[str]


class DateStats(Base):
    affiliate_id: str | UUID
    group_by: Literal["date"]
    period: Period
    data: list[DateDataItem]
