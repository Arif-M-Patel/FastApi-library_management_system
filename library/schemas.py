from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Type
from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from library.models import  User, Book, Author ,Borrowing

# Bse MOdels
class BookBase(BaseModel):
    title: str
    author: str
    author_id: int
    description: str

class AuthorBase(BaseModel):
    name: str
    biography: str
    nationality: str

class UserBase(BaseModel):
    # id : int
    name: str
    password: str
    email: str
    phone_number: str

class BorrowingBase(BaseModel):
    user_id: int
    book_id: int
    borrowed_date: Optional[date]
    due_date: Optional[date]
    returned_date: Optional[date]
    # user: str = "User"  
    # book: str = "Book"  

# Create Models

class BookCreate(BookBase):
    pass

class AuthorCreate(AuthorBase):
    pass

class UserCreate(UserBase):
    pass

class BorrowingCreate(BorrowingBase):
    pass

# Models with ids
class Book(BookBase):
    # id: int
    # borrowings: List[Borrowing] = []

    class Config:
        orm_mode = True





class User(UserBase):
    # id: int
    # name: str
    # email: str
    # phone_number: str
    #borrowed_books: List["Borrowing"]    #when we add here then it creates circular loop

    class Config:
        orm_mode = True


class Borrowing(BorrowingBase):
    # id: int
    # user: str = "User"  
    # book: str = "Book"
    # id: int
    user_id: int
    book_id: int
    borrowed_date: Optional[date]
    due_date: Optional[date]
    returned_date: Optional[date]
    # user: Optional[User] = None
    # book: Optional[Book] = None

    class Config:
        orm_mode = True

# Show Models
class ShowBorrowing(BaseModel):
    # id : int
    # user: Optional[ShowUser] = None
    # book: Optional[ShowBook] = None
    user_id: int
    book_id: int
    borrowed_date: Optional[date]
    due_date: Optional[date]
    returned_date: Optional[date]
    # name: str  
    # title: str  

    class Config:
        orm_mode = True

class ShowBook(BaseModel):
    id : int
    title: str
    author: str
    description: str
    # borrowings: List[ShowBorrowing] = []

    class Config:
        orm_mode = True

#class Autor it is defined here for pydantic error
class Author(AuthorBase):
    id: int
    # books: List[ShowBook] = []

    class Config:
        orm_mode = True

class ShowAuthor(BaseModel):
    # id : int
    name: str
    biography: str
    nationality: str
    # books: List[ShowBook] = []

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    id : int
    name: str
    email: str
    phone_number: str
    # borrowed_books: List[str]

    class Config:
        orm_mode = True




# utilisty models----------
class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
