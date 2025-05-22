import sqlite3
import threading

# ensure thread-safety
_db_lock = threading.Lock()
DB_PATH = "siteia1_simple.db"

# initialize SQLite database
def init_db():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # orders: one row per checkout
        c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name    TEXT NOT NULL,
            email        TEXT NOT NULL,
            phone        TEXT NOT NULL,
            address      TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            subtotal     REAL NOT NULL,
            taxes        REAL NOT NULL,
            total_price  REAL NOT NULL,
            timestamp    TEXT NOT NULL
        )
        """)
        # order_items: one row per product line
        c.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id   INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            name       TEXT NOT NULL,
            price      REAL NOT NULL,
            quantity   INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
        """)
        conn.commit()
        conn.close()

# Initialize on import
init_db()

from datetime import datetime
import pprint
from flask import Blueprint, render_template, session, redirect, url_for, request, flash

checkout_pages = Blueprint("checkout", __name__)

@checkout_pages.route("/checkout", methods=["GET", "POST"])
def checkout_page():
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("cart.cart_page"))

    # pricing
    subtotal    = sum(item["price"] * item["count"] for item in cart.values())
    tax_rate    = 0.10
    taxes       = subtotal * tax_rate
    total_price = subtotal + taxes

    if request.method == "POST":
        # Prepare a human-readable dump for console
        order_info = {
            "full_name":      request.form.get("full_name", ""),
            "email":          request.form.get("email", ""),
            "phone":          request.form.get("phone", ""),
            "address":        request.form.get("address", ""),
            "payment_method": request.form.get("payment_method", ""),
            "subtotal":       subtotal,
            "taxes":          taxes,
            "total_price":    total_price,
            "timestamp":      datetime.utcnow().isoformat(),
            "cart_items": [
                {
                    "product_id": int(pid),
                    "name":        item["name"],
                    "unit_price":  item["price"],
                    "quantity":    item["count"],
                    "line_total":  item["price"] * item["count"]
                }
                for pid, item in cart.items()
            ]
        }
        pprint.pprint(order_info)

        # Persist to SQLite
        with _db_lock:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            # insert into orders
            c.execute("""
              INSERT INTO orders
                (full_name, email, phone, address, payment_method,
                 subtotal, taxes, total_price, timestamp)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
              order_info["full_name"],
              order_info["email"],
              order_info["phone"],
              order_info["address"],
              order_info["payment_method"],
              order_info["subtotal"],
              order_info["taxes"],
              order_info["total_price"],
              order_info["timestamp"]
            ))
            order_id = c.lastrowid

            # insert each line item
            for item in order_info["cart_items"]:
                c.execute("""
                  INSERT INTO order_items
                    (order_id, product_id, name, price, quantity)
                  VALUES (?, ?, ?, ?, ?)
                """, (
                  order_id,
                  item["product_id"],
                  item["name"],
                  item["unit_price"],
                  item["quantity"]
                ))

            conn.commit()
            conn.close()

        # Clear cart and redirect
        session.pop("cart", None)
        flash("Thank you! Your order has been placed.", "success")
        return redirect(url_for("checkout.checkout_success"))

    # GET: render form
    return render_template(
        "checkout.html",
        cart        = cart,
        subtotal    = subtotal,
        taxes       = taxes,
        total_price = total_price
    )

# redirect to success page
@checkout_pages.route("/checkout/success")
def checkout_success():
    return render_template("checkout_success.html")
