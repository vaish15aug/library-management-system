from sqlalchemy.orm import Session
from models.book import Book
from models.system import System
from datetime import date, timedelta,datetime
from models.user import User
from schema.system import CheckoutRequest, CheckoutResponse, ReturnRequest
from database import getDb
db:Session = getDb()

#  checkout service
# def checkout_bookDb(book_id: str, user_id: str):
#     try:
#         # Check if the book exists and is available
#         book = db.query(Book).filter(Book.id == book_id).first()
#         if not book:
#             return {"status": "error", "error": "Book not found"}
       
        
#         if not book.is_available:
#             return {"status": "error", "error": "Book is already checked out"}

#         # Check if the user exists
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             return {"status": "error", "error": "User not found"}

#         # Process checkout if all conditions are met
#         checkout_date = datetime.now()
#         due_date = checkout_date + timedelta(days=15)
#         fine = 0

#         system = System(
#             user_id=user_id,
#             book_id=book_id,
#             checkout_date=checkout_date,
#             due_date=due_date,
#             fine=str(fine),
#             is_returned=False
#         )
#         book.is_available = False
#         db.add(system)
#         db.commit()
#         db.refresh(system)
#         return {"status": "success", "data": system}
    
#     except Exception as e:
#         db.rollback()
#         print(e)
#         raise Exception("Failed to create checkout record")


def checkout_bookDb(book_id: str, user_id: str):
    try:
        
        # Check if the book exists and is available
        book = db.query(Book).filter(Book.id == book_id).first()
        # if not book:
        #     return {"status": "error", "error": "Book not found"}
       
        # if not book.is_available:
        #     return {"status": "error", "error": "Book is already checked out"}

        # # Check if the user exists
        user = db.query(User).filter(User.id == user_id).first()
        # if not user:
        #     return {"status": "error", "error": "User not found"}
      

        checkout_records = db.query(System).filter(System.book_id == book_id, System.user_id == user_id, System.is_returned == False).all()
        if len(checkout_records) > 0:
            return {"status": "error", "error": "Book is already checked out"}

        if book is None:
            return {"status": "error", "error": "Book not found"}
        
        if user is None:
            return {"status": "error", "error": "User not found"}


        # Process checkout if all conditions are met
        checkout_date = datetime.now()
        due_date = checkout_date + timedelta(days=15)
        fine = 0

        system = System(
            user_id=user_id,
            book_id=book_id,
            checkout_date=checkout_date,
            due_date=due_date,
            fine=str(fine),
            is_returned=False
        )
        book.is_available = False
        db.add(system)
        db.commit()
        db.refresh(system)
        return system
    
    except Exception as e:
        db.rollback()
        print(e)
        raise Exception("Failed to create checkout record")



# return book


def return_book_db(data: ReturnRequest):
    try:
        # Use `data.id` to fetch the checkout record from the database
        system_entry = db.query(System).filter(System.id == data.id).first()
        
        # Check if the checkout record exists
        if not system_entry:
            raise Exception("Checkout record not found")

        # Check if the book is already returned
        if system_entry.is_returned:
            raise Exception("Book already returned")
        
        
        # Process the return
        return_date = datetime.now()
        system_entry.is_returned = True

        if system_entry.due_date is not None and return_date > system_entry.due_date:
            days_late = (return_date - system_entry.due_date).days
            system_entry.fine = days_late * 5
        else:
            system_entry.fine = 0  

        # Set the book as available
        book = db.query(Book).filter(Book.id == system_entry.book_id).first()
        book.is_available = True

        db.commit()
        db.refresh(system_entry)
        return system_entry
    except Exception as e:
        db.rollback()
        print(e)
        raise Exception(str(e))

 # fine management

def manage_fineDb(book_id: int, user_id: int, fine: str):
    try:
       

        fine_records = db.query(System).filter(System.book_id == book_id, System.user_id == user_id).all()
        
        if not isinstance(book_id, int):
            raise ValueError("book_id must be an integer")
        
        if not isinstance(user_id, int):
            raise ValueError("user_id must be an integer")

        if not isinstance(fine, str):
            raise ValueError("fine must be a string")

        for record in fine_records:
            record.fine = fine
            record.updated_at = datetime.now()  
            
            record.due_date = record.due_date or datetime.now().date()  
            record.checkout_date = record.checkout_date or datetime.now().date()
            record.is_returned = record.is_returned if record.is_returned is not None else False

        db.commit()
    
        for record in fine_records:
            db.refresh(record)
        
        return fine_records

    except Exception as e:
        db.rollback()
        print(e)
        raise Exception("Failed to manage fine")
    

#  get all
def get_all_systemDb( offset: int = 0, limit: int = 10):
    try:
       
        system_query = db.query(System).all()
       
        systems = system_query
     
       
        count = db.query(System).count()
       
        return {"count": count, "rows": systems}
        
    except Exception as e:
        print(e)
        raise Exception("Failed to find system list")