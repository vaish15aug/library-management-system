from services.admin import checkAdminDb, createAdminDb, adminLoginDb, adminLogout
from helpers.jwtToken import createAccessToken, createRefreshToken,verifyToken
from helpers.redisHelper import setData, getData, delData
from schema.admin import AdminCreate,AdminLogin, AdminLogout
from fastapi import HTTPException, Header
import bcrypt
import traceback
from database import getDb
from sqlalchemy.orm import Session


    # Admin signup 
def createAdmin(data: AdminCreate, db: Session = getDb()):
    try:
        data_dict = data
        email = data_dict.email
        print("user", data_dict)
        adminExist = checkAdminDb(email, db)
        if adminExist is not None:
            raise HTTPException(status_code=400, detail="Account already exist")
        adminInfo = createAdminDb(data_dict, db)
        if adminInfo is None:
            raise HTTPException(status_code=400, detail="Failed to create account")
        
        return { "status": 201, "message": "Account created successfully" }
    
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# admin login

def adminLogin(data: AdminLogin,  db:Session =getDb()):
    try:
        data_dict = data
        email = data_dict.email 
        print("admin",data_dict) 
       
        
        adminInfo = adminLoginDb(data_dict, db)
        if adminInfo is None:
            raise HTTPException(status_code=400, detail="Failed to login ")
      
        
        payload = { "id": adminInfo.id, "email": adminInfo.email, "is_super":adminInfo.is_super }
        accessToken = createAccessToken(payload)
        refreshToken = createRefreshToken(payload)

        setData(accessToken, adminInfo.email)
        
        responseData = {
            "accessToken": accessToken,
            "refreshToken": refreshToken,
            
        }

        return { "status": 200, "message": "Login successfull", "data": responseData }
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))
    

# admin logout


def admin_logout(Authorization: str = Header(None), db: Session = getDb()):
    try:
        # Check if the Authorization header is present
        if Authorization is None:
            raise HTTPException(status_code=400, detail="Authorization header missing")
        
        # Ensure the Authorization header is in the correct Bearer format
        if not Authorization.startswith("Bearer "):
            raise HTTPException(status_code=400, detail="Invalid authorization header format. Expected 'Bearer <token>'")
        
        # Extract the token from the Authorization header
        token = Authorization.split(" ")[1]
        
        # Verify the token using the jwtToken helper
        payload = verifyToken(token)
        
        # Call the logout service to invalidate the token or perform necessary logout operations
        adminLogout(token, db)

        return {"message": "Logout successful"}
    
    except HTTPException as http_err:
        raise http_err  # Propagate HTTPExceptions for valid error responses
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during logout")




 





