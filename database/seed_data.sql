-- ShopFlow seed data — 16 products, 4 categories
-- Run:  sqlite3 shopflow.db < database/seed_data.sql
-- (The app also seeds this automatically on first run, so this file is
--  mainly for buyers who want to inspect / reload the demo data by hand.)

INSERT INTO products (name, description, price, old_price, category, stock, rating) VALUES
('Wireless Noise-Cancelling Headphones', 'Bluetooth 5.3 headphones with 40-hour battery, deep bass and a built-in mic for calls.', 2999, 4499, 'Electronics', 24, 4.8),
('Smartwatch Fit Pro', 'AMOLED display, heart-rate + sleep tracking, step counter, 7-day battery, water resistant.', 2499, 3999, 'Electronics', 18, 4.6),
('Mechanical Keyboard RGB', 'Hot-swappable mechanical keyboard with RGB backlight, blue switches and detachable cable.', 2799, 3499, 'Electronics', 32, 4.7),
('Portable Bluetooth Speaker', '20W waterproof speaker with 18-hour playtime, perfect for home and outdoor use.', 1799, 2599, 'Electronics', 40, 4.5),
('Men''s Cotton Casual Shirt', 'Breathable 100% cotton shirt, slim fit, available in blue and white. Machine washable.', 899, 1499, 'Fashion', 55, 4.4),
('Women''s Running Shoes', 'Lightweight running shoes with cushioned sole and breathable mesh upper.', 1999, 3299, 'Fashion', 27, 4.7),
('Classic Denim Jacket', 'Durable denim jacket with button front and chest pockets. A wardrobe staple.', 1599, 2499, 'Fashion', 15, 4.6),
('Leather Wallet — Bifold', 'Genuine leather bifold wallet with 8 card slots, 2 currency pockets and RFID blocking.', 699, 1199, 'Fashion', 60, 4.5),
('Ceramic Dinner Set (16 pcs)', '16-piece ceramic dinner set for 4 people — plates, bowls and cups in a modern matte finish.', 2299, 3499, 'Home & Living', 12, 4.8),
('LED Desk Lamp with USB Charging', 'Adjustable LED desk lamp with 3 colour modes, touch control and a USB charging port.', 999, 1699, 'Home & Living', 38, 4.6),
('Cotton Bedsheet — Queen Size', '300-thread-count cotton bedsheet with 2 pillow covers. Soft, breathable and fade-resistant.', 1199, 1999, 'Home & Living', 22, 4.4),
('Stainless Steel Water Bottle 1L', 'Double-wall insulated steel bottle, keeps drinks cold 24 hours / hot 12 hours. Leak-proof.', 549, 899, 'Home & Living', 80, 4.7),
('Yoga Mat — Anti-Slip 6mm', '6mm thick anti-slip yoga mat with carry strap. Extra cushioning for knees and joints.', 799, 1299, 'Sports & Fitness', 45, 4.5),
('Adjustable Dumbbell Set 20kg', 'Pair of adjustable dumbbells (2.5–10kg each) with non-slip grips for home workouts.', 3499, 5499, 'Sports & Fitness', 9, 4.8),
('Cricket Bat — Kashmir Willow', 'Full-size Kashmir willow cricket bat with grip and protective cover. For tennis-ball cricket.', 1299, 1999, 'Sports & Fitness', 20, 4.3),
('Gym Duffel Bag 35L', '35L waterproof gym bag with shoe compartment, wet pocket and adjustable shoulder strap.', 1099, 1799, 'Sports & Fitness', 33, 4.6);
