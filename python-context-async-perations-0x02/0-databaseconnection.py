# File: 0-databaseconnection.py
import sqlite3

class DatabaseConnection:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    # Example usage
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        print(results)
