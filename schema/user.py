from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[int] = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password:constr(min_length=8)
    phone: int
   

class UserLogin(BaseModel):
    email: EmailStr
    password:constr(min_length=8)


class UserLogout(BaseModel):
    email:EmailStr
    password:constr(min_length=8)


# class UserUpdate(BaseModel):
#     # id:int
#     name:str
#     phone:int

class DeleteUser(BaseModel):
    name: str
    email: EmailStr
    password:constr(min_length=8)
    phone: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    class Config:
        from_attributes = True

class UserLogout(BaseModel):
   email:EmailStr
   

