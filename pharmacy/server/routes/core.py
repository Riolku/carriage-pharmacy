from flask import render_template, request

from pharmacy.server.routes.utils import *

def render(*a, **k):
  return render_template(*a, **k, __navbar_elements = [("/about", "About")])

@app.route("/")
def serve_root():
  return render("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def serve_signup():
  if request.method == "GET":
    return render("signup.html")