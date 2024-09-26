from services.user import checkUser, createUserDb, userLoginDb, userUpdateDb,deleteUserDb, find_userDb, userlogoutDb
from helpers.jwtToken import createAccessToken, createRefreshToken
from helpers.redisHelper import setData,getData, delData
from schema.user import UserCreate, UserLogin, UserUpdate, UserResponse
from fastapi import  HTTPException, Depends
import bcrypt
import traceback
from database import getDb
from sqlalchemy.orm import Session
from middleware.auth import check_jwt
from helpers.jwtToken import verifyToken
from typing import Dict
from helpers import jwtToken
from jose import JWTError


# user signup
def createUser(data: UserCreate):
    try:
        data_dict = data
        email = data_dict.email
        print("user", data_dict)
        userExist = checkUser(email)
        if userExist is not None:
            raise HTTPException(status_code=400, detail="Account already exist")
        userInfo = createUserDb(data_dict)
        if userInfo is None:
            raise HTTPException(status_code=400, detail="Failed to create account")
        
        return { "status": 201, "message": "Account created successfully" }
    
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))


#  user login
def userLogin(data: UserLogin):
    try:
        data_dict = data
        email = data_dict.email 
        print("user",data_dict)
        userInfo = userLoginDb(data_dict)
        if userInfo is None:
            raise HTTPException(status_code=404, detail="User not found")  
        
        payload = { "id": userInfo.id, "email": userInfo.email }
        accessToken = createAccessToken(payload)
        refreshToken = createRefreshToken(payload)
       
        setData(accessToken, userInfo.email)
        
        return { "status": 200, "message": "Login successfull" }
    except Exception as e:
          print("error",e)
          raise HTTPException(status_code=500, detail=str(e))
    
# update user
def updateUser(data:UserUpdate, id:str, payload: Dict):
    try:
        print("payload", payload)
        user = userUpdateDb(data,id)
        if user is None:
            raise HTTPException(status_code=404,detail="user not found")
        return{"status":201, "message":"User update Successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e) )
          

# delete user

def delete_user(id=str, payload: Dict= Depends(verifyToken)):
    try:
        print("payload", payload)
        result = deleteUserDb(id)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status":201, "message": "User deleted successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# find user

def get_user(id: str, payload: Dict):
    try:
        print("payload", payload)
        db_user = find_userDb(id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_response = UserResponse.model_validate(db_user)
        return user_response
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



# def user_logout(id: str):
#     try:
#         print(4)
#         result=userlogoutDb(id)
#         if result is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         delData(verifyToken)
#         print(5)
#         return {"status":201,"message": "User logout successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



def user_logout(id: str, payload: Dict ):
    try:
        print("Decoded token payload:", payload)

        if not payload:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        result = userlogoutDb(id)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        delData(payload["id"]) 
        
        print("User logged out successfully.")
        return {"status": 201, "message": "User logged out successfully"}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
