import pandas as pd
import sqlite3


def read_csv():
    return pd.read_csv("users.csv")


def save_users(connection, df):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    for index, row in df.iterrows():
        connection.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (row["Name"], row["Email"])
        )

    connection.commit()


def display_users(connection):
    users = connection.execute(
        "SELECT id, name, email FROM users"
    )

    for user in users:
        print(user)


def main():
    connection = None

    try:
        df = read_csv()

        connection = sqlite3.connect("users.db")

        save_users(connection, df)

        display_users(connection)

    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        print(f"CSV error: {e}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    main()
