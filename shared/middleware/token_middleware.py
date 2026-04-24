from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from shared.jwt_handler.handler import get_token_data


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Missing Authorization header",
            )

        try:
            token = auth_header.split(" ")[1]
            affiliate_data = get_token_data(token)
            request.state.affiliate = affiliate_data
        except (IndexError, Exception) as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token: {str(e)}",
            )

        return await call_next(request)
