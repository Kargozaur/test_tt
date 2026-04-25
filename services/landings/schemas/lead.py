import re

from pydantic import BaseModel, Field, field_validator


class LeadRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str = Field(..., min_length=1, max_length=20)
    country: str = Field(..., min_length=1, max_length=3)
    offer_id: int
    affiliate_id: int

    @field_validator("phone", mode="after")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^\+?[0-9\s\-\(\)]{5,20}$", v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("country", mode="after")
    @classmethod
    def validate_country(cls, v: str):
        if not re.match(r"^[A-Z]{2}$", v.upper()):
            raise ValueError("Country must be ISO 3166-1 alpha-2 format (e.g., UA)")
        return v.upper()


class LeadResponse(BaseModel):
    message: str
    lead_id: str | None = None
