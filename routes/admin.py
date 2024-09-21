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

@adminRouter.post("/logout")
def logout(logout:AdminLogout):
    return admin_logout(logout)