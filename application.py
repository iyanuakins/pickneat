import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.auth import login_handler,register_handler
from controllers.admin import user_management_handler, user_view_handler
from controllers.user import application_handler, complain_handler, profile_handler, dashboard_handler
from controllers.log import transaction_history_handler, order_history_handler
from controllers.menu import menu_handler, edit_menu_handler, delete_menu_handler, add_menu_handler, manage_order_handler, view_menu_handler

# # Configure application
app = Flask(__name__)

# # Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Configure CS50 Library to use SQLite database
database = SQL("sqlite:///pickneat.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return register_handler(request, database)
  
@app.route("/login", methods=["GET", "POST"])
def login():
    return login_handler(request, database)

@app.route("/dashboard")
def dashboard():
    return dashboard_handler(database)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    return profile_handler(request, database)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/apply", methods=["GET", "POST"])
def apply():
    return application_handler(request, database)

@app.route("/contact", methods=["GET", "POST"])
def complain():
    return complain_handler(request, database)

@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    return user_management_handler(request, database)

@app.route("/manage_user", methods=["GET", "POST"])
def manage_user():
    return user_view_handler(request, database)
  
@app.route("/transaction_history", methods=["GET", "POST"])
def transaction_history():
    return transaction_history_handler(request, database)

@app.route("/order_history", methods=["GET", "POST"])
def order_history():
    return order_history_handler(request, database)

@app.route("/manage_menu")
def menu_manage():
    return menu_handler(database)

@app.route("/edit_menu/<id>", methods=["GET", "POST"])
def edit_menu(id):
    return edit_menu_handler(request, database, id)

@app.route("/add_menu", methods=["GET", "POST"])
def add_menu():
    return add_menu_handler(request, database)

@app.route("/all_menus")
def all_menus():
    return render_template("all_menus.html")

@app.route("/fund")
def fund():
    user = database.execute("SELECT * FROM users WHERE username = :username", username = session.get("username"))
    order = database.execute("SELECT * FROM orders WHERE user = :user AND status='pending'", user = session.get("username"))
    return render_template("funding_page.html", order = order, user = user)

@app.route("/delete_menu/<id>")
def delete_menu(id):
    return delete_menu_handler(id, request, database)

@app.route("/manage_order")
@app.route("/manage_order/<id>")
def manage_order(id='14.info'):
    return manage_order_handler(id, request, database)
  
@app.route("/browse", methods=["GET", "POST"])
def view_menu():
    return view_menu_handler(request, database)
