"""
ShopFlow — Complete E-Commerce Store
Flask + SQLite (MySQL schema included in database/schema.sql)
Run:  python app/app.py   then open http://127.0.0.1:5000

Demo accounts (created automatically on first run):
  Admin:    admin@shopflow.com / admin123
  Customer: demo@shopflow.com  / demo123
"""
import os
import sqlite3
from functools import wraps

from flask import (Flask, g, redirect, render_template, request,
                   session, url_for, flash, abort)
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "shopflow.db")

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"),
            static_folder=os.path.join(BASE_DIR, "static"))
app.secret_key = "shopflow-dev-secret-change-in-production"
app.config["DATABASE"] = DB_PATH

# ---------------------------------------------------------------- DB helpers
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

PRODUCTS = [
    ("Wireless Noise-Cancelling Headphones", "Bluetooth 5.3 headphones with 40-hour battery, deep bass and a built-in mic for calls.", 2999, 4499, "Electronics", 24, 4.8),
    ("Smartwatch Fit Pro", "AMOLED display, heart-rate + sleep tracking, step counter, 7-day battery, water resistant.", 2499, 3999, "Electronics", 18, 4.6),
    ("Mechanical Keyboard RGB", "Hot-swappable mechanical keyboard with RGB backlight, blue switches and detachable cable.", 2799, 3499, "Electronics", 32, 4.7),
    ("Portable Bluetooth Speaker", "20W waterproof speaker with 18-hour playtime, perfect for home and outdoor use.", 1799, 2599, "Electronics", 40, 4.5),
    ("Men's Cotton Casual Shirt", "Breathable 100% cotton shirt, slim fit, available in blue and white. Machine washable.", 899, 1499, "Fashion", 55, 4.4),
    ("Women's Running Shoes", "Lightweight running shoes with cushioned sole and breathable mesh upper.", 1999, 3299, "Fashion", 27, 4.7),
    ("Classic Denim Jacket", "Durable denim jacket with button front and chest pockets. A wardrobe staple.", 1599, 2499, "Fashion", 15, 4.6),
    ("Leather Wallet — Bifold", "Genuine leather bifold wallet with 8 card slots, 2 currency pockets and RFID blocking.", 699, 1199, "Fashion", 60, 4.5),
    ("Ceramic Dinner Set (16 pcs)", "16-piece ceramic dinner set for 4 people — plates, bowls and cups in a modern matte finish.", 2299, 3499, "Home & Living", 12, 4.8),
    ("LED Desk Lamp with USB Charging", "Adjustable LED desk lamp with 3 colour modes, touch control and a USB charging port.", 999, 1699, "Home & Living", 38, 4.6),
    ("Cotton Bedsheet — Queen Size", "300-thread-count cotton bedsheet with 2 pillow covers. Soft, breathable and fade-resistant.", 1199, 1999, "Home & Living", 22, 4.4),
    ("Stainless Steel Water Bottle 1L", "Double-wall insulated steel bottle, keeps drinks cold 24 hours / hot 12 hours. Leak-proof.", 549, 899, "Home & Living", 80, 4.7),
    ("Yoga Mat — Anti-Slip 6mm", "6mm thick anti-slip yoga mat with carry strap. Extra cushioning for knees and joints.", 799, 1299, "Sports & Fitness", 45, 4.5),
    ("Adjustable Dumbbell Set 20kg", "Pair of adjustable dumbbells (2.5–10kg each) with non-slip grips for home workouts.", 3499, 5499, "Sports & Fitness", 9, 4.8),
    ("Cricket Bat — Kashmir Willow", "Full-size Kashmir willow cricket bat with grip and protective cover. For tennis-ball cricket.", 1299, 1999, "Sports & Fitness", 20, 4.3),
    ("Gym Duffel Bag 35L", "35L waterproof gym bag with shoe compartment, wet pocket and adjustable shoulder strap.", 1099, 1799, "Sports & Fitness", 33, 4.6),
]

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(open(os.path.join(BASE_DIR, "database", "schema.sql")).read())
    if db.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO products (name, description, price, old_price, category, stock, rating) VALUES (?,?,?,?,?,?,?)",
            PRODUCTS)
    if db.execute("SELECT COUNT(*) FROM users WHERE email='admin@shopflow.com'").fetchone()[0] == 0:
        db.execute("INSERT INTO users (name, email, password_hash, is_admin) VALUES (?,?,?,1)",
                   ("Shop Admin", "admin@shopflow.com", generate_password_hash("admin123")))
    if db.execute("SELECT COUNT(*) FROM users WHERE email='demo@shopflow.com'").fetchone()[0] == 0:
        db.execute("INSERT INTO users (name, email, password_hash, is_admin) VALUES (?,?,?,0)",
                   ("Demo Customer", "demo@shopflow.com", generate_password_hash("demo123")))
    db.commit()
    db.close()

