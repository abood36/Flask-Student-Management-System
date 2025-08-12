# Booky (Flask + MySQL) — Student Manager

Simple Flask application to manage students (CRUD) with:

- Flask, Flask-SQLAlchemy, Flask-Migrate
- MySQL (PyMySQL driver)
- Flask-WTF + CSRF
- Flask-Login (simple admin)
- Bootstrap 5 frontend
- Features:
  CRUD for students: create, view, update, delete
  MySQL database via SQLAlchemy ORM
  Admin authentication with Flask-Login
  Search by name, email, or roll number
  Pagination for large lists
  CSV export of filtered student list
  Clean project structure (app factory + blueprints + services)

## Quick start (Windows)

1. Clone repo:
   git clone https://github.com/<your-user>/booky-flask-mysql.git
   cd booky-flask-mysql

2. Create virtualenv and activate:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Install and start MySQL server and create database and user in MySQL shell:
   CREATE DATABASE booky_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'booky_user'@'localhost' IDENTIFIED BY 'yourpassword';
   GRANT ALL PRIVILEGES ON booky_db.\* TO 'booky_user'@'localhost';
   FLUSH PRIVILEGES;

5. Copy .env.example to .env and set secrets:
   copy .env.example .env
   Edit .env:
   SECRET_KEY=<strong-random-hex>
   DATABASE_URL=mysql+pymysql://booky_user:yourpassword@localhost:3306/booky_db?charset=utf8mb4
   FLASK_ENV=development

6. Run migrations:
   set FLASK_APP=run.py
   flask db init
   flask db migrate -m "init"
   flask db upgrade

7. Create admin user:
   flask create-admin
   Follow the prompts for username/password.

8. Run the app:
   flask run
   Open http://127.0.0.1:5000/students

Quick start (macOS/Linux):
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# edit .env as above

export FLASK_APP=run.py
flask db init
flask db migrate -m "init"
flask db upgrade
flask create-admin
flask run

Environment variables:
SECRET_KEY: Random secure key for Flask session & CSRF
DATABASE_URL: MySQL connection string (mysql+pymysql://...)
FLASK_ENV: development for debug mode, production for prod

Project structure:
booky-flask-mysql/
app/
**init**.py
config.py
extensions.py
models.py
services.py
auth/
students/
templates/
static/
run.py
requirements.txt
.env.example
README.md

Possible improvements:
Add user roles / permission system
Unit tests with pytest
Docker support
File uploads for student profile pictures

License: MIT
