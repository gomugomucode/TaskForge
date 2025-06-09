

from flask import Flask, render_template, request, redirect, url_for
from taskforge.task import Task
from taskforge.task_manager import TaskManager
from taskforge.database import init_db

init_db()


app = Flask(__name__)
tm = TaskManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('q', '')
    tasks = tm.search_tasks(query) if query else tm.list_tasks()
    return render_template('index.html', tasks=tasks, query=query)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        priority = request.form['priority']
        task = Task(title=title, deadline=deadline, priority=priority)
        tm.add_task(task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/delete/<int:index>')
@login_required
def delete_task(index):
    tm.delete_task(index)
    return redirect(url_for('index'))

@app.route('/toggle/<int:index>')
@login_required
def toggle_task(index):
    tm.toggle_task(index)  
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
