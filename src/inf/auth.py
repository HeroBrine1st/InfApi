import settings

from datetime import datetime
from hashlib import sha256
from fastapi import HTTPException
from fastapi.security import APIKeyCookie, OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request

def validate(credentials: OAuth2PasswordRequestForm):
    if credentials.username != settings.LOGIN or credentials.password != settings.PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            # headers={"WWW-Authenticate": "Basic"},
        )
    return True

def get_cookie():
    return sha256(sha256(settings.COOKIE_BASE.encode("UTF-8")).digest() + sha256(str(datetime.now().date()).encode("UTF-8")).digest()).hexdigest()

class CookieAuth(APIKeyCookie):
    async def __call__(self, request: Request):
        result = await super().__call__(request)
        if result == get_cookie():
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid cookie",
                headers={"WWW-Authenticate": "Cookie"},
            )
