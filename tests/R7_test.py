from library_service import (
    get_patron_status_report, return_book_by_patron
)
from tests.tools import borrow_book_helper, borrow_past_book_helper, digit_generator
import pytest

# Tests

def test_patron_status_books_borrowed_valid():
    """Test the returned borrowed books when getting a patron status with valid input."""
    patron, id = borrow_book_helper()

    report = get_patron_status_report(patron)
    
    assert report is not None
    assert "curr_books" in report 
    assert "borrow_count" in report
    assert report["borrow_count"] > 0
    assert report["borrow_count"] == len(report["curr_books"])

    assert report["curr_books"][0]["book_id"] == id

def test_patron_status_books_prev_borrowed_valid():
    """Test the returned previously borrowed books when getting a patron status with valid input."""
    patron, id = borrow_book_helper()

    success, message = return_book_by_patron(patron, id)

    assert success == True

    report = get_patron_status_report(patron)
    
    assert report is not None
    assert "prev_books" in report 
    assert "borrow_count" in report
    assert report["borrow_count"] == 0
    assert report["borrow_count"] == len(report["curr_books"])

    assert len(report["prev_books"]) == 1
    assert report["prev_books"][0]["book_id"] == id

def test_patron_status_patron_too_long():
    """Test getting a patron status with a patron id that is too long."""
    patron, id = borrow_book_helper()

    report = get_patron_status_report(patron+"1")
    
    assert report is not None
    assert "status" in report
    assert "patron" in report["status"]

def test_patron_status_patron_too_short():
    """Test getting a patron status with a patron id that is too short."""
    patron, id = borrow_book_helper()

    report = get_patron_status_report(patron[1:])
    
    assert report is not None
    assert "status" in report
    assert "patron" in report["status"]

def test_patron_status_no_books_no_history():
    """Test that no books nor history are in a patron status with valid input."""
    patron = digit_generator(6)

    report = get_patron_status_report(patron)
    
    assert report is not None
    assert "curr_books" in report
    assert "prev_books" in report
    assert "borrow_count" in report
    assert report["borrow_count"] == 0
    assert len(report["curr_books"]) == 0
    assert len(report["prev_books"]) == 0

def test_patron_status_late_fee():
    """Test the late fees owed in a patron status with valid input."""
    patron, id = borrow_past_book_helper(300)

    report = get_patron_status_report(patron)
    assert report is not None
    assert "curr_books" in report and len(report["curr_books"]) > 0
    assert report["curr_books"][0]["fee_amount"] == "15.00"