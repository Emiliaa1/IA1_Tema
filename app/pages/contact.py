from flask import Blueprint, render_template, session, request, redirect, url_for

contact_pages = Blueprint("contact", __name__)

@contact_pages.route("/contact")
def contact_page():
    # Display contact page
    return render_template("contact.html")