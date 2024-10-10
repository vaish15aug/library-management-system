from services.user import checkUser, createUserDb, userLoginDb, userUpdateDb,deleteUserDb, find_userDb, userlogoutDb
from helpers.jwtToken import createAccessToken, createRefreshToken
from helpers.redisHelper import setData,getData, delData
from schema.user import UserCreate, UserLogin, UserUpdate, UserResponse
from fastapi import  HTTPException, Depends
import traceback
from database import getDb
from sqlalchemy.orm import Session
from middleware.auth import check_jwt
from helpers.jwtToken import verifyToken
from typing import Dict
from helpers import jwtToken
from jose import JWTError


# user signup


def createUser(data:UserCreate):
    try:
        if 'email' not in data:
            raise HTTPException(status_code=400, detail="Email is required")
        if 'password' not in data:
            raise HTTPException(status_code=400, detail="Password is required")
        if 'name' not in data:
            raise HTTPException(status_code=400, detail="Name is required")
        if 'phone' not in data:
            raise HTTPException(status_code=400, detail="Phone number is required")

        email = data['email']
        userExist = checkUser(email)
        if userExist is not None:
            raise HTTPException(status_code=400, detail="Account already exists")

        userInfo = createUserDb(data)
        if userInfo is None:
            raise HTTPException(status_code=400, detail="Failed to create account")

        return { "status": 201, "message" : "Account created successfully" }

    except HTTPException as http_ex:
        raise http_ex
    
    except Exception as e:
        print("error",e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


#  user login
def userLogin(data: dict):
    try:
        if 'email' not in data:
            raise HTTPException(status_code=400, detail="Email is required")
        if 'password' not in data:
            raise HTTPException(status_code=400, detail="Password is required")
        data_dict = data
        email = data_dict["email"]
        # email = data_dict.email 
        print("user",data_dict)
        # userInfo = userLoginDb(email)
        userInfo = userLoginDb(data) 
        if userInfo is None:
            raise HTTPException(status_code=404, detail="User not found")  
        
        payload = { "id": userInfo.id, "email": userInfo.email }
        accessToken = createAccessToken(payload)
        refreshToken = createRefreshToken(payload)
        detail={
           "accessToken": accessToken,
           "refreshToken": refreshToken
        }
        setData(accessToken, userInfo.email)
        
        return { "status": 200,"message": "Login successful" , "data":detail }
    
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
          print("error",e)
          raise HTTPException(status_code=500, detail=str(e))




    

# update user
def updateUser(data:UserUpdate, payload: Dict):
    try:
        print("payload", payload)
        id = payload["id"]
        print("Updating user with ID:", id)
        user = userUpdateDb(data, id)
        if user is None:
            raise HTTPException(status_code=404,detail="user not found")
        return{"status":201, "message":"User update Successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e) )
          

# delete user

def delete_user(payload: Dict):
    try:
        print("payload", payload)
        id = payload["id"]
        print("Updating user with ID:", id)
        result = deleteUserDb(id)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status":201, "message": "User deleted successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# find user

def get_user(payload: Dict):
    try:
        print("payload", payload)
        id = payload["id"]
        db_user = find_userDb(id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_response = UserResponse.model_validate(db_user)
        return user_response
         
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# user logout

def user_logout( payload: Dict, authorization: str):
    try:
        print("Decoded token payload:", payload)
        print("headers", authorization)
        token=authorization.split(" ")[1]
        print("token",token)
        val = delData(token) 
        print("value", val)
        
        print("User logged out successfully.")
        return {"status": 201, "message": "User logged out successfully"}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
