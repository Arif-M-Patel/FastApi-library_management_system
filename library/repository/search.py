from sqlalchemy.orm import Session
from sqlalchemy import or_
from library import models, schemas
from fastapi import HTTPException, status

def search_books(db: Session, title: str = None, author: str = None):
    # Check if both title and author are None
    if title is None and author is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide at least one search criteria (title or author)")

    # Initialize the query with the Book model
    query = db.query(models.Book)

    # If title parameter is provided, filter by title
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    # If author parameter is provided, join with Author model and filter by author name
    if author:
        query = query.join(models.Author).filter(models.Author.name.ilike(f"%{author}%"))

    # Retrieve the results of the query
    results = query.all()

    # Check if results are empty, and raise an exception if no books are found
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found matching the criteria")

    # Return the results
    return results
