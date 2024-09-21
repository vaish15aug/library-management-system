from fastapi import HTTPException
from sqlalchemy.orm import Session
from schema.book import BookCreate, BookResponse, BookUpdate, DeleteBook 
from services.book import createBookDb, get_bookDb, updateBookDb, deleteBookDb, get_all_bookDB
from database import getDb
from fastapi import Query


# create a book
def createBook(data: BookCreate, db: Session = getDb()):
    try:
        book = createBookDb(data, db)
        if book is None:
            raise HTTPException(status_code=400, detail="Failed to create book")
        return { "status": 201, "message": "Book created successfully" }
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
    


    # get a single book

def get_book(id: str, db: Session = getDb()):
    try:
       
        db_book = get_bookDb(id, db)
       
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        book_response = BookResponse.model_validate(db_book)
        
        return book_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# update book

def update_book(data: BookUpdate, id:str,db: Session =getDb()):
    try:
        book = updateBookDb(data,id,  db)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        return {"status": 201, "message": "Book updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# delete book

def delete_book(id=str, db: Session= getDb()):
    try:
        result = deleteBookDb(id, db)
        return {"message": "Book deleted successfully", "book": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# GET all book list

def get_all_books(
   
    offset: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(10, le=100, description="Pagination limit"),
    db: Session = getDb()
):
    try:
        print(1)
        books_data = get_all_bookDB(db, offset=offset, limit=limit)
        print(2)
        return {"message": "Books list", "book": books_data}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


