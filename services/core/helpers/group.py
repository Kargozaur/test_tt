import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.models.models import Lead, Offer


async def group_by_date(
    session: AsyncSession, affiliate_id: int, start: dt.datetime, end: dt.datetime
) -> dict:
    query = (
        sa.select(
            sa.func.date(Lead.created_at).label("date"),
            sa.func.count(Lead.id).label("count"),
            sa.func.array_agg(Lead.lead_id).label("lead_ids"),
        )
        .where(
            sa.and_(
                Lead.affiliate_id == affiliate_id,
                Lead.created_at >= start,
                Lead.created_at <= end,
            )
        )
        .group_by(sa.func.date(Lead.created_at))
        .order_by("date")
    )

    result = await session.execute(query)
    rows = result.all()

    return {
        "affiliate_id": affiliate_id,
        "group_by": "date",
        "period": {
            "date_from": start.date().isoformat(),
            "date_to": end.date().isoformat(),
        },
        "data": [
            {"date": str(row.date), "count": row.count, "leads": row.lead_ids or []}
            for row in rows
        ],
    }


async def group_by_offer(
    session: AsyncSession, affiliate_id: int, start: dt.datetime, end: dt.datetime
) -> dict:
    query = (
        sa.select(
            Offer.id.label("offer_id"),
            Offer.name.label("offer_name"),
            sa.func.count(Lead.id).label("count"),
            sa.func.array_agg(Lead.lead_id).label("lead_ids"),
        )
        .join(Offer, Lead.offer_id == Offer.id)
        .where(
            sa.and_(
                Lead.affiliate_id == affiliate_id,
                Lead.created_at >= start,
                Lead.created_at <= end,
            )
        )
        .group_by(Offer.id, Offer.name)
        .order_by(Offer.name)
    )

    result = await session.execute(query)
    rows = result.all()

    return {
        "affiliate_id": affiliate_id,
        "group_by": "offer",
        "period": {
            "date_from": start.date().isoformat(),
            "date_to": end.date().isoformat(),
        },
        "data": [
            {
                "offer_id": row.offer_id,
                "offer_name": row.offer_name,
                "count": row.count,
                "leads": row.lead_ids or [],
            }
            for row in rows
        ],
    }
