from jose import  JWTError, jwt
from datetime import datetime, timedelta, timezone
from helpers.envVars import jwtSecret, jwtAlgorithm
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from helpers.redisHelper import getData

security= HTTPBearer()

def createAccessToken(payload: dict):
    try:
        expire = datetime.now(tz=timezone.utc) + timedelta(hours=24)
        print("expiry", expire)
        payload.update({ "exp": expire, "tokenType": "access" })
        accessToken = jwt.encode(payload, jwtSecret, algorithm = jwtAlgorithm)
        print("access token",accessToken)
        return accessToken
    except JWTError as e:
        print("access",e)
        raise Exception(e)


def createRefreshToken(payload: dict):
    try:
        expire = datetime.now(tz=timezone.utc) + timedelta(hours=24)
        payload.update({ "exp": expire, "tokenType": "refresh" })
        refreshToken = jwt.encode(payload, jwtSecret, algorithm = jwtAlgorithm)
        print("refresh token", refreshToken)
        return refreshToken
    except JWTError as e:
        print("refresh",e)
        raise Exception(e)


# def verifyToken(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     try:
#         print("creds", credentials)
#         token = credentials.credentials
#         email= getData(token)
#         if email is None:
#             raise HTTPException(status_code=403, detail="forbidden")
#         payload = jwt.decode(token, jwtSecret, algorithms = jwtAlgorithm)
#         return payload
#     except JWTError as e:
#         print(e)
#         raise HTTPException(status_code=401, detail="Invalid token")


def verifyToken(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials  # Extract the token from the request
        print("Token:", token)
        
        # Check the token in Redis (or other persistent storage)
        email = getData(token)
        if email is None:
            raise HTTPException(status_code=403, detail="Forbidden: Invalid token")

        # Decode the JWT token
        payload = jwt.decode(token, jwtSecret, algorithms=[jwtAlgorithm])
        return payload  # Return the decoded payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



    

    

