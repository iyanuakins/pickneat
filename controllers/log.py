from flask import render_template, session, redirect

def transaction_history_handler(request, database):
    
    #Default render all transaction in table format
    if request.method == "GET":
        records = database.execute("SELECT * FROM transactions WHERE username=:username", username=session.get("username"))
        return render_template("transaction_history.html", table=records)
    
    #Store Variables
    username = session.get("username")
    transaction_type = request.form.get("transaction")
    view = request.form["view"]
    date_type = request.form["date_type"]


    # #Renders Table in Year for User
    # if view == "table" and date_type == "yearly":
    #     records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction", username=username, transaction=transaction_type)
        
    #     sorter = []
    #     value_table = {}

    #     #Cummulate the Sum of all particular Transaction Based on Year
    #     for transaction in records:
    #         year = transaction["time_stamp"].split("-")[0]
    #         sorter.append(year)

    #         try:
    #             value_table[year] += int(transaction["amount"])
    #         except:
    #             value_table[year] = int(transaction["amount"])

    #     #Sort Table Values
    #     sorted = []
    #     for year in sorter:
    #         if not year in sorted:
    #             sorted.append(year)
        
    #     return render_template("transaction_history.html", detail_table=value_table, transaction_type=transaction_type, sort=sorted.sort())
    
    # #Renders Table in Months for User
    # elif view == "table":
    #     records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction", username=username, transaction=transaction_type)

    #     sorter = []
    #     value_table = {}
    #     for transaction in records:
    #         month = transaction["time_stamp"].split("-")[1]
    #         year = transaction["time_stamp"].split("-")[0]
    #         sorter.append(f'{year}/{month}')

    #         try:
    #             value_table[f'{year}/{month}'] += int(transaction["amount"])
    #         except:
    #             value_table[f'{year}/{month}'] = int(transaction["amount"])

    #     #Sort Table Value
    #     sorted = []
    #     for month in sorter:
    #         if not month in sorted:
    #             sorted.append(month)

    #     return render_template("transaction_history.html", detail_table=value_table, transaction_type = transaction_type, sort=sorted.sort())

    # #Render Chart in Year for User
    # if view == "chart" and date_type == "yearly":

    #     records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction",  username=username, transaction=transaction_type)

    #     sorter = []
    #     chart_values = {}
    #     #Cummulate the Sum of all particular Transaction Based on Year
    #     for transaction in records:
    #         year = transaction["time_stamp"].split("-")[0]
    #         sorter.append(year)
    #         try:
    #             chart_values[year] += int(transaction["amount"])
    #         except:
    #             chart_values[year] = int(transaction["amount"])


    #     #Sort Table For Chart
    #     sorted = []
    #     for year in sorter:
    #         if not year in sorted:
    #             sorted.append(year)

    #     #Transaction is a Dictionary of Items
    #     return render_template("transaction_history.html", chart=sorted, values=chart_values, labels=sorted.sort(), legend="YEARLY")
    
    # #Render Chart in Months for User
    # else:
    #     records = database.execute("SELECT * FROM transactions WHERE username=:username and transaction_type=:transaction",  username=username, transaction=transaction_type)
    #     sorter = []
    #     chart_values = {}
        
    #     for transaction in records:
    #         month = transaction["time_stamp"].split("-")[1]
    #         year = transaction["time_stamp"].split("-")[0]
    #         sorter.append(f'{year}/{month}')

    #         try:
    #             chart_values[f'{year}/{month}'] += int(transaction["amount"])
    #         except:
    #             chart_values[f'{year}/{month}'] = int(transaction["amount"])

    #     sorted = []
    #     for month in sorter:
    #         if not month in sorted:
    #             sorted.append(month)

    #     #Transaction is a Dictionary of Items
    #     return render_template("transaction_history.html", chart=sorted, values=chart_values, labels=sorted.sort(), legend="MONTHLY")



def order_history_handler(request, database):
    #Default render all orders in table format
    if request.method == "GET":
        records = database.execute("SELECT * FROM orders WHERE user=:username", username=session.get("username"))
        return render_template("order_history.html", table=records)
    
    # #Resuable Variables
    # username = session["username"]
    # date_type = request.form["date_type"]
    # status = request.form["status"]
    # view = request.form["view"]

    # #Renders Table in Year for User
    # if view == "table" and date_type == "yearly":
    #     records = database.execute("SELECT * FROM orders WHERE user=:username and status=:status", username=username, status=status)
        
    #     sorter = []
    #     table_value = {}

    #     #Cummulate the Sum of all particular status Based on Year
    #     for order in records:
    #         year = order["time_stamp"].split("-")[0]
    #         sorter.append(year)
    #         try:
    #             table_value[year] += int(order["total_cost"])
    #         except:
    #             table_value[year] = int(order["total_cost"])

    #     sorted = []
    #     for year in sorter:
    #         if not year in sorted:
    #             sorted.append(year)

    #     #Order is a Dictionary of Items
    #     return render_template("order_history.html", detail_table=table_value, status_type=status, sort=sorted.sort())
    
    # #Renders Table in Months for User
    # elif view == "table":
    #     records = database.execute("SELECT * FROM orders WHERE user=:username and status=:status", username=username, status=status)

    #     sorter = []
    #     table_value = {}
    #     for order in records:
    #         month = order["time_stamp"].split("-")[1]
    #         year = order["time_stamp"].split("-")[0]
    #         sorter.append(f'{year}/{month}')

    #         try:
    #             table_value[f'{year}/{month}'] += int(order["total_cost"])
    #         except:
    #             table_value[f'{year}/{month}'] = int(order["total_cost"])

    #     sorted = []
    #     for year in sorter:
    #         if not year in sorted:
    #             sorted.append(year)

    #     return render_template("order_history.html", detail_table=table_value, status_type=status, sort=sorted.sort())

    # #Render Chart in Year for User
    # if view == "chart" and date_type == "yearly":

    #     records = database.execute("SELECT * FROM orders WHERE user=:username and status=:status",  username=username, status=status)

    #     sorter = []
    #     chart_value = {}

    #     #Cummulate the Sum of all particular status Based on Year
    #     for order in records:
    #         year = order["time_stamp"].split("-")[0]
    #         sorter.append(year)
    #         try:
    #             chart_value[year] += int(order["total_cost"])
    #         except:
    #             chart_value[year] = int(order["total_cost"])

    #     sorted = []
    #     for year in sorter:
    #         if not year in sorted:
    #             sorted.append(year)

    #     #status is a Dictionary of Items
    #     return render_template("order_history.html", chart=sorted, values=chart_value, labels=sorted.sort(), legend="YEARLY")
    
    # #Render Chart in Months for User
    # else:
    #     records = database.execute("SELECT * FROM orders WHERE user=:username and status=:status",  username=username, status=status)
        
    #     sorter = []
    #     chart_value = {}

    #     for order in records:
    #         month = order["time_stamp"].split("-")[1]
    #         year = order["time_stamp"].split("-")[0]
    #         sorter.append(f'{year}/{month}')
    #         try:
    #             chart_value[f'{year}/{month}'] += int(order["total_cost"])
    #         except:
    #             chart_value[f'{year}/{month}'] = int(order["total_cost"])

    #     sorted = []
    #     for year in sorter:
    #         if not year in sorted:
    #             sorted.append(year)         

    #     #status is a Dictionary of Items
    #     return render_template("order_history.html", chart=sorted, values=chart_value, labels=sorted.sort(), legend="MONTHLY")

