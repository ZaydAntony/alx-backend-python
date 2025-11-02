#!/usr/bin/python3
import seed


def stream_users_in_batches(batch_size):
    """Yields users in batches."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) FROM user_data;")
    total_rows = cursor.fetchone()['COUNT(*)']

    for offset in range(0, total_rows, batch_size):
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset};")
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes each batch: filters users with age > 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
