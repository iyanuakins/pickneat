from flask import render_template, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.error import error
from controllers.auth import logged_in

def dashboard_handler(database):

    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    if user[0]["user_type"] == "user":
        
    pass