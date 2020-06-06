from flask import session

def assert_cart(func):
  def inner(*args, **kwargs):
    session.setdefault('cart', {})

    return func(*args, **kwargs)
    
  return inner
  
@assert_cart
def get_cart():
  return session['cart']

@assert_cart
def get_from_cart(pid):
  return session['cart'].get(pid, ("", 0))

@assert_cart
def set_cart(pid, note, quantity):
  session['cart'][pid] = (note, quantity)
  if quantity == 0:
    del session['cart'][pid]