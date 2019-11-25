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
    order = database.execute("SELECT * FROM orders WHERE id=:id", id=int(id))[0]
    if not order["status"] == "pending":
        flash("Order Does Not Exist", 'danger')
        return redirect("/manage_order")

    database.execute("UPDATE orders SET status='confirmed' WHERE id=:id", id=int(id))
    buyer = database.execute("SELECT username FROM users WHERE username=:username", username=order["user"])[0]
    vendor = database.execute("SELECT * FROM users WHERE username=:username", username=session.get("username"))[0]

    database.execute("UPDATE users SET balance=:balance WHERE username=:username", balance=vendor["balance"]+order["total_cost"], username=session.get("username"))

    #Insert transaction details into database
    database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES ( :username, :transaction_type, :amount, :description, :status, :time_stamp)", 
                                        username = session["username"], 
                                        transaction_type = "order", 
                                        amount = order['total_cost'], 
                                        description = f"Order was Processed Successfully",
                                        status = "confirmed", 
                                        time_stamp = datetime.now())
    subject = "Notification of order processing"
    message = f"This is to inform you that your of order has been accepted and is been processed by the vendor.\n Thanks for choosing pick'n'eat."
    database.execute("INSERT INTO messages (sender, receiver, subject, message, status, time_stamp) VALUES ( :username, :receiver, :subject, :message, :status, :time_stamp)", 
                                            username = "Admin", receiver = buyer["username"], subject = subject, message = message, status = "unread", time_stamp = datetime.now())

    session['balance'] -= order['total_cost']

    flash("Order Accepted Successfully", 'success')
    return redirect("/manage_order")


#Rejecting Order
def cancel_order_handler(id, database):
    order = database.execute("SELECT * FROM orders WHERE id=:id", id=int(id))[0]
    if not order["status"] == "pending":
        flash("Order Does Not Exist", 'danger')
        return redirect("/manage_order")

    database.execute("UPDATE orders SET status='cancelled' WHERE id=:id", id=int(id))
    buyer = database.execute("SELECT * FROM users WHERE username=:username", username=order["user"])[0]
    database.execute("UPDATE users SET balance=:balance WHERE username=:username", balance=buyer["balance"]+order["total_cost"], username=buyer["username"])

    #Insert transaction details into database
    database.execute("INSERT INTO transactions (username, transaction_type, amount, description, status, time_stamp) VALUES ( :username, :transaction_type, :amount, :description, :status, :time_stamp)", 
                                        username = buyer["username"], 
                                        transaction_type = "order", 
                                        amount = order['total_cost'], 
                                        description = f"Order for meal cancelled by the Vendor",
                                        status = "cancelled", 
                                        time_stamp = datetime.now())
    subject = "Notification of order cancellation"
    message = f"This is to inform you that your of order has been cancelled by the vendor.\n A sum of {order['total_cost']} naira has been credited in to your wallet as refund.\n We regret all inconvinences.\n Thanks for choosing pick'n'eat."
    database.execute("INSERT INTO messages (sender, receiver, subject, message, status, time_stamp) VALUES ( :username, :receiver, :subject, :message, :status, :time_stamp)", 
                                            username = "Admin", receiver = buyer["username"], subject = subject, message = message, status = "unread", time_stamp = datetime.now())
    flash("Order Cancelled Successfully", 'warning')
    return redirect("/manage_order")