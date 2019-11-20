from flask import render_template, session, redirect


def transaction_history_handler(request, database):
    #Default render all transaction in table format
    if request.method == "GET":
        records = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        return render_template("transaction_history.html", table=records)
    
    
    username = session.get("username")
    type = request.form.get("date_type")
    transaction = request.form.get("transaction")
    time = []
    amount = []
    transactions = {}
    months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    #Renders Table in Year for User
    if request.form.get("view") == "table" and request.form.get("date_type") == "yearly":
        records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction", username=username, transaction=transaction)
        #Cummulate the Sum of all particular Transaction Based on Year
        for transaction in records:
            month = transaction["time_stamp"].split("/")[0]
            try:
                transactions[month] += transaction["amount"]
            except:
                transactions[month] = transaction["amount"]

        #Transaction is a Dictionary of Items
        return render_template("transaction_history.html", detail_table=transactions, transaction_type=transaction["transaction_type"])
    
    #Renders Table in Months for User
    elif request.form.get("view") == "table":
        records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction", username=username, transaction=transaction)

        for transaction in records:
            year = months[int(transaction["time_stamp"].split("/")[1])]
            try:
                transactions[year+", "+month] += transaction["amount"]
            except:
                transactions[year+", "+month] = transaction["amount"]
        #Transaction is a Dictionary of Items
        return render_template("transaction_history.html", detail_table=transactions, month=months)

    #Render Chart in Year for User
    if request.form.get("view") == "chart" and request.form.get("date_type") == "yearly":

        records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction",  username=username, transaction=transaction)

        #Cummulate the Sum of all particular Transaction Based on Year
        for transaction in records:
            month = transaction["time_stamp"].split("/")[0]
            try:
                transactions[month] += transaction["amount"]
            except:
                transactions[month] = transaction["amount"]

        for key in transactions:
            amount.append(transactions[key])
            time.append(key)

        #Transaction is a Dictionary of Items
        return render_template("transaction_history.html", chart=transactions, values=amount, labels=time, legend="YEARLY")
    
    #Render Chart in Months for User
    else:
        records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction",  username=username, transaction=transaction)
        for transaction in records:
            year = months[int(transaction["time_stamp"].split("/")[1])]
            try:
                transactions[year+", "+month] += transaction["amount"]
            except:
                transactions[year+", "+month] = transaction["amount"]
        for key in transactions:
            amount.append(transactions[key])
            time.append(key)            

        #Transaction is a Dictionary of Items
        return render_template("transaction_history.html", chart=transactions, values=amount, labels=time, legend="MONTHLY")


def order_history_handler(request, database):
    pass