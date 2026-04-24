from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.settings.jwt import JWTSettings
from shared.settings.postgres import PostgresSettings
from shared.settings.redis import RedisSettings


class Settings(BaseSettings):
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

    model_config = SettingsConfigDict(
        case_sensitive=False, arbitrary_types_allowed=True
    )


settings = Settings()
