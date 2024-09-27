from services.admin import checkAdminDb, createAdminDb, adminLoginDb, adminlogoutDb, adminUpdateDb, find_adminDb
from helpers.jwtToken import createAccessToken, createRefreshToken,verifyToken
from helpers.redisHelper import setData, getData, delData
from schema.admin import AdminCreate,AdminLogin, AdminLogout, AdminUpdate, AdminResponse
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
        detail={
           "accessToken": accessToken,
           "refreshToken": refreshToken
        }

        setData(accessToken, adminInfo.email)
        
        return { "status": 200, "message": "Login successfull", "data":detail }
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# admin logout

    
def admin_logout( payload: Dict, authorization: str):
    try:
        print("Decoded token payload:", payload)
        print("headers", authorization)
        token=authorization.split(" ")[1]
        print("token",token)
        val = delData(token) 
        print("value", val)
        
        print("Admin logged out successfully.")
        return {"status": 201, "message": "Admin logged out successfully"}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

    # admin update
def updateAdmin(data:AdminUpdate, payload: Dict):
    try:
        print("payload", payload)
        id = payload["id"]
        print("Updating user with ID:", id)
        user = adminUpdateDb(data,id)
        if user is None:
            raise HTTPException(status_code=404,detail=" Admin not found")
        return{"status":201, "message":"Admin update Successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e) )
    


        #   find admin
def get_admin(payload: Dict):
    try:
        print("payload", payload)
        id = payload["id"]
        db_user = find_adminDb(id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        admin_response = AdminResponse.model_validate(db_user)
        return admin_response
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
