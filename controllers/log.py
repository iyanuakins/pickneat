from flask import render_template, session, redirect


def transaction_history_handler(request, database):
    #Default render all transaction in table format
    if request.method == "GET":
        records = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        return render_template("transaction_history.html", table=records)
    
    username = session.get("username")
    transactions = {}

    #Renders Table for User
    if request.form.get("view") == "table" and request.form.get("data_type") == "yearly":
        records = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        for transaction in records:
            transactions[transaction["time_stamp"].split(",")[0]] += int(transaction["time_stamp"].split(",")[0])
            pass
        return render_template("transaction_history.html", table="transactions")
    else:
        records = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        for transaction in records:
            transaction["time_stamp"].split(",")[1]
            pass
        return render_template("transaction_history.html", table="transactions")



    if request.form.get("view") == "chart":

        legend = "FUNDING" if request.form.get("transaction") == "credit" else "EXPENSES"
        temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                        61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                        70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
        times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
                '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
                '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']

        if request.form.get("date_type") == "year":
            records = database.execute("SELECT * FROM transactions WHERE username=:username and time_stamp>:timestamp and transaction_type=:transaction")
            return render_template("transaction_history.html", chart=transactions, values=temperatures, labels=times, legend=legend)
        
        elif request.form.get("date_type") == "month":
            records = database.execute("SELECT * FROM transactions WHERE username=:username and time_stamp>:timestamp and transaction_type=:transaction")
            return render_template("transaction_history.html", chart=transactions, values=temperatures, labels=times, legend=legend)

        records = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        return render_template("transaction_history.html", chart="default_chart", values=temperatures, labels=times, legend=legend)
def order_history_handler(request, database):
    pass