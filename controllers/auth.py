from flask import render_template, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash

def login_handler(request, database):
    
    #Handles Logged In State
    try:
        if session.get("username"):
            return logged_in(database=database)
    except:
        pass

    #Handles Rendering of Login Page
    if request.method == "GET":
        return render_template("login.html")

    #Final Validation of Username
    if not request.form.get("username").strip():
        return error("Username Field Is Blank", 400)

    #Final Validation of Password
    if not request.form.get("password").strip():
        return error("Password Field Is Blank", 400)

    #Recieves Information about User from Database
    user = database.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

    #Check for the autheticity of Password and Username Supplied
    try:
        user[0]["username"]

        if not check_password_hash(user[0]["password"], request.form.get("password")):
            return error("Invalid Password", 400)
    except:
        return error("Invalid Password/Username", 400)
    

    #Remembers Logged In User
    session["username"] = user[0]["username"]

    #Handles DashBoard Display
    return logged_in(database=database)


def logged_in(database):
    if not session.get("username"):
        return redirect("/login")

    return redirect("/dashboard")


def error(message, code):
    pass