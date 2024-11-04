from sqlalchemy.orm import Session
from models.book import Book
from schema.book import BookCreate, BookUpdate, BookResponse
from database import getDb
from typing import List, Optional
db:Session = getDb()
from sqlalchemy import or_
# create book
def createBookDb(data: BookCreate):
    try:
        book = Book(
            book_name=data.book_name,
            author=data.author,
            category=data.category,
            publish_date=data.publish_date,
            is_available= data.is_available,

        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("Failed to create book")



# get single book 

def get_bookDb(id: str):
    try:
       
        book = db.query(Book).filter(Book.id == id).first()
      
        if book is None:
            raise Exception("Book not found")
      
        return book
    except Exception as e:
        print(e)
        raise Exception("Failed to find book")

    
#  get all book

def get_all_bookDB( offset: int = 0, limit: int = 10):
    try:
        print(1)
        books_query = db.query(Book).all()
        print(2)
        books = books_query
        print(3)
       
        count = db.query(Book).count()
        print(4)
        return {"count": count, "rows": books}
        
    except Exception as e:
        print(e)
        raise Exception("Failed to find book list")


# update book
def updateBookDb(id:str,data: BookUpdate):
    try:
       
        book = db.query(Book).filter(Book.id == id).first()
      
        if book is None:
            raise Exception("Book not found")
         
        if data.book_name:
            book.book_name = data.book_name
        if data.author:
            book.author = data.author
        if data.category:
            book.category = data.category    
        if data.publish_date:
            book.publish_date = data.publish_date
       
        db.commit()
        db.refresh(book)
        return book
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("Failed to update book")


# Delete book

def deleteBookDb(id: str):
    try:
        
        db_book = db.query(Book).filter(Book.id == id).first()

        if db_book:  
            db.delete(db_book)
            db.commit()
            return db_book  
        else:
            raise Exception("Book  not found")

    except Exception as e:
        print(e)
        db.rollback()  
        raise Exception("Failed to delete book ")
    
# search book 

def  search_booksDb(search_param: str = None, category: str = None, is_available: bool = None):
    try:
        query = db.query(Book)
        
        if search_param:
            query = query.filter(or_(   
                Book.book_name.ilike(f"%{search_param}%"),
                Book.author.ilike(f"%{search_param}%")
            ))
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))
        
        if is_available is not None:
            query = query.filter(Book.is_available == is_available)

        return query.all()
    except Exception as e:
        raise Exception(f"Failed to search books: {str(e)}")


    

 