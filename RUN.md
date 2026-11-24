# ShopFlow — How to Run

## Requirements
- Python 3.10 or newer (tested with Python 3.12.3)
- No other software needed. SQLite is built into Python.

## Exact commands

```bash
cd shopflow-ecommerce

# 1. Create a virtual environment (do this once)
python -m venv .venv

# 2. Activate it
source .venv/bin/activate
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Windows CMD:         .venv\Scripts\activate.bat

# 3. Install dependencies (do this once)
pip install -r requirements.txt

# 4. Run the app
python app/app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Demo accounts

- Admin: **admin@shopflow.com / admin123** — go to http://127.0.0.1:5000/admin
- Customer: **demo@shopflow.com / demo123**

## Starting fresh

Delete the database file and run again — it is recreated and re-seeded:

```bash
rm shopflow.db
python app/app.py
```

## Stopping the server

Press `Ctrl+C` in the terminal where the app is running.

## Deploying for a real buyer (summary)

- Change `app.secret_key` in `app/app.py` to a random secret.
- Change the admin password (log in as admin, or delete the demo accounts
  from the database and create a new admin in the app).
- Run behind a production server, e.g. `pip install gunicorn` then
  `gunicorn -w 4 -b 0.0.0.0:8000 "app.app:app"` from the project folder
  (note: the Flask app object is `app.app` because the code is in `app/app.py`).
- Use the MySQL schema in `database/schema.sql` if the buyer wants MySQL.
