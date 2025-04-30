# Book Alchemy

Book Alchemy is a modern Flask web application for managing your personal library. You can add, view, and rate books and authors, with automatic fetching of book covers and synopses from external APIs. The app features a responsive UI, dark/light mode, and a search and sort system.

## Features

- Add, view, and delete books and authors
- Rate books (1-10)
- Automatic fetching of book covers and synopses from Google Books and Open Library
- Modern, responsive UI with light/dark mode toggle
- Search and sort your library by title or author
- All data stored in a local SQLite database

## Project Structure

- `app.py` — Main Flask application
- `data_models.py` — SQLAlchemy models for books and authors
- `seed.py` — CLI command to seed the database with sample data
- `requirements.txt` — Python dependencies (exact versions)
- `static/` — Static files (CSS)
- `templates/` — Jinja2 HTML templates
- `data/library.sqlite` — SQLite database file (created automatically)

## Setup Instructions (macOS)

### 1. Clone the repository and navigate to the project folder

```bash
git clone <your-repo-url>
cd book-alchemy
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root

Your `.env` file should contain:

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_RUN_PORT=5001
```

- You can change `FLASK_RUN_PORT` if you want to use a different port.
- `SECRET_KEY` is set in `app.py` for development, but for production you should set it in your `.env`.

**Warning:** The application will not run without a valid `.env` file containing these variables.

### 5. Initialize the database (optional, for first run or reseeding)

```bash
flask seed-db
```

This will populate the database with sample authors and books. The database file will be created at `data/library.sqlite`.

### 6. Run the application

```bash
flask run
```

The app will be available at http://127.0.0.1:5001/

## Notes

- To reset the database, delete the `data/library.sqlite` file and rerun the seed command.
- All static assets (CSS) are in the `static/` folder.
- All HTML templates are in the `templates/` folder.
- For production, use a production-ready server and set a secure `SECRET_KEY` in your environment.

---

For any issues or contributions, please open an issue or pull request.
