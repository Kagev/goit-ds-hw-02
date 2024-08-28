import sqlite3
from faker import Faker

fake = Faker()

def create_tables(cursor):
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        ''')

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        raise

def populate_tables(cursor):
    try:
        cursor.execute('DELETE FROM status')

        statuses = ['new', 'in progress', 'completed']
        cursor.executemany('INSERT INTO status (name) VALUES (?)', [(status,) for status in statuses])

        users = [(fake.name(), fake.email()) for _ in range(10)]
        cursor.executemany('INSERT INTO users (fullname, email) VALUES (?, ?)', users)


        cursor.execute('SELECT id FROM users')
        user_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute('SELECT id FROM status')
        status_ids = [row[0] for row in cursor.fetchall()]

        tasks = []
        for _ in range(20):
            title = fake.sentence()
            description = fake.text()
            status_id = fake.random.choice(status_ids)
            user_id = fake.random.choice(user_ids)
            tasks.append((title, description, status_id, user_id))

        cursor.executemany('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)', tasks)

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        conn.commit()

if __name__ == "__main__":
    try:
        conn = sqlite3.connect('db/task_management.db')
        cursor = conn.cursor()

        create_tables(cursor)
        populate_tables(cursor)

    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    finally:
        if conn:
            conn.close()
