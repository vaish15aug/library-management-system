from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from schema.system import CheckoutRequest, CheckoutResponse, ReturnRequest, ManageFineRequest
from models.book import Book
from database import getDb
from fastapi import Query
from services.system import checkout_bookDb, return_book_db, manage_fineDb, get_all_systemDb
from models.user import User
from helpers.jwtToken import verifyToken
from typing import Dict

#  checkout book
def checkout_book(data: CheckoutRequest, payload: Dict= Depends(verifyToken) ):
    try:
        print("payload", payload)
        if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
        checkout_record = checkout_bookDb(
            user_id=data.user_id,
            book_id=data.book_id,
            
        )
        return {"message": "Book successfully checked out", "checkout": checkout_record}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   


# return book
def return_book(data:ReturnRequest, payload:Dict= Depends(verifyToken)):
    try:
        print("payload",payload)
        result = return_book_db(data)
        if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
        return {"message": "Book successfully returned", "return": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  



#  fine management
def manage_fines(data: ManageFineRequest, payload:Dict= Depends(verifyToken)):
    try:
        print("payload",payload)
        if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
        fine_records = manage_fineDb(
            book_id=data.book_id,
            fine=data.fine,
            
        )
        fine_record_dicts = [record.__dict__ for record in fine_records]
        for record in fine_record_dicts:
          
            record.pop('_sa_instance_state', None)

        return {"message": "Fine managed successfully", "fine_record": fine_record_dicts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# get all system list
def get_all_systems(
    payload : Dict= Depends(verifyToken),
    offset : int = Query(0, ge=0, description="Pagination offset"),
    limit : int = Query(10, le=100, description="Pagination limit")
    
):
    try:
        print("payload",payload)
        if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
        system_data = get_all_systemDb( offset=offset, limit=limit)
        return {"message": "System list", "book": system_data}
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))