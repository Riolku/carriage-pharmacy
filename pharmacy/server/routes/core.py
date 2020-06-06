import json, re

from flask import redirect, render_template, request, flash

from pharmacy.auth import login_user, logout_user, user
from pharmacy.database import Users, Products, ProductTypes
from pharmacy.server.routes.utils import *

def render(*a, **k):
  return render_template(*a, **k, __navbar_elements = [("/order", "Order"), ("/about", "About")], user = user)

@app.route("/")
def serve_root():
  return render("index.html")

@app.route("/order", methods = ["GET", "POST"])
def serve_order():
  if not user:
    return redirect("/signin?next=/order", code = 303)
  if request.method == "GET":
    return render("order.html", products = Products.query.all(), product_types = ProductTypes.query.all())
  else:
    return json.dumps(request.form)

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
    
    u = Users.query.filter_by(email = email).first()
    
    if not u or not u.check_pass(password):
      flash("Invalid Credentials!", "error")
      return render_template("signin.html", _email = email)
    
    login_user(u)
    
    return redirect(request.args.get("next", "/"), code = 33)

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
    
    return redirect(request.args.get("next", "/"), code = 303)