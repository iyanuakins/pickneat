import os
from flask import render_template, session, redirect
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from controllers.error import error
from datetime import datetime


#Vendor application Handler
def application_handler(request, database):
    if request.method == "GET":
        return render_template("vendor_application.html")

    if not request.form.get("business_name"):
        return error("Must provide business name", 400)

    if not request.form.get("business_number"):
        return error("Must provide business number", 400)

    if not request.form.get("business_address"):
        return error("Must provide business address", 400)

    database.execute("UPDATE users SET business_name = :business_name, business_number = :business_number, business_address = :business_address WHERE usersname = :username",
                                    username = session.get["username"], business_name = request.form.get("business_name"), business_number = request.form.get("business_number"), business_address = request.form.get("business_address"))
    return render_template("dashboard.html")
        
#User complaint Handler
def complain_handler(request, database):
    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")

    #Retrieves User Information from Database
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    if request.method == "GET":
        return render_template("contact.html", user = user[0])
    
    return render_template("dashboard.html")        


#Profile view and route handler
def profile_handler(request, database):
    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")

    #Retrieves User Information from Database
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    #Handles GET request to Page
    if request.method == "GET":
        return render_template("profile.html", user=user[0])

    #Dummy for Image Url
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
                            full_name = request.form.get("full_name") if request.form.get("full_name").strip() else user[0]["full_name"],
                            email = request.form.get("email") if request.form.get("email").strip() else user[0]["email"],
                            phone_number = request.form.get("phone_number") if request.form.get("phone_number").strip() else user[0]["phone_number"],
                            address = request.form.get("address") if request.form.get("address").strip() else user[0]["address"],
                            user_image = user_image,
                            business_name = request.form.get("business_name") if request.form.get("business_name").strip() else user[0]["business_name"],
                            business_address = request.form.get("business_address") if request.form.get("business_address").strip() else user[0]["business_address"],
                            business_number = request.form.get("business_number") if request.form.get("business_number").strip() else user[0]["business_number"],
                            username=session.get("username"))

    #Stores New Image in Project
    if request.files["user_image"]:
        add_image = user_image.rsplit("/images/", 1)[1]
        image.save(os.path.join("static/images", add_image))
    
    #Refreshes Page
    return redirect("/profile")

#Dashboard view and route handler
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

