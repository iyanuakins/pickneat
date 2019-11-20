from flask import render_template, session, redirect
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from controllers.error import error
from datetime import datetime


def user_management_handler(request, database):
    if request.method == "GET":
        #Retrieves all users from Database
        users = database.execute("SELECT id, full_name, username, email, user_type, status FROM users")
        return render_template("user_management.html", users = users)

    #Retrieves User Information from Database
    if  request.form.get("filters"):
        if request.form.get("filters") == "all_users":
            users = database.execute("SELECT id, full_name, username, email, user_type, status FROM users")
            return render_template("user_management.html", users = users)
        users = database.execute("SELECT id, full_name, username, email, user_type, status FROM users WHERE user_type = :user_type", user_type = request.form.get("filters"))
        return render_template("user_management.html", users = users)
    if request.form.get("id"):
        user = database.execute("SELECT * FROM users WHERE id = :id", id = request.form.get("id"))
        return render_template("view_user.html", user = user)