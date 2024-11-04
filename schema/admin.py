from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[int] = None

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
    

# class AdminUpdate(BaseModel):
#     name:str
#     phone:int


class AdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    class Config:
        from_attributes = True
 