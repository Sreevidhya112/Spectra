from flask import Flask, render_template, request, redirect, url_for
import pickle
import os
from datetime import datetime

app = Flask(__name__)

TASK_FILE = "tasks.pkl"

class Task:
    def __init__(self, description, due_date, priority):
        self.description = description
        self.due_date = due_date
        self.priority = priority if priority.lower() in ["low", "medium", "high"] else "Meh"
        self.is_completed = False

    def __str__(self):
        status = "✅ Done (or at least we say so)" if self.is_completed else "🕓 Procrastinating..."
        return f"{self.description} (Due: {self.due_date}, Priority: {self.priority}, Status: {status})"

def load_tasks():
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "rb") as f:
                return pickle.load(f)
        except:
            print("❌ Couldn't load your glorious task history.")
            return []
    return []

def save_tasks(tasks):
    try:
        with open(TASK_FILE, "wb") as f:
            pickle.dump(tasks, f)
    except:
        print("💥 Save failed. Oops.")

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    due_date = request.form['due_date']
    priority = request.form['priority']
    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    except:
        print("Invalid date. Using far future instead.")
        due_date_obj = datetime(2099, 12, 31).date()

    task = Task(description, due_date_obj, priority)
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id].is_completed = True
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

