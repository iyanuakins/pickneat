import os
from flask import render_template, session, redirect
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

def delete_menu_handler(id,request, database):
    if request.method == "GET":
        database.execute("DELETE FROM menu WHERE id=:id", id=id)
    return redirect("/manage_menu")

def view_menu_handler(request, database):
    if request.method == "GET":
        menus = database.execute("SELECT * FROM menu WHERE status = 'available'")
        return render_template("all_menus.html", menus = menus)
