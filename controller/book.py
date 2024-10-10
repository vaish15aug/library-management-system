from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schema.book import BookCreate, BookResponse, BookUpdate, DeleteBook 
from services.book import createBookDb, get_bookDb, updateBookDb, deleteBookDb, get_all_bookDB,search_booksDb
from database import getDb
from fastapi import Query
from helpers.jwtToken import verifyToken
from typing import Dict, Optional
from jose import JWTError

# # create a book
# def createBook(data: BookCreate, payload:Dict):
#     try:
#         print("payload", payload)
#         book = createBookDb(data)
#         if not payload.get("is_super"):
#             raise HTTPException(status_code=403, detail="You are not authorized to create a book")
#         if book is None:
#             raise HTTPException(status_code=400, detail="Failed to create book")
#         return { "status": 201, "message": "Book created successfully" }
#     except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))

def createBook(data: Dict, payload: Dict):
    try:
    
        book_data = BookCreate(**data)  
        print("payload", payload)
        book = createBookDb(book_data)
    
        if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to create a book")
        
        if book is None:
            raise HTTPException(status_code=400, detail="Failed to create book")
        
        return {"status": 201, "message": "Book created successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    # get a single book

def get_book(id: str):
    try:

        db_book = get_bookDb(id)
       
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        book_response = BookResponse.model_validate(db_book).model_dump()
        
        return book_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# update book
def update_book(data: BookUpdate, id:str, payload:Dict):
    try:
        book = updateBookDb(id, BookUpdate(**data))
        
        print("payload", payload)
        # book = updateBookDb(book_data,id)
        if not payload.get("is_super"):
           raise HTTPException(status_code=403, detail="You are not authorized to update a book")
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        return {"status": 201, "message": "Book updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# delete book


def delete_book(id=str, payload: Dict= Depends(verifyToken)):
    try:
        print("payload", payload)
        result = deleteBookDb(id)
        if not payload.get("is_super"):
             raise HTTPException(status_code=403, detail="You are not authorized to delete a book")
        return {"message": "Book deleted successfully", "book": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
  
    

# GET all book list

def get_all_books(
    payload:Dict,
    offset: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(10, le=100, description="Pagination limit")
):
    try:
        print("payload", payload)
        books_data = get_all_bookDB( offset=offset, limit=limit)
        return {"message": "Books list", "book": books_data}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


# serach book


def search_books(search_param: str = None, category: str = None, is_available: bool = None, payload: Dict= Depends(verifyToken)):
    try:
        print("payload", payload)
        
        db_books = search_booksDb(search_param=search_param, category=category, is_available=is_available)
        
        if not db_books:
            raise HTTPException(status_code=404, detail="No books found matching the criteria.")
        
        return [BookResponse.model_validate(book) for book in db_books]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



