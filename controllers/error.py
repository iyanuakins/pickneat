from flask import  render_template
def error(message, code):
    status_message = ""
    if code == 400:
        status_message = "Bad Request"
    elif code == 401:
        status_message = "Unauthorized"
    elif code == 403:
        status_message = "Forbidden"

    data = [message, status_message]
    return render_template("error.html", data = data)