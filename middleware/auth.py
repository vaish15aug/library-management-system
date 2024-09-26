from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Dict, Any
from database import getDb
from models.admin import Admin
from helpers.jwtToken import verifyToken 
from helpers import redisHelper
from helpers.redisHelper import getData, delData, setData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def check_jwt(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        user = getData(token)
        if user is None:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        payload = verifyToken(token)

        # user = redisHelper.get(token)


        return {"payload": payload}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def is_super(user: Dict[str, Any] = Depends(check_jwt)) -> Admin:
    admin = user["user"]
    if not Admin.is_super: 
        raise HTTPException(status_code=403, detail="Permission denied")
    return admin
