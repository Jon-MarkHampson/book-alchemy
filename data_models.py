from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import Text

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'  # Explicitly set table name if needed
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    death_date = db.Column(db.Date, nullable=True)
    # Add bio column
    bio = db.Column(db.Text, nullable=True)

    # Add cascade='all, delete-orphan' to automatically delete books when author is deleted
    books = db.relationship('Book', back_populates='author',
                            lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Author {self.name}>'

    def __str__(self):
        return super().__str__()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True,
                     nullable=True)  # Allow nullable ISBNs
    title = db.Column(db.String(120), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'authors.id'), nullable=False)  # Changed 'author.id' to 'authors.id'
    # Use Text for potentially long synopses, make it nullable
    synopsis = db.Column(db.Text, nullable=True)
    # Store cover image URL
    cover_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True)  # Add rating column

    # Define the relationship to Author
    # backref creates a virtual 'books' attribute on the Author model
    # cascade='all, delete-orphan' means related books are deleted if the author is deleted
    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f'<Book {self.title}>'

    def __str__(self):
        return super().__str__()
