import os
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from flask import request, render_template, flash
from flask import redirect, url_for

app = Flask(__name__)

# Get absolute path to project directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Use an absolute path for SQLite URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data', 'library.sqlite')
# Add a secret key for flash messages
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    sort_by = request.args.get('sort', 'title')  # Default sort by title
    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:  # Default to sorting by title
        books = Book.query.order_by(Book.title).all()

    books_data = []
    for book in books:
        cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg"
        # Basic check if image exists (optional, requires request)
        try:
            response = requests.head(cover_url, timeout=2)
            if response.status_code != 200:
                cover_url = None # Or a placeholder image URL
        except requests.exceptions.RequestException:
            cover_url = None # Or a placeholder image URL
        books_data.append({
            'title': book.title,
            'author': book.author.name,
            'cover_url': cover_url
        })

    return render_template('home.html', books=books_data)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        # Corrected field names based on data_models.py
        birthdate = request.form['birthdate']
        date_of_death = request.form['date_of_death']

        # Handle empty date_of_death
        if not date_of_death:
            date_of_death = None

        # Use correct column names from model
        new_author = Author(name=name, birth_date=birthdate,
                            death_date=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        # Redirect after POST to prevent form resubmission on refresh
        return redirect(url_for('add_author'))

    # Render the form for GET requests
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Get all authors for the dropdown
    authors = Author.query.order_by(Author.name).all()
    if request.method == 'POST':
        isbn = request.form['isbn']  # Get ISBN
        title = request.form['title']
        # Corrected field name based on data_models.py
        # Assuming year maps to date for simplicity
        publication_date = request.form['publication_year']
        author_id = request.form['author_id']

        # Basic validation (can be expanded)
        if not isbn or not title or not publication_date or not author_id:
            flash('Please fill out all fields.', 'error')
            return render_template('add_book.html', authors=authors)

        # Check if ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash('A book with this ISBN already exists.', 'error')
            return render_template('add_book.html', authors=authors)

        # Use correct column names from model
        new_book = Book(isbn=isbn, title=title, publication_date=publication_date,
                        author_id=int(author_id))
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))  # Redirect after POST

    # Render the form for GET requests, passing authors to the template
    return render_template('add_book.html', authors=authors)

def main():
    app.run(host='127.0.0.1', port=5001, debug=True)
    
    
if __name__ == '__main__':
    main()