# ---------------------------------------------------------------- auth helpers
def current_user():
    if "user_id" not in session:
        return None
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please log in first.", "error")
            return redirect(url_for("login", next=request.path), code=303)
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or not user["is_admin"]:
            flash("Admin access only.", "error")
            return redirect(url_for("login"), code=303)
        return f(*args, **kwargs)
    return wrapper

@app.context_processor
def inject_globals():
    cart = session.get("cart", {})
    return {"current_user": current_user(), "cart_count": sum(cart.values()),
            "inr": lambda n: f"₹{n:,.0f}"}

# ---------------------------------------------------------------- storefront
@app.route("/")
def index():
    db = get_db()
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    sort = request.args.get("sort", "newest")
    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if category:
        sql += " AND category=?"
        params.append(category)
    sorts = {"price_low": "price ASC", "price_high": "price DESC",
             "name": "name ASC", "rating": "rating DESC", "newest": "id DESC"}
    sql += " ORDER BY " + sorts.get(sort, "id DESC")
    products = db.execute(sql, params).fetchall()
    categories = [r["category"] for r in db.execute(
        "SELECT DISTINCT category FROM products ORDER BY category")]
    return render_template("index.html", products=products, categories=categories,
                           q=q, category=category, sort=sort)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not product:
        abort(404)
    related = db.execute(
        "SELECT * FROM products WHERE category=? AND id!=? LIMIT 4",
        (product["category"], product_id)).fetchall()
    return render_template("product.html", product=product, related=related)

# ---------------------------------------------------------------- cart
def cart_items():
    db = get_db()
    cart = session.get("cart", {})
    items, total = [], 0
    for pid, qty in cart.items():
        p = db.execute("SELECT * FROM products WHERE id=?", (int(pid),)).fetchone()
        if p:
            items.append({"product": p, "qty": qty, "subtotal": p["price"] * qty})
            total += p["price"] * qty
    return items, total

@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def cart_add(product_id):
    db = get_db()
    p = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not p:
        abort(404)
    qty = max(1, int(request.form.get("qty", 1)))
    cart = session.get("cart", {})
    cart[str(product_id)] = min(cart.get(str(product_id), 0) + qty, p["stock"])
    session["cart"] = cart
    flash(f"Added {p['name']} to cart.", "success")
    return redirect(request.form.get("next") or url_for("cart"), code=303)

@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def cart_remove(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("cart"), code=303)

@app.route("/cart/update/<int:product_id>", methods=["POST"])
def cart_update(product_id):
    qty = max(0, int(request.form.get("qty", 1)))
    cart = session.get("cart", {})
    if qty == 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = qty
    session["cart"] = cart
    return redirect(url_for("cart"), code=303)

# ---------------------------------------------------------------- checkout / orders
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("index"), code=303)
    user = current_user()
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form.get("phone", "").strip()
        address = request.form["address"].strip()
        city = request.form["city"].strip()
        pincode = request.form["pincode"].strip()
        payment = request.form.get("payment_method", "Cash on Delivery")
        if not all([name, email, address, city, pincode]):
            flash("Please fill in all required fields.", "error")
            return render_template("checkout.html", items=items, total=total, user=user)
        db = get_db()
        cur = db.execute(
            "INSERT INTO orders (user_id, customer_name, customer_email, customer_phone, address, city, pincode, total, payment_method) VALUES (?,?,?,?,?,?,?,?,?)",
            (user["id"] if user else None, name, email, phone, address, city, pincode, total, payment))
        order_id = cur.lastrowid
        for item in items:
            p = item["product"]
            db.execute("INSERT INTO order_items (order_id, product_id, product_name, price, quantity) VALUES (?,?,?,?,?)",
                       (order_id, p["id"], p["name"], p["price"], item["qty"]))
            db.execute("UPDATE products SET stock = stock - ? WHERE id=?", (item["qty"], p["id"]))
        db.commit()
        session["cart"] = {}
        return redirect(url_for("order_success", order_id=order_id), code=303)
    return render_template("checkout.html", items=items, total=total, user=user)

