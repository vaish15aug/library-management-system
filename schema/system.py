from pydantic import BaseModel
from datetime import date

class CheckoutRequest(BaseModel):
    id:int
    user_id: int
    book_id: int
    checkout_date: date
    due_date: date
    is_returned: bool
    fine:str

class CheckoutResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    checkout_date: date
    due_date: date
    is_returned: bool
    fine:str

class ReturnRequest(BaseModel):
    id: int


class ManageFineRequest(BaseModel):
    book_id: int
    fine: str
 
    