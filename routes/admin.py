from fastapi import APIRouter, Depends
from schema.admin import AdminCreate, AdminLogin, AdminLogout, AdminUpdate
from controller.admin import adminLogin, createAdmin, admin_logout, updateAdmin
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


@adminRouter.put("/update/{id}")
def update(id:str,update:AdminUpdate,  payload:Dict = Depends(verifyToken)):
    return updateAdmin(update,id, payload)