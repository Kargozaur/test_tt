import datetime as dt

import jwt
from fastapi import HTTPException

from shared.settings.settings import settings


def create_affiliate(affiliate: int) -> str:
    payload: dict = {
        "id": affiliate,
        "exp": dt.datetime.now(dt.UTC) + dt.timedelta(minutes=30),
    }
    return jwt.encode(payload, settings.jwt.key, algorithm=settings.jwt.alg)


def get_token_data(token: str) -> dict:
    credential_exc = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt.key, settings.jwt.alg)
        affiliate_id = payload.get("id")
        if affiliate_id is None:
            raise credential_exc
        return {"id": affiliate_id}
    except jwt.PyJWTError:
        raise credential_exc
