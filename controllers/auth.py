from flask import render_template, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.error import error

#Registration Handler
def register_handler(request, database):
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("full_name"):
            return error("Must provide full name", 403)

        # Ensure username was submitted
        if not request.form.get("username").strip():
            return error("Must provide username", 403)

        # Ensure phone number was submitted
        if not request.form.get("phone_number"):
            return error("Must provide phone number", 403)

        # Ensure username was submitted
        if not request.form.get("email"):
            return error("Must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password").strip():
            return error("Must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation").strip():
            return error("Must repeat password enterd for confirmation", 403)

        #Confirm Password match
        elif request.form.get("confirmation").strip() != request.form.get("password").strip():
            return error("Passwords entered does not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) > 0:
            return error("Username taken, try another", 403)

        # Query database for username
        db.execute("INSERT INTO users (full_name, username, email, phone_number, address, user_type, password, time_stamp) VALUES ( :full_name, :username, :email, :phone_number, :address, :user_type, :password, :time_stamp)",
                                                 full_name = request.form.get("full_name"), username = request.form.get("username").strip(), email = request.form.get("email").strip(), phone_number = request.form.get("phone_number"), address = request.form.get("address"),
                                                  user_type = "user", password = generate_password_hash(request.form.get("password").strip()), time_stamp = datetime.now())

        return render_template("login.html")
    else:
        return render_template("register.html")

      
#Login Handler
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