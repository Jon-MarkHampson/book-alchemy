import os
import re
import requests
from flask import Flask, request, render_template, flash, redirect, url_for
from sqlalchemy import or_
from datetime import datetime
from data_models import db, Author, Book
import seed

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
    sort_by = request.args.get("sort", "title")
    search_query = request.args.get("search_query", "")

    query = Book.query.options(db.joinedload(Book.author)).join(Author)

    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(Book.title.ilike(search_term), Author.name.ilike(search_term))
        )

    if sort_by == "author":
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    books_data = []
    invalid_isbns = []
    updated_books = False

    # Fetch covers and synopses if missing
    for book in books:
        cover_url = book.cover_url
        synopsis = book.synopsis  # Get existing synopsis
        fetch_method_cover = "Cached" if cover_url else "None"
        fetch_method_synopsis = "Cached" if synopsis else "None"

        # --- Fetch if cover OR synopsis is missing ---
        if not cover_url or not synopsis:
            # Attempt to fetch missing data from external sources
            # Reset fetch methods if we are attempting a fetch
            if not cover_url:
                fetch_method_cover = "None"
            if not synopsis:
                fetch_method_synopsis = "None"

            # --- ISBN Validation (only relevant for cover fetching, keep as is) ---
            if not cover_url and not is_valid_isbn(book.isbn):
                print(
                    f"Warning: Potentially invalid ISBN format for '{book.title}': {book.isbn}"
                )
                invalid_isbns.append(
                    {"id": book.id, "title": book.title, "isbn": book.isbn}
                )

            # --- Attempt 1: Google Books API by ISBN ---
            if book.isbn and (not cover_url or not synopsis):
                google_books_api_url_isbn = (
                    f"https://www.googleapis.com/books/v1/volumes?q=isbn:{book.isbn}"
                )
                try:
                    response = requests.get(google_books_api_url_isbn, timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    if data.get("totalItems", 0) > 0 and "items" in data:
                        volume_info = data["items"][0].get("volumeInfo", {})
                        # Fetch Cover
                        if not cover_url:
                            image_links = volume_info.get("imageLinks", {})
                            new_cover_url = image_links.get(
                                "thumbnail"
                            ) or image_links.get("smallThumbnail")
                            if new_cover_url:
                                cover_url = new_cover_url
                                fetch_method_cover = "Google Books (ISBN)"
                                print(
                                    f"Found cover for '{book.title}' via {fetch_method_cover}"
                                )
                        # Fetch Synopsis
                        if not synopsis:
                            new_synopsis = volume_info.get("description")
                            if new_synopsis:
                                synopsis = new_synopsis
                                fetch_method_synopsis = "Google Books (ISBN)"
                                print(
                                    f"Found synopsis for '{book.title}' via {fetch_method_synopsis}"
                                )
                except requests.exceptions.RequestException:
                    pass
                except Exception:
                    pass

            # --- Attempt 2: Open Library Covers API by ISBN (Only for covers) ---
            if not cover_url and book.isbn:
                # ... existing Open Library cover fetching logic ...
                # (No changes needed here as it only fetches covers)
                print(f"Google Books failed for '{book.title}', trying Open Library...")
                # Add default=false
                open_library_cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg?default=false"
                try:
                    head_response = requests.head(
                        open_library_cover_url, timeout=3, allow_redirects=True
                    )
                    if (
                        head_response.status_code == 200
                        and "image"
                        in head_response.headers.get("Content-Type", "").lower()
                    ):
                        cover_url = open_library_cover_url
                        fetch_method_cover = "Open Library (ISBN)"
                        print(
                            f"Found cover for '{book.title}' via {fetch_method_cover}"
                        )
                    elif head_response.status_code == 302:
                        redirect_url = head_response.headers.get("Location")
                        if (
                            redirect_url
                            and "notfound" not in redirect_url.lower()
                            and "placeholder" not in redirect_url.lower()
                        ):
                            get_response = requests.get(
                                open_library_cover_url, timeout=3, allow_redirects=True
                            )
                            if (
                                get_response.status_code == 200
                                and "image"
                                in get_response.headers.get("Content-Type", "").lower()
                            ):
                                cover_url = get_response.url
                                fetch_method_cover = "Open Library (ISBN - Redirect)"
                                print(
                                    f"Found cover for '{book.title}' via {fetch_method_cover}"
                                )
                            else:
                                print(
                                    f"Open Library redirect for '{book.title}' did not lead to a valid image."
                                )
                        else:
                            print(
                                f"Open Library redirect for '{book.title}' seems to be a placeholder."
                            )
                    else:
                        print(
                            f"No valid cover found on Open Library for '{book.title}' (Status: {head_response.status_code}, Content-Type: {head_response.headers.get('Content-Type')})"
                        )
                except requests.exceptions.RequestException:
                    pass
                except Exception:
                    pass

            # --- Attempt 3: Google Books API by Title + Author (if other methods failed) ---
            if not cover_url or not synopsis:
                print(f"Trying Google Books by Title+Author for '{book.title}'...")
                query_title = re.sub(r"[^\w\s]", "", book.title)
                query_author = re.sub(r"[^\w\s]", "", book.author.name)
                google_books_api_url_title = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query_title}+inauthor:{query_author}"
                try:
                    response = requests.get(google_books_api_url_title, timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    if data.get("totalItems", 0) > 0 and "items" in data:
                        volume_info = data["items"][0].get("volumeInfo", {})
                        # Fetch Cover
                        if not cover_url:
                            image_links = volume_info.get("imageLinks", {})
                            new_cover_url = image_links.get(
                                "thumbnail"
                            ) or image_links.get("smallThumbnail")
                            if new_cover_url:
                                cover_url = new_cover_url
                                fetch_method_cover = "Google Books (Title+Author)"
                                print(
                                    f"Found cover for '{book.title}' via {fetch_method_cover}"
                                )
                        # Fetch Synopsis
                        if not synopsis:
                            new_synopsis = volume_info.get("description")
                            if new_synopsis:
                                synopsis = new_synopsis
                                fetch_method_synopsis = "Google Books (Title+Author)"
                                print(
                                    f"Found synopsis for '{book.title}' via {fetch_method_synopsis}"
                                )
                except requests.exceptions.RequestException:
                    pass
                except Exception:
                    pass

        # --- Update the database if new data was found ---
        if fetch_method_cover not in [
            "Cached",
            "None",
        ] or fetch_method_synopsis not in ["Cached", "None"]:
            if fetch_method_cover not in ["Cached", "None"]:
                print(f"Caching cover URL for '{book.title}': {cover_url}")
                book.cover_url = cover_url
            if fetch_method_synopsis not in ["Cached", "None"]:
                print(f"Caching synopsis for '{book.title}'")
                book.synopsis = synopsis
            db.session.add(book)
            updated_books = True
        elif fetch_method_cover == "None" and fetch_method_synopsis == "None":
            print(
                f"Could not find cover or synopsis for '{book.title}' from any source."
            )

        # --- Append data for template ---
        books_data.append(
            {
                "id": book.id,
                "title": book.title,
                "author_id": book.author.id,
                "author": book.author.name,
                "cover_url": cover_url,
                "rating": book.rating,
                # Synopsis is not needed on the home page list, but fetched if missing
            }
        )

    # --- Commit updates ---
    if updated_books:
        try:
            db.session.commit()
            print("Committed updated cover URLs and/or synopses to database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing updates: {e}")
            flash("Error saving updated book details to the database.", "error")

    if invalid_isbns:
        isbn_links = [
            f'<a href="{url_for('book_detail', book_id=item['id'])}">{item['title']} ({item['isbn']})</a>'
            for item in invalid_isbns
        ]
        flash(
            f"Warning: Found {len(invalid_isbns)} books with potentially invalid ISBN formats: {', '.join(isbn_links)}. Check console logs.",
            "warning",
        )

    return render_template("home.html", books=books_data, search_query=search_query)


# --- Detail Page Routes ---


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    # Eager load author, no need to fetch synopsis here as it should be fetched by home()
    book = Book.query.options(db.joinedload(Book.author)).get_or_404(book_id)
    # If synopsis is somehow still missing, we could add a fallback fetch here,
    # but ideally home() handles it.
    return render_template("book_detail.html", book=book)


@app.route("/author/<int:author_id>")
def author_detail(author_id):
    # Use get_or_404 to handle cases where the author ID doesn't exist
    # Eager load books for the author detail page
    author = Author.query.options(db.joinedload(Author.books)).get_or_404(author_id)
    return render_template("author_detail.html", author=author)


# --- Action Routes ---


@app.route("/book/<int:book_id>/rate", methods=["POST"])
def rate_book(book_id):
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
    book = Book.query.get_or_404(book_id)
    if book.cover_url:
        book.cover_url = None
        db.session.commit()
        flash(
            f'Cover removed for "{book.title}". It will be re-fetched on next load.',
            "success",
        )
    else:
        flash(f'"{book.title}" already has no cover cached.', "info")
    return redirect(url_for("book_detail", book_id=book_id))


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
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
