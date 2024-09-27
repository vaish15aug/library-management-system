from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.book import BookCreate, BookUpdate
from controller.book import createBook, get_book, update_book, delete_book, get_all_books
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

