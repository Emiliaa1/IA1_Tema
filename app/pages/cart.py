from flask import Blueprint, render_template, session, request, redirect, url_for

cart_pages = Blueprint("cart", __name__)

@cart_pages.route("/cart")
def cart_page():
    cart = session.get("cart", {})
    # Compute total
    total_price = sum(item["price"] * item["count"] for item in cart.values())
    return render_template("cart.html", cart=cart, total_price=total_price)

@cart_pages.route("/cart/empty", methods=["GET"])
def empty_cart():
    session.pop("cart", None)  # Clear the cart from the session
    return redirect(url_for("cart.cart_page"))

# Remove item from cart
@cart_pages.route("/cart/remove-item", methods=["GET"])
def remove_from_cart():
    pid = request.args.get("id")
    if pid:
        cart = session.get("cart", {})
        cart.pop(pid, None)
        session["cart"] = cart
    return redirect(url_for("cart.cart_page"))

# Decrement item count in cart
@cart_pages.route("/cart/decrease-item", methods=["GET"])
def decrease_item():
    pid = request.args.get("id")
    if pid:
        cart = session.get("cart", {})
        if pid in cart:
            # Decrement or remove
            if cart[pid]["count"] > 1:
                cart[pid]["count"] -= 1
            else:
                cart.pop(pid)
            session["cart"] = cart
    return redirect(url_for("cart.cart_page"))

# Reuse add-to-cart for increasing quantity on cart page
@cart_pages.route("/cart/add-item", methods=["GET"])
def add_to_cart_from_cart():
    pid = request.args.get("id")
    if pid:
        cart = session.get("cart", {})
        if pid in cart:
            cart[pid]["count"] += 1
            session["cart"] = cart
    return redirect(url_for("cart.cart_page"))