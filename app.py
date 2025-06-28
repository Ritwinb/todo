from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory list to store tasks
tasks = []
task_id_counter = 1  # Unique ID generator

@app.route('/')
def home():
    return render_template('home.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    global task_id_counter
    content = request.form.get("task")
    if content:
        task = {"id": task_id_counter, "content": content}
        tasks.append(task)
        task_id_counter += 1
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('home'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    # Placeholder for complete logic, you can add status later
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
