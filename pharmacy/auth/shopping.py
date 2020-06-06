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
def add_to_cart(pid, note, quantity):
  session['cart']['pid'] = dict(
    id = pid,
    notes = note,
    qty = quantity
  )
  
@assert_cart
def remove_from_cart(pid, quantity = -1):
  if pid not in session['cart']: return None
  
  if quantity == -1 or quantity >= session['cart'][pid]['qty']:
    i = session['cart'][pid]
    
    del session['cart'][pid]
    
    return i
  
  session['cart'][pid]['qty'] -= quantity
  return session['cart'][pid]