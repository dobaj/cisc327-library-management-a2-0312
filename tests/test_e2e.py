import time
import re
from playwright.sync_api import Page, expect, sync_playwright
from datetime import datetime
from tools import add_book_helper, borrow_book_helper, digit_generator

root_url = "http://127.0.0.1:5000/"

def test_add_and_borrow_book(page: Page):
    title = "Test Book"
    author = "Test Author"
    isbn = str(digit_generator())
    count = "10"

    page.goto(root_url)

    expect(page).to_have_title("Library Management System")

    # Try to start add book process
    add_book = page.get_by_role("link", name=re.compile("Add New Book", re.IGNORECASE))
    add_book.click()

    expect(page).to_have_url(re.compile("add_book"))

    # Fill in details
    fill = page.get_by_role("textbox",name="Title").filter(visible=True)
    fill.fill(title)

    fill = page.get_by_role("textbox",name="Author").filter(visible=True)
    fill.fill(author)

    fill = page.get_by_label("ISBN").filter(visible=True)
    fill.fill(isbn)

    fill = page.get_by_label("Total Copies").filter(visible=True)
    fill.fill(count)

    # Submit
    add_book = page.get_by_role("button", name=re.compile("Add Book", re.IGNORECASE)).filter(visible=True)
    add_book.click()

    confirmation = page.get_by_text(re.compile(f'Book "{title}" has been successfully added to the catalog.', re.IGNORECASE))
    expect(confirmation).to_be_visible()

    # Try to find book in display
    rows = page.get_by_role("row") 
    row = rows.filter(has_text=isbn)

    # Looks complicated but this just makes sure all the fields are in this row
    assert all(e in row.inner_text() for e in [title,author,isbn,count+"/"+count])

    # Time to borrow
    patron_id = digit_generator(6)
    # Fill in id
    patron_input = row.get_by_placeholder(re.compile("Patron ID"))
    patron_input.fill(patron_id)

    patron_button = row.get_by_role("button", name=re.compile("Borrow", re.IGNORECASE))
    patron_button.click()

    # Make sure it happened
    confirmation = page.get_by_text(re.compile("Successfully borrowed"))
    expect(confirmation).to_be_visible()



def test_status_then_return(page: Page):
    # Make sure we have a book that is borrowed
    # Using helper func from other tests
    title, author = "Test Novel", "Test Writer"
    patron_id, id = borrow_book_helper(title, author)
    id = str(id)

    page.goto(root_url+"status")

    # Fill in id and search
    patron_input = page.get_by_role("textbox", name=re.compile("Patron ID"))
    patron_input.fill(patron_id)
    
    patron_button = page.get_by_role("button", name=re.compile("Search", re.IGNORECASE))
    patron_button.click()

    # Look for book in currently borrowed table
    table = page.get_by_role("table").filter(has_text="Fees Due")
    row = None
    for r in table.all():
        # Use one liner from earlier
        print(r.inner_text())
        if all(e in r.inner_text() for e in [title,author,id]):
            row = r
    
    assert row

    # Return now
    page.goto(root_url+"return")

    # Fill details
    fill = page.get_by_role("textbox",name="Patron ID").filter(visible=True)
    fill.fill(patron_id)

    fill = page.get_by_label("Book ID").filter(visible=True)
    fill.fill(id)

    return_book = page.get_by_role("button", name=re.compile("Return", re.IGNORECASE)).filter(visible=True)
    return_book.click()

    # Confirm return works
    confirmation = page.get_by_text(re.compile(f'Book returned successfully. Late fees: 0.00, Days overdue: 0', re.IGNORECASE))
    expect(confirmation).to_be_visible()
