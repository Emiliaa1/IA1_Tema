from flask import Blueprint, render_template, request
from app.data.products import products

products_pages = Blueprint("products", __name__)

@products_pages.route("/products", methods=["GET"])
def products_page():
    # Get filter and sort parameters
    category = request.args.get("category", "")
    sort = request.args.get("sort", "name")

    # Ensure all products have a category key
    for product in products:
        product.setdefault("category", "Uncategorized")

    # Filter products by category
    filtered_products = [p for p in products if not category or p["category"] == category]

    # Sort products
    if sort == "price_asc":
        filtered_products.sort(key=lambda x: x["price"])
    elif sort == "price_desc":
        filtered_products.sort(key=lambda x: x["price"], reverse=True)
    else:  # Default sort by name
        filtered_products.sort(key=lambda x: x["name"])

    # Get unique categories for the filter dropdown
    categories = sorted(set(p["category"] for p in products))

    return render_template(
        "products.html",
        products=filtered_products,
        categories=categories,
        selected_category=category,
        sort=sort
    )