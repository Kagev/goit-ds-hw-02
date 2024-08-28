import sqlite3

def get_user_tasks(user_id):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM tasks WHERE user_id = ?'
    cursor.execute(query, (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_by_status(status_name):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT * FROM tasks
    WHERE status_id = (SELECT id FROM status WHERE name = ?)
    '''
    cursor.execute(query, (status_name,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, new_status):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    UPDATE tasks
    SET status_id = (SELECT id FROM status WHERE name = ?)
    WHERE id = ?
    '''
    cursor.execute(query, (new_status, task_id))
    conn.commit()
    conn.close()

def get_users_without_tasks():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT * FROM users
    WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
    '''
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return users

def add_new_task(title, description, status_name, user_id):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?)
    '''
    cursor.execute(query, (title, description, status_name, user_id))
    conn.commit()
    conn.close()

def get_incomplete_tasks():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT * FROM tasks
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    '''
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = 'DELETE FROM tasks WHERE id = ?'
    cursor.execute(query, (task_id,))
    conn.commit()
    conn.close()

def find_users_by_email(email_pattern):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE email LIKE ?'
    cursor.execute(query, (email_pattern,))
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_name(user_id, new_name):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = 'UPDATE users SET fullname = ? WHERE id = ?'
    cursor.execute(query, (new_name, user_id))
    conn.commit()
    conn.close()

def count_tasks_by_status():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT s.name, COUNT(t.id) AS task_count
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name
    '''
    cursor.execute(query)
    counts = cursor.fetchall()
    conn.close()
    return counts

def get_tasks_by_email_domain(email_domain):
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT t.*
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE ?
    '''
    cursor.execute(query, (f'%{email_domain}%',))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_without_description():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM tasks WHERE description IS NULL OR description = '' '
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_users_tasks_in_progress():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT u.fullname, t.title
    FROM users u
    JOIN tasks t ON u.id = t.user_id
    WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress')
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_user_task_count():
    conn = sqlite3.connect('db/task_management.db')
    cursor = conn.cursor()
    query = '''
    SELECT u.fullname, COUNT(t.id) AS task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.fullname
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def main():
    # Example usages
    user_id = 1
    print("Tasks for user with ID 1:", get_user_tasks(user_id))

    status_name = 'new'
    print("Tasks with status 'new':", get_tasks_by_status(status_name))

    task_id = 2
    new_status = 'in progress'
    update_task_status(task_id, new_status)
    print(f"Task {task_id} status updated to '{new_status}'")

    print("Users without tasks:", get_users_without_tasks())

    title = 'New Task'
    description = 'Task Description'
    add_new_task(title, description, status_name, user_id)
    print(f"Added new task '{title}' for user {user_id}")

    print("Incomplete tasks:", get_incomplete_tasks())

    task_id = 3
    delete_task(task_id)
    print(f"Task {task_id} deleted")

    email_pattern = '%@example.com'
    print("Users with email pattern '@example.com':", find_users_by_email(email_pattern))

    new_name = 'Updated Name'
    update_user_name(user_id, new_name)
    print(f"User {user_id}'s name updated to '{new_name}'")

    print("Task count by status:", count_tasks_by_status())

    email_domain = 'example.com'
    print(f"Tasks for users with email domain '{email_domain}':", get_tasks_by_email_domain(email_domain))

    print("Tasks without description:", get_tasks_without_description())

    print("Users and tasks in progress:", get_users_tasks_in_progress())

    print("User task counts:", get_user_task_count())

if __name__ == '__main__':
    main()
