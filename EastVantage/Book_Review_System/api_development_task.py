import typing
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()


class Book:
    def __init__(self, title: str, author: str, publication_year: int):
        self.title = title
        self.author = author
        self.publication_year = publication_year


class Review:
    def __init__(self, text: str, rating: int):
        self.text = text
        self.rating = rating


books_db = []
reviews_db = {}


@app.post("/books/")
def add_book(title: str, author: str, publication_year: int):
    book = Book(title=title, author=author, publication_year=publication_year)
    books_db.append(book)
    return {"message": "Book added successfully"}


@app.post("/books/{book_id}/reviews/")
def submit_review(book_id: int, text: str, rating: int):
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    review = Review(text=text, rating=rating)
    if book_id not in reviews_db:
        reviews_db[book_id] = []
    reviews_db[book_id].append(review)
    return {"message": "Review submitted successfully"}


@app.get("/books/")
def get_books(author: typing.Optional[str] = None, publication_year: typing.Optional[int] = None):
    filtered_books = books_db
    if author:
        filtered_books = [book for book in filtered_books if book.author == author]
    if publication_year:
        filtered_books = [book for book in filtered_books if book.publication_year == publication_year]
    return filtered_books


@app.get("/books/{book_id}/reviews/")
def get_reviews(book_id: int):
    if book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    if book_id not in reviews_db:
        return {"message": "No reviews found for this book"}
    return reviews_db[book_id]


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


def main():
    uvicorn.run(app, host="0.0.0.0", port=4200)


if __name__ == "__main__":
    main()
