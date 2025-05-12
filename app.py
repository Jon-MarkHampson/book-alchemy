import os
from flask import Flask, request, render_template, flash, redirect, url_for
from datetime import datetime
from data_models import db, Author, Book
import seed
from helpers import (
    _build_book_query,
    _fetch_and_update_book_metadata,
    _update_db_if_needed,
    _handle_invalid_isbns,
)

app = Flask(__name__)

# Set up the base directory and database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data", "library.sqlite"
)
app.config["SECRET_KEY"] = "your_secret_key"

db.init_app(app)
seed.init_cli(app)

# Create tables if they don't exist. For production, use Flask-Migrate.
with app.app_context():
    db.create_all()


def is_valid_isbn(isbn):
    """Check if the ISBN is in a valid format (not a checksum validation)."""
    if not isbn:
        return False
    isbn = isbn.replace("-", "").replace(" ", "").upper()
    if len(isbn) == 10 and (
        isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1] == "X")
    ):
        return True
    if len(isbn) == 13 and isbn.isdigit():
        return True
    return False


@app.route("/")
def home():
    """Display the homepage with a list of books.

    Handles sorting and searching of books.
    Fetches book metadata (cover, synopsis) if missing and updates
    the database.
    """
    sort_by = request.args.get("sort", "title")
    search_query = request.args.get("search_query", "")

    query = _build_book_query(sort_by, search_query)
    books = query.all()

    books_data = []
    invalid_isbns = []
    updated_books = False

    for book in books:
        cover_url, synopsis = _fetch_and_update_book_metadata(book)

        if not book.cover_url and not is_valid_isbn(book.isbn):
            invalid_isbns.append(
                {"id": book.id, "title": book.title, "isbn": book.isbn}
            )

        if _update_db_if_needed(book, cover_url, synopsis):
            updated_books = True

        books_data.append(
            {
                "id": book.id,
                "title": book.title,
                "author_id": book.author.id,
                "author": book.author.name,
                "cover_url": cover_url or book.cover_url,
                "rating": book.rating,
            }
        )

    if updated_books:
        try:
            db.session.commit()
            print("Committed updated cover URLs and/or synopses to database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing updates: {e}")
            flash("Error saving updated book details to the database.", "error")

    _handle_invalid_isbns(invalid_isbns)

    return render_template("home.html", books=books_data, search_query=search_query)


# --- Detail Page Routes ---


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    """Display the detail page for a specific book."""
    # Eager load author, no need to fetch synopsis here
    # as it should be fetched by home()
    book = Book.query.options(db.joinedload(Book.author)).get_or_404(book_id)
    return render_template("book_detail.html", book=book)


@app.route("/author/<int:author_id>")
def author_detail(author_id):
    """Display the detail page for a specific author and their books."""
    # Use get_or_404 to handle cases where the author ID doesn't exist
    # Eager load books for the author detail page
    author = Author.query.options(db.joinedload(Author.books)).get_or_404(author_id)
    return render_template("author_detail.html", author=author)


# --- Action Routes ---


@app.route("/book/<int:book_id>/rate", methods=["POST"])
def rate_book(book_id):
    """Rate a book and update its rating in the database."""
    book = Book.query.get_or_404(book_id)
    rating = request.form.get("rating", type=int)
    if rating is not None and 1 <= rating <= 10:
        book.rating = rating
        db.session.commit()
        flash(f'Rating updated for "{book.title}".', "success")
    else:
        flash("Invalid rating value.", "error")
    return redirect(url_for("book_detail", book_id=book_id))


@app.route("/book/<int:book_id>/remove_cover", methods=["POST"])
def remove_cover(book_id):
    """Remove the cover URL for a book, allowing it to be re-fetched."""
    book = Book.query.get_or_404(book_id)
    if book.cover_url:
        book.cover_url = None
        db.session.commit()
        flash(
            f'Cover removed for "{book.title}".It will be re-fetched on next load.',
            "success",
        )
    else:
        flash(f'"{book.title}" already has no cover cached.', "info")
    return redirect(url_for("book_detail", book_id=book_id))


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Delete a book from the database."""
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.title}" deleted successfully.', "success")
        return redirect(url_for("home"))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book "{book.title}": {e}', "error")
        return redirect(url_for("book_detail", book_id=book_id))


@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    """Delete an author and all their associated books from the database."""
    author = Author.query.get_or_404(author_id)
    author_name = author.name  # Get name before deleting
    try:
        # Because of cascade='all, delete-orphan', deleting the author
        # will automatically delete their associated books.
        db.session.delete(author)
        db.session.commit()
        flash(
            f'Author "{author_name}" and all associated books deleted successfully.',
            "success",
        )
        return redirect(url_for("home"))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting author "{author_name}": {e}', "error")
        # Redirect back to author detail or home if detail page won't exist
        return redirect(url_for("home"))


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Handle the addition of a new author.

    GET: Displays the form to add an author.
    POST: Processes the form submission and adds the author to the database.
    """
    if request.method == "POST":
        name = request.form["name"]
        birthdate_str = request.form["birthdate"]
        date_of_death_str = request.form["date_of_death"]
        # Get bio from form
        bio = request.form.get("bio")
        birthdate_obj = None
        date_of_death_obj = None
        try:
            if birthdate_str:
                birthdate_obj = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
            if date_of_death_str:
                date_of_death_obj = datetime.strptime(
                    date_of_death_str, "%Y-%m-%d"
                ).date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return render_template("add_author.html")
        new_author = Author(
            name=name, birth_date=birthdate_obj, death_date=date_of_death_obj, bio=bio
        )
        db.session.add(new_author)
        db.session.commit()
        flash("Author added successfully!", "success")
        return redirect(url_for("add_author"))

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Handle the addition of a new book.

    GET: Displays the form to add a book, populating authors for selection.
    POST: Processes the form submission and adds the book to the database.
    """
    authors = Author.query.order_by(Author.name).all()
    if request.method == "POST":
        isbn = request.form["isbn"]
        title = request.form["title"]
        publication_date_str = request.form["publication_year"]
        author_id = request.form["author_id"]
        publication_date_obj = None
        if not isbn or not title or not publication_date_str or not author_id:
            flash("Please fill out all fields.", "error")
            return render_template("add_book.html", authors=authors)
        try:
            if publication_date_str:
                publication_date_obj = datetime.strptime(
                    publication_date_str, "%Y-%m-%d"
                ).date()
        except ValueError:
            flash("Invalid publication date format. Please use YYYY-MM-DD.", "error")
            return render_template("add_book.html", authors=authors)
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash("A book with this ISBN already exists.", "error")
            return render_template("add_book.html", authors=authors)
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_date=publication_date_obj,
            author_id=int(author_id),
        )
        db.session.add(new_book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for("add_book"))

    return render_template("add_book.html", authors=authors)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
