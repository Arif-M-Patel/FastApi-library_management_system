from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from library import models, schemas
from library.repository import author
from library.database import get_db
from library import oauth2

router = APIRouter(
    prefix="/author",
    tags=['Authors']
)

get_db = get_db

@router.post('/', response_model=schemas.ShowAuthor, status_code=status.HTTP_201_CREATED)
def create_author(request: schemas.AuthorCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return author.create_author(request=request, db=db, current_user=current_user)

@router.get('/{id}', response_model=schemas.Author, status_code=200)
def get_author(id: int, db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return author.get_author(id,db=db, current_user=current_user)

@router.get('/', response_model=List[schemas.Author])
def get_all_authors(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return author.get_all_authors(db=db)

@router.put('/{id}',  status_code=status.HTTP_202_ACCEPTED)
def update_author(id: int, request: schemas.ShowAuthor, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return author.update_author(id,request=request, db=db, current_user=current_user)

@router.delete('/{id}')
def delete_author(id: int,  db: Session = Depends(get_db),  current_user: schemas.User = Depends(oauth2.get_current_user)):
    return author.delete_author(id, db=db, current_user=current_user)
