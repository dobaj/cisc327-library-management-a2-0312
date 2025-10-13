from library_service import (
    add_book_to_catalog
)
from tests.tools import digit_generator

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", digit_generator(), 5)
    
    assert success == True
    assert "successfully added" in message.lower()

# def test_add_book_invalid_isbn_too_short():
#     """Test adding a book with ISBN too short."""
#     success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
#     assert success == False
#     assert "13 digits" in message

### New tests

def test_add_book_invalid_no_title():
    """Test adding a book with no title."""
    success, message = add_book_to_catalog("", "Test Author", "1234567893123", 5)
    
    assert success == False
    assert "Title" in message

def test_add_book_invalid_title_too_long():
    """Test adding a book with a title that's too long."""
    success, message = add_book_to_catalog("a"*201, "Test Author", "1234567893123", 5)
    
    assert success == False
    assert "Title" in message

def test_add_book_invalid_no_author():
    """Test adding a book with no author."""
    success, message = add_book_to_catalog("Test Book", "", "1234567893123", 5)
    
    assert success == False
    assert "Author" in message

def test_add_book_invalid_isbn_too_long():
    """Test adding a book with an ISBN that is too long."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "12345678901234", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_isbn_letters():
    """Test adding a book with an ISBN containing letters."""
    success, message = add_book_to_catalog("Test Book", "Test Author", digit_generator(12)+"X", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_negative_copies():
    """Test adding a book with a negative amount of total copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567894123", -5)
    
    assert success == False
    assert "Total" in message

def test_add_book_invalid_string_copies():
    """Test adding a book with a non-numerical copy count."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567896123", "5")
    
    assert success == False
    assert "Total" in message