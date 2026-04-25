import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from redis.asyncio import Redis

from services.landings.helper.get_redis import get_redis
from services.landings.helper.prepare_lead import prepare_lead
from services.landings.schemas.lead import LeadRequest, LeadResponse

router = APIRouter(prefix="/landings", tags=["leads"])


@router.post("/lead", response_model=LeadResponse)
async def create_lead(
    request: Request, lead_data: LeadRequest, client: Redis = Depends(get_redis)
):
    current_affiliate = request.state.affiliate["id"]
    if current_affiliate != lead_data.affiliate_id:
        raise HTTPException(
            status_code=403, detail="affiliate_id in request does not match token"
        )
    lead_id = str(uuid.uuid7())
    queue_data = prepare_lead(lead_id, lead_data)
    await client.lpush("leads:queue", json.dumps(queue_data))  # ty:ignore[invalid-await]
    return LeadResponse(message="Accepted and queued for processing", lead_id=lead_id)
