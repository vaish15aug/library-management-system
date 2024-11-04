from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    name = Column(String, index = True)
    email= Column(String, unique = True)
    password = Column(String)
    phone= Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())


