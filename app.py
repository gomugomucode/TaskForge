

from taskforge.task import Task
from taskforge.task_manager import TaskManager
from taskforge.database import init_db
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# database for tasks
init_db()


app = Flask(__name__)
tm = TaskManager()
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# User Model
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# load the user
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return User(*user) if user else None

# database setup for user data
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()
init_db()

# Routes
# ---------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash("Registered successfully. Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Try logging in.", "danger")
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            user_obj = User(*user)
            login_user(user_obj)
            session['username'] = user_obj.username  # ✅ FIXED: Use user_obj instead of user
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    # Clear only specific session keys if needed
    session.pop('username', None)  # Remove username from session
    session.pop('user_id', None)   # Remove user_id if you store it
    
    logout_user()  # This handles Flask-Login's session cleanup
    flash("Logged out.", "info")
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    query = request.args.get('q', '')
    tasks = tm.search_tasks(query) if query else tm.list_tasks()
    return render_template('index.html', username=current_user.username, tasks=tasks, query=query)

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
