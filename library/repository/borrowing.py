from sqlalchemy.orm import Session
from library import models, schemas
from fastapi import HTTPException, status

def create_borrowing(request: schemas.ShowBorrowing, db: Session,  current_user: schemas.User):
    db_borrowing = models.Borrowing(user_id=request.user_id, book_id=request.book_id, borrowed_date=request.borrowed_date, due_date=request.due_date,
        returned_date=request.returned_date)
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing


def get_all_borrowings(db: Session, current_user: schemas.User):
    return db.query(models.Borrowing).all()

def get_borrowing(id: int, db: Session,  current_user: schemas.User):
    db_borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == id).first()
    if not db_borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Borrowing with the id {id} is not available")
    return db_borrowing



def update_borrowing(id: int,request: schemas.BorrowingCreate, db: Session,current_user: schemas.User):
    db_borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == id).first()
    if not db_borrowing :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Borrowing with id {id} not found")

    # db_borrowing.update(request.dict())
    # Update the fields based on the request
    db_borrowing.user_id = request.user_id
    db_borrowing.book_id = request.book_id
    db_borrowing.borrowed_date = request.borrowed_date
    db_borrowing.due_date = request.due_date
    db_borrowing.returned_date = request.returned_date
    db.commit()
    return {"message": f"Borrowing with id {id} updated successfully", "borrowing": db_borrowing}




def delete_borrowing(id: int, db: Session, current_user: schemas.User):
    db_borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == id).first()
    if not db_borrowing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Borrowing with id {id} not found")


    db.delete(db_borrowing)
    db.commit()
    return {"message": f"Borrowing with id {id} deleted successfully"}



