from flask import render_template, session, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from controllers.error import error

#Registration Handler
def register_handler(request, database):
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("full_name"):
            flash("Must provide full name", "danger")
            return redirect("/register")

        # Ensure username was submitted
        if not request.form.get("username").strip():
            flash("Must provide username", "danger")
            return redirect("/register")

        # Ensure phone number was submitted
        try:
            if int(request.form.get("phone_number")):
                pass
        except:
            flash("Must provide phone number", "danger")
            return redirect("/register")


        # Ensure username was submitted
        if not request.form.get("email"):
            flash("Must provide email", "danger")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password").strip():
            flash("Must provide password", "danger")
            return redirect("/register")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation").strip():
            flash("Must repeat password enterd for confirmation", "danger")
            return redirect("/register")

        #Confirm Password match
        elif request.form.get("confirmation").strip() != request.form.get("password").strip():
            flash("Passwords entered does not match", "danger")
            return redirect("/register")

        # Query database for username
        rows = database.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) > 0:
            flash("Username taken, try another", "danger")
            return redirect("/register")

        # Query database for username
        database.execute("INSERT INTO users (full_name, username, email, phone_number, address, user_type, password, time_stamp) VALUES ( :full_name, :username, :email, :phone_number, :address, :user_type, :password, :time_stamp)",
                                                 full_name = request.form.get("full_name"), username = request.form.get("username").strip(), email = request.form.get("email").strip(), phone_number = request.form.get("phone_number"), address = request.form.get("address"),
                                                  user_type = "user", password = generate_password_hash(request.form.get("password").strip()), time_stamp = datetime.now())

        return render_template("login.html")
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
    user = database.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))

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
    return redirect("/dashboard")

