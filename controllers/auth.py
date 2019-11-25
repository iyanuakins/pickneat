from flask import render_template, session, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from controllers.error import error

#Registration Handler
def username_check_handler(request, database):
    if request.method == "POST":
        req = request.get_json()
        # Query database for username
        rows = database.execute("SELECT * FROM users WHERE username = :username",
                          username=req["username"].lower())
        if len(rows) > 0:
            res = {"error": "Username taken, try another"}
            return res
        return {"valid": "good"}
        
                          
#Registration Handler
def register_handler(request, database):
    if request.method == "POST":
        req = request.get_json()
        # Ensure name was submitted
        if not req["full_name"]:
            res = {"error": "Must provide full name"}
            return res

        # Ensure username was submitted
        if not req["username"].strip():
            res = {"error": "Must provide username"}
            return res

        # Ensure phone number was submitted
        if not req["full_name"]:
            res = {"error": "Must provide phone number"}
            return res
        else:
            try:
                if int(req["phone_number"]):
                    pass
            except:
                res = {"error": "Must provide valid phone number"}
                return res


        # Ensure username was submitted
        if not req["email"]:
            res = {"error": "Must provide email"}
            return res

        # Ensure password was submitted
        elif not req["password"].strip():
            res = {"error": "Must provide password"}
            return res

        # Ensure password confirmation was submitted
        elif not req["confirmation"].strip():
            res = {"error": "Must repeat password enterd for confirmation"}
            return res

        #Confirm Password match
        elif req["confirmation"].strip() != req["password"].strip():
            res = {"error": "Passwords entered does not match"}
            return res

        # Query database for username
        rows = database.execute("SELECT * FROM users WHERE username = :username",
                          username=req["username"].lower())

        if len(rows) > 0:
            res = {"error": "Username taken, try another"}
            return res

        # Query database for username
        database.execute("INSERT INTO users (full_name, username, email, phone_number, address, user_type, password, time_stamp) VALUES ( :full_name, :username, :email, :phone_number, :address, :user_type, :password, :time_stamp)",
                                                 full_name = req["full_name"], username = req["username"].lower().strip(), email = req["email"].strip(), phone_number = req["phone_number"], address = req["address"],
                                                  user_type = "user", password = generate_password_hash(req["password"].strip()), time_stamp = datetime.now())
        res = {"success": "Done"}
        flash("Registratioin successful, Please login", "success")
        return res
    else:
        return render_template("register.html")

      
#Login Handler
def login_handler(request, database):
    #Handles Rendering of Login Page
    if request.method == "GET":
        return render_template("login.html")

    #Final Validation of Username
    if not request.form.get("username").strip():
        flash("Username Field Is Blank", "danger")
        return redirect("/login")

    #Final Validation of Password
    if not request.form.get("password").strip():
        flash("Password Field Is Blank", "danger")
        return redirect("/login")

    #Recieves Information about User from Database
    user = database.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username").lower())

    #Check for the autheticity of Password and Username Supplied
    try:
        user[0]["username"]

        if not check_password_hash(user[0]["password"], request.form.get("password")):
            flash("Invalid Password", "danger")
            return redirect("/login")
    except:
        flash("Invalid Password/Username", "danger")
        return redirect("/login")
    

    #Remembers Logged In User
    session["username"] = user[0]["username"]
    session["user_type"] = user[0]["user_type"]
    session["user_view"] = user[0]["user_view"]

    #Handles DashBoard Display
    if session.get("menu_id"):
        return redirect("/preview")
    return redirect("/dashboard")

