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


#     # Admin signup 
def createAdmin(data: AdminCreate):
    try:
        
        if 'email' not in data:
            raise HTTPException(status_code=400, detail="Email is required")
        if 'password' not in data:
            raise HTTPException(status_code=400, detail="Password is required")
        if 'name' not in data:
            raise HTTPException(status_code=400, detail="Name is required")
        if 'phone' not in data:
            raise HTTPException(status_code=400, detail="Phone number is required")
        if 'is_super' not in data:
            raise HTTPException(status_code=400, detail="is_super is required")
        email = data['email']
        adminExist = checkAdminDb(email)

        if adminExist is not None:
            raise HTTPException(status_code=400, detail="Account already exist")
        adminInfo = createAdminDb(data)
        if adminInfo is None:
            raise HTTPException(status_code=400, detail="Failed to create account")
        
        return { "status": 201, "message": "Account created successfully" }
    
    except HTTPException as http_ex:
        raise http_ex
  
    except Exception as e:
        print("error",e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# admin login

def adminLogin(data: AdminLogin):
    try:
        if 'email' not in data:
            raise HTTPException(status_code=400, detail="Email is required")
        if 'password' not in data:
            raise HTTPException(status_code=400, detail="Password is required")
        data_dict = data
        email = data_dict["email"]
        print("admin",data_dict) 
       
        
        adminInfo = adminLoginDb(data)
        if adminInfo is None:
            raise HTTPException(status_code=400, detail="Failed to login")
      
        
        payload = { "id": adminInfo.id, "email": adminInfo.email, "is_super":adminInfo.is_super }
        accessToken = createAccessToken(payload)
        refreshToken = createRefreshToken(payload)
        detail={
           "accessToken": accessToken,
           "refreshToken": refreshToken
        }

        setData(accessToken, adminInfo.email)
        
        return { "status": 200, "message": "Login successfull", "data":detail }
    
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# admin logout

    
def admin_logout( payload: Dict, authorization: str):
    try:
        print("Decoded token payload:", payload)
        print("headers", authorization)
        # id = payload.get("id")
        # db_admin = adminlogoutDb(id)
        # if db_admin is None:
        #     raise HTTPException(status_code=404, detail="Admin not found")
        token=authorization.split(" ")[1]
        print("token",token)
        
        val = delData(token) 
        print("value", val)
        
        return {"status": 201, "message": "Admin logged out successfully"}
    
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


    # admin update

def updateAdmin(data: AdminUpdate, payload: dict):
    try:
        id = payload["id"]
        
        if not data.name and not data.phone:
            raise HTTPException(status_code=400, detail="Only name, phone number can be updated")
        admin = adminUpdateDb(data, id)
        
        if admin is None:
            raise HTTPException(status_code=404, detail="Admin not found")
        
        return {"status": 201, "message": "Admin updated successfully"}
    
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



        #   find admin


def get_admin(id: int):
    try:
        if not isinstance(id, int):
            raise HTTPException(status_code=400, detail="Please provide valid id")
        print("id", id)
        db_user = find_adminDb(id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Admin not found")
        admin_response = AdminResponse.model_validate(db_user)
        return {"status": 200,"message": "Admin found successfully", "data": admin_response}
      
    except HTTPException as http_ex:
        raise http_ex 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    


