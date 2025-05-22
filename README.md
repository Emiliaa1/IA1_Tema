# Maison Verdite – Sustainable Clothing Shop

## Project Overview

Maison Verdite is a web application for a sustainable clothing shop, built with Flask. It allows users to browse products, filter and sort them, add items to a cart, and complete a checkout process. The site is designed to be clean, user-friendly, and easily deployable via Docker.

---

## Features

- **Product Catalog:** Dynamic product listing with images, descriptions, categories, and prices.
- **Filtering & Sorting:** Users can filter products by category and sort by name or price.
- **Shopping Cart:** Add, remove, and update quantities of products. Cart persists across sessions.
- **Checkout:** Collects user contact and delivery information, displays order summary, and stores orders in a SQLite database.
- **Contact Page:** Stylish, informative contact page with company info and a map.
- **Responsive Design:** Uses Bootstrap for a modern, responsive interface.
- **Dockerized:** Easily build and run the app in a container.

---

## Implementation & Design Choices

- **Flask:** Chosen for its simplicity and flexibility for small-to-medium web apps.
- **Jinja2 Templates:** For dynamic HTML rendering and clean separation of logic and presentation.
- **Bootstrap:** For rapid, responsive, and visually appealing UI development.
- **SQLite:** Lightweight, file-based database suitable for small deployments and easy sharing.
- **Session-based Cart:** Cart data is stored in the Flask session, making it persistent for each user.
- **Cache-Control Headers:** Ensures cart and order data is always up-to-date, even when using browser navigation buttons.

---

## Third-Party Libraries

- **Flask** – Core web framework.
- **Bootstrap** – Frontend framework for responsive design.
- **(Optional) FontAwesome** – For icons on the contact page and elsewhere.

**Why:**  
These libraries are widely used, well-documented, and make development faster and more reliable.  
Direct use of `sqlite3` keeps the stack simple and avoids unnecessary abstraction for a small project.

---

## Challenges & Solutions

- **Session Consistency:** Ensuring the cart count is always correct, even after browser navigation.  
  _Solution:_ Added cache-control headers to force fresh page loads.
- **Database Initialization:** Guaranteeing the database and tables exist before first use.  
  _Solution:_ Called the DB/table creation function at app startup.

---

## Bonuses & Improvements

- **Product Filtering & Sorting:** Users can filter by category and sort by price or name.
- **Order Storage in Database:** Orders are saved in a SQLite database, not just as files.
- **"Empty Cart" Button:** Users can clear their cart with a single click.
- **Cart Count in Navbar:** The number of items in the cart is always visible.
- **Cart functionality and layout:** When there are too many items in the cart the products section becomes a scrollable list. Items can be incremented/decremented individually in the cart page, while updating at the same time the order summary and price. 

---

## How to Run

1. **Build the Docker image:**
   ```sh
   docker build -t iap1-tema ./
2. **Run the container:**
   ```sh
   docker run -p 5000:5000 -it iap1-tema
3. **Visit:**
   ```sh
   http://localhost:5000