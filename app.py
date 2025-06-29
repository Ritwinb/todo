from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'tasks.db'

# Create tasks table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS tasks')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

# Get all tasks
def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, completed FROM tasks")
        tasks = cursor.fetchall()
        return [{"id": row[0], "content": row[1], "completed": bool(row[2])} for row in tasks]


# Add a task
def add_task_to_db(content):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (content) VALUES (?)", (content,))
        conn.commit()

# Delete a task
def delete_task_from_db(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

@app.route('/')
def home():
    tasks = get_tasks()
    return render_template('home.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    content = request.form.get("task")
    if content:
        add_task_to_db(content)
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    delete_task_from_db(task_id)
    return redirect(url_for('home'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    complete_task_in_db(task_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        init_db()
    app.run(debug=True)
