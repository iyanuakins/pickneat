
def register_handler(request, database):
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("full_name"):
            return error("Must provide full name", 403)

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Must provide username", 403)

        # Ensure phone number was submitted
        if not request.form.get("phone_number"):
            return error("Must provide phone number", 403)

        # Ensure username was submitted
        if not request.form.get("email"):
            return error("Must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return error("Must repeat password enterd for confirmation", 403)

        #Confirm Password match
        elif request.form.get("confirmation") != request.form.get("password"):
            return error("Passwords entered does not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        if len(rows) > 0:
            return error("Username taken, try another", 403)

        # Query database for username
        db.execute("INSERT INTO users (full_name, username, email, phone_number, address, user_type, password, time_stamp) VALUES ( :full_name, :username, :email, :phone_number, :address, :user_type, :password, :time_stamp)",
                                                 full_name = request.form.get("full_name"), username = request.form.get("username"), email = request.form.get("email"), phone_number = request.form.get("phone_number"), address = request.form.get("address"),
                                                  user_type = "user", password = generate_password_hash(request.form.get("password")), time_stamp = datetime.now())

        return render_template("login.html")
    else:
        return render_template("register.html")