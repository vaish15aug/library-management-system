from services.admin import checkAdminDb, createAdminDb, adminLoginDb, adminlogoutDb
from helpers.jwtToken import createAccessToken, createRefreshToken,verifyToken
from helpers.redisHelper import setData, getData, delData
from schema.admin import AdminCreate,AdminLogin, AdminLogout
from fastapi import HTTPException, Header
import bcrypt
import traceback
from sqlalchemy.orm import Session
from helpers.jwtToken import verifyToken
from typing import Dict



    # Admin signup 
def createAdmin(data: AdminCreate):
    try:
        data_dict = data
        email = data_dict.email
        print("user", data_dict)
        adminExist = checkAdminDb(email)
        if adminExist is not None:
            raise HTTPException(status_code=400, detail="Account already exist")
        adminInfo = createAdminDb(data_dict)
        if adminInfo is None:
            raise HTTPException(status_code=400, detail="Failed to create account")
        
        return { "status": 201, "message": "Account created successfully" }
    
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# admin login

def adminLogin(data: AdminLogin):
    try:
        data_dict = data
        email = data_dict.email 
        print("admin",data_dict) 
       
        
        adminInfo = adminLoginDb(data_dict)
        if adminInfo is None:
            raise HTTPException(status_code=400, detail="Failed to login ")
      
        
        payload = { "id": adminInfo.id, "email": adminInfo.email, "is_super":adminInfo.is_super }
        accessToken = createAccessToken(payload)
        refreshToken = createRefreshToken(payload)

        setData(accessToken, adminInfo.email)
        
        return { "status": 200, "message": "Login successfull" }
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# admin logout

# def admin_logout(id: str):
#     try:
#         adminlogoutDb(id)
#         return {"message": "Admin logout successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def admin_logout(id: str, payload: Dict ):
    try:
        print("Decoded token payload:", payload)

        if not payload:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        result = adminlogoutDb(id)
        if result is None:
            raise HTTPException(status_code=404, detail="Admin not found")
        
        delData(payload["id"]) 
        
        print("Admin logged out successfully.")
        return {"status": 201, "message": "Admin logged out successfully"}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
