import sqlite3

# Database setup
def create_connection():
    conn = sqlite3.connect('todo_list.db')
    return conn

def create_table():
    conn = create_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority INTEGER,
                status TEXT,
                category TEXT
            );
        ''')
    conn.close()

create_table()

# CRUD operations
def add_task(title, description, due_date, priority, status, category):
    conn = create_connection()
    with conn:
        conn.execute('''
            INSERT INTO tasks (title, description, due_date, priority, status, category)
            VALUES (?, ?, ?, ?, ?, ?);
        ''', (title, description, due_date, priority, status, category))
    conn.close()

def delete_task(task_id):
    conn = create_connection()
    with conn:
        conn.execute('DELETE FROM tasks WHERE id = ?;', (task_id,))
    conn.close()

def update_task(task_id, title, description, due_date, priority, status, category):
    conn = create_connection()
    with conn:
        conn.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, priority = ?, status = ?, category = ?
            WHERE id = ?;
        ''', (title, description, due_date, priority, status, category, task_id))
    conn.close()

def get_tasks(filter_by=None, value=None):
    conn = create_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM tasks'
    if filter_by:
        query += f' WHERE {filter_by} = ?'
        cursor.execute(query, (value,))
    else:
        cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Command-line interface
def display_menu():
    print("\nTo-Do List Application")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Update Task")
    print("4. View Tasks")
    print("5. Mark Task as Complete")
    print("6. Filter Tasks")
    print("7. Exit")

def get_task_details():
    title = input("Title: ")
    description = input("Description: ")
    due_date = input("Due Date (YYYY-MM-DD): ")
    priority = int(input("Priority (1-5): "))
    status = input("Status (Not Started/In Progress/Complete): ")
    category = input("Category: ")
    return title, description, due_date, priority, status, category

def main():
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            title, description, due_date, priority, status, category = get_task_details()
            add_task(title, description, due_date, priority, status, category)
            print("Task added successfully!")
        
        elif choice == 2:
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
            print("Task deleted successfully!")
        
        elif choice == 3:
            task_id = int(input("Enter task ID to update: "))
            title, description, due_date, priority, status, category = get_task_details()
            update_task(task_id, title, description, due_date, priority, status, category)
            print("Task updated successfully!")
        
        elif choice == 4:
            tasks = get_tasks()
            for task in tasks:
                print(task)
        
        elif choice == 5:
            task_id = int(input("Enter task ID to mark as complete: "))
            update_task(task_id, None, None, None, None, "Complete", None)
            print("Task marked as complete!")
        
        elif choice == 6:
            filter_by = input("Filter by (status/category/due_date): ")
            value = input(f"Enter {filter_by}: ")
            tasks = get_tasks(filter_by, value)
            for task in tasks:
                print(task)
        
        elif choice == 7:
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
