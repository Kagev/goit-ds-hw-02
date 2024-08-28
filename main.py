import sqlite3


def get_tasks(cursor):
    cursor.execute('SELECT id, title, description FROM tasks')
    return cursor.fetchall()


def get_users(cursor):
    cursor.execute('SELECT id, fullname FROM users')
    return cursor.fetchall()


def get_statuses(cursor):
    cursor.execute('SELECT id, name FROM status')
    return cursor.fetchall()


def view_tasks(cursor):
    tasks = get_tasks(cursor)
    if tasks:
        print("Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2][:50]}...")
    else:
        print("No tasks found.")


def view_users(cursor):
    users = get_users(cursor)
    if users:
        print("Users:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}")
    else:
        print("No users found.")


def view_statuses(cursor):
    statuses = get_statuses(cursor)
    if statuses:
        print("Statuses:")
        for status in statuses:
            print(f"ID: {status[0]}, Name: {status[1]}")
    else:
        print("No statuses found.")


def search_user(cursor):
    search_query = input("Enter the email, name, or ID of the user to search: ").strip()

    try:
        if search_query.isdigit():
            user_id = int(search_query)
            cursor.execute('SELECT id, fullname, email FROM users WHERE id = ?', (user_id,))
        else:
            cursor.execute('SELECT id, fullname, email FROM users WHERE email = ?', (search_query,))
            user = cursor.fetchone()
            if user:
                print(f"User found: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
                return

            cursor.execute('SELECT id, fullname, email FROM users WHERE fullname LIKE ?', (f'%{search_query}%',))

        user = cursor.fetchone()
        if user:
            print(f"User found: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        else:
            print("User not found.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def delete_user(cursor, conn):
    email = input("Enter the email of the user to delete: ")
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    conn.commit()
    if cursor.rowcount > 0:
        print("User and associated tasks deleted successfully.")
    else:
        print("User not found.")


def main_menu(cursor, conn):
    while True:
        print("\nMain Menu:")
        print("1. View Tasks")
        print("2. View Users")
        print("3. View Statuses")
        print("4. Search User")
        print("5. Delete User")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            view_tasks(cursor)
        elif choice == "2":
            view_users(cursor)
        elif choice == "3":
            view_statuses(cursor)
        elif choice == "4":
            search_user(cursor)
        elif choice == "5":
            delete_user(cursor, conn)
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()

    main_menu(cursor, conn)

    conn.close()


if __name__ == "__main__":
    main()
