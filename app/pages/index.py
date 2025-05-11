from flask import Blueprint, render_template
from app.data.products import products

index_pages = Blueprint("index", __name__)

@index_pages.route("/")
def index_page():
    return render_template("index.html", products=products)