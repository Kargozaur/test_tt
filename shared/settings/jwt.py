import datetime as dt

from pydantic import SecretStr

from . import BaseSettings, SettingsConfigDict


class JWTSettings(BaseSettings):
    key: SecretStr
    alg: str = "HS256"
    short: dt.timedelta = dt.timedelta(minutes=30)

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="JWT_"
    )
