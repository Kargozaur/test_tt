import asyncio
import datetime as dt
import json

import sqlalchemy as sa
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from services.core.db.db_conf import get_db
from services.core.models.models import Affiliate, Lead, Offer
from shared.redis_client.client import get_redis_client


class LeadWorker:
    def __init__(self):
        self.redis: Redis | None = None
        self.running = True

    def initialize(self) -> None:
        self.redis: Redis = get_redis_client()

    async def check_duplicate(self, session: AsyncSession, lead_data: dict) -> bool:
        threshhold = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=10)
        query = sa.select(Lead).where(
            Lead.name == lead_data["name"],
            Lead.phone == lead_data["phone"],
            Lead.affiliate_id == lead_data["affiliate_id"],
            Lead.offer_id == lead_data["offer_id"],
            Lead.created_at >= threshhold,
        )
        result = await session.execute(query)
        return result.scalar_one_or_none() is not None

    async def verify_foreign_keys(self, session: AsyncSession, lead_data: dict) -> bool:
        offer_query = sa.select(Offer).where(Offer.id == lead_data["offer_id"])
        offer = await session.execute(offer_query)
        if not offer.scalar_one_or_none():
            return False

        affiliate_query = sa.select(Affiliate).where(
            Affiliate.id == lead_data["affiliate_id"]
        )
        affiliate = await session.execute(affiliate_query)
        if not affiliate.scalar_one_or_none():
            return False

        return True

    async def process_lead(self, lead_data: dict):
        async for session in get_db():
            if await self.check_duplicate(session, lead_data):
                print(f"Duplicate lead{lead_data['lead_id']}")
                return

            if await self.verify_foreign_keys(session, lead_data):
                print(
                    f"Invalid offer_id or affiliate_id for lead: {lead_data['lead_id']}"
                )
                return

            lead = Lead(
                lead_id=lead_data["lead_id"],
                name=lead_data["name"],
                phone=lead_data["phone"],
                country=lead_data["country"],
                offer_id=lead_data["offer_id"],
                affiliate_id=lead_data["affiliate_id"],
            )
            try:
                session.add(lead)
                await session.commit()

            except Exception as exc:
                await session.rollback()
                print(
                    f"Exception occured while proceeding {lead_data['lead_id']}: {exc}"
                )
            finally:
                break

    async def run(self):
        self.initialize()
        while self.running:
            try:
                result = await self.redis.brpop("leads:queue", timeout=1)  # ty:ignore[invalid-await, unresolved-attribute]

                if result:
                    _, message = result
                    lead_data = json.loads(message)
                    await self.process_lead(lead_data)

                await asyncio.sleep(0.1)
            except Exception as exc:
                print(f"Error: {exc}")
                await asyncio.sleep(1)

    async def stop(self):
        self.running = False
        if self.redis:
            await self.redis.close()
            self.redis = None


async def start_worker():
    worker = LeadWorker()
    try:
        await worker.run()
    except KeyboardInterrupt:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(start_worker())
