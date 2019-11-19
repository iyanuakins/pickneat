from flask import render_template, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.error import error


#Vendor application Handler
def application_handler(request, database):
    if request.methods == "GET":
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
        
