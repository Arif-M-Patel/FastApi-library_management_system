from fastapi import FastAPI, Depends, HTTPException
from library import  models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from library.database import engine, SessionLocal
from library.routers import authentication, book, user,  search, author  ,borrowing


app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(authentication.router)
app.include_router(book.router)
app.include_router(author.router)
app.include_router(user.router)
app.include_router(borrowing.router)
app.include_router(search.router)

