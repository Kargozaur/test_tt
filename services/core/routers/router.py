import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.db_conf import get_db
from services.core.helpers.group import group_by_date, group_by_offer

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", status_code=200)
async def get_leads_analytics(
    request: Request,
    date_from: dt.date = Query(..., description="Start date (YYYY-MM-DD)"),
    date_to: dt.date = Query(..., description="End date (YYYY-MM-DD)"),
    group: str = Query(
        ..., pattern="^(date|offer)$", description="Group by 'date' or 'offer'"
    ),
    session: AsyncSession = Depends(get_db),
):
    affiliate_id = request.state.affiliate["id"]

    start_datetime = dt.datetime.combine(date_from, dt.datetime.min.time())
    end_datetime = dt.datetime.combine(date_to, dt.datetime.max.time())

    if group == "date":
        return await group_by_date(session, affiliate_id, start_datetime, end_datetime)
    elif group == "offer":
        return await group_by_offer(session, affiliate_id, start_datetime, end_datetime)
    else:
        raise HTTPException(status_code=400, detail="Invalid group parameter")
