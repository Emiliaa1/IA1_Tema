from flask import Blueprint, render_template

cart_pages = Blueprint("cart", __name__)

@cart_pages.route("/cart")
def cart_page():
    return render_template("cart.html")