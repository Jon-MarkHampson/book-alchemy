import click
from flask.cli import with_appcontext
from datetime import datetime
from data_models import db, Author, Book


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """
    Seeds the database with initial data. This will only add data if the tables
    are empty.
    """
    # Remove the following block comments to clear data before seeding.
    # Book.query.delete()
    # Author.query.delete()
    # db.session.commit()

    # Add authors if the table is empty
    if Author.query.count() == 0:
        authors_data = [
            {
                "name": "J.K. Rowling",
                "birth_date": "1965-7-31",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Stephen King",
                "birth_date": "1947-9-21",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Dan Brown",
                "birth_date": "1964-6-22",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "John Grisham",
                "birth_date": "1955-2-8",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "George R.R. Martin",
                "birth_date": "1948-9-20",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Suzanne Collins",
                "birth_date": "1962-8-10",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "E.L. James",
                "birth_date": "1963-3-7",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Paula Hawkins",
                "birth_date": "1972-8-26",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Gillian Flynn",
                "birth_date": "1971-2-24",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Stieg Larsson",
                "birth_date": "1954-8-15",
                "death_date": "2004-11-9",
                "bio": None,
            },
            {
                "name": "Khaled Hosseini",
                "birth_date": "1965-3-4",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Yann Martel",
                "birth_date": "1963-6-25",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Markus Zusak",
                "birth_date": "1975-6-23",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Audrey Niffenegger",
                "birth_date": "1963-6-13",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Alice Sebold",
                "birth_date": "1963-9-6",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Kathryn Stockett",
                "birth_date": "1969-1-1",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Andy Weir",
                "birth_date": "1972-6-16",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Ernest Cline",
                "birth_date": "1972-3-29",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Celeste Ng",
                "birth_date": "1980-7-30",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Delia Owens",
                "birth_date": "1949-4-4",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Michelle Obama",
                "birth_date": "1964-1-17",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Tara Westover",
                "birth_date": "1986-9-27",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "James Clear",
                "birth_date": None,
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Mark Manson",
                "birth_date": "1984-3-9",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Yuval Noah Harari",
                "birth_date": "1976-2-24",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Malcolm Gladwell",
                "birth_date": "1963-9-3",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Brené Brown",
                "birth_date": "1965-11-18",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Elizabeth Gilbert",
                "birth_date": "1969-7-18",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Cheryl Strayed",
                "birth_date": "1968-9-17",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Bill Bryson",
                "birth_date": "1951-12-8",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Michael Lewis",
                "birth_date": "1960-10-15",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Walter Isaacson",
                "birth_date": "1952-5-20",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Erik Larson",
                "birth_date": "1954-1-3",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "David McCullough",
                "birth_date": "1933-7-7",
                "death_date": "2022-8-7",
                "bio": None,
            },
            {
                "name": "Ron Chernow",
                "birth_date": "1949-3-3",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Jon Krakauer",
                "birth_date": "1954-4-12",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Rebecca Skloot",
                "birth_date": "1972-9-19",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Mary Roach",
                "birth_date": "1959-3-20",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Susan Cain",
                "birth_date": "1968-5-1",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Daniel Kahneman",
                "birth_date": "1934-3-5",
                "death_date": "2024-3-27",
                "bio": None,
            },
            {
                "name": "Stephen Hawking",
                "birth_date": "1942-1-8",
                "death_date": "2018-3-14",
                "bio": None,
            },
            {
                "name": "Carl Sagan",
                "birth_date": "1934-11-9",
                "death_date": "1996-12-20",
                "bio": None,
            },
            {
                "name": "Richard Dawkins",
                "birth_date": "1941-3-26",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Neil Gaiman",
                "birth_date": "1960-11-10",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Margaret Atwood",
                "birth_date": "1939-11-18",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Kazuo Ishiguro",
                "birth_date": "1954-11-8",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Haruki Murakami",
                "birth_date": "1949-1-12",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Cormac McCarthy",
                "birth_date": "1933-7-20",
                "death_date": "2023-6-13",
                "bio": None,
            },
            {
                "name": "Philip Pullman",
                "birth_date": "1946-10-19",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Ken Follett",
                "birth_date": "1949-6-5",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Diana Gabaldon",
                "birth_date": "1952-1-11",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Nicholas Sparks",
                "birth_date": "1965-12-31",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Jodi Picoult",
                "birth_date": "1966-5-19",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Stephenie Meyer",
                "birth_date": "1973-12-24",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Veronica Roth",
                "birth_date": "1988-8-19",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Rick Riordan",
                "birth_date": "1964-6-5",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Jeff Kinney",
                "birth_date": "1971-2-19",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Dav Pilkey",
                "birth_date": "1966-3-4",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Dr. Seuss",
                "birth_date": "1904-3-2",
                "death_date": "1991-9-24",
                "bio": None,
            },
            {
                "name": "Roald Dahl",
                "birth_date": "1916-9-13",
                "death_date": "1990-11-23",
                "bio": None,
            },
            {
                "name": "Shel Silverstein",
                "birth_date": "1930-9-25",
                "death_date": "1999-5-10",
                "bio": None,
            },
            {
                "name": "Eric Carle",
                "birth_date": "1929-6-25",
                "death_date": "2021-5-23",
                "bio": None,
            },
            {
                "name": "J.R.R. Tolkien",
                "birth_date": "1892-1-3",
                "death_date": "1973-9-2",
                "bio": None,
            },
            {
                "name": "George Orwell",
                "birth_date": "1903-6-25",
                "death_date": "1950-1-21",
                "bio": None,
            },
            {
                "name": "Agatha Christie",
                "birth_date": "1890-9-15",
                "death_date": "1976-1-12",
                "bio": None,
            },
            {
                "name": "Paulo Coelho",
                "birth_date": "1947-8-24",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Gabriel Garcia Marquez",
                "birth_date": "1927-3-6",
                "death_date": "2014-4-17",
                "bio": None,
            },
            {
                "name": "Umberto Eco",
                "birth_date": "1932-1-5",
                "death_date": "2016-2-19",
                "bio": None,
            },
            {
                "name": "Mario Puzo",
                "birth_date": "1920-10-15",
                "death_date": "1999-7-2",
                "bio": None,
            },
            {
                "name": "Arthur Golden",
                "birth_date": "1956-12-6",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Frank McCourt",
                "birth_date": "1930-8-19",
                "death_date": "2009-7-19",
                "bio": None,
            },
            {
                "name": "Mitch Albom",
                "birth_date": "1958-5-23",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "John Green",
                "birth_date": "1977-8-24",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "R.J. Palacio",
                "birth_date": "1963-7-13",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Angie Thomas",
                "birth_date": "1988-9-20",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Andy Griffiths",
                "birth_date": "1961-9-3",
                "death_date": None,
                "bio": None,
            },
            {
                "name": "Terry Denton",
                "birth_date": "1950-7-26",
                "death_date": None,
                "bio": None,
            },
        ]
        added_author_names = set()
        authors_to_add = []
        for data in authors_data:
            if data["name"] not in added_author_names:
                try:
                    birth_date_obj = (
                        datetime.strptime(data["birth_date"], "%Y-%m-%d").date()
                        if data["birth_date"]
                        else None
                    )
                    death_date_obj = (
                        datetime.strptime(data["death_date"], "%Y-%m-%d").date()
                        if data["death_date"]
                        else None
                    )
                    author = Author(
                        name=data["name"],
                        birth_date=birth_date_obj,
                        death_date=death_date_obj,
                        bio=data["bio"],
                    )
                    authors_to_add.append(author)
                    added_author_names.add(data["name"])
                except Exception:
                    continue
        if authors_to_add:
            db.session.bulk_save_objects(authors_to_add)
            db.session.commit()

    # Add books if the table is empty
    if Book.query.count() == 0:
        books_data = [
            {
                "isbn": "9780590353427",
                "title": "Harry Potter and the Sorcerer's Stone",
                "publication_date": "1998-9-1",
                "author_name": "J.K. Rowling",
            },
            {
                "isbn": "9780345806789",
                "title": "It",
                "publication_date": "1986-9-15",
                "author_name": "Stephen King",
            },
            {
                "isbn": "9780307474278",
                "title": "The Da Vinci Code",
                "publication_date": "2003-3-18",
                "author_name": "Dan Brown",
            },
            {
                "isbn": "9780440245969",
                "title": "The Firm",
                "publication_date": "1991-2-1",
                "author_name": "John Grisham",
            },
            {
                "isbn": "9780553593716",
                "title": "A Game of Thrones",
                "publication_date": "1996-8-1",
                "author_name": "George R.R. Martin",
            },
            {
                "isbn": "9780439023481",
                "title": "The Hunger Games",
                "publication_date": "2008-9-14",
                "author_name": "Suzanne Collins",
            },
            {
                "isbn": "9780345803481",
                "title": "Fifty Shades of Grey",
                "publication_date": "2012-4-3",
                "author_name": "E.L. James",
            },
            {
                "isbn": "9781594633669",
                "title": "The Girl on the Train",
                "publication_date": "2015-1-13",
                "author_name": "Paula Hawkins",
            },
            {
                "isbn": "9780307588371",
                "title": "Gone Girl",
                "publication_date": "2012-6-5",
                "author_name": "Gillian Flynn",
            },
            {
                "isbn": "9780307454546",
                "title": "The Girl with the Dragon Tattoo",
                "publication_date": "2008-9-16",
                "author_name": "Stieg Larsson",
            },
            {
                "isbn": "9781594631931",
                "title": "The Kite Runner",
                "publication_date": "2003-5-29",
                "author_name": "Khaled Hosseini",
            },
            {
                "isbn": "9780156027328",
                "title": "Life of Pi",
                "publication_date": "2001-9-11",
                "author_name": "Yann Martel",
            },
            {
                "isbn": "9780375842207",
                "title": "The Book Thief",
                "publication_date": "2006-3-14",
                "author_name": "Markus Zusak",
            },
            {
                "isbn": "9780156029438",
                "title": "The Time Traveler's Wife",
                "publication_date": "2003-9-1",
                "author_name": "Audrey Niffenegger",
            },
            {
                "isbn": "9780316666343",
                "title": "The Lovely Bones",
                "publication_date": "2002-7-3",
                "author_name": "Alice Sebold",
            },
            {
                "isbn": "9780425232200",
                "title": "The Help",
                "publication_date": "2009-2-10",
                "author_name": "Kathryn Stockett",
            },
            {
                "isbn": "9780804139021",
                "title": "The Martian",
                "publication_date": "2014-2-11",
                "author_name": "Andy Weir",
            },
            {
                "isbn": "9780307887436",
                "title": "Ready Player One",
                "publication_date": "2011-8-16",
                "author_name": "Ernest Cline",
            },
            {
                "isbn": "9780143127550",
                "title": "Little Fires Everywhere",
                "publication_date": "2017-9-12",
                "author_name": "Celeste Ng",
            },
            {
                "isbn": "9780735219090",
                "title": "Where the Crawdads Sing",
                "publication_date": "2018-8-14",
                "author_name": "Delia Owens",
            },
            {
                "isbn": "9781524763138",
                "title": "Becoming",
                "publication_date": "2018-11-13",
                "author_name": "Michelle Obama",
            },
            {
                "isbn": "9780399590504",
                "title": "Educated",
                "publication_date": "2018-2-20",
                "author_name": "Tara Westover",
            },
            {
                "isbn": "9780735211292",
                "title": "Atomic Habits",
                "publication_date": "2018-10-16",
                "author_name": "James Clear",
            },
            {
                "isbn": "9780062457714",
                "title": "The Subtle Art of Not Giving a F*ck",
                "publication_date": "2016-9-13",
                "author_name": "Mark Manson",
            },
            {
                "isbn": "9780062316097",
                "title": "Sapiens: A Brief History of Humankind",
                "publication_date": "2015-2-10",
                "author_name": "Yuval Noah Harari",
            },
            {
                "isbn": "9780062464316",
                "title": "Homo Deus: A Brief History of Tomorrow",
                "publication_date": "2017-2-21",
                "author_name": "Yuval Noah Harari",
            },
            {
                "isbn": "9780316017930",
                "title": "Outliers: The Story of Success",
                "publication_date": "2008-11-18",
                "author_name": "Malcolm Gladwell",
            },
            {
                "isbn": "9780316057905",
                "title": "The Tipping Point: How Little Things Can Make a Big Difference",
                "publication_date": "2000-3-1",
                "author_name": "Malcolm Gladwell",
            },
            {
                "isbn": "9781592408412",
                "title": "Daring Greatly",
                "publication_date": "2012-9-11",
                "author_name": "Brené Brown",
            },
            {
                "isbn": "9780143038412",
                "title": "Eat, Pray, Love",
                "publication_date": "2006-2-16",
                "author_name": "Elizabeth Gilbert",
            },
            {
                "isbn": "9780307592736",
                "title": "Wild: From Lost to Found on the Pacific Crest Trail",
                "publication_date": "2012-3-20",
                "author_name": "Cheryl Strayed",
            },
            {
                "isbn": "9780767908177",
                "title": "A Short History of Nearly Everything",
                "publication_date": "2003-5-6",
                "author_name": "Bill Bryson",
            },
            {
                "isbn": "9780393338829",
                "title": "The Big Short: Inside the Doomsday Machine",
                "publication_date": "2010-3-15",
                "author_name": "Michael Lewis",
            },
            {
                "isbn": "9781451648539",
                "title": "Steve Jobs",
                "publication_date": "2011-10-24",
                "author_name": "Walter Isaacson",
            },
            {
                "isbn": "9780375726671",
                "title": "The Devil in the White City",
                "publication_date": "2003-2-11",
                "author_name": "Erik Larson",
            },
            {
                "isbn": "9780743226719",
                "title": "John Adams",
                "publication_date": "2001-5-22",
                "author_name": "David McCullough",
            },
            {
                "isbn": "9781594200090",
                "title": "Alexander Hamilton",
                "publication_date": "2004-4-26",
                "author_name": "Ron Chernow",
            },
            {
                "isbn": "9780385486804",
                "title": "Into the Wild",
                "publication_date": "1996-1-12",
                "author_name": "Jon Krakauer",
            },
            {
                "isbn": "9781400052172",
                "title": "The Immortal Life of Henrietta Lacks",
                "publication_date": "2010-2-2",
                "author_name": "Rebecca Skloot",
            },
            {
                "isbn": "9780393324822",
                "title": "Stiff: The Curious Lives of Human Cadavers",
                "publication_date": "2003-4-17",
                "author_name": "Mary Roach",
            },
            {
                "isbn": "9780307352156",
                "title": "Quiet: The Power of Introverts in a World That Can't Stop Talking",
                "publication_date": "2012-1-24",
                "author_name": "Susan Cain",
            },
            {
                "isbn": "9780374533557",
                "title": "Thinking, Fast and Slow",
                "publication_date": "2011-10-25",
                "author_name": "Daniel Kahneman",
            },
            {
                "isbn": "9780553380163",
                "title": "A Brief History of Time",
                "publication_date": "1988-4-1",
                "author_name": "Stephen Hawking",
            },
            {
                "isbn": "9780345539434",
                "title": "Cosmos",
                "publication_date": "1980-9-28",
                "author_name": "Carl Sagan",
            },
            {
                "isbn": "9780618918249",
                "title": "The God Delusion",
                "publication_date": "2006-10-2",
                "author_name": "Richard Dawkins",
            },
            {
                "isbn": "9780393340996",
                "title": "American Gods",
                "publication_date": "2001-6-19",
                "author_name": "Neil Gaiman",
            },
            {
                "isbn": "9780385490818",
                "title": "The Handmaid's Tale",
                "publication_date": "1986-2-17",
                "author_name": "Margaret Atwood",
            },
            {
                "isbn": "9781400078776",
                "title": "Never Let Me Go",
                "publication_date": "2005-4-5",
                "author_name": "Kazuo Ishiguro",
            },
            {
                "isbn": "9780307389838",
                "title": "1Q84",
                "publication_date": "2011-10-25",
                "author_name": "Haruki Murakami",
            },
            {
                "isbn": "9780307387896",
                "title": "The Road",
                "publication_date": "2006-9-26",
                "author_name": "Cormac McCarthy",
            },
            {
                "isbn": "9780440418320",
                "title": "The Golden Compass",
                "publication_date": "1996-4-1",
                "author_name": "Philip Pullman",
            },
            {
                "isbn": "9780451419656",
                "title": "The Pillars of the Earth",
                "publication_date": "1989-10-12",
                "author_name": "Ken Follett",
            },
            {
                "isbn": "9780440212562",
                "title": "Outlander",
                "publication_date": "1991-6-1",
                "author_name": "Diana Gabaldon",
            },
            {
                "isbn": "9780446608955",
                "title": "The Notebook",
                "publication_date": "1996-10-1",
                "author_name": "Nicholas Sparks",
            },
            {
                "isbn": "9780743454537",
                "title": "My Sister's Keeper",
                "publication_date": "2004-4-6",
                "author_name": "Jodi Picoult",
            },
            {
                "isbn": "9780316015844",
                "title": "Twilight",
                "publication_date": "2005-10-5",
                "author_name": "Stephenie Meyer",
            },
            {
                "isbn": "9780062024039",
                "title": "Divergent",
                "publication_date": "2011-4-25",
                "author_name": "Veronica Roth",
            },
            {
                "isbn": "9780786838653",
                "title": "The Lightning Thief",
                "publication_date": "2005-7-1",
                "author_name": "Rick Riordan",
            },
            {
                "isbn": "9780810993136",
                "title": "Diary of a Wimpy Kid",
                "publication_date": "2007-4-1",
                "author_name": "Jeff Kinney",
            },
            {
                "isbn": "9780545581608",
                "title": "Dog Man",
                "publication_date": "2016-8-30",
                "author_name": "Dav Pilkey",
            },
            {
                "isbn": "9780394800011",
                "title": "Green Eggs and Ham",
                "publication_date": "1960-8-12",
                "author_name": "Dr. Seuss",
            },
            {
                "isbn": "9780142410318",
                "title": "Charlie and the Chocolate Factory",
                "publication_date": "1964-1-17",
                "author_name": "Roald Dahl",
            },
            {
                "isbn": "9780060256654",
                "title": "The Giving Tree",
                "publication_date": "1964-10-7",
                "author_name": "Shel Silverstein",
            },
            {
                "isbn": "9780399226908",
                "title": "The Very Hungry Caterpillar",
                "publication_date": "1969-6-3",
                "author_name": "Eric Carle",
            },
            {
                "isbn": "9780061122416",
                "title": "The Alchemist",
                "publication_date": "1988-1-1",
                "author_name": "Paulo Coelho",
            },
            {
                "isbn": "9780061120084",
                "title": "One Hundred Years of Solitude",
                "publication_date": "1967-5-30",
                "author_name": "Gabriel Garcia Marquez",
            },
            {
                "isbn": "9780151446476",
                "title": "The Name of the Rose",
                "publication_date": "1980-1-1",
                "author_name": "Umberto Eco",
            },
            {
                "isbn": "9780451205766",
                "title": "The Godfather",
                "publication_date": "1969-3-10",
                "author_name": "Mario Puzo",
            },
            {
                "isbn": "9780679781582",
                "title": "Memoirs of a Geisha",
                "publication_date": "1997-9-23",
                "author_name": "Arthur Golden",
            },
            {
                "isbn": "9780684842670",
                "title": "Angela's Ashes",
                "publication_date": "1996-9-5",
                "author_name": "Frank McCourt",
            },
            {
                "isbn": "9780751529814",
                "title": "Tuesdays with Morrie",
                "publication_date": "1997-8-18",
                "author_name": "Mitch Albom",
            },
            {
                "isbn": "9780525478812",
                "title": "The Fault in Our Stars",
                "publication_date": "2012-1-10",
                "author_name": "John Green",
            },
            {
                "isbn": "9780375869020",
                "title": "Wonder",
                "publication_date": "2012-2-14",
                "author_name": "R.J. Palacio",
            },
            {
                "isbn": "9780062498533",
                "title": "The Hate U Give",
                "publication_date": "2017-2-28",
                "author_name": "Angie Thomas",
            },
            {
                "isbn": "9781250026903",
                "title": "The 13-Story Treehouse",
                "publication_date": "2013-4-1",
                "author_name": "Andy Griffiths",
            },
        ]

        # Fetch authors from DB to link by ID
        authors_in_db = {author.name: author.id for author in Author.query.all()}
        books_to_add = []

        for data in books_data:
            author_id = authors_in_db.get(data["author_name"])
            if author_id:
                try:
                    publication_date_obj = (
                        datetime.strptime(data["publication_date"], "%Y-%m-%d").date()
                        if data["publication_date"]
                        else None
                    )
                    book = Book(
                        isbn=data["isbn"],
                        title=data["title"],
                        publication_date=publication_date_obj,
                        author_id=author_id,
                        synopsis=None,
                        cover_url=None,
                        rating=None,
                    )
                    books_to_add.append(book)
                except Exception:
                    continue
        if books_to_add:
            db.session.bulk_save_objects(books_to_add)
            db.session.commit()

    # Print a message when seeding is complete
    print("Database seeding check complete.")


def init_cli(app):
    app.cli.add_command(seed_db_command)
