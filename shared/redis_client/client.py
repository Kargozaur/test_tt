from redis.asyncio import Redis

from shared.settings.settings import settings


def get_redis_client() -> Redis:
    redis_client = Redis.from_url(settings.redis.dsn, decode_responses=True)
    return redis_client
