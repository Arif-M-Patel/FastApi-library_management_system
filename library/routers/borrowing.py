from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from library import database, schemas, models
from library.repository import borrowing
from library import database
from library import oauth2
from datetime import datetime 


router = APIRouter(
    prefix="/borrowing",
    tags=['Borrowings']
)

get_db = database.get_db

@router.post('/check_out', response_model=schemas.ShowBorrowing)
def check_out_book(request: schemas.BorrowingCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Validate user existence
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate book existence
    book = db.query(models.Book).filter(models.Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    current_date = datetime.now().date()
    if request.due_date and request.due_date <= current_date:
        raise HTTPException(status_code=400, detail="Due date must be in the future")

    # Ensure the user has not already borrowed the same book
    existing_borrowing = (
        db.query(models.Borrowing)
        .filter(models.Borrowing.user_id == request.user_id, models.Borrowing.book_id == request.book_id)
        .first()
    )
    if existing_borrowing:
        raise HTTPException(status_code=400, detail="User has already borrowed the same book")

    # Create a new borrowing entry
    db_borrowing = models.Borrowing(**request.dict())
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)

    return db_borrowing

@router.get('/users_with_borrowings', response_model=list[schemas.ShowUser])
def get_users_with_borrowings(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Query users with associated borrowings
    users_with_borrowings = (
        db.query(models.User)
        .join(models.Borrowing, models.User.id == models.Borrowing.user_id)
        .distinct()
        .all()
    )

    return users_with_borrowings


@router.get('/{id}', response_model=schemas.ShowBorrowing, status_code=200)
def get_borrowing(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return borrowing.get_borrowing(id, db=db, current_user=current_user)

@router.get('/', response_model=List[schemas.Borrowing])
def get_all_borrowings(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return borrowing.get_all_borrowings(db, current_user)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_borrowing(id: int, request: schemas.ShowBorrowing, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate book existence
    book = db.query(models.Book).filter(models.Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Validate date logic 
    current_date = datetime.now().date()
    if request.due_date and request.due_date <= current_date:
        raise HTTPException(status_code=400, detail="Due date must be in the future")

    # Ensure the user has not already borrowed the same book
    existing_borrowing = (
        db.query(models.Borrowing)
        .filter(models.Borrowing.user_id == request.user_id, models.Borrowing.book_id == request.book_id)
        .first()
    )
    if existing_borrowing:
        raise HTTPException(status_code=400, detail="User has already borrowed the same book")
    return borrowing.update_borrowing(id, request=request, db=db, current_user=current_user)


@router.delete('/{id}')
def delete_borrowing(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return borrowing.delete_borrowing(id, db=db, current_user=current_user)











