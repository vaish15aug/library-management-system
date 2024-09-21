from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    name = Column(String, index=True)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    is_super = Column(Boolean, default=False )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


