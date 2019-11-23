from flask import session, redirect, render_template, flash
from datetime import datetime

def display_cart_handler(database):
    cart = {}
    cart_menu = []

    try:
        recieved_cart = database.execute("SELECT * FROM users WHERE username=:username", username=session["username"])[0]["cart"].split("-")

        for order in recieved_cart:
            if "." in order:
                menu_id = order.split('.')[0]
                quantity = order.split('.')[1]

                try:
                    cart[menu_id] += int(quantity)
                except:
                    cart[menu_id] = int(quantity)

        
        for order in cart:
            menu = database.execute("SELECT * FROM menu WHERE id=:menu_id", menu_id=order)[0]
            menu['quantity'] = cart[order]

            cart_menu.append(menu)

    except:
        return render_template('display_cart.html', cart={})

    session["cart"] = len(cart)

    return render_template('display_cart.html', cart=cart, cart_menu=cart_menu)


def add_cart_handler(id, request, database):
    try:
        quantity = int(request.form["quantity"])
    except:
        quantity = 1

    user = database.execute("SELECT * FROM users WHERE username=:username", username=session["username"])[0]
    cart = user['cart']

    if user["cart"] == "None":
        cart = '-'

    database.execute("UPDATE users SET cart=:cart WHERE username=:username", username=session["username"], cart=f'{cart}{id}.{quantity}-')

    session["menu_id"] = int(id)
    session["qty"] = int(quantity)

    menu = database.execute("SELECT * FROM menu WHERE id=:menu_id", menu_id=int(id))[0]

    return render_template("preview.html", menu = menu, qty = quantity, user = user, total_cost = menu['price']*quantity, cart=quantity)

def delete_cart_handler(id, database):
    
    cart = database.execute("SELECT * FROM users WHERE username=:username", username=session["username"])[0]["cart"].split("-")
    newcart = []

    for order in cart:
        if not order.split(".")[0] == id.split(".")[0]:
            newcart.append(order)
    
    session["cart"] = len(newcart)

    newcart = "-".join(newcart)

    database.execute("UPDATE users SET cart=:cart WHERE username=:username", username=session["username"], cart=newcart)

    return redirect("/display_cart")

def clear_cart_handler(database):

    database.execute("UPDATE users SET cart=:cart WHERE username=:username", username=session["username"], cart="")

    session["cart"] = 0

    return redirect("/display_cart")

def process_cart_handler(request, database):
    # Collect User Current Information
    user = database.execute("SELECT * FROM users WHERE username=:username", username=session["username"])[0]

    #Keep tab of cart processing
    current_balance = user["balance"]
    failed_order = []
    successful_order = []

    #Process Order one at a time
    for order in request.form:

        #Collect Current Order information
        menu_id = int(order)
        menu = database.execute("SELECT * FROM menu WHERE id=:menu_id", menu_id=menu_id)[0]

        # VERIFY CURRENT ORDER

        # Check for Menu availiability
        if not menu["status"] == "available":
            menu["reason"] = "Order is no longer available"
            failed_order.append(menu)
            continue
        
        #Verify quantity
        try:
            quantity = int(request.form[order])
            total_cost = int(menu["price"])*quantity

            # Check for Money in Purse eligibility
            if current_balance < total_cost:
                menu["reason"] = "Insufficient Balance"
                failed_order.append(menu)
                continue

            # Check for Quantity Supplied
            if quantity == 0:
                menu["reason"] = "Quantity Not Specified"
                failed_order.append(menu)
                continue
        except:
            # When Quantity is not supplied
            menu["reason"] = "Quantity Not Specified"
            failed_order.append(menu)
            continue
        
        #PROCESS VALID ORDERS

        #Insert order details into database
        database.execute("INSERT INTO orders (user, vendor, quantity, total_cost, price, time_stamp) VALUES ( :user, :vendor, :quantity, :total_cost, :price, :time_stamp)",
                                            user = user["username"], 
                                            vendor = menu["vendor"], 
                                            quantity = quantity, 
                                            total_cost = total_cost,
                                            price = menu["price"], 
                                            time_stamp = datetime.now())

        #Insert transaction details into database
        database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES ( :username, :transaction_type, :amount, :description, :status, :time_stamp)", 
                                            username = session["username"], 
                                            transaction_type = "order", 
                                            amount = total_cost, 
                                            description = f"Payment for {quantity} plate(s) of {menu['name']}",
                                            status = "pending", 
                                            time_stamp = datetime.now())

        #Update for next Order 
        current_balance -= total_cost
        successful_order.append(menu)
        
    session['cart'] = 0

    #Update user information after processing all orders
    database.execute("UPDATE users SET balance = :balance, cart=:cart WHERE username = :username", balance = current_balance, cart="", username = user["username"])

    #Return to Order Summary
    flash("Order was processed successful.", "success")
    return render_template('cart_summary.html', success=successful_order, failure=failed_order)

    