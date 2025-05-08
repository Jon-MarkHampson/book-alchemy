from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    death_date = db.Column(db.Date, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    books = db.relationship(
        "Book", back_populates="author", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return super().__str__()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    title = db.Column(db.String(120), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return super().__str__()
