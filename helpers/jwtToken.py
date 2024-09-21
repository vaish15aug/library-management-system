from jose import  JWTError, jwt
from datetime import datetime, timedelta, timezone
from helpers.envVars import jwtSecret, jwtAlgorithm


def createAccessToken(payload: dict):
    try:
        expire = datetime.now(tz=timezone.utc) + timedelta(hours=2)
        print("expiry", expire)
        payload.update({ "exp": expire, "tokenType": "access" })
        accessToken = jwt.encode(payload, jwtSecret, algorithm=jwtAlgorithm)
        print("access token",accessToken)
        return accessToken
    except JWTError as e:
        print("access",e)
        raise Exception(e)

def createRefreshToken(payload: dict):
    try:
        expire = datetime.now(tz=timezone.utc) + timedelta(hours=24)
        payload.update({ "exp": expire, "tokenType": "refresh" })
        refreshToken = jwt.encode(payload, jwtSecret, algorithm=jwtAlgorithm)
        print("refresh token", refreshToken)
        return refreshToken
    except JWTError as e:
        print("refresh",e)
        raise Exception(e)

def verifyToken(token: str):
    try:
        payload = jwt.decode(token, jwtSecret, algorithm=jwtAlgorithm)
        return payload
    except JWTError as e:
        print(e)
        raise Exception(e)