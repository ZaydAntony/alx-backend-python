#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator that yields ages of all users one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")

    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()


def average_age():
    """Compute average age using generator without loading entire dataset."""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    average_age()
