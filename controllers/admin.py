from flask import render_template, session, redirect
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from controllers.error import error
from datetime import datetime


def user_management_handler(request, database):
    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")
        
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


def user_view_handler(request, database):
    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")

    if request.method == "GET":
        return redirect("/manage_users")

    if request.method == "POST":
        #Retrieves User Information from Database
        if  not request.form.get("action"):
            error("Action must be selected", 400)
        database.execute("UPDATE users SET status = :status WHERE id = :id", status = request.form.get("action"), id = request.form.get("id"))
        return redirect("/manage_users")