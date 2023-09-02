import pytest
from app import app, db, Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Create a context for the database
    with app.app_context():
        db.create_all()
    
    yield client

    # Clean up the database after the test
    with app.app_context():
        db.drop_all()
        
def test_add_book(client):
    # Test adding a new book
    response = client.post('/books', json={'title': 'Test Book', 'author': 'Test Author'})
    assert response.status_code == 200
    assert 'Book added successfully!' in response.get_json()['message']

def test_get_books(client):
    # Test retrieving all books
    response = client.get('/books')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_book():
    # Create a new book to get its ID
    response = client.post("/books", json={"title": "Sample Book", "author": "Sample Author"})
    assert response.status_code == 200

    # Extract the ID from the response
    book_id = response.json["id"]

    # Use the book_id in the URL to retrieve the book
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert "id" in response.json  # Ensure that the 'id' key is present in the response
    assert "title" in response.json
    assert "author" in response.json


# Add more test cases for other endpoints (update and delete)

@pytest.fixture
def cleanup():
    """Clean up the database after each test."""
    with app.app_context():
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    pytest.main()
