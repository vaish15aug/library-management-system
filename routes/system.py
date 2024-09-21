from fastapi import APIRouter
from schema.system import CheckoutRequest, CheckoutResponse
from services.system import checkout_bookDb,return_book_db,manage_fineDb, get_all_systemDb
from controller.system import checkout_book, return_book, manage_fines, get_all_systems


systemRouter = APIRouter(prefix="/system")

@systemRouter.post("/checkout")
def create(create:CheckoutResponse):
    return checkout_book(create)

@systemRouter.put("/returns")
def give(give:CheckoutRequest):
    return return_book(give)

@systemRouter.post("/fine-manage")
def fine(fine:CheckoutResponse):
    return manage_fines(fine)

# @systemRouter.get("/get_one/{id}")
# def get(id:str):
#     return get_all_systems(id)

@systemRouter.get("/find_all")
def getA(offset: int = 0, limit: int = 10):
    print(0)
    return get_all_systems(offset=offset, limit=limit)


