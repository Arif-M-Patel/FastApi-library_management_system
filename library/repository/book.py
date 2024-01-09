from sqlalchemy.orm import Session
from library import models, schemas
from fastapi import HTTPException, status


def get_all_books(db: Session):
    books = db.query(models.Book).all()
    return books


def create_book(request: schemas.Book, db: Session, current_user: schemas.User):
    # Check if author_id is provided
    if request.author_id is not None:
        # Check if the author with the provided author_id exists
        author = db.query(models.Author).filter(models.Author.id == request.author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail=f"Author not found with id: {request.author_id}")

    new_book = models.Book(
        title=request.title,
        author=request.author,
        description=request.description,
        author_id=request.author_id
    )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return new_book



def destroy_book(id: int, db: Session, current_user: schemas.User):
    # Check if the book with the provided ID exists
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found")


    # Delete the book
    db.delete(book)
    db.commit()
    return {"message": f"Book with id {id} deleted successfully"}


def update_book(id: int, request: schemas.BookCreate, db: Session , current_user: schemas.User):
    book = db.query(models.Book).filter(models.Book.id == id)

    if not book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {id} not found")

    book.update(request.dict())
    db.commit()
    return {"message": f"Book with id {id} updated successfully", "author": book}


def show_book(id: int, db: Session , current_user: schemas.User):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with the id {id} is not available")
    return book
