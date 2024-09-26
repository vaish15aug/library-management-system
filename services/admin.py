from schema.admin import AdminCreate, AdminLogin, AdminLogout
from models.admin import Admin
from sqlalchemy.orm import Session
import bcrypt
from fastapi import Depends
from helpers.redisHelper import setData, getData ,delData
from helpers import redisHelper, jwtToken
from helpers.jwtToken import verifyToken
from helpers.redisHelper import setData
from datetime import datetime, timedelta
from database import getDb
db:Session = getDb()

    
def checkAdminDb(email):
    try:

        AdminInfo = db.query(Admin).filter(Admin.email == email).first()
        if AdminInfo:
            return AdminInfo
        else: 
            return None
    except Exception as e:
        print(e)
        raise Exception(e)
    
    
# signup
def createAdminDb(data):
    try:

        AdminInfo = Admin(
            name= data.name,
            email = data.email,
            phone = data.phone,
            is_super= data.is_super,
            password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                       )
        db.add(AdminInfo)
        db.commit()
        db.refresh(AdminInfo)

        if AdminInfo: 
            return AdminInfo
        else: 
            return None
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception(e)


# login service
def adminLoginDb(data: AdminLogin):
    try:
        
        adminInfo = db.query(Admin).filter(Admin.email == data.email).first()
        print(adminInfo)
        if adminInfo is None:
            return None

        password = adminInfo.password
        if not bcrypt.checkpw(data.password.encode("utf-8"),
            password.encode("utf-8")):
            raise Exception("Incorrect password")

        return adminInfo
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception(e)
    
    


def adminlogoutDb(id: str):
    try:
        print(1)
        db_admin = db.query(Admin).filter(Admin.id == id).first()
        print(2)
        if db_admin:  
            db.delete(db_admin)
            db.commit()
            return db_admin 
        else:
            raise Exception("admin  not found")
    except Exception as e:
        print(e)
        print(3)
        db.rollback()  
        raise Exception(" An error occurred during logout")


   
