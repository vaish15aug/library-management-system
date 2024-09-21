from sqlalchemy.orm import Session
from models.book import Book
from models.system import System
from datetime import date, timedelta,datetime
from models.user import User
from schema.system import CheckoutRequest, CheckoutResponse, ReturnRequest


#  checkout service
def checkout_bookDb(book_id: str, user_id: str, db: Session):
    try:
        
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise Exception("Book not found")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("User not found")

        if not book.is_available:
            raise Exception("Book is already checked out")
        
       
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
def return_book_db(data: ReturnRequest, db: Session):
    try:
       
        system_entry = db.query(System).filter(System.id == data.id).first()

        if not system_entry:
            raise Exception("Checkout record not found")

        if system_entry.is_returned:
            raise Exception("Book already returned")

        return_date = datetime.now()
        system_entry.due_date = return_date
        system_entry.is_returned = True

        
        if system_entry.due_date is not None and return_date > system_entry.due_date:
            days_late = (return_date - system_entry.due_date).days
            system_entry.fine = days_late * 5
        else:
            system_entry.fine = 0  

        book = db.query(Book).filter(Book.id == system_entry.book_id).first()
        book.is_available = True

        db.commit()
        db.refresh(system_entry)
        return system_entry
    except Exception as e:
        
        db.rollback()
        print(e)
        raise Exception("Failed to return book")


 # fine management

def manage_fineDb(book_id: int, fine: str, db: Session):
    try:
        if not isinstance(book_id, int):
            raise ValueError("book_id must be an integer")
        
        if not isinstance(fine, str):
            raise ValueError("fine_amount must be a string")

        fine_records = db.query(System).filter(System.book_id == book_id).all()
        
        if not fine_records:
            raise Exception("No fine records found for the given book_id")

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

# def get_all_systemDb(db: Session, offset: int = 0, limit: int = 10):
#     try:
#         print(1)
#         records_query = db.query(System).offset(offset).limit(limit)
#         records = records_query.all()
#         print(2)
#         count = db.query(System).count()
#         print(3)
#         records_dict = [record.as_dict() for record in records] 
#         print(4)
#         return {"count": count, "rows": records_dict}
#     except Exception as e:
#         print(e)
#         raise Exception("Failed to retrieve system records")

def get_all_systemDb(db: Session, offset: int = 0, limit: int = 10):
    try:
        print(1)
        system_query = db.query(System).all()
        print(2)
        systems = system_query
        print(3)
       
        count = db.query(System).count()
        print(4)
        return {"count": count, "rows": systems}
        
    except Exception as e:
        print(e)
        raise Exception("Failed to find system list")