from database import get_all_books
from library_service import (
    add_book_to_catalog,
    borrow_book_by_patron
)
from tests.tools import digit_generator


### New tests

def test_get_new_book_valid():
    """Test getting a recently added book from the database."""
    isbn = digit_generator()
    title = "Test Book 1"
    author = "Test Author 1"

    success, message = add_book_to_catalog(title, author, isbn, 5)
    
    assert success == True

    book_list = get_all_books()

    in_list = False
    for book in book_list:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):
            in_list = True

    assert in_list == True

def test_get_all_books_valid_sorted():
    """Test that books returned from the database are sorted."""
    book_list = get_all_books()

    titles = [book["title"] for book in book_list]

    assert titles == sorted(titles)

def test_get_all_books_valid_populated():
    """Test that books returned from the database have all fields."""
    book_list = get_all_books()

    empty_field = False
    fields = ["id", "title", "author", "isbn", "available_copies", "total_copies"]

    for book in book_list:
        for field in fields:
            if field not in book or book[field] is None:
                empty_field = True    

    assert empty_field == False

def test_get_all_books_valid_borrow_change():
    """Test that books returned from the database change their available count when borrowed."""
    isbn = digit_generator()
    title = "Test Book 1"
    author = "Test Author 1"
    patron = digit_generator(6)

    success, message = add_book_to_catalog(title, author, isbn, 5)
    
    assert success == True

    #Test book is in the database

    book_list = get_all_books()

    in_list = False
    id = -1
    for book in book_list:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True 
            id = book["id"]

            assert book["available_copies"] == book["total_copies"]

    assert in_list == True

    borrow_book_by_patron(patron, id)

    # Now check the update is reflected

    book_list = get_all_books()

    in_list = False
    for book in book_list:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True
            assert book["available_copies"] == book["total_copies"] - 1

    assert in_list == True
