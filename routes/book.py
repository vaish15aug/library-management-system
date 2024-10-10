from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.book import BookCreate, BookUpdate, BookResponse
from controller.book import createBook, get_book, update_book, delete_book, get_all_books,search_books
from fastapi import Query
from helpers.jwtToken import verifyToken
from middleware import auth
from typing import Dict



bookRouter = APIRouter(prefix="/books")

@bookRouter.post("/create")
def create(create: BookCreate, payload:Dict = Depends(verifyToken)):
    return createBook(create, payload)

@bookRouter.get("/fetch_one/{id}")
def findBook( id:str,payload:Dict = Depends(verifyToken)):
    return get_book(id, payload)

@bookRouter.put("/update/{id}")
def update(id:str,update:BookUpdate,payload:Dict = Depends(verifyToken)):
    return update_book(id,update, payload)

@bookRouter.delete("/delete/{id}")
def delete(payload:Dict = Depends(verifyToken)):
    return delete_book(payload)

@bookRouter.get("/fetch_all")
def getA(offset: int = 0, limit: int = 10, payload:Dict = Depends(verifyToken)):
    return get_all_books(payload=payload,offset=offset, limit=limit)


@bookRouter.get("/search")
def search_books_route(
    # book_name: str = None,
    # author: str = None,
    category: str = None,
    is_available: bool = None,
    search_param: str = None,
    payload: Dict = Depends(verifyToken)
):
    return search_books(search_param = search_param, category = category, is_available = is_available, payload = payload)


