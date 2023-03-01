import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_connection():
    conn = sqlite3.connect('school.db')
    return conn

def create_tables():
    db = get_connection()
    db.execute("""
        CREATE TABLE IF NOT EXISTS programs 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        description TEXT)
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
