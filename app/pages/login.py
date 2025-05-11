from flask import Blueprint, render_template

login_pages = Blueprint("login", __name__)

@login_pages.route("/login")
def login_page():
    return render_template("login.html")