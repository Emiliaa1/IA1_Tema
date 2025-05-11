from flask import session, Blueprint, request, redirect, render_template

index_pages = Blueprint("index", __name__)

@index_pages.route("/")
def index_page():
    return render_template("index.html")

