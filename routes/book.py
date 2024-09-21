from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.book import BookCreate, BookUpdate
from controller.book import createBook, get_book, update_book, delete_book, get_all_books
from fastapi import Query



bookRouter = APIRouter(prefix="/books")

@bookRouter.post("/create")
def create(create: BookCreate):
    return createBook(create)

@bookRouter.get("/fetch_one/{id}")
def findBook(id: str):
    return get_book(id)

@bookRouter.put("/update/{id}")
def update(id:str,update:BookUpdate):
    return update_book(id,update)

@bookRouter.delete("/delete/{id}")
def delete(id:str):
    return delete_book(id)

@bookRouter.get("/fetch_all")
def getA(offset: int = 0, limit: int = 10):
    print(0)
    return get_all_books(offset=offset, limit=limit)
