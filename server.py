from flask import Flask, render_template, request

app = Flask(__name__)

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
