import time

from config import JWT_ALGORITHM, SECRET
from jwt import encode as encode_, decode as decode_, InvalidSignatureError
from database.pd_models import UserBase
from fastapi import Request, Response, HTTPException


def encode(data: dict):
    if data.get('expires') is None:
        return None
    return encode_(data, SECRET, algorithm=JWT_ALGORITHM)


def decode(token: str):
    decoded = decode_(token, SECRET, algorithms=JWT_ALGORITHM)
    if decoded.get('expires') <= time.time():
        return None
    return decoded


def encode_user(user: UserBase):
    return encode({
        'expires': time.time() + (60*60*24*15),
        'username': user.username,
        'password': user.password
    })


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class JWTBearer(HTTPBearer):
    @staticmethod
    def __info_jwt__(token: str):
        try:
            return decode(token)
        except InvalidSignatureError:
            return False

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            user = self.__info_jwt__(credentials.credentials)
            if not user or user.get('expires') <= time.time():
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return UserBase(username=user.get('username'), password=user.get('password'))
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
