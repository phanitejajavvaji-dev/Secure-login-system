from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username,password)
            )
            conn.commit()
            return redirect('/login')
        except:
            return "User already exists"

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect('/dashboard')

        return "Invalid Credentials"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html',
                               username=session['user'])

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
