from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(data: dict):

    payload = data.copy()

    expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiry)

    payload["exp"]=expiry

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )


def decode_access_token(access_token: str):
    return (
        jwt.decode(
            access_token,
            settings.jwt_secret,
            algorithms=ALGORITHM
        )
    )

