from redis.asyncio import Redis

from shared.settings.settings import settings


def get_redis_client():
    redis_client = Redis.from_url(settings.redis.dsn)
    return redis_client
