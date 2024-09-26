from fastapi import APIRouter, Depends
from schema.system import CheckoutRequest, CheckoutResponse
from services.system import checkout_bookDb,return_book_db,manage_fineDb, get_all_systemDb
from controller.system import checkout_book, return_book, manage_fines, get_all_systems
from helpers.jwtToken import verifyToken
from middleware import auth
from typing import Dict


systemRouter = APIRouter(prefix="/system")

@systemRouter.post("/checkout")
def create(create:CheckoutResponse, payload:Dict = Depends(verifyToken)):
    return checkout_book(create, payload)

@systemRouter.put("/returns")
def give(give:CheckoutRequest, payload:Dict = Depends(verifyToken)):
    return return_book(give,payload)

@systemRouter.post("/fine-manage")
def fine(fine:CheckoutResponse, payload:Dict = Depends(verifyToken)):
    return manage_fines(fine, payload)


@systemRouter.get("/find_all")
def getA(offset: int = 0, limit: int = 10, payload:Dict = Depends(verifyToken)):
    return get_all_systems(offset=offset, limit=limit, payload=payload)




