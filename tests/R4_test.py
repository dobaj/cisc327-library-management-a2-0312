from database import get_book_by_id
from library_service import (
    borrow_book_by_patron, return_book_by_patron
)
from tests.tools import add_book_helper, borrow_book_helper, borrow_past_book_helper, digit_generator

# Tests

def test_return_book_valid():
    """Test returning a book with valid input."""
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)
    assert success == True

def test_return_book_invalid_twice():
    """Test returning a book with valid input twice."""
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)
    assert success == True

    success, message = return_book_by_patron(patron, id)
    assert success == False

def test_return_book_valid_overdue():
    """Test returning a book with valid input."""
    patron, id = borrow_past_book_helper(15)

    success, message = return_book_by_patron(patron, id)
    assert success == True
    assert "Days overdue: 1" in message
    assert "Late fees: 0.50" in message

def test_return_book_invalid_book_not_borrowed():
    """Test returning a book that is not borrowed."""
    id = add_book_helper()
    patron = digit_generator(6)

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "not borrowed" in message

def test_return_book_invalid_patron_id_too_long():
    """Test returning a book where the patron id is too long."""
    patron, id = borrow_book_helper()
    patron+="1"

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "patron" in message

def test_return_book_invalid_invalid_book_id():
    """Test returning a book where the book id is invalid."""
    id = digit_generator(20)*-1
    patron = digit_generator(6)

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "invalid" in message
