from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Dict, Any
from database import getDb
from models.admin import Admin
from helpers.jwtToken import verifyToken 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def check_jwt(token: str = Depends(oauth2_scheme), db: Session = Depends(getDb)) -> Dict[str, Any]:
    try:
        # Verify the token
        payload = verifyToken(token)
        email = payload.get("email")

        if email is None:
            raise HTTPException(status_code=403, detail="Invalid token, no email found")

        # Fetch user from the database
        user = db.query(Admin).filter(Admin.email == email).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {"user": user, "payload": payload}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def is_super(user: Dict[str, Any] = Depends(check_jwt)) -> Admin:
    admin = user["user"]
    if not Admin.is_super: 
        raise HTTPException(status_code=403, detail="Permission denied")
    return admin
