import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, send_from_directory
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'laksja9asd80asd09asd098asdsdkdf7763sdsds'
app.config['SESSION_TYPE'] = 'filesystem'


def get_connection():
    conn = sqlite3.connect('school.db')
    return conn

def check_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_connection()
        g.user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


def create_tables():
    db = get_connection()
    db.execute("""
        CREATE TABLE IF NOT EXISTS programs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        description TEXT)
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT,
        password TEXT,
        role TEXT,
        program_id INT,
        FOREIGN KEY (program_id) REFERENCES programs (id))
    """)

create_tables()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/account/<username>")
def account(username=None):
    return render_template("account.html", username=username)


@app.route("/subscribe", methods=['POST'])
def subscribe():
    return "<h1>" + request.form['email'] + "</h1>"

@app.route("/subscribe/form")
def subscribe_form():
    return render_template("subscribe.html")

@app.route('/add/program/form')
def add_program_form():
    return render_template('add_program_form.html');

@app.route('/add/program', methods=['POST'])
def add_program():
    db = get_connection()
    title = request.form['title']
    description = request.form['description']
    db.execute("INSERT INTO programs (title, description) VALUES (?, ?)", (title, description))
    db.commit()
    return redirect(url_for('programs'))

@app.route('/programs')
def programs():
    db = get_connection()
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM programs")
    return render_template('programs.html', programs=result)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_connection()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        error = None

        if user is None:
            error = "User does not exist"
        elif password != user[2]: 
            error = "Wrong credentials"
        else:
            session.clear()
            session['user_id'] = user[0]
            if user[3] == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('profile'))
        print(error)

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    check_user()
    if g.user is None:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/dashboard')
def dashboard():
    check_user()
    if g.user is None or g.user[3] != 'admin':
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/users/program')
def users_program():
    db = get_connection()
    cursor = db.cursor()
    result = cursor.execute("""SELECT u.id, u.username, p.title
                            FROM users u
                            INNER JOIN programs p ON u.program_id=p.id""")
    return render_template('users.html', users=result)

@app.route('/api/users/programs')
def api_users_program():
    db = get_connection()
    cursor = db.cursor()
    result = cursor.execute("""SELECT u.id, u.username, p.title
                            FROM users u
                            INNER JOIN programs p ON u.program_id=p.id""")
    return jsonify(result.fetchall())

@app.route('/images')
def images():
    return render_template('images.html')

@app.route('/user/images')
def user_images():
    return render_template('protected_images.html')

@app.route('/protected/<path:path>')
def protected(path):
    check_user()
    if g.user is None:
        return send_from_directory('protected', 'images/noaccess.jpg')
    return send_from_directory('protected', path)