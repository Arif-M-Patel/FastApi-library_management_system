from sqlalchemy.orm import Session
from library import models, schemas
from fastapi import HTTPException, status

def create_author(request: schemas.Author, db: Session,   current_user: schemas.User ):
    new_author = models.Author(name=request.name, biography=request.biography, nationality=request.nationality)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def get_all_authors(db: Session):
    return db.query(models.Author).all()

def get_author(id: int, db: Session,  current_user: schemas.User):
    db_author = db.query(models.Author).filter(models.Author.id == id).first()
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with the id {id} is not available")
    return db_author

def update_author( id: int, request: schemas.AuthorCreate, db: Session, current_user: schemas.User):
    db_author = db.query(models.Author).filter(models.Author.id == id)
    
    if not db_author.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {id} not found")

    db_author.update(request.dict())
    db.commit()
    return {"message": f"Author with id {id} updated successfully", "author": db_author}



def delete_author(id: int, db: Session, current_user: schemas.User):
    # Check if the book with the provided ID exists
    db_author = db.query(models.Author).filter(models.Author.id == id).first()
    if not db_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with id {id} not found")


    # Delete the book
    db.delete(db_author)
    db.commit()
    return {"message": f"Author with id {id} deleted successfully"}