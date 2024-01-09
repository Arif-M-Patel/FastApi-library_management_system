# library/routers.py
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from library import schemas, database, oauth2, models
from sqlalchemy.orm import Session
from library.repository import user
from library.database import get_db


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create_user(request=request, db=db)

@router.get('/{id}', response_model=schemas.ShowUser, status_code= 200)
def get_user(id=int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.show_user(id, db=db, current_user=current_user)

@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_all_users(db = db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED )
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.update_user(id, request=request, db=db, current_user=current_user)


