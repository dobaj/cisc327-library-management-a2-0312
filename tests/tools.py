
from datetime import datetime, timedelta
import math
import random

from database import get_book_by_isbn, insert_borrow_record, update_book_availability
from library_service import add_book_to_catalog, borrow_book_by_patron


def digit_generator(len: int = 13):
    return str(math.floor(random.random()*10**len)).zfill(len)


def add_book_helper(total: int = 10):
    # Adds a book and returns it's id
    isbn = digit_generator()
    success, message = add_book_to_catalog("Test Book", "Test Author", isbn, total)
    
    print(message) # Print message in case ISBN already exists
    assert success == True
    
    return get_book_by_isbn(isbn)["id"]

def borrow_book_helper():
    id = add_book_helper()
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