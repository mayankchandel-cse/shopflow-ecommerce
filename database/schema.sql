-- ShopFlow — database schema (SQLite, default)
-- A MySQL version of the same schema is at the bottom of this file.
-- The app creates this schema automatically on first run (see app/app.py),
-- so you do NOT need to run this file by hand for the demo.
-- To create it manually:  sqlite3 shopflow.db < database/schema.sql

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    price REAL NOT NULL,
    old_price REAL,
    category TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image TEXT NOT NULL DEFAULT '',
    rating REAL NOT NULL DEFAULT 4.5,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT NOT NULL DEFAULT '',
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    pincode TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Placed',
    payment_method TEXT NOT NULL DEFAULT 'Cash on Delivery',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products (category);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders (user_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items (order_id);

-- ============================================================================
-- MySQL version (same tables, MySQL syntax) — use this if the buyer wants MySQL
-- ============================================================================
-- CREATE DATABASE IF NOT EXISTS shopflow CHARACTER SET utf8mb4;
-- USE shopflow;
--
-- CREATE TABLE users (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   name VARCHAR(120) NOT NULL,
--   email VARCHAR(160) NOT NULL UNIQUE,
--   password_hash VARCHAR(255) NOT NULL,
--   is_admin TINYINT NOT NULL DEFAULT 0,
--   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );
--
-- CREATE TABLE products (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   name VARCHAR(180) NOT NULL,
--   description TEXT NOT NULL,
--   price DECIMAL(10,2) NOT NULL,
--   old_price DECIMAL(10,2) NULL,
--   category VARCHAR(80) NOT NULL,
--   stock INT NOT NULL DEFAULT 0,
--   image VARCHAR(255) NOT NULL DEFAULT '',
--   rating DECIMAL(2,1) NOT NULL DEFAULT 4.5,
--   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );
--
-- CREATE TABLE orders (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   user_id INT NULL,
--   customer_name VARCHAR(120) NOT NULL,
--   customer_email VARCHAR(160) NOT NULL,
--   customer_phone VARCHAR(20) NOT NULL DEFAULT '',
--   address TEXT NOT NULL,
--   city VARCHAR(80) NOT NULL,
--   pincode VARCHAR(12) NOT NULL,
--   total DECIMAL(10,2) NOT NULL,
--   status VARCHAR(30) NOT NULL DEFAULT 'Placed',
--   payment_method VARCHAR(40) NOT NULL DEFAULT 'Cash on Delivery',
--   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   FOREIGN KEY (user_id) REFERENCES users (id)
-- );
--
-- CREATE TABLE order_items (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   order_id INT NOT NULL,
--   product_id INT NOT NULL,
--   product_name VARCHAR(180) NOT NULL,
--   price DECIMAL(10,2) NOT NULL,
--   quantity INT NOT NULL,
--   FOREIGN KEY (order_id) REFERENCES orders (id),
--   FOREIGN KEY (product_id) REFERENCES products (id)
-- );
