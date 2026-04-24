import datetime as dt

from services.landings.schemas.lead import LeadRequest


def prepare_lead(lead_id: str, lead_data: LeadRequest) -> dict:
    queue_data: dict[str, str | int | dt.datetime] = {
        "lead_id": lead_id,
        "name": lead_data.name,
        "phone": lead_data.phone,
        "country": lead_data.country,
        "offer_id": lead_data.offer_id,
        "affiliate_id": lead_data.affiliate_id,
        "received_at": dt.datetime.now(dt.UTC),
    }
    return queue_data
