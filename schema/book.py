from pydantic import BaseModel

from datetime import date

class BookCreate(BaseModel):
    book_name: str
    author: str
    category: str
    publish_date: date
    is_available: bool
    
   
class BookUpdate(BaseModel):
    book_name: str
    author: str
    category: str
    publish_date: date
    
class DeleteBook(BaseModel):
    id:int
    book_name: str
    author: str
    category: str
    publish_date: date
    is_available: bool

class BookResponse(BaseModel):
    id: int
    book_name: str
    author: str
    category: str
    publish_date: date
    is_available: bool
    class Config:
        from_attributes = True

 