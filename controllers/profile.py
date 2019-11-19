import os
from flask import render_template, session, redirect
from werkzeug.utils import secure_filename
from datetime import datetime

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
        user_image = datetime.now().strftime("%m%d%Y%H%M%S")+"."+extension

    #Checks for Image ELigibility for possible change to default
    if not "." in user_image:
        user_image = user[0]["user_image"]
    elif not extension:
        if not extension.upper() in ["JPEG", "JPG", "PNG", "GIF"]:
            user_image = user[0]["user_image"]
    elif user[0]["user_image"]:
        #Removes previous User Image
       os.remove(os.path.join("static/images", user[0]["user_image"]))

    #Updates User Information to Database
    database.execute("UPDATE users SET (full_name, email, phone_number, address, user_image, business_name, business_address, business_number)=(:name, :email, :phone_number, :address, :user_image, :business_name, :business_address, :business_number) WHERE username=:username",
                            name = request.form.get("full_name") if request.form.get("full_name") else user[0]["full_name"],
                            email = request.form.get("email") if request.form.get("email") else user[0]["email"],
                            phone_number = request.form.get("phone_number") if request.form.get("phone_number") else user[0]["phone_number"],
                            address = request.form.get("address") if request.form.get("address") else user[0]["address"],
                            user_image = user_image,
                            business_name = request.form.get("business_name") if request.form.get("business_name") else user[0]["business_name"],
                            business_address = request.form.get("business_address") if request.form.get("business_address") else user[0]["business_address"],
                            business_number = request.form.get("business_number") if request.form.get("business_number") else user[0]["business_number"],
                            username=session.get("username"))

    #Stores New Image in Project
    if request.files["user_image"]:
        image.save(os.path.join("static/images", user_image))
    
    #Refreshes Page
    return redirect("/profile")
