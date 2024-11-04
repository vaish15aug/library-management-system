from schema.admin import AdminCreate, AdminLogin, AdminLogout, AdminUpdate
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
            name= data['name'],
            email = data['email'],
            phone = data['phone'],
            is_super= data['is_super'],
            password = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"))
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
        
        adminInfo = db.query(Admin).filter(Admin.email == data['email']).first()
        print(adminInfo)
        if adminInfo is None:
            return None

        password = adminInfo.password
        if not bcrypt.checkpw(data['password'].encode("utf-8"),
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


   
# def adminUpdateDb(data:AdminUpdate,id:str):
#     try:
        
#         # if not data.id:
#         #     raise ValueError("User ID must be provided for update")
#         admin = db.query(Admin).filter(Admin.id == id).first()
        
#         if admin is None:
#             raise Exception("User not found")
#         if "name" in data:
#             admin.name = data["name"]
#             print(f"Updated name to: {admin.name}")
#         if "phone" in data:
#             admin.phone = data["phone"]
#             print(f"Updated phone to: {admin.phone}")
#         # if data.name:
#         #     admin.name = data.name
#         # if data.phone:
#         #     admin.phone= data.phone
      
#         db.commit()
#         db.refresh(admin)
#         return admin
#     except Exception as e:
#         print(e)
#         db.rollback()
#         raise Exception("failed to update admin")

def adminUpdateDb(data: AdminUpdate, id: str):
    try:
        admin = db.query(Admin).filter(Admin.id == id).first()
        
        if admin is None:
            # raise Exception("Admin not found")
            return None
        if data.name:
            admin.name = data.name
            print(f"Updated name to: {admin.name}")
        if data.phone:
            admin.phone = data.phone
            print(f"Updated phone to: {admin.phone}")
    
        db.commit()
        db.refresh(admin)
        return admin

    except Exception as e:
        print("Exception in updating admin:", e)
        db.rollback()
        raise Exception("Failed to update admin")



#   find admin
def find_adminDb(id: str):
    try:
        user = db.query(Admin).filter(Admin.id == id).first()
        # if user is None:
        #     raise Exception("admin not found")
        return user
    except Exception as e:
        print(e)
        raise Exception("Failed to find admin")
    


