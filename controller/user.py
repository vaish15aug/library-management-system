from services.user import checkUser, createUserDb, userLoginDb, userUpdateDb,deleteUserDb, find_userDb
from helpers.jwtToken import createAccessToken, createRefreshToken
from helpers.redisHelper import setData
from schema.user import UserCreate, UserLogin, UserUpdate, UserResponse
from fastapi import  HTTPException, Depends
import bcrypt
import traceback
from database import getDb
from sqlalchemy.orm import Session


# user signup
def createUser(data: UserCreate, db: Session = getDb()):
    try:
        data_dict = data
        email = data_dict.email
        print("user", data_dict)
        userExist = checkUser(email, db)
        if userExist is not None:
            raise HTTPException(status_code=400, detail="Account already exist")
        userInfo = createUserDb(data_dict, db)
        if userInfo is None:
            raise HTTPException(status_code=400, detail="Failed to create account")
        
        return { "status": 201, "message": "Account created successfully" }
    
    except Exception as e:
        print("error",traceback.print_exception(e))
        raise HTTPException(status_code=500, detail=str(e))

#  user login
def userLogin(data: UserLogin , db:Session =getDb()):
    try:
        data_dict = data
        email = data_dict.email 
        print("user",data_dict)
        userInfo = userLoginDb(data_dict, db)
        if userInfo is None:
            raise HTTPException(status_code=404, detail="User not found")  
        
        payload = { "id": userInfo.id, "email": userInfo.email }
        accessToken = createAccessToken(payload)
        refreshToken = createRefreshToken(payload)
       
        setData(accessToken, userInfo.email)
        
        responseData = {
            "accessToken": accessToken,
            "refreshToken": refreshToken,
        }
        return { "status": 200, "message": "Login successfull", "data": responseData }
    except Exception as e:
          print("error",e)
          raise HTTPException(status_code=500, detail=str(e))
    
# update user

def updateUser(data:UserUpdate,id:str, db: Session =getDb()):
    try:
    
        user = userUpdateDb(data,id,db)
        if user is None:
            raise HTTPException(status_code=404,detail="user not found")
        return{"status":201, "message":"User update Successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e) )
          

# delete user

def delete_user(id=str, db: Session= getDb()):
    try:
        result = deleteUserDb(id, db)
        return {"message": "User deleted successfully", "user": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# find user

def get_user(id: str, db: Session = getDb()):
    try:
        db_user = find_userDb(id, db)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_response = UserResponse.model_validate(db_user)
        return user_response
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
