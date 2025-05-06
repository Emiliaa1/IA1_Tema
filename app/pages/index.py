from flask import session, Blueprint, request, redirect, render_template

index_pages = Blueprint("index", __name__)

@index_pages.route("/")
def index_page():
    #if not session.get("auth", False):
    #    return redirect("/login", code=302)
    return render_template("index.html")

@index_pages.route("/contact")
def contact_page():
    return render_template("contact.html")