@app.route("/order/<int:order_id>")
def order_success(order_id):
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order:
        abort(404)
    items = db.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,)).fetchall()
    return render_template("order_success.html", order=order, items=items)

@app.route("/orders")
@login_required
def my_orders():
    db = get_db()
    user = current_user()
    orders = db.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",
                        (user["id"],)).fetchall()
    return render_template("orders.html", orders=orders)

# ---------------------------------------------------------------- auth
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name, email = request.form["name"].strip(), request.form["email"].strip().lower()
        password = request.form["password"]
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")
        db = get_db()
        if db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
            flash("An account with this email already exists.", "error")
            return render_template("register.html")
        cur = db.execute("INSERT INTO users (name, email, password_hash) VALUES (?,?,?)",
                         (name, email, generate_password_hash(password)))
        db.commit()
        session["user_id"] = cur.lastrowid
        flash("Account created. Welcome to ShopFlow!", "success")
        return redirect(url_for("index"), code=303)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(request.args.get("next") or url_for("index"), code=303)
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out.", "success")
    return redirect(url_for("index"), code=303)

# ---------------------------------------------------------------- admin
@app.route("/admin")
@admin_required
def admin_dashboard():
    db = get_db()
    total_sales = db.execute("SELECT COALESCE(SUM(total),0) FROM orders").fetchone()[0]
    order_count = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    product_count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    user_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    low_stock = db.execute("SELECT * FROM products WHERE stock <= 15 ORDER BY stock ASC").fetchall()
    recent_orders = db.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 8").fetchall()
    top_products = db.execute(
        "SELECT product_name, SUM(quantity) AS sold, SUM(price*quantity) AS revenue "
        "FROM order_items GROUP BY product_name ORDER BY sold DESC LIMIT 5").fetchall()
    return render_template("admin_dashboard.html", total_sales=total_sales,
                           order_count=order_count, product_count=product_count,
                           user_count=user_count, low_stock=low_stock,
                           recent_orders=recent_orders, top_products=top_products)

@app.route("/admin/products")
@admin_required
def admin_products():
    products = get_db().execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return render_template("admin_products.html", products=products)

@app.route("/admin/products/new", methods=["GET", "POST"])
@admin_required
def admin_product_new():
    if request.method == "POST":
        db = get_db()
        db.execute("INSERT INTO products (name, description, price, old_price, category, stock, rating) VALUES (?,?,?,?,?,?,?)",
                   (request.form["name"], request.form["description"], float(request.form["price"]),
                    float(request.form["old_price"] or 0) or None, request.form["category"],
                    int(request.form["stock"]), float(request.form.get("rating", 4.5))))
        db.commit()
        flash("Product added.", "success")
        return redirect(url_for("admin_products"), code=303)
    return render_template("admin_product_form.html", product=None)

@app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_product_edit(product_id):
    db = get_db()
    product = db.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not product:
        abort(404)
    if request.method == "POST":
        db.execute("UPDATE products SET name=?, description=?, price=?, old_price=?, category=?, stock=?, rating=? WHERE id=?",
                   (request.form["name"], request.form["description"], float(request.form["price"]),
                    float(request.form["old_price"] or 0) or None, request.form["category"],
                    int(request.form["stock"]), float(request.form.get("rating", 4.5)), product_id))
        db.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin_products"), code=303)
    return render_template("admin_product_form.html", product=product)

@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def admin_product_delete(product_id):
    db = get_db()
    db.execute("DELETE FROM products WHERE id=?", (product_id,))
    db.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("admin_products"), code=303)

@app.route("/admin/orders")
@admin_required
def admin_orders():
    orders = get_db().execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template("admin_orders.html", orders=orders)

@app.route("/admin/orders/<int:order_id>", methods=["GET", "POST"])
@admin_required
def admin_order_detail(order_id):
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order:
        abort(404)
    if request.method == "POST":
        db.execute("UPDATE orders SET status=? WHERE id=?",
                   (request.form["status"], order_id))
        db.commit()
        flash("Order status updated.", "success")
        return redirect(url_for("admin_order_detail", order_id=order_id), code=303)
    items = db.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,)).fetchall()
    return render_template("admin_order_detail.html", order=order, items=items)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()
    print("ShopFlow running at http://127.0.0.1:5000")
    print("Admin: admin@shopflow.com / admin123   |   Demo: demo@shopflow.com / demo123")
    app.run(host="127.0.0.1", port=5000, debug=False)
