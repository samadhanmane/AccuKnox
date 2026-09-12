import requests
import sqlite3


API_URL = "https://openlibrary.org/search.json?q=python&limit=10"
DB_NAME = "books.db"


def fetch_books():
    try:
        response = requests.get(API_URL, timeout=60)
        response.raise_for_status()

        data = response.json()
        return data.get("docs", [])

    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return []

    except ValueError:
        print("Invalid JSON response from API.")
        return []


def create_database(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            publication_year INTEGER
        )
    """)


def save_books(connection, books):
    try:
        for book in books:
            title = book.get("title")
            if not title:
                continue
            authors = book.get("author_name", [])
            author = ", ".join(authors)
            year = book.get("first_publish_year")

            connection.execute("""
                INSERT INTO books (title, author, publication_year)
                VALUES (?, ?, ?)
                """,(title, author, year)
            )

        connection.commit()

    except sqlite3.Error as e:
        connection.rollback()
        print(f"Database error: {e}")


def display_books(connection):
    books = connection.execute(
        "SELECT id, title, author, publication_year FROM books"
    )

    for i in books:
        print(i)


def main():
    books = fetch_books()

    if not books:
        print("No books received from the API.")
        return

    connection = None

    try:
        connection = sqlite3.connect(DB_NAME)

        create_database(connection)
        save_books(connection, books)
        display_books(connection)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    main()
