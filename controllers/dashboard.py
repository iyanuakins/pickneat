from flask import render_template, session, redirect

def dashboard_handler(database):

    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")

    #Retrieves User Information To Enable Processing
    user = database.execute("SELECT user_type, user_view FROM users WHERE username=:username", username=session.get("username"))
    session["user_type"] = user[0]["user_type"]
    session["user_view"] = user[0]["user_view"]
    user_type = user[0]["user_type"]
    user_view = user[0]["user_view"]

    #Renders Admin DashBoard
    if user_type == "admin":
        userdetail = database.execute("SELECT full_name, username, email, phone_number, address, user_image, balance FROM users WHERE username=:username",
                                                                        username=session.get("username"))
        return render_template("admin_dashboard.html", user=userdetail[0])

    #Renders Vendor DashBoard
    if user_type == "vendor" and user_view == "vendor":
        userdetail = database.execute("SELECT username, email, user_image, balance, business_name, business_address, business_number FROM users WHERE username=:username", 
                                                                        username=session.get("username"))
        return render_template("vendor_dashboard.html", user=userdetail[0])

    #Renders Buyer DashBoard
    if user_type == "user" or user_view == "user":
        userdetail = database.execute("SELECT full_name, username, email, phone_number,	address, user_image, balance, status, user_view FROM users WHERE username=:username",
                                                                        username=session.get("username"))
        return render_template("dashboard.html", user=userdetail[0])
    
    session.clear()
    return redirect("/login")

