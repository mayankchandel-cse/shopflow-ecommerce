# ShopFlow — Complete E-Commerce Store

A full-stack e-commerce web app, ready to run and ready to sell.
Built with **Python Flask + SQLite** (a MySQL version of the schema is included),
plain HTML/CSS/JS on the front end — no paid services, no licensed frameworks.

## What it does

**Customer storefront**
- Product catalog — **16 real sample products** in 4 categories:
  Electronics, Fashion, Home & Living, Sports & Fitness
- Search, category filter, and sort (newest, price low→high / high→low, top rated, name A–Z)
- Product detail pages with related products
- Cart — add, update quantity, remove (stored in the session)
- Checkout — name, email, phone, address, city, PIN code, payment method
  (Cash on Delivery / UPI / Card — **demo only, no real payment is taken**)
- Order confirmation page with order number, items and total

**Accounts**
- Sign up / log in — passwords are **hashed** (Werkzeug), never stored in plain text
- Order history for logged-in users (`/orders`)

**Admin dashboard** (`/admin`, admin account only)
- Sales totals, order count, product count, user count
- Top-selling products, low-stock list (15 or fewer)
- Add / edit / delete products
- View all orders, open an order, change its status
  (Placed → Confirmed → Shipped → Delivered / Cancelled)
- Stock is reduced automatically when an order is placed

**Design**
- Clean, responsive layout — works on mobile, tablet and desktop
- No external images or CDNs needed; product tiles use CSS gradients

## Demo accounts (created automatically on first run)

| Role | Email | Password |
|---|---|---|
| Admin | admin@shopflow.com | admin123 |
| Customer | demo@shopflow.com | demo123 |

> Change these passwords before giving the store to a real client.

## How to run

See [RUN.md](RUN.md) for the exact commands. Short version:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
```

Then open **http://127.0.0.1:5000**

The database (`shopflow.db`) is created automatically on first run from
`database/schema.sql`, seeded with the 16 products and the two demo accounts.
To start fresh, delete `shopflow.db` and run again.

## Project structure

```
shopflow-ecommerce/
├── app/
│   ├── app.py            # Flask app — all routes, auth, cart, checkout, admin
│   └── __init__.py
├── templates/            # 15 Jinja templates (storefront, auth, admin)
│   ├── base.html  index.html  product.html  cart.html  checkout.html
│   ├── order_success.html  orders.html  login.html  register.html  404.html
│   └── admin_dashboard.html  admin_products.html  admin_product_form.html
│       admin_orders.html  admin_order_detail.html
├── static/
│   ├── css/style.css     # responsive design, no framework
│   └── js/main.js
├── database/
│   ├── schema.sql        # SQLite schema + MySQL version in comments
│   └── seed_data.sql     # the 16 sample products (also seeded by the app)
├── requirements.txt      # Flask 3.1.3, Werkzeug 3.1.9
├── .gitignore
├── README.md             # this file
├── RUN.md                # exact run commands
└── gig.md                # Fiverr gig pack for selling this project
```

## Customising for a buyer

- **Change the products:** edit the list in `app/app.py` (`PRODUCTS`) or use the
  admin panel — Add Product. Or edit `database/seed_data.sql` and delete `shopflow.db`.
- **Change the currency / prices:** prices are in ₹ (INR) in the seed data;
  the `inr()` helper in `app/app.py` formats them.
- **Use MySQL instead of SQLite:** the MySQL schema is in
  `database/schema.sql` (bottom half). Create the database, run that schema,
  then point the app at MySQL — or ask the seller for the MySQL version.
- **Add a real payment gateway:** checkout currently records
  Cash on Delivery / UPI / Card as a demo choice. Razorpay / Stripe can be
  added as a paid extra (see gig Premium tier).

## Test results — tested 24 Nov 2026

Run locally with Python 3.12 + Flask 3.1.3, tested with `curl` against the
live server at http://127.0.0.1:5000. All tests passed (0 errors, 0 × 405/500):

| # | Test | Result |
|---|---|---|
| 1 | Home page loads, all 16 products shown | PASS — 200 |
| 2 | Search `?q=headphones` returns the headphones | PASS |
| 3 | Category filter + sort (`Fashion`, price low→high) | PASS — cheapest first |
| 4 | Product detail page `/product/1` | PASS — 200 |
| 5 | Add to cart (qty 2) → cart total ₹5,998 | PASS — 200 |
| 6 | Update cart quantity to 1 → total ₹2,999 | PASS |
| 7 | Register a new user | PASS — "Account created" |
| 8 | Guest checkout → order confirmation page | PASS — Order #1, ₹5,998, status Placed |
| 9 | Cart empties after an order is placed | PASS |
| 10 | Stock reduced (product 1: 24 → 22 after selling 2) | PASS |
| 11 | Login as demo customer (correct password) | PASS — "Welcome back" |
| 12 | Wrong password rejected | PASS — "Invalid email or password" |
| 13 | Logged-in checkout → order appears in My Orders | PASS — Order #2, ₹899 |
| 14 | Admin login, dashboard shows total sales ₹5,998 | PASS — 200 |
| 15 | Admin: add a product, edit its price, delete it | PASS — product 17 added, edited, then 404 after delete |
| 16 | Admin: change order status to Shipped | PASS — order #1 now Shipped |
| 17 | Non-admin user blocked from `/admin` | PASS — redirected to login, "Admin access only" |
| 18 | Search with no matches shows "No products match" | PASS |
| 19 | Product page for a missing product | PASS — 404 |
| 20 | Static CSS and JS load | PASS — 200 |

Note: an early test run used `curl -X POST -L`, which re-sends POST on
redirects and produced 405s in the test client only. The app was fixed to
use proper 303 (See Other) redirects after every POST, and browsers follow
those correctly. Re-tested with plain `curl --data -L`: 0 × 405 in the log.
