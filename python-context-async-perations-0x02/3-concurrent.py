# File: 3-concurrent.py
import asyncio
import aiosqlite

async def async_fetch_users(db_name="users.db"):
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users;") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users(db_name="users.db"):
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40;") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    """Run both queries concurrently."""
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:", users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
