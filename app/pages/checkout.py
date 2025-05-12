import os
import json
from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, request

checkout_pages = Blueprint("checkout", __name__)

@checkout_pages.route("/checkout", methods=["GET", "POST"])
def checkout_page():
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("cart.cart_page"))

    # Compute subtotal and total price (including tax)
    subtotal = sum(item["price"] * item["count"] for item in cart.values())
    tax_rate = 0.10  # 10% tax
    taxes = subtotal * tax_rate
    total_price = subtotal + taxes

    if request.method == "POST":
        # Collect form data
        order_data = {
            "full_name": request.form.get("full_name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "payment_method": request.form.get("payment_method"),
            "cart": cart,
            "subtotal": subtotal,
            "taxes": taxes,
            "total_price": total_price,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Print order data to the console
        print(json.dumps(order_data, indent=4))

        # Save order data to a file
        os.makedirs("submitted-data", exist_ok=True)
        order_file = f"submitted-data/order_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        with open(order_file, "w") as f:
            json.dump(order_data, f, indent=4)

        # Clear the cart and redirect to success page
        session.pop("cart", None)
        return redirect(url_for("checkout.checkout_success"))

    return render_template("checkout.html", cart=cart, subtotal=subtotal, taxes=taxes, total_price=total_price)

@checkout_pages.route("/checkout/success")
def checkout_success():
    return render_template("checkout_success.html")