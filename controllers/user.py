import os
from functools import wraps
from flask import flash, render_template, session, redirect
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from controllers.error import error
from datetime import datetime


#Vendor application Handler
def application_handler(request, database):
    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")
        
    if request.method == "GET":
        return render_template("vendor_application.html")

    if not request.form.get("business_name"):
        flash("Must provide business name", 'warning')
        return redirect("/apply")

    if not request.form.get("business_number"):
        flash("Must provide business number", 'warning')
        return redirect("/apply")

    if not request.form.get("business_address"):
        flash("Must provide business address", 'warning')
        return redirect("/apply")

    database.execute("UPDATE users SET business_name = :business_name, business_number = :business_number, business_address = :business_address, application = :application WHERE username = :username",
                                    username = session["username"], business_name = request.form.get("business_name"), business_number = request.form.get("business_number"), business_address = request.form.get("business_address"), application = "pending")
    
    flash("Application Successfully Submitted", 'success')
    return redirect("/dashboard")
        
#User complaint Handler
def complain_handler(request, database):

    #Retrieves User Information from Database
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    if request.method == "GET":
        return render_template("contact.html", user = user[0])
    
    return render_template("dashboard.html")        

#Profile view and route handler
def profile_handler(request, database):

    #Retrieves User Information from Database
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    #Handles GET request to Page
    if request.method == "GET":
        return render_template("profile.html", user=user[0])
    
    #Check Whether Numbers are Integers
    try:
        if int(request.form.get("phone_number")): #and not len(request.form.get("phone_number")) < 11 and len(request.form.get("phone_number")) < 11
            pass
        if session.get("user_type") == "vendor":
            if int(request.form.get("business_number")): #and len(request.form.get("business_number")) < 11 and len(request.form.get("business_number")) < 11
                pass
    except:
        flash("Enter Valid Number", 'danger')
        return redirect("/profile")

    #Get Values from fields or retain former
    full_name = user[0]["full_name"] if not request.form.get("full_name").strip() else request.form.get("full_name")
    email = user[0]["email"] if not request.form.get("email").strip() else request.form.get("email")
    address = user[0]["address"] if not request.form.get("address").strip() else request.form.get("address")
    try:
        business_name = user[0]["business_name"] if not request.form.get("business_name").strip() else request.form.get("business_name")
    except:
        business_name = user[0]["business_name"]
    try:
        business_address = user[0]["business_address"] if not request.form.get("business_address").strip() else request.form.get("business_address")
    except:
        business_address = user[0]["business_address"]
    try:
        int(request.form.get("phone_number"))
        phone_number = request.form['phone_number']
    except:
        phone_number = user[0]["phone_number"]
    try:
        int("234"+request.form.get("business_number"))
        business_number = request.form['business_number']
    except:
        business_number = user[0]["business_number"]
    
    user_image = ""
    extension = ""

    #Create Filename for File
    if request.files["user_image"]:
        image = request.files["user_image"]
        image_name = secure_filename(image.filename)
        user_image = image.filename
        extension = user_image.rsplit(".", 1)[1]
        user_image = "static/images/"+datetime.now().strftime("%m%d%Y%H%M%S")+"."+extension

    #Checks for Image ELigibility for possible change to default
    if not "." in user_image:
        user_image = user[0]["user_image"]
    elif not extension:
        if not extension.upper() in ["JPEG", "JPG", "PNG", "GIF"]:
            user_image = user[0]["user_image"]
    elif user[0]["user_image"]:
        #Removes previous User Image
        remove_image = user[0]["user_image"].rsplit("/images/", 1)[1]
        os.remove(os.path.join("static/images", remove_image))

    #Updates User Information to Database
    database.execute("UPDATE users SET (full_name, email, phone_number, address, user_image, business_name, business_address, business_number)=(:full_name, :email, :phone_number, :address, :user_image, :business_name, :business_address, :business_number) WHERE username=:username",
                                            full_name = full_name, email = email, phone_number = phone_number, address = address, user_image = user_image, business_name = business_name, business_address = business_address,  business_number = business_number, username=session.get("username"))

    #Stores New Image in Project
    if request.files["user_image"]:
        add_image = user_image.rsplit("/images/", 1)[1]
        image.save(os.path.join("static/images", add_image))
    
    #Refreshes Page
    flash("Profile Updated", 'success')
    return redirect("/profile")

#Dashboard view and route handler
def dashboard_handler(database):

    #Retrieves User Information To Enable Processing
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))[0]
    session["user_type"] = user["user_type"]
    session["user_view"] = user["user_view"]
    session["balance"] = user["balance"]

    user_type = user["user_type"]
    user_view = user["user_view"]

    #Process cart Information
    try:
        cart = user["cart"].split("-")

        #Set Cart Information on Session
        session["cart"] = len(cart) - 1
    except:
        session["cart"] = 0

    userdetail = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))[0]

    #Renders Admin DashBoard
    if user_type == "admin":
        return render_template("admin_dashboard.html", user=userdetail)

    #Renders Vendor DashBoard
    if user_type == "vendor" and user_view == "vendor":
        return redirect("/history_chart")

    #Renders Buyer DashBoard
    if user_type == "user" or user_view == "user":
        return render_template("dashboard.html", user=userdetail)
    
    session.clear()
    return redirect("/login")

#Withdrawal Manager
def withdrawal_handler(request, database):
    
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    if request.method == "GET":
        return render_template("withdrawal.html", user=user[0])

    try:
        amount = int(request.form.get("amount"))
    except:
        flash("Enter valid amount", 'warning')
        return redirect("/withdraw")

    if amount <= 0 or amount > user[0]["balance"]*0.98:
        flash("Insufficient Balance", 'danger')
        return redirect("/withdraw")

    session['balance'] -= amount

    database.execute("UPDATE users SET balance=:new_balance WHERE username=:username", new_balance=user[0]["balance"]-amount,  username=session.get("username"))
    

    #Insert transaction details into database
    database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES ( :username, :transaction_type, :amount, :description, :status, :time_stamp)", 
                                        username = session["username"], 
                                        transaction_type = "withdrawal", 
                                        amount = amount, 
                                        description = f"Made withdrawal of NGN {amount} ",
                                        status = "success", 
                                        time_stamp = datetime.now())

    flash("Withdraw Successful", 'success')
    return redirect('/dashboard')

#Switch Vendor View
def switch_vendor_view(view, database):

    if not session.get("user_type") == "vendor":
        return redirect("/dashboard")

    if view == "vendor":
        database.execute("UPDATE users SET user_view='vendor' WHERE username=:username", username=session.get("username"))

    if view == "user":
        database.execute("UPDATE users SET user_view='user' WHERE username=:username", username=session.get("username"))

    return redirect("/dashboard")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("username"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username"):
            return redirect("/dashboard")
        return f(*args, **kwargs)
    return decorated_function