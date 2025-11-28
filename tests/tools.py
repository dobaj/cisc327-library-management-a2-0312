
from datetime import datetime, timedelta
import math
import random

from database import get_book_by_isbn, insert_borrow_record, update_book_availability
from services.library_service import add_book_to_catalog, borrow_book_by_patron


def digit_generator(len: int = 13):
    return str(math.floor(random.random()*10**len)).zfill(len)


def add_book_helper(total: int = 10, title="Test Book", author="Test Author"):
    # Adds a book and returns it's id
    isbn = digit_generator()
    success, message = add_book_to_catalog(title, author, isbn, total)
    
    print(message) # Print message in case ISBN already exists
    assert success == True
    
    return get_book_by_isbn(isbn)["id"]

def borrow_book_helper(title="Test Book", author="Test Author"):
    id = add_book_helper(10,title,author)
    patron = digit_generator(6)

    success, message = borrow_book_by_patron(patron, id)
    print(message)
    assert success == True

    return patron, id

def borrow_past_book_helper(days: int = 14):
    id = add_book_helper()
    patron = digit_generator(6)
    date = datetime.now()-timedelta(days=days)
    duedate = datetime.now()-timedelta(days=days-14)

    success = insert_borrow_record(patron, id, date, duedate)
    availability_success = update_book_availability(id, -1)
    
    assert success == True
    assert availability_success == True

    return patron, id

# Stubs

def invalidLateStub(mocker):
    # Missing key variables
    mocker.patch('services.library_service.calculate_late_fee_for_book', 
        return_value={ 
            'days_overdue': 0,
        })
    
def notLateStub(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book', 
        return_value={ 
            'fee_amount': 0,
            'days_overdue': 0,
            'status': 'Book is not overdue'
        })

def lateStub(mocker):
    mocker.patch('services.library_service.calculate_late_fee_for_book', 
        return_value={ 
            'fee_amount': 9.5,
            'days_overdue': 13,
            'status': 'Book is overdue'
        })

def validBookStub(mocker):
    mocker.patch('services.library_service.get_book_by_id', 
        return_value={
            "title": "To Kill A Mockingbird", 
            "author": "Harper Lee", 
            "isbn":"1234567890123", 
            "total_copies": 5, 
            "available_copies": 4
        })

def invalidBookStub(mocker):
    mocker.patch('services.library_service.get_book_by_id', 
        return_value=None)

def insertBookFalse(mocker):
    mocker.patch('services.library_service.insert_book',
        return_value=False)

def insertBorrowFalse(mocker):
    mocker.patch('services.library_service.insert_borrow_record', return_value=False)

def updateAvailFalse(mocker):
    mocker.patch('services.library_service.update_book_availability', return_value=False)

def updateBorrowFalse(mocker):
    mocker.patch('services.library_service.update_borrow_record_return_date', return_value=False)