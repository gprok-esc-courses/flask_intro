import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g, send_from_directory
from flask import jsonify
from db import get_connection
from controllers.api_controller import api
from controllers.page_controller import page
from flask_jwt_extended import JWTManager
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'laksja9asd80asd09asd098asdsdkdf7763sdsds'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['JWT_SECRET_KEY'] = "ansuas8769asd98hsaodas98duasdhajdhosahsad7asdsaoi"
jwt = JWTManager(app)

app.register_blueprint(api)
app.register_blueprint(page)


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
    return redirect(url_for('page.home'))

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


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        check_user()
        if g.user is None:
            return "Only registered users can upload"
        if not os.path.isdir(app.root_path + '/uploads/' + g.user[1]):
            os.mkdir(app.root_path + '/uploads/' + g.user[1])
        file = request.files['file']
        if file.filename.split('.')[-1] != 'jpg':
            return "Only jpg images allowed"
        file.save(os.path.join(app.root_path + '/uploads/' + g.user[1] + '/', secure_filename(file.filename)))
        return "File Uploaded"