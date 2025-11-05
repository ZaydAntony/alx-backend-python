#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to MySQL server (no specific database yet)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=.env(PASSWORD),  # adjust if needed
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=env(PASSWORD),
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,0) NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data from CSV into the user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
