from datetime import datetime, timedelta

import pytest
from database import insert_borrow_record
from library_service import calculate_late_fee_for_book
from tests.tools import add_book_helper, borrow_past_book_helper, digit_generator


# Tests

def test_late_fee_valid_not_due():
    """Test calculating a late fee for a not due book with valid input."""
    patron, id = borrow_past_book_helper(1)

    fees = calculate_late_fee_for_book(patron, id)
    assert fees is not None
    assert "days_overdue" in fees
    assert fees["days_overdue"] == 0

def test_late_fee_valid_overdue():
    """Test calculating a late fee for an overdue book with valid input."""
    patron, id = borrow_past_book_helper(15)

    fees = calculate_late_fee_for_book(patron, id)
    assert fees is not None
    assert "days_overdue" in fees
    assert "fee_amount" in fees
    assert fees["days_overdue"] == 1
    assert fees["fee_amount"] == pytest.approx(0.5, abs=0.02)

def test_late_fee_valid_overdue_over_week():
    """Test calculating a late fee for an overdue book over a week with valid input."""
    patron, id = borrow_past_book_helper(27)

    fees = calculate_late_fee_for_book(patron, id)
    assert fees is not None
    assert "days_overdue" in fees
    assert "fee_amount" in fees
    assert fees["days_overdue"] == 13
    assert fees["fee_amount"] == pytest.approx(9.5, abs=0.02)

def test_late_fee_valid_maximum_due():
    """Test calculating the max late fee for an overdue book with valid input."""
    patron, id = borrow_past_book_helper(300)

    fees = calculate_late_fee_for_book(patron, id)
    assert fees is not None
    assert "fee_amount" in fees
    assert fees["fee_amount"] == pytest.approx(15, abs=0.02)

def test_late_fee_invalid_patron_id_too_long():
    """Test calculating the late fee for a book with a patron id that is too long."""
    patron, id = borrow_past_book_helper(300)

    fees = calculate_late_fee_for_book(patron+"1", id)
    assert fees is not None
    assert "status" in fees
    assert "patron" in fees["status"]

def test_late_fee_invalid_book_not_borrowed():
    """Test calculating the late fee for a book that is not borrowed."""
    id = add_book_helper()
    patron = digit_generator(6)

    fees = calculate_late_fee_for_book(patron, id)
    assert fees is not None
    assert "status" in fees
    assert "not borrowed" in fees["status"]

def test_late_fee_invalid_book_invalid_id():
    """Test calculating the late fee for a book which has an invalid id."""
    id = add_book_helper()
    patron = digit_generator(6)

    fees = calculate_late_fee_for_book(patron, id*-1)
    assert fees is not None
    assert "status" in fees
    assert "invalid" in fees["status"]
