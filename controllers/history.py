from flask import render_template, session, request, redirect

def history_chart_handler(request, database):
    
    if request.method == "GET":
        transaction_type = "withdrawal"
        legend = "WITHDRAWAL HISTORY" 
        detail = "Made Withdrawal of "
    else:
        trans = request.form['transaction'] if request.form['transaction'] else 'withdrawal'
        if trans == 'funding':
            transaction_type = 'funding'
            legend = "FUNDING HISTORY" 
            detail = "Funded account with "
        elif trans == 'order':
            transaction_type = 'order'
            legend = "ORDERING HISTORY" 
            detail = "Total order of "
        else:
            transaction_type = 'withdrawal'
            legend = "WITHDRAWAL HISTORY" 
            detail = "Made Withdrawal of "

    records = database.execute("SELECT * FROM transactions WHERE username=:username",  username=session['username'])
    
    #Retrieves if any data for labels and values for Chart
    values = {}
    labels = []
  
    for transaction in records:

        date = transaction["time_stamp"].split("-")

        day = date[2]
        month = date[1]
        year = date[0]

        #Transaction types handlers
        if transaction['transaction_type'].lower() == transaction_type:
            if not f'{year}/{month}/{day}' in labels:
                labels.append(f'{year}/{month}/{day}')
            try:
                values[f'{year}/{month}/{day}'] += int(transaction["amount"])
            except:
                values[f'{year}/{month}/{day}'] = int(transaction["amount"])
    labels.sort()
    #Transaction is a Dictionary of Items
    return render_template(
                            'vendor_dashboard.html', 
                            values=values,
                            labels=labels, 
                            legend=legend, 
                            detail=detail
                            )

