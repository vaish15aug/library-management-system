from pydantic import BaseModel, EmailStr, constr


class AdminCreate(BaseModel):
    name: str 
    phone: int
    email: EmailStr
    password: constr(min_length=8)
    is_super:bool
   

class AdminLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class AdminLogout(BaseModel):
    email: EmailStr
    

class AdminUpdate(BaseModel):
    name:str
    phone:int

   