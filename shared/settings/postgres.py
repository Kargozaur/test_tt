from pydantic import PostgresDsn

from . import BaseSettings


class PostgresSettings(BaseSettings):
    """This data should be in .env, but to make it easy I'll leave it as it is"""

    host: str = "database"
    port: int = 5432
    user: str = "postgres"
    password: str = "1234"
    database: str = "leads_db"

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.host,
                username=self.user,
                password=self.password,
                port=self.port,
                path=self.database,
            )
        )
