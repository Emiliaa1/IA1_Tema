from flask import Blueprint, render_template, session, request, redirect, url_for
from app.data.products import products

index_pages = Blueprint("index", __name__)

@index_pages.route("/")
def index_page():
    # Front page listing products
    return render_template("index.html", products=products)

@index_pages.route("/cart/add-item", methods=["GET"])
def add_to_cart():
    # Get product ID as int
    product_id = request.args.get("id", type=int)
    if not product_id:
        return redirect(url_for("index.index_page"))

    # Find the product
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return redirect(url_for("index.index_page"))

    # Load or initialize cart
    cart = session.get("cart", {})
    pid = str(product_id)

    # Increment or add
    if pid in cart:
        cart[pid]["count"] += 1
    else:
        cart[pid] = {
            "name":  product["name"],
            "price": product["price"],
            "count": 1
        }

    session["cart"] = cart
    return redirect(url_for("cart.cart_page"))