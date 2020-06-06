import json, re

from flask import redirect, render_template, request, flash, abort, jsonify

from datetime import datetime

from pharmacy.auth import login_user, logout_user, user, get_cart, get_from_cart, set_cart
from pharmacy.database import Users, Products, ProductTypes, Orders
from pharmacy.server.routes.utils import *
from pharmacy.utils.time import get_time

def render(*a, **k):
  return render_template(*a, **k, __navbar_elements = [("/about", "About"), ("/faq", "FAQ"), ("/browse", "Browse Products"), ("/checkout", "Checkout")], user = user)

@app.route("/")
def serve_root():
  print(request.path)
  return render("index.html")
  
@app.route("/about")
def serve_about():
  return render("about.html")
  
@app.route("/faq")
def serve_faq():
  return render("faq.html")
  
@app.route("/browse")
def serve_browse():
  return render("browse.html", products = Products.query.all(), product_types = ProductTypes.query.all())
  
@app.route("/product/<int:id>")
def serve_product(id):
  p = Products.query.filter_by(id = id).first()
  
  if not p: abort(404)
  
  if request.method == "GET":
    current = get_from_cart(id)
    return render("product.html", product = p, note = current[0], qty = current[1])
    
  else:
    if not user: return redirect("/signin?next=/product/%d" % id, code = 303)

    notes = request.form['notes']
    quantity = request.form['quantity']
    
    set_cart(id, notes, quantity)
    
    flash("Item added to cart!")
    
    return redirect("/browse", code = 303)
    
@app.route("/api/available-times/<y>/<m>/<d>")
def serve_available_times(y, m, d):
  start = 9
  end = 20
  
  t1 = datetime(y, m, d, start, 0).timestamp()
  t2 = datetime(y, m, d, end, 0).timestamp()
  
  ts = {e.time for e in Orders.query.filter(t1 <= Orders.time <= t2).all()}
  
  dayt = datetime(y, m, d, 0, 0).timestamp()
  
  av = []
  
  for i in range(start, end):
    for x in range(2):
      if (dayt + i * 3600 + x * 1800) not in ts:
        av.append("%.1f" % (i + 0.5 * x))

  return jsonify(av)

@app.route("/checkout", methods = ["GET", "POST"])
def serve_checkout():
  if not user:
    return redirect("/signin?next=/checkout", code = 303)
    
  if request.method == "GET":
    return render("checkout.html", cart = get_cart(), product_types = ProductTypes.query.all(), order_types = OrderTypes.query.all())
    
  else:
    notes = request.form['notes']
    cart = get_cart()
    otid = request.form['order_type']
    date = request.form['date']
    payment = request.form['payment']
    
    year, month, day = map(int, date.split("/"))
    form_time = request.form['time']
    dt = datetime(year, month, day, int(form_time), time.endswith("5") * 30)
    ts = int(dt.timestamp())
    
    if not Orders.create(int(otid), ts, cart, notes, payment):
      flash("This time has been taken! Please try again!", "error")
    
    flash("Your order has been created. Thank you!", "success")
    
    return redirect("/", code = 303)
    
@app.route("/view-order/<int:id>")
def serve_view_order(id):
  if not user:
    return redirect("/signin?next=/view-order/%d" % id, code = 303)
    
  if not user.admin:
    abort(403)
    
  o = Orders.query.filter_by(id = id).first()
  
  if not o: abort(404)
    
  return render("view_order.html", order = o)
  

@app.route("/view-orders")
def serve_view_orders():
  if not user:
    return redirect("/signin?next=/view-order/%d" % id, code = 303)
    
  if not user.admin:
    abort(403)
    
  os = Orders.query.filter_by(get_time() - 2 * 60 <= Orders.time <= get_time() + 48 * 60 * 60).all()
  
  return render("view_orders.html", orders = os)
    
@app.route("/edit-profile", methods = ['GET', 'POST'])
def serve_edit_profile():
  if not user:
    return redirect("/signin?next=/edit-profile")
    
  if request.method == "POST":
    name = request.form['name'].strip() or None
    address = request.form['address'].strip() or None
    password = request.form['password'] or None
    rpassword = request.form['rpassword'] or None
    postal = request.form['postal_code'].strip() or None
    
    fail = False
    
    if password != rpassword:
      flash("Passwords do not match!")
      
      fail = True
      
    if not re.match(r"(^[A-Za-z][0-9][A-Za-z]\s*[0-9][A-Za-z][0-9]$)", postal):
      flash("Please enter a valid postal code!", "error")
      fail = True
    
    if not fail:
      user.update(name = name, password = password, address = address, postal_code = postal)
  
      flash("Your changes were saved!", "success")
      
    else:
      flash("Your changes were not saved!")
      
    
    return render(_name = name, _address = address, _postal = postal)
    
  return render("edit_profile.html")
    
    
@app.route("/logout")
def serve_logout():
  logout_user()
  return redirect(request.args.get("next", "/"), code = 303)

@app.route("/signin", methods = ["GET", "POST"])
def serve_signin():
  if request.method == "GET":
    return render("signin.html")
  else:
    email = request.form["email"].strip()
    password = request.form["password"]
    
    u = Users.login(email, password)
    
    if not u:
      flash("Invalid Credentials!", "error")
      return render_template("signin.html", _email = email)
    
    login_user(u)
    
    flash("Welcome back!", "success")
    
    return redirect(request.args.get("next", "/"), code = 303)

@app.route("/signup", methods = ["GET", "POST"])
def serve_signup():
  if request.method == "GET":
    return render("signup.html")
  else:
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    password = request.form["password"]
    rpassword = request.form["rpassword"]
    address = request.form["address"].strip()
    postal = request.form["postal"].strip()
    
    fail = False
    
    if not name:
      flash("Please enter your name!", "error")
      fail = True
    
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
      flash("Please enter a valid email address!", "error")
      fail = True
    elif Users.query.filter_by(email = email).count() > 0:
      flash("That email address is already in use!", "error")
      fail = True
      
    if password != rpassword:
      flash("Passwords don't match!", "error")
      fail = True

    if not re.match(r"(^[A-Za-z][0-9][A-Za-z]\s*[0-9][A-Za-z][0-9]$)", postal):
      flash("Please enter a valid postal code!", "error")
      fail = True
    
    postal = postal[:3] + postal[-3:]
      
    if fail:
      return render("signup.html", _name = name, _email = email, _address = address, _postal = postal)
    
    Users.create(name, email, password, address.upper(), postal.upper())
    
    login_user(Users.query.filter_by(email = email).first())
    
    flash("Welcome!", "success")
    
    return redirect(request.args.get("next", "/"), code = 303)
    
    
@app.errorhandler(404)
def serve_404(e):
  return "404"

@app.errorhandler(403)
def serve_403(e):
  return "403"

@app.route("/favicon.ico")
def serve_favicon():
  return redirect("/static/ico/favicon.ico", code = 303)