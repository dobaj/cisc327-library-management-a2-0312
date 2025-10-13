"""
Catalog Routes - Book catalog related endpoints
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_all_books
from library_service import add_book_to_catalog, get_patron_status_report

status_bp = Blueprint('status', __name__)

@status_bp.route('/')
def index():
    """Home page redirects to status page."""
    return redirect(url_for('status.status'))

@status_bp.route('/status',methods=["GET","POST"])
def status():
    """
    Search for patron's borrowed and previously borrowed books.
    Web interface for R7: Book Search Functionality
    """
    if request.method == 'GET':
        return render_template('status.html')
    
    patron_id = request.form.get('patron_id', '').strip()
    
    if not patron_id:
        return render_template('status.html', curr_books=[], prev_books = [], patron_id='')
    

    result = get_patron_status_report(patron_id)
    
    if "curr_books" not in result or "prev_books" not in result:
        flash('Something went wrong.', 'error')
    
    return render_template('status.html', curr_books=result["curr_books"], prev_books = result["prev_books"], patron_id=patron_id)