from fastapi import FastAPI, HTTPException
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    rating = Column(Integer)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Book", back_populates="reviews")


Book.reviews = relationship("Review", back_populates="book")


class BookReviewAPI:
    def __init__(self):

        DATABASE_URL = "postgresql://atsd:testposgre@localhost:5432/testdb"
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

        self.app = FastAPI()

        @self.app.post("/books/")
        def create_book(title: str, author: str, publication_year: int):
            db = self.SessionLocal()
            book = Book(title=title, author=author, publication_year=publication_year)
            db.add(book)
            db.commit()
            db.refresh(book)
            return book

        @self.app.get("/books/{book_id}/")
        def read_book(book_id: int):
            db = self.SessionLocal()
            book = db.query(Book).filter(Book.id == book_id).first()
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            return book

        @self.app.put("/books/{book_id}/")
        def update_book(book_id: int, title: str, author: str, publication_year: int):
            db = self.SessionLocal()
            book = db.query(Book).filter(Book.id == book_id).first()
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            book.title = title
            book.author = author
            book.publication_year = publication_year
            db.commit()
            return book

        @self.app.delete("/books/{book_id}/")
        def delete_book(book_id: int):
            db = self.SessionLocal()
            book = db.query(Book).filter(Book.id == book_id).first()
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            db.delete(book)
            db.commit()
            return {"message": "Book deleted successfully"}

        @self.app.post("/books/{book_id}/reviews/")
        def create_review(book_id: int, text: str, rating: int):
            db = self.SessionLocal()
            review = Review(text=text, rating=rating, book_id=book_id)
            db.add(review)
            db.commit()
            db.refresh(review)
            return review

        @self.app.get("/books/{book_id}/reviews/")
        def read_reviews(book_id: int):
            db = self.SessionLocal()
            reviews = db.query(Review).filter(Review.book_id == book_id).all()
            if not reviews:
                raise HTTPException(status_code=404, detail="No reviews found for this book")
            return reviews

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=4200)


if __name__ == "__main__":
    api = BookReviewAPI()
    api.run()
