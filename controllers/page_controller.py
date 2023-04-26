from flask import Blueprint, render_template

page = Blueprint('page', __name__)

@page.before_request
def hook():
    print("Page hook called")

@page.route("/")
def home():
    return render_template('index.html')

@page.route("/about")
def about():
    return render_template('about.html')


@page.route("/account/<username>")
def account(username=None):
    return render_template("account.html", username=username)