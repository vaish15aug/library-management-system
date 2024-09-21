from fastapi import APIRouter
from schema.user import UserCreate, UserLogin, UserUpdate, UserResponse
from controller.user import userLogin, createUser, updateUser, delete_user, get_user
from database import getDb
from sqlalchemy.orm import Session

userRouter = APIRouter(prefix="/user")

@userRouter.post("/login")
def login(login: UserLogin):
    return userLogin(login)

@userRouter.post("/create")
def create(create: UserCreate):
    return createUser(create)

@userRouter.put("/update/{id}")
def update(id:str,update:UserUpdate):
    return updateUser(update,id)

@userRouter.delete("/user_delete/{id}")
def deletes(id:str):
    return delete_user(id)


@userRouter.get("/get_one/{id}")
def findUser(id: str):
    return get_user(id)

