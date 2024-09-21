from sqlalchemy.orm import Session
from models.book import Book
from schema.book import BookCreate, BookUpdate


# create book
def createBookDb(data: BookCreate, db: Session):
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

def get_bookDb(id: str, db: Session):
    try:
       
        book = db.query(Book).filter(Book.id == id).first()
      
        if book is None:
            raise Exception("Book not found")
      
        return book
    except Exception as e:
        print(e)
        raise Exception("Failed to find book")

    
#  get all book

def get_all_bookDB(db: Session, offset: int = 0, limit: int = 10):
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
def updateBookDb(id:str,data: BookUpdate, db: Session):
    try:
       
        # if not data.id:
        #     raise ValueError("Book ID must be provided for update")
       
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

def deleteBookDb(id: str, db: Session):
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


