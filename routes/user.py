from fastapi import APIRouter, Depends, Header
from schema.user import UserCreate, UserLogin, UserUpdate, UserResponse
from controller.user import userLogin, createUser, updateUser, delete_user, get_user, user_logout
from database import getDb
from sqlalchemy.orm import Session
from helpers.jwtToken import verifyToken
from middleware import auth
from typing import Dict, Annotated

userRouter = APIRouter(prefix="/user")

@userRouter.post("/login")
def login(login: UserLogin):
    return userLogin(login)

@userRouter.post("/create")
def create(create: UserCreate):
    return createUser(create)

@userRouter.put("/update")
def update(update:UserUpdate,  payload:Dict = Depends(verifyToken)):
    return updateUser(update, payload)

@userRouter.delete("/user_delete/{id}")
def deletes( payload:Dict = Depends(verifyToken)):
    return delete_user(payload)


@userRouter.get("/get_one")
def findUser(payload:Dict = Depends(verifyToken)):
    return get_user(payload)


@userRouter.delete("/logout")
def deletes(  payload:Dict = Depends(verifyToken), authorization:Annotated[str | None,Header()] = None):
    return user_logout(payload, authorization)



