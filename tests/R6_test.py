from library_service import add_book_to_catalog, search_books_in_catalog
from tests.tools import digit_generator

# Tests

def test_search_exact_title_valid():
    """Test an exact title search for a book with valid input."""
    # Add book
    isbn = digit_generator()
    title = "Test Search Book "+isbn
    author = "Test author"
    success, message = add_book_to_catalog(title, author, isbn, 5)

    assert success == True

    # Search
    results = search_books_in_catalog(title, "title")

    assert len(results) > 0

    in_list = False
    for book in results:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True

    assert in_list == True

def test_search_partial_title_valid():
    """Test a partial title search for a book with valid input."""
    # Add book
    isbn = digit_generator()
    title = "Test Search Book "+isbn
    author = "Test author"
    success, message = add_book_to_catalog(title, author, isbn, 5)

    assert success == True

    # Search
    results = search_books_in_catalog(title[4:], "title")

    assert len(results) > 0

    in_list = False
    for book in results:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True

    assert in_list == True

def test_search_partial_author_valid():
    """Test a partial author search for a book with valid input."""
    # Add book
    isbn = digit_generator()
    title = "Test Search Book"
    author = "Test aUthor "+isbn
    success, message = add_book_to_catalog(title, author, isbn, 5)

    assert success == True

    # Search
    results = search_books_in_catalog(author[4:].lower(), "author")

    assert len(results) > 0

    in_list = False
    for book in results:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True

    assert in_list == True

def test_search_exact_isbn_valid():
    """Test an exact isbn search for a book with valid input."""
    # Add book
    isbn = digit_generator()
    title = "Test Search Book"
    author = "Test author "+isbn
    success, message = add_book_to_catalog(title, author, isbn, 5)

    assert success == True

    # Search
    results = search_books_in_catalog(isbn, "isbn")

    assert len(results) > 0

    in_list = False
    for book in results:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True

    assert in_list == True

def test_search_exact_isbn_no_match():
    """Test an exact isbn search for a book with no matching isbn."""
    # Add book
    isbn = digit_generator()
    title = "Test Search Book"
    author = "Test author "+isbn
    success, message = add_book_to_catalog(title, author, isbn, 5)

    assert success == True

    # Search
    # Slightly different isbn
    results = search_books_in_catalog(isbn[1:]+"9", "isbn") 

    in_list = False
    for book in results:
        if (book["isbn"] == isbn and 
            book["title"] == title and 
            book["author"] == author and 
            book["total_copies"] == 5):

            in_list = True

    assert in_list == False