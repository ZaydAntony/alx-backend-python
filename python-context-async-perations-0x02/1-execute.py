# File: 1-execute.py
import sqlite3

class ExecuteQuery:
    """Context manager to execute a query with parameters."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
       
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?;"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print(results)
