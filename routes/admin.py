from fastapi import APIRouter, Depends, Header
from schema.admin import AdminCreate, AdminLogin, AdminLogout, AdminUpdate
from controller.admin import adminLogin, createAdmin, admin_logout, updateAdmin, get_admin
from helpers.jwtToken import verifyToken
from middleware import auth
from typing import Dict, Annotated


adminRouter = APIRouter(prefix="/admin")



@adminRouter.post("/create")
def create(create: AdminCreate):
    return createAdmin(create)

@adminRouter.post("/login")
def login(login:AdminLogin):
    return adminLogin(login)


@adminRouter.delete("/logout")
def delete(payload:Dict = Depends(verifyToken),authorization:Annotated[str | None,Header()] = None):
    return admin_logout(payload, authorization)


@adminRouter.put("/update")
def update(update:AdminUpdate,  payload:Dict = Depends(verifyToken)):
    return updateAdmin(update, payload)


@adminRouter.get("/get_single")
def findUser(payload:Dict = Depends(verifyToken)):
    return get_admin(payload)

