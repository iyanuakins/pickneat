from flask import render_template, session

#Menu Management
def menu_handler(database):
    #Collates All of the Menu in database by Vendor
    menus = database.execute("SELECT * FROM menu WHERE vendor=:username", username=session.get("username"))
    return render_template("vendor_menu.html", menus=menus)

#Edit Single Menu
def edit_menu_handler(request, database, id):
    return render_template("menu_update.html")