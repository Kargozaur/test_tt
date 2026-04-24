import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.db_conf import get_db
from services.core.helpers.group import group_by_date, group_by_offer
from shared.jwt_handler.handler import get_token_data

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("")
async def get_leads_analytics(
    date_from: dt.date = Query(..., description="Start date (YYYY-MM-DD)"),
    date_to: dt.date = Query(..., description="End date (YYYY-MM-DD)"),
    group: str = Query(
        ..., regex="^(date|offer)$", description="Group by 'date' or 'offer'"
    ),
    current_affiliate: dict = Depends(get_token_data),
    session: AsyncSession = Depends(get_db),
):
    affiliate_id = current_affiliate["id"]

    start_datetime = dt.datetime.combine(date_from, dt.datetime.min.time())
    end_datetime = dt.datetime.combine(date_to, dt.datetime.max.time())

    if group == "date":
        return await group_by_date(session, affiliate_id, start_datetime, end_datetime)
    elif group == "offer":
        return await group_by_offer(session, affiliate_id, start_datetime, end_datetime)
    else:
        raise HTTPException(status_code=400, detail="Invalid group parameter")
