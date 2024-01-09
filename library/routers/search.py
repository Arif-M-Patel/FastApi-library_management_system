# routers/search.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from library import database, schemas, repository, oauth2
from library.repository import search

router = APIRouter(prefix="/search", tags=['Search'])

get_db = database.get_db

@router.get('/books/', response_model=List[schemas.Book])
def search_books(
    title: str = None,
    author: str = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return repository.search.search_books(db, title=title, author=author)

