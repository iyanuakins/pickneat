import os
from flask import render_template, session, redirect, flash
from controllers.error import error
from werkzeug.utils import secure_filename
from datetime import datetime

#Menu Management
def menu_handler(database):
    #Collates All of the Menu in database by Vendor
    menus = database.execute("SELECT * FROM menu WHERE vendor=:username", username=session.get("username"))
    return render_template("vendor_menu.html", menus=menus)

#Edit Single Menu
def edit_menu_handler(request, database, id):

    #Renders Page for Single Menu Editing
    if request.method == "GET":
        session["edit_menu"] = id
        menu = database.execute("SELECT * FROM menu WHERE id=:id", id=id)
            
        return render_template("menu_update.html", menu=menu[0])

    menu = database.execute("SELECT * FROM menu WHERE id=:id and vendor=:user", id=session.get("edit_menu"), user=session.get("username"))

    if len(menu) < 1:
        return error("Error While Processing Your Request", 403)

    
    #Dummy for Image Url
    menu_image = ""
    extension = ""

    #Create Filename for File
    if request.files["image"]:
        image = request.files["image"]
        image_name = secure_filename(image.filename)
        menu_image = image.filename
        extension = menu_image.rsplit(".", 1)[1]
        menu_image = "static/images/"+datetime.now().strftime("%m%d%Y%H%M%S")+"."+extension

    #Checks for Image ELigibility for possible change to default
    if not "." in menu_image:
        menu_image = menu[0]["image"]
    elif not extension:
        if not extension.upper() in ["JPEG", "JPG", "PNG", "GIF"]:
            menu_image = menu[0]["image"]
    elif menu[0]["image"]:
        #Removes previous menu Image
        remove_image = menu[0]["image"].rsplit("/images/", 1)[1]
        os.remove(os.path.join("static/images", remove_image))

    #Updates menu Information to Database
    database.execute("UPDATE menu SET (image, status, name, price, description)=(:image, :status, :name, :price, :description) WHERE vendor=:username and id=:id",
                                            id = session.get("edit_menu"),
                                            image = menu_image,
                                            status = request.form.get("status") if request.form.get("status") else menu[0]["status"],
                                            name = request.form.get("name") if request.form.get("name") else menu[0]["name"],
                                            price = request.form.get("price") if request.form.get("price") else menu[0]["price"],
                                            description = request.form.get("description") if request.form.get("description") else menu[0]["description"],
                                            username = session.get("username"),)
     #Stores New Image in Project
    if request.files["image"]:
        add_image = menu_image.rsplit("/images/", 1)[1]
        image.save(os.path.join("static/images", add_image))
    
    #Refreshes Page
    return redirect("/manage_menu")

#Deletes Single Menu
def delete_menu_handler(id,request, database):
    if request.method == "GET":
        database.execute("DELETE FROM menu WHERE id=:id", id=id)
    return redirect("/manage_menu")
  
#Adds Menu to Gallery
def add_menu_handler(request, database):

    if request.method == "GET":
        return render_template("menu_add.html")

    #Dummy for Image Url
    user_image = ""
    extension = ""

    #Create Filename for File
    if request.files["image"]:
        image = request.files["image"]
        image_name = secure_filename(image.filename)
        menu_image = image.filename
        extension = menu_image.rsplit(".", 1)[1]
        menu_image = "static/images/"+datetime.now().strftime("%m%d%Y%H%M%S")+"."+extension

    #Checks for Image ELigibility for possible change to default
    if not "." in menu_image or not extension.upper() in ["JPEG", "JPG", "PNG", "GIF"]:
        return error("Supply Appropriate Image", 400)
        
    if not request.form.get("name").strip():
        return error("Enter a valid name", 400)

    try:
        if int(request.form.get("price")) > 0:
            pass
    except:
        return error("Enter a valid price", 400)

    if not request.form.get("description").strip():
        return error("Please Describe Your Meal", 400)

    database.execute("INSERT INTO menu (image, vendor, time_stamp, name, price, description) VALUES (:image, :vendor, :time_stamp, :name, :price, :description)",
                                                                                                            image = menu_image,
                                                                                                            vendor =  session.get("username"),
                                                                                                            name =  request.form.get("name"),
                                                                                                            price =  request.form.get("price"),
                                                                                                            description =  request.form.get("description"),
                                                                                                            time_stamp = datetime.now(),
                                                                                                            )

    #Stores New Image in Project
    if request.files["image"]:
        add_image = menu_image.rsplit("/images/", 1)[1]
        image.save(os.path.join("static/images", add_image))

    return redirect("/manage_menu")

def view_menu_handler(request, database):
    if request.method == "GET":
        menus = database.execute("SELECT * FROM menu WHERE status = 'available'")
        return render_template("all_menus.html", menus = menus)

def single_view_menu_handler(id, request, database):
    if request.method == "GET":
        menu = database.execute("SELECT * FROM menu WHERE id = :id ", id = id)
        vendor = menu[0]["vendor"]
        user = database.execute("SELECT business_name, business_address, user_image FROM users WHERE username = :vendor ", vendor = vendor)
        return render_template("single_menu.html", menu = menu[0], vendor = user[0])


def order_handler(request, database):
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("quantity"):
            return error("Must provide quantity", 400)

        # Ensure username was submitted
        if not request.form.get("menu_id").strip():
            return error("Must provide Menu ID", 403)

        if session.get("username"):
            menu = database.execute("SELECT * FROM menu WHERE id = :id ", id = request.form.get("menu_id").strip())
            vendor = menu[0]["vendor"]
            price = int(menu[0]["price"])
            menu_name = menu[0]["name"]
            total_cost = int(request.form.get("quantity")) * menu[0]["price"]
            user = database.execute("SELECT balance FROM users WHERE username = :user ", user = session["username"])
            user_balance = user[0]["balance"]
            if user_balance < total_cost:
                return "insufficient"
            else:
                qty = int(request.form.get("quantity"))
                database.execute("UPDATE users SET balance = :new_balance WHERE username = :user ", new_balance = user_balance - total_cost, user = session["username"])
                
                #Insert order details into database
                database.execute("INSERT INTO orders (user, vendor, quantity, total_cost, price, time_stamp) VALUES ( :user, :vendor, :quantity, :total_cost, :price, :time_stamp)",
                                                 user = session["username"], vendor = vendor, quantity = qty, total_cost = total_cost, price = price, time_stamp = datetime.now())
                
                desc = "Payment for {} plate(s) of {}".format(qty, menu_name)
                #Insert transaction details into database
                database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES ( :username, :transaction_type, :amount, :description, :status, :time_stamp)", 
                                                    username = session["username"], transaction_type = "order", amount = total_cost, description = desc, status = "pending", time_stamp = datetime.now())
                flash("Order was successful and is been processed.", "success")
                return redirect("/dashboard")
        else:
            flash("Authentication required to complete order process, please login or register to continue", "danger")
            return redirect("/login")

