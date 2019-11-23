
from flask import redirect, render_template, request, session
from controllers.auth import login_handler,register_handler
from controllers.admin import user_management_handler, user_view_handler
from controllers.user import application_handler, complain_handler, profile_handler, dashboard_handler, withdrawal_handler, switch_vendor_view, \
                        login_required, logout_required
from controllers.log import transaction_history_handler, order_history_handler
from controllers.menu import menu_handler, edit_menu_handler, delete_menu_handler, add_menu_handler, \
                      view_menu_handler, single_view_menu_handler, order_handler, order_preview_handler
from controllers.order import manage_order_handler,  manage_single_order_handler, accept_order_handler, manage_order_handler, cancel_order_handler
from controllers.cart import add_cart_handler, delete_cart_handler, display_cart_handler, clear_cart_handler, process_cart_handler
from controllers.history import history_cart_handler

def router(app=0, database=0, id=0):
    @app.route("/")
    def index():
        menus = database.execute("SELECT * FROM menu ORDER BY random() LIMIT 3;")
        return render_template("index.html", menus = menus)

    @app.route("/register", methods=["GET", "POST"])
    @logout_required
    def register():
        return register_handler(request, database)
    
    @app.route("/login", methods=["GET", "POST"])
    @logout_required
    def login():
        return login_handler(request, database)

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return dashboard_handler(database)

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        return profile_handler(request, database)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    @app.route("/apply", methods=["GET", "POST"])
    @login_required
    def apply():
        return application_handler(request, database)

    @app.route("/contact", methods=["GET", "POST"])
    @login_required
    def complain():
        return complain_handler(request, database)

    @app.route("/manage_users", methods=["GET", "POST"])
    @login_required
    def manage_users():
        return user_management_handler(request, database)

    @app.route("/manage_user", methods=["GET", "POST"])
    @login_required
    def manage_user():
        return user_view_handler(request, database)
    
    @app.route("/transaction_history", methods=["GET", "POST"])
    @login_required
    def transaction_history():
        return transaction_history_handler(request, database)

    @app.route("/order_history", methods=["GET", "POST"])
    @login_required
    def order_history():
        return order_history_handler(request, database)

    @app.route("/manage_menu")
    @login_required
    @login_required
    def menu_manage():
        return menu_handler(database)

    @app.route("/edit_menu/<id>", methods=["GET", "POST"])
    @login_required
    def edit_menu(id):
        return edit_menu_handler(request, database, id)

    @app.route("/add_menu", methods=["GET", "POST"])
    @login_required
    def add_menu():
        return add_menu_handler(request, database)

    @app.route("/all_menus")
    def all_menus():
        return render_template("all_menus.html")

    @app.route("/fund")
    def fund():
        user = database.execute("SELECT * FROM users WHERE username = :username", username = session.get("username"))
        order = database.execute("SELECT * FROM orders WHERE user = :user AND status='pending'", user = session.get("username"))
        return render_template("funding_page.html", order = order, user = user)

    @app.route("/delete_menu/<id>")
    @login_required
    def delete_menu(id):
        return delete_menu_handler(id, request, database)

    @app.route("/manage_order")
    @login_required
    def manage_order():
        return manage_order_handler(database)

    @app.route("/manage_order/<id>")
    @login_required
    def manage_single_order(id):
        return manage_single_order_handler(id, database)

    @app.route("/cancel_order/<id>")
    @login_required
    def cancel_order(id):
        return cancel_order_handler(id, database)

    @app.route("/accept_order/<id>")
    @login_required
    def accept_order(id):
        return accept_order_handler(id, database)

    @app.route("/browse", methods=["GET", "POST"])
    def view_menu():
        return view_menu_handler(request, database)

    @app.route("/order_menu/<int:id>")
    def single_view_menu(id):
        return single_view_menu_handler(id, request, database)

    @app.route("/order", methods = ["POST"])
    def order():
        return order_handler(request, database)
    
    @app.route("/withdraw", methods=["GET", "POST"])
    @login_required
    def withdraw_cash():
        return withdrawal_handler(request, database)
        
    @app.route("/switch_view/<view>")
    @login_required
    def switch_view(view):
        return switch_vendor_view(view, database)

    @app.route("/preview", methods = ["GET","POST"])
    def preview_order():
        return order_preview_handler(request, database)
    
    @app.route("/display_cart")
    def display_cart():
        return display_cart_handler(database)

    @app.route("/add_cart/<id>", methods=["POST", "GET"])
    def add_cart(id):
        return add_cart_handler(id, request, database)
    
    @app.route("/delete_cart/<id>", methods=["POST"])
    def delete_cart_handler(id):
        return delete_cart_handler(id, database)

    @app.route("/clear_cart")
    def clear_cart():
        return clear_cart_handler(database)

    @app.route("/process_cart", methods=["POST"])
    def process_cart():
        return process_cart_handler(request, database)

    @app.route("/history_cart")
    def history_cart():
        return history_cart_handler(database)