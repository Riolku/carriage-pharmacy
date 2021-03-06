from pharmacy import app

from pharmacy.auth.manage_user import user
from pharmacy.utils.time import get_time

from flask import request

# Globals in templates
@app.context_processor
def context_processor():
  return dict(
    user = user,
    get_time = get_time
  )

#@app.before_request
def debug():
  print(request.environ)
  
  print()
  
  print(request.headers)
  
#@app.route("/")
def test_index():
  return "HI"