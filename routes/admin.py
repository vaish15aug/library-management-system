from fastapi import APIRouter, Depends
from schema.admin import AdminCreate, AdminLogin, AdminLogout
from controller.admin import adminLogin, createAdmin, admin_logout
from helpers.jwtToken import verifyToken
from middleware import auth
from typing import Dict

adminRouter = APIRouter(prefix="/admin")


@adminRouter.post("/create")
def create(create: AdminCreate):
    return createAdmin(create)

@adminRouter.post("/login")
def login(login:AdminLogin):
    return adminLogin(login)


@adminRouter.delete("/logout/{id}")
def delete(id:str,payload:Dict = Depends(verifyToken)):
    return admin_logout(id, payload)