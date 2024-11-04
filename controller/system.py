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
# def checkout_book(data: CheckoutRequest, payload: Dict= Depends(verifyToken) ):
#     try:
#         print("payload", payload)
#         if not payload.get("is_super"):
#             raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
#         checkout_record = checkout_bookDb(
#             user_id=data.user_id,
#             book_id=data.book_id,
            
#         )
#         return {"message": "Book successfully checked out", "checkout": checkout_record}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))   



# def checkout_book(data: CheckoutRequest, payload: dict):
#     try:
#         if not payload.get("is_super"):
#             raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
        
#         # Call the service function
#         result = checkout_bookDb(
#             user_id=data["user_id"],
#             book_id=data["book_id"]
#         )
        
#         # Check for specific error messages
#         if result["status"] == "error":
#             error_message = result["error"]
#             if error_message == "Book not found":
#                 raise HTTPException(status_code=404, detail="Book not found")
            
#             if error_message == "User not found":
#                 raise HTTPException(status_code=404, detail="User not found")
            
#             if error_message == "Book is already checked out":
#                 raise HTTPException(status_code=400, detail="Book is already checked out")
           
#         # Return success response if no errors
#         return {"status": 201, "message": "Book successfully checked out", "checkout": result["data"]}
    
#     except HTTPException as e:
#         raise e
#     except Exception:
#         raise HTTPException(status_code=500, detail=str(e))

def checkout_book(data: CheckoutRequest, payload: dict):
    try:
        if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to checkout a book")
        
        # Call the service function
        result = checkout_bookDb(
            user_id=data["user_id"],
            book_id=data["book_id"]
        )
        
        # Check for specific error messages
        if result["status"] == "error":
            error_message = result["error"]
            if error_message == "Book not found":
                raise HTTPException(status_code=404, detail="Book not found")
            
            elif error_message == "User not found":
                raise HTTPException(status_code=400, detail="User not found")
            
            elif error_message == "Book is already checked out":
                raise HTTPException(status_code=400, detail="Book is already checked out")

        # Return success response if no errors
        return {"status": 201, "message": "Book successfully checked out", "checkout": result["data"]}
    
    except HTTPException as http_ex:
        raise http_ex 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# return book
      
def return_book(data: dict, payload: dict):
    if not payload.get("is_super"):
        raise HTTPException(status_code=403, detail="You are not authorized to return a book")
    
    try:
        return_request = ReturnRequest(**data)  
        result = return_book_db(return_request) 

        return {"status": 201, "message": "Book successfully returned", "return": result} 
    
    except Exception as e:
        error_message = str(e)
        if error_message == "Checkout record not found":
            raise HTTPException(status_code=404, detail="Checkout record not found")
        elif error_message == "Book already returned":
            raise HTTPException(status_code=404, detail="Book already returned")
        else:
            raise HTTPException(status_code=500, detail="Failed to return book")



#  fine management

def manage_fines(data:dict, payload: dict):
    if not payload.get("is_super"):
            raise HTTPException(status_code=403, detail="You are not authorized to manage fine")
   
    try:
        # print("payload", payload)
         # Validate `book_id`
        if not isinstance(data.get("book_id"), int):
            raise HTTPException(status_code=422, detail="book_id must be an integer")
        
        # Validate `user_id`
        if not isinstance(data.get("user_id"), int):
            raise HTTPException(status_code=422, detail="user_id must be an integer")
        
        # Validate `fine`
        if not isinstance(data.get("fine"), str):
            raise HTTPException(status_code=400, detail="fine must be a string")
        
        # Check if user is authorized
        
        fine_records = manage_fineDb(
            book_id=data.book_id,
            user_id=data.user_id,
            fine=data.fine,
        )
      
        fine_record_dicts = [record.__dict__ for record in fine_records]
        
        for record in fine_record_dicts:
            record.pop('_sa_instance_state', None)
        
        return {"status": 201, "message": "Fine managed successfully", "fine_record": fine_record_dicts}

    except HTTPException as http_ex:
        raise http_ex 
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
            raise HTTPException(status_code=403, detail="You are not authorized to get system list")
        system_data = get_all_systemDb( offset=offset, limit=limit)
        return {"status": 201, "message": "System list", "book": system_data}
   
    except HTTPException as http_ex:
        raise http_ex    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))