## A1 - Matt Dobaj - 20350312 - TA Group 1

function name | implementation status (complete/partial) | what is missing
|---|---|---|
| R1 Add Book | partial | Does not check that the ISBN is 13 digits, only that it is 13 characters long. ISBN-13s cannot contain anything other than numbers.
| R2 Book Catalog Display | complete | nothing
| R3 Book Borrowing Interface | partial | The borrow limit in the app is 6, not 5 as described in the requirements.
| R4 Book Return Processing | partial | Does not allow user to return books. Does not update available copies or record return date. Does not calculate or display any late fees.
| R5 Late Fee Calculation API | partial | Does not calculate late fees based on decription's parameters. Returns nothing.
| R6 Book Search Functionality | partial | Does not search through book catalog. Does not return books in the same format as the catalog display.
| R7 Patron Status Report | partial | Does not display patron status with borrowed books, late fees, number of books borrowed, or borrowing history. There is also no menu option for showing the patron status in the main interface. 

# Test Summary
Requirement | Test Overview | Failed Tests
--|--|--
R1 Add Book | Tests for a variety of input handling cases involving no title, a title that is too long, no author, an invalid isbn number, and an invalid number of book copies. | Fails case where an ISBN containing letters is used. This fails the requirement where the ISBN should be 13 digits, not characters.
R2 Book Catalog Display | Tests that the database reflects a recently added book, that all books are returned sorted, that all book fields are populated, and that borrowing a book changes the available copies. | Fails no cases. 
R3 Book Borrowing Interface | Tests borrowing a book with valid input, invalid patron ids, exceeding the borrow limit, a book that is unavailable, and a book with an invalid id. | Fails the borrow limit test as the logic allows the user to borrow 6 books, not 5 as per the requirements.
R4 Book Return Processing | Tests that a book can be returned with valid input and input handling cases involving a book that is not borrowed, a patron id that is too long, and a book with an invalid id. | Fails all tests as this requirement is not implemented.
R5 Late Fee Calculation API | Tests that a late fee is not calculated for a book that is not late. Tests input handling for invalid patron ids, book ids and for when a book is not borrowed. Tests when a book is considered late and that the late fee is capped to the maximum fee. | Fails all tests as this requirement is not implemented.
R6 Book Search Functionality | Tests for a search with an exact match for the title or isbn of a book, and the case insensitive partial match of the title or author of a book. Also tests the search for an isbn that no book is associated with. | Fails all tests as this requirement is not implemented.
R7 Patron Status Report | Tests that the number of borrowed books is valid, that no books nor history are returned when no books have been borrowed, that the late fee for a borrowed book matches its expected value, and tests input handling for an invalid patron id. | Fails all tests as this requirement is not implemented.