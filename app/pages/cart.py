from flask import Blueprint, render_template, session, jsonify
from app.data.products import products

cart_pages = Blueprint("cart", __name__)

@cart_pages.route("/cart")
def cart_page():
    return render_template("cart.html")

@cart_pages.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", [])
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        cart.append(product)
        session["cart"] = cart
        return jsonify({"message": f"{product['name']} added to cart!"})
    return jsonify({"message": "Product not found!"}), 404