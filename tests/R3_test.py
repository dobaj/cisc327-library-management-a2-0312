from services.library_service import borrow_book_by_patron
from tests.tools import add_book_helper, digit_generator, insertBorrowFalse, updateAvailFalse

# Tests

def test_borrow_book_valid():
    """Test borrowing a book with valid input."""
    id = add_book_helper()
    patron = digit_generator(6)

    success, message = borrow_book_by_patron(patron, id)
    assert success == True
    assert "successfully" in message.lower()

def test_borrow_book_invalid_patron_too_long():
    """Test borrowing a book with a patron id that is too long."""
    id = add_book_helper()
    patron = "1234567"

    success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "patron" in message

def test_borrow_book_invalid_patron_letters():
    """Test borrowing a book with a patron id with letters."""
    id = add_book_helper()
    patron = digit_generator(5)+"X"

    success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "patron" in message

def test_borrow_book_invalid_borrow_limit():
    """Test borrowing a book too many times."""
    id = add_book_helper()
    patron = digit_generator(6)

    success, message = True, ""
    for _ in range(6):
        success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "limit" in message

def test_borrow_book_invalid_book_unavailable():
    """Test borrowing a book that is unavailable."""
    id = add_book_helper(1)
    patron = digit_generator(6)

    success, message = True, ""
    for _ in range(2):
        success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "available" in message

def test_borrow_book_invalid_invalid_book_id():
    """Test borrowing a book with an invalid id."""
    id = digit_generator(20)*-1
    patron = digit_generator(6)

    success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "not found" in message

def test_borrow_book_insert_db_error(mocker):
    """Test borrowing a book with an insert db error."""
    insertBorrowFalse(mocker)
    id = add_book_helper()
    patron = digit_generator(6)

    success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "database error" in message.lower()

def test_borrow_book_availability_db_error(mocker):
    """Test borrowing a book with an update availability db error."""
    updateAvailFalse(mocker)
    id = add_book_helper()
    patron = digit_generator(6)

    success, message = borrow_book_by_patron(patron, id)
    assert success == False
    assert "database error" in message.lower()