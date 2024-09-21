from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, func
from database import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    book_name = Column(String, index=True)
    author = Column(String)
    category = Column(String)
    publish_date=Column(Date)
    is_available = Column(Boolean, autoincrement=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


    