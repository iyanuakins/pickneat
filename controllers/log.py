from flask import render_template, session, redirect


def transaction_history_handler(request, database):
    #Default render all transaction in table format
    if request.method == "GET":
        transactions = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        return render_template("transaction_history.html", transactions=transactions)

    

def order_history_handler(request, database):
    pass