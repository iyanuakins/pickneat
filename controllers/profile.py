from flask import render_template, session, redirect

def profile_handler(request, database):
    #Handles Authentication of User
    if not session.get("username"):
        return redirect("/login")

    user_type = session.get("user_type")
    user_view = session.get("user_view")

    #Handles GET request to Page
    if request.method == "GET":
        return get_profile(user_type, user_view, database)

    if user_type == "admin":
        return update_admin_info(request, database)
    elif user_type == "vendor" and user_view == "vendor":
        return update_vendor_info(request, database)
    elif user_type == "user" or user_view == "user":
        return update_user_info(request, database)


def get_profile(user_type, user_view, database):

    #Verifying Current User
    if user_type == "admin":
        userdetail = database.execute("SELECT (name, username, email, phone_number, address, user_image, balance,) FROM users WHERE username=:username",
                                                                        username=session.get("username"))
    elif user_type == "vendor" and user_view == "vendor":
        userdetail = database.execute("SELECT (username, email, user_image, balance, business_name, business_address, business_number) FROM users WHERE username=:username", 
                                                                        username=session.get("username"))
    elif user_type == "user" or user_view == "user":
        userdetail = database.execute("SELECT (name, username, email, phone_number,	address, user_image, balance, status) FROM users WHERE username=:username",
                                                                        username=session.get("username"))

    #Renders Appropriate Profile Page
    return render_template("profile.html", user=userdetail[0])
    

def update_admin_info(request, database):
    database.execute("UPDATE users SET (name,username,email,phone_number,address,user_image)=(:name,:email,:phone,:address,:image) users WHERE username=:username",
                                                                        name = request.form.get("name"),
                                                                        email = request.form.get("email"),
                                                                        phone = request.form.get("phone"),
                                                                        address = request.form.get("address"),
                                                                        image = request.form.get("image"),
                                                                        username=session.get("username"))
    return redirect("/profile")

def update_vendor_info(request, database):
    database.execute("UPDATE users SET (business_name, email, business_number,business_address, image_url)=(:name,:email,:phone,:address,:image) users WHERE username=:username",
                                                                        name = request.form.get("business_name"),
                                                                        email = request.form.get("business_email"),
                                                                        phone = request.form.get("business_number"),
                                                                        address = request.form.get("business_address"),
                                                                        image = request.form.get("image_url"),
                                                                        username=session.get("username"))
    return redirect("/profile")

def update_user_info(request, database):
    database.execute("UPDATE users SET (name,username,email,phone_number,address,user_image)=(:name,:email,:phone,:address,:image) users WHERE username=:username",
                                                                        name = request.form.get("name"),
                                                                        email = request.form.get("email"),
                                                                        phone = request.form.get("phone"),
                                                                        address = request.form.get("address"),
                                                                        image = request.form.get("image"),
                                                                        username=session.get("username"))
    return redirect("/profile")
