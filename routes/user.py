from fastapi import APIRouter, Depends
from schema.user import UserCreate, UserLogin, UserUpdate, UserResponse
from controller.user import userLogin, createUser, updateUser, delete_user, get_user, user_logout
from database import getDb
from sqlalchemy.orm import Session
from helpers.jwtToken import verifyToken
from middleware import auth
from typing import Dict

userRouter = APIRouter(prefix="/user")

@userRouter.post("/login")
def login(login: UserLogin):
    return userLogin(login)

@userRouter.post("/create")
def create(create: UserCreate):
    return createUser(create)

@userRouter.put("/update/{id}")
def update(id:str,update:UserUpdate,  payload:Dict = Depends(verifyToken)):
    return updateUser(update,id, payload)

@userRouter.delete("/user_delete/{id}")
def deletes(id:str,  payload:Dict = Depends(verifyToken)):
    return delete_user(id,payload)


@userRouter.get("/get_one/{id}")
def findUser(id: str, payload:Dict = Depends(verifyToken)):
    return get_user(id, payload)


@userRouter.delete("/logout/{id}")
def deletes( id:str, payload:Dict = Depends(verifyToken)):
    return user_logout(id, payload)



