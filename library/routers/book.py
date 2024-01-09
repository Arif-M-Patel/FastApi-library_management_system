from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from library import models, schemas
from library.repository import book
from library import database
from library import oauth2


router = APIRouter(
    prefix="/book",
    tags=['Books']
)

get_db = database.get_db

@router.post('/', response_model=schemas.ShowBook, status_code=status.HTTP_201_CREATED)
def create_book(request: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return book.create_book(request=request, db=db, current_user=current_user)

@router.get('/{id}', response_model=schemas.ShowBook, status_code=200,)
def get_book(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return book.show_book(id, db=db, current_user=current_user)

@router.get('/', response_model=List[schemas.ShowBook])
def get_all_books(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return book.get_all_books( db=db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_book(id: int, request: schemas.Book, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return book.update_book(id, request=request, db=db, current_user=current_user)

@router.delete('/{id}')
def delete_book(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return book.destroy_book(id, db=db, current_user=current_user)