from fastapi import HTTPException
from sqlalchemy.orm import Session
from schema.system import CheckoutRequest, CheckoutResponse, ReturnRequest, ManageFineRequest
from models.book import Book
from database import getDb
from fastapi import Query
from services.system import checkout_bookDb, return_book_db, manage_fineDb,get_all_systemDb
from models.user import User

#  checkout book
def checkout_book(data: CheckoutRequest, db: Session = getDb()):
    try:
        print(0)
        checkout_record = checkout_bookDb(
            user_id=data.user_id,
            book_id=data.book_id,
            db=db
        )
        print(1)
        return {"message": "Book successfully checked out", "checkout": checkout_record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   


# return book
def return_book(data:ReturnRequest, db: Session = getDb()):
    try:
        result = return_book_db(data, db)
        return {"message": "Book successfully returned", "return": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  



#  fine management
def manage_fines(data: ManageFineRequest, db: Session = getDb()):
    try:
        fine_records = manage_fineDb(
            book_id=data.book_id,
            fine=data.fine,
            db=db
        )
        fine_record_dicts = [record.__dict__ for record in fine_records]
        for record in fine_record_dicts:
          
            record.pop('_sa_instance_state', None)

        return {"message": "Fine managed successfully", "fine_record": fine_record_dicts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


def get_all_systems(
    offset: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(10, le=100, description="Pagination limit"),
    db: Session = getDb()
):
    try:
        print(1)
        system_data = get_all_systemDb(db, offset=offset, limit=limit)
        print(2)
        return {"message": "System list", "book": system_data}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))