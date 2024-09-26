from fastapi import APIRouter
from schema.admin import AdminCreate, AdminLogin, AdminLogout
from controller.admin import adminLogin, createAdmin, admin_logout

adminRouter = APIRouter(prefix="/admin")


@adminRouter.post("/create")
def create(create: AdminCreate):
    return createAdmin(create)

@adminRouter.post("/login")
def login(login:AdminLogin):
    return adminLogin(login)


@adminRouter.delete("/logout/{id}")
def delete(id:str):
    return admin_logout(id)