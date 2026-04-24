from pydantic import RedisDsn

from . import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: int = 6379
    db: int = 0
    leads_queue: str = "leads:queue"

    @property
    def dsn(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis", host=self.host, port=self.port, path=f"/{self.db}"
            )
        )
