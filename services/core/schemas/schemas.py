from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Period(BaseModel):
    date_from: str
    date_to: str


class Base[T](BaseModel):
    affiliate_id: str | UUID
    period: Period
    data: list[T]

    model_config = ConfigDict(from_attributes=True)


class OfferDataItem(BaseModel):
    offer_id: int
    offer_name: str
    count: int
    leads: list[str] = []


class OfferStats(Base[OfferDataItem]):
    group_by: Literal["offer"] = "offer"


class DateDataItem(BaseModel):
    date: str
    count: int
    leads: list[str] = []


class DateStats(Base[DateDataItem]):
    group_by: Literal["date"] = "date"
