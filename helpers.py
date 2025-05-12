import re
import requests
from flask import flash, url_for
from sqlalchemy import or_
from data_models import db, Author, Book


def _build_book_query(sort_by, search_query):
    """Build the query for fetching books based on sort and search parameters."""
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

    return query


def _fetch_from_google_books(query_url):
    """Fetch book metadata from Google Books API."""
    try:
        response = requests.get(query_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def _fetch_cover_from_open_library(isbn):
    """Fetch book cover from Open Library API."""
    open_library_cover_url = (
        f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
    )
    try:
        head_response = requests.head(
            open_library_cover_url, timeout=3, allow_redirects=True
        )
        if (
            head_response.status_code == 200
            and "image" in head_response.headers.get("Content-Type", "").lower()
        ):
            return open_library_cover_url
    except requests.exceptions.RequestException:
        pass
    return None


def _fetch_and_update_book_metadata(book):
    """Fetch and update book metadata (cover and synopsis) if missing."""
    cover_url = book.cover_url
    synopsis = book.synopsis

    if not cover_url or not synopsis:
        if book.isbn:
            google_books_api_url_isbn = (
                f"https://www.googleapis.com/books/v1/volumes?q=isbn:{book.isbn}"
            )
            data = _fetch_from_google_books(google_books_api_url_isbn)
            if data and data.get("totalItems", 0) > 0 and "items" in data:
                volume_info = data["items"][0].get("volumeInfo", {})
                if not cover_url:
                    image_links = volume_info.get("imageLinks", {})
                    cover_url = image_links.get("thumbnail") or image_links.get(
                        "smallThumbnail"
                    )
                if not synopsis:
                    synopsis = volume_info.get("description")

        if not cover_url and book.isbn:
            cover_url = _fetch_cover_from_open_library(book.isbn)

        if not cover_url or not synopsis:
            query_title = re.sub(r"[^\w\s]", "", book.title)
            query_author = re.sub(r"[^\w\s]", "", book.author.name)
            google_books_api_url_title = (
                "https://www.googleapis.com/books/v1/volumes?q=intitle:"
                f"{query_title}+inauthor:{query_author}"
            )
            data = _fetch_from_google_books(google_books_api_url_title)
            if data and data.get("totalItems", 0) > 0 and "items" in data:
                volume_info = data["items"][0].get("volumeInfo", {})
                if not cover_url:
                    image_links = volume_info.get("imageLinks", {})
                    cover_url = image_links.get("thumbnail") or image_links.get(
                        "smallThumbnail"
                    )
                if not synopsis:
                    synopsis = volume_info.get("description")

    return cover_url, synopsis


def _update_db_if_needed(book, cover_url, synopsis):
    """Update the database if new metadata is found."""
    updated = False
    if cover_url and cover_url != book.cover_url:
        book.cover_url = cover_url
        updated = True
    if synopsis and synopsis != book.synopsis:
        book.synopsis = synopsis
        updated = True
    if updated:
        db.session.add(book)
    return updated


def _handle_invalid_isbns(invalid_isbns):
    """Flash a warning for books with invalid ISBNs."""
    if invalid_isbns:
        isbn_links = [
            f'<a href="{url_for("book_detail", book_id=item["id"])}">'
            f'{item["title"]} ({item["isbn"]})</a>'
            for item in invalid_isbns
        ]
        flash(
            f"Warning: Found {len(invalid_isbns)} books with potentially invalid "
            f"ISBN formats: {', '.join(isbn_links)}. Check console logs.",
            "warning",
        )
