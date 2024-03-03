from fastapi.testclient import TestClient
from main import BookReviewAPI

client = TestClient(BookReviewAPI().app)


def test_create_review():
    response = client.post("/books/1/reviews/", json={"text": "Test review", "rating": 5})
    assert response.status_code == 201
    assert response.json()["text"] == "Test review"
    assert response.json()["rating"] == 5


def test_read_reviews():
    response = client.get("/books/1/reviews/")
    assert response.status_code == 200
    assert len(response.json()) > 0


if __name__ == "__main__":
    test_create_review()
    test_read_reviews()
