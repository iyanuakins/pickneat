from flask import render_template, session, redirect, flash
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

def app_management_handler(request, database):
    if request.method == "GET":
        apps = database.execute("SELECT username, business_name, business_number, business_address FROM users WHERE application = :app", app = "pending")
        return render_template("vendor_verification.html", apps = apps)

    if request.method == "POST":
        #Retrieves User Information from Database
        if  not request.form.get("action") or not request.form.get("username"):
            flash("Bad form request", "danger")
            apps = database.execute("SELECT username, business_name, business_number, business_address FROM users WHERE application = :app", app = "pending")
            return render_template("vendor_verification.html", apps = apps)
        
        action = request.form.get("action")

        if action == "accept":
            database.execute("UPDATE users SET user_type = :user_type, application = :application WHERE username = :username", user_type = "vendor", application = "", username = request.form.get("username"))
            apps = database.execute("SELECT username, business_name, business_number, business_address FROM users WHERE application = :app", app = "pending")
            flash("Vendor application successfully accepted", "success")
            return render_template("vendor_verification.html", apps = apps)
        elif action == "reject":
            database.execute("UPDATE users SET application = :application WHERE username = :username", application = "", username = request.form.get("username"))
            apps = database.execute("SELECT username, business_name, business_number, business_address FROM users WHERE application = :app", app = "pending")
            flash("Vendor application successfully rejected", "success")
            return render_template("vendor_verification.html", apps = apps)

def transaction_log_handler(request, database):
    table = database.execute("SELECT * FROM transactions")
    return render_template("all_transactions.html", table = table)

def order_log_handler(request, database):
    orders = database.execute("SELECT * FROM orders")
    return render_template("all_orders.html", orders = orders)

def menu_log_handler(request, database):
    menus = database.execute("SELECT * FROM menu")
    return render_template("menu_log.html", menus = menus)

def admin_dashboard_handler(request, database):
    
    if request.method == "GET":
        legend = "Users" 
        detail = "Users registration"

    records = database.execute("SELECT * FROM users")
    
    #Retrieves if any data for labels and values for Chart
    values = {}
    labels = []
  
    for user in records:

        date = user["time_stamp"].split(" ")[0]

        #Transaction types handlers
        if user['user_type'] != "admin":
            if not f'{date}' in labels:
                labels.append(f'{date}')
            try:
                values[f'{date}'] += 1
            except:
                values[f'{date}'] = 1
    labels.sort()
    #Transaction is a Dictionary of Items
    return render_template(
                            'admin_dashboard.html', 
                            values=values,
                            labels=labels, 
                            legend=legend, 
                            detail=detail
                            )


# #admin complaint Handler
# def admin_complain_handler(request, database):
#     #Retrieves User Information from Database
#     user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))
#     if request.method == "GET":
#         return render_template("contact.html", user = user[0])
#     if not request.form.get("subject"):
#         flash("Must enter message subject", 'warning')
#         return redirect("/contact")

#     if not request.form.get("message"):
#         flash("Must enter message", 'warning')
#         return redirect("/contact")
#     #Insert transaction details into database
#     admins = database.execute("SELECT username FROM users WHERE user_type=:user_type", user_type="admin")
#     for admin in admins:
#         database.execute("INSERT INTO messages (sender, receiver, subject, message, status, time_stamp) VALUES ( :username, :receiver, :subject, :message, :status, :time_stamp)", 
#                                             username = session["username"], receiver = admin["username"], subject = request.form.get("subject"), message = request.form.get("message"), status = "unread", time_stamp = datetime.now())
#     flash("Message successfully sent, we will get back to you ASAP", 'success')
#     return redirect("/dashboard")       
