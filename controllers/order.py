from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime
from controllers.error import error

#Displays all Pending Orders
def manage_order_handler(database):
    orders = database.execute("SELECT * FROM orders WHERE vendor=:vendor and status='pending'", vendor=session.get("username"))
    return render_template("order_view.html", orders=orders)

#Displays Selected Order
def manage_single_order_handler(id, database):
    order = database.execute("SELECT * FROM orders WHERE id=:id", id=int(id))
    user = database.execute("SELECT * FROM users WHERE username=:username", username=order[0]["user"])
    return render_template("single_order.html", order=order[0], user=user[0])
    
#Accepts Order
def accept_order_handler(id, database):
    order = database.execute("SELECT * FROM orders WHERE id=:id", id=int(id))
    if not order[0]["status"] == "pending":
        return error("This Order Has Been Accepted Earlier", 400)

    database.execute("UPDATE orders SET status='confirmed' WHERE id=:id", id=int(id))
    vendor = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))

    database.execute("UPDATE users SET balance=:balance WHERE username=:username", balance=vendor[0]["balance"]+order[0]["total_cost"], username=session.get("username"))

    database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES (:username, 'order', :amount, 'accepted order', 'confirmed', :time_stamp)",
                                                username=session.get("username"),
                                                amount=order[0]["total_cost"], 
                                                time_stamp = datetime.now(),)

    return redirect("/manage_order")


#Rejecting Order
def cancel_order_handler(id, database):
    order = database.execute("SELECT * FROM orders WHERE id=:id", id=int(id))
    if not order[0]["status"] == "pending":
        return error("This Order Has Been Cancelled Earlier", 400)

    database.execute("UPDATE orders SET status='cancelled' WHERE id=:id", id=int(id))
    buyer = database.execute("SELECT * FROM users WHERE username=:username", username=order[0]["user"])

    database.execute("UPDATE users SET balance=:balance WHERE username=:username", balance=buyer[0]["balance"]+order[0]["total_cost"], username=buyer[0]["username"])

    database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES (:username, 'order', :amount, 'cancelled order', 'cancelled', :time_stamp)",
                                                username=buyer[0]["username"],
                                                amount=order[0]["total_cost"], 
                                                time_stamp = datetime.now(),)

    return redirect("/manage_order")