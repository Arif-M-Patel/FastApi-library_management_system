from sqlalchemy.orm import joinedload
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from library.database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False) #, nullable=False

    author_info = relationship("Author", back_populates="books")
    borrowings = relationship("Borrowing", back_populates="book")

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    biography = Column(String)
    nationality = Column(String)

    books = relationship("Book", back_populates="author_info")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, index=True)
    phone_number = Column(String)

    borrowed_books = relationship('Borrowing', back_populates="user")

class Borrowing(Base):
    __tablename__ = 'borrowings'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrowed_date = Column(Date, default=datetime.now)
    due_date = Column(Date)
    returned_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowings")

  