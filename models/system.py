from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func
from database import Base

class System(Base):
    __tablename__ = 'system'
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    book_id = Column(Integer)
    user_id = Column(Integer)
    checkout_date = Column(Date)
    due_date = Column(Date)
    fine = Column(String)
    is_returned= Column(Boolean, autoincrement=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())





