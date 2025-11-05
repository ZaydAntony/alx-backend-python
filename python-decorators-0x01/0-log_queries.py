#!/usr/bin/python3
from datetime import datetime
import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] Executing SQL Query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] Query execution completed.\n")
        return result
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
users = fetch_all_users(query="SELECT * FROM users")
print(users)
