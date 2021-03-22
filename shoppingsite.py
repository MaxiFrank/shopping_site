"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons, customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# will remove line in production
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""
    if 'customer' not in session:
        session['customer'] = None
    print(session.items())
    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    order_total = 0
    cart_melons = []

    cart = session.get("cart", {})

    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)

        total_cost = quantity * melon.price
        order_total += total_cost

        melon.quantity = quantity
        melon.total_cost = total_cost

        cart_melons.append(melon)

    return render_template("cart.html", cart=cart_melons, order_total=order_total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    
    if 'cart' in session:
        cart = session['cart']
    else:
        session['cart'] = {}
        cart = session['cart']

    cart[melon_id] = cart.get(melon_id, 0) + 1
    flash("Melon successfully added to cart.")
    
    # the message actually gets flashed when it got redicreted to /cart because cart.html extends from base.html
    return redirect("/cart") 


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    # get user-provided name and password from request.form
    user_name = request.form['email']
    password = request.form['password']

    # - use customers.get_by_email() to retrieve corresponding Customer
    customer = customers.get_by_email(user_name)

    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    if customer != None:
        # - if they match, store the user's email in the session, flash a success
         #   message and redirect the user to the "/melons" route
        if customer.password == password:
            session['customer'] = user_name
            flash("Login successful!")
            session['logged_in_customer_email'] = True
            print(session.items())
            return redirect("/melons")
        # - if they don't, flash a failure message and redirect back to "/login"
        else:
            flash("Incorrect password")
            return redirect("/login")
    # - do the same if a Customer with that email doesn't exist
    else:
        flash("No customer with that email found.")
        return redirect("/login")

@app.route("/logout", methods=["GET", "POST"])
def process_logout():
    session.pop("logged_in_customer_email", None)
    print(session.items())
    flash("logged out")
    return redirect("/melons")



@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""
    
    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
