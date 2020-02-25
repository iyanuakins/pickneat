import os
from functools import wraps
from flask import flash, render_template, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from controllers.error import error
from datetime import datetime


#Vendor application Handler
def application_handler(request, database):
    if request.method == "GET":
        #Retrieves User Information from Database
        user = database.execute("SELECT application FROM users WHERE username=:username", username=session.get("username"))
        if user[0]["application"] == "pending":
            flash("You have a pending application under review", "info")
            return redirect("/dashboard")
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
    if not request.form.get("subject"):
        flash("Must enter message subject", 'warning')
        return redirect("/contact")

    if not request.form.get("message"):
        flash("Must enter message", 'warning')
        return redirect("/contact")
    #Insert transaction details into database
    admins = database.execute("SELECT username FROM users WHERE user_type=:user_type", user_type="admin")
    for admin in admins:
        database.execute("INSERT INTO messages (sender, receiver, subject, message, status, time_stamp) VALUES ( :username, :receiver, :subject, :message, :status, :time_stamp)", 
                                            username = session["username"], receiver = admin["username"], subject = request.form.get("subject"), message = request.form.get("message"), status = "unread", time_stamp = datetime.now())
    flash("Message successfully sent, we will get back to you ASAP", 'success')
    return redirect("/dashboard")       

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

    #Change Password implementation
    try:
        if request.form['password']:
            if not request.form['confirmation'] == request.form['password']:
                flash('Password Do Not Match', 'danger')
                return redirect('/profile')
            password = generate_password_hash(request.form['password'])
        else:
            password = user[0]['password']
    except:
        password = user[0]['password']

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

    username = session['username']
    #Updates User Information to Database
    database.execute(f"UPDATE users SET (full_name, password, email, phone_number, address, user_image, business_name, business_address, business_number)\
        =('{full_name}', '{password}', '{email}', '{phone_number}', '{address}', '{user_image}', '{business_name}', '{business_address}', '{business_number}') WHERE username='{username}'")

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
        return redirect("/admin_dashboard")

    #Renders Vendor DashBoard
    if user_type == "vendor" and user_view == "vendor":
        return redirect("/history_chart")

    #Renders Buyer DashBoard
    if user_type == "user" or user_view == "user":
        menu = database.execute('SELECT * FROM menu WHERE status="available" ORDER BY random() LIMIT 4;')
        return render_template("dashboard.html", user=userdetail, menus=menu)
    
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

#Password Reset
def forgot_password_handler(request, database):
    if request.method == "GET":
        return render_template('forgot_password.html')

    if not request.form['username']:
        flash('Username Must be Provided')
        return redirect('/forgot_password')

    if not request.form['password'] == request.form['confirmation']:
        flash('Password Mismatch!', 'warning')
        return redirect('/forgot_password')

    user = database.execute('SELECT username FROM users WHERE username=:username', username=request.form['username'])

    if not user:
        flash('Your Password Request Was Acknowledged', 'info')
        return redirect('/login')
    
    database.execute('UPDATE users SET password=:password WHERE username=:username', password=generate_password_hash(request.form['password']), username=request.form['username'])
    
    flash('Password Changed Successfully', 'success')
    return redirect('/login')

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

def admin_route_guard(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_type"] != "admin":
            session.clear()
            flash("Out of bound, please login", "danger")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def vendor_route_guard(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_type"] != "vendor":
            session.clear()
            flash("Out of bound, please login", "danger")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_information_handler(request, database):
    if request.method == "POST":
        res = request.get_json()
        user = database.execute("SELECT balance, cart FROM users WHERE username=:username", username = res["username"])
        balance = user[0]["balance"]
        try:
            cart = f"{user[0]['cart']}{res['local_menu']}".split('-')
            cart_number = []
            for item in cart:
                menu_id = item.split('.')[0]
                if not menu_id in cart_number and '.' in item:
                    cart_number.append(menu_id)  
            cart_number = len(cart_number)
            if res['local_menu']:
                database.execute("UPDATE users SET cart=:cart WHERE username=:username", cart=f"{user[0]['cart']}{res['local_menu']}", username=res['username'])
        except:
            cart_number = 0
        return {"res": "success", "balance": balance, 'cart':f'{cart_number}'}

def funding_handler(request, database):

    user = database.execute("SELECT * FROM users WHERE username = :username", username = session.get("username"))

    if request.method == "POST":
        data = request.get_json()
        amount = int(user[0]["balance"])+int(data['amount'])
        database.execute('UPDATE users SET balance=:bal WHERE username=:user', bal=amount, user=user[0]["username"])


        #Insert transaction details into database
        database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES ( :username, :transaction_type, :amount, :description, :status, :time_stamp)", 
                                        username = session["username"], 
                                        transaction_type = "funding", 
                                        amount = data['amount'], 
                                        description = f"Funded Account Successfully with {data['amount']}",
                                        status = "success", 
                                        time_stamp = datetime.now())
        return {'amount':amount}
                                    
    order = database.execute("SELECT * FROM orders WHERE user = :user AND status='pending'", user = session.get("username"))
    return render_template("funding_page.html", order = order, user = user)


def notification_count_handler(request, database):
    if request.method == "POST":
        counts = database.execute("SELECT receiver FROM messages WHERE receiver=:username AND status=:status", username = session["username"], status="unread")
        if len(counts) > 0:
            return {"res": "success", "count": len(counts)}
        return {"res": "success", "count": 0}


def notification_handler(request, database):
    if request.method == "POST":
        counts = database.execute("SELECT id FROM messages WHERE receiver=:username AND status=:status", username = session["username"], status="unread")
        if len(counts) > 0:
            return {"res": "success", "count": len(counts)}
        return {"res": "success", "count": 0}
    messages = database.execute("SELECT * FROM messages WHERE receiver=:username AND NOT status=:status", username = session["username"], status="deleted")
    return render_template("notifications.html", messages = messages)

def read_notification_handler(id, request, database):
    if request.method == "GET":
        message = database.execute("SELECT * FROM messages WHERE id=:id", id = id)
        database.execute("UPDATE messages SET status=:status WHERE id=:id", id = id, status = "read")
        return {"res": "success", "message": message[0]}
        
def del_notification_handler(id, request, database):
    if request.method == "GET":
        database.execute("UPDATE messages SET status=:status WHERE id=:id", id = id, status = "deleted")
        flash("Message successfully deleted","success")
        return {"res": "success"}
                                 
    return render_template("funding_page.html", order = order, user = user)