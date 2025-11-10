from database import get_book_by_id
from services.library_service import (
    borrow_book_by_patron, return_book_by_patron
)
from tests.tools import add_book_helper, borrow_book_helper, borrow_past_book_helper, digit_generator, invalidLateStub, updateAvailFalse, updateBorrowFalse

# Tests

def test_return_book_valid():
    """Test returning a book with valid input."""
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)
    assert success == True
    assert "successful" in message.lower()

def test_return_book_invalid_twice():
    """Test returning a book with valid input twice."""
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)
    assert success == True
    assert "successful" in message.lower()

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "not borrowed" in message.lower()

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

def test_return_book_late_error(mocker):
    """Test returning a book with an invalid response from calc late fees."""
    invalidLateStub(mocker)
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "error occured" in message.lower()


def test_return_book_update_borrow_error(mocker):
    """Test returning a book with an update borrow db error."""
    updateBorrowFalse(mocker)
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "database error" in message.lower()

def test_return_book_availability_error(mocker):
    """Test returning a book with an availability db error."""
    patron, id = borrow_book_helper()
    
    updateAvailFalse(mocker)

    success, message = return_book_by_patron(patron, id)
    assert success == False
    assert "database error" in message.lower()