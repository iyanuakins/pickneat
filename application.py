import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.auth import login_handler,register_handler
from controllers.user import application_handler, complain_handler, profile_handler, dashboard_handler

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