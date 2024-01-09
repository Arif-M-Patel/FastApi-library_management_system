from sqlalchemy.orm import Session
from library import models, schemas
from fastapi import HTTPException, status
from library.hashing import Hash  

def get_all_users(db: Session):
    users = db.query(models.User).all()
    return users

def create_user(request: schemas.User, db: Session):
    hashed_password = Hash.bcrypt(request.password)
    
    new_user = models.User(name=request.name, email=request.email, password=hashed_password, phone_number=request.phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show_user(id: int, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return new_user

def update_user(id: int, request: schemas.User, db: Session, current_user: schemas.User):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} not found")
    user.name = request.name
    user.email = request.email
    hashed_password = Hash.bcrypt(request.password)
    user.password = hashed_password
    user.phone_number = request.phone_number
    
    db.commit()
    db.refresh(user)
    return {"message": f"User with id {id} updated successfully!" , "author": user}
  

def destroy_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User with id {id} deleted successfully"}