from flask import session

def assert_cart(func):
  def inner(*args, **kwargs):
    session.setdefault('cart', [])

    return func(*args, **kwargs)
    
  return inner
  
@assert_cart
def get_cart():
  return session['cart']

@assert_cart
def add_to_cart(pid, note, quantity):
  session['cart'].append(dict(
    id = pid,
    notes = note,
    qty = quantity
  ))
  
@assert_cart
def remove_from_cart(index, quantity = -1):
  if index >= len(session['cart']): return None
  
  if quantity == -1 or quantity >= session['cart'][index]['qty']:
    return session['cart'].pop(index)
  
  session['cart'][index]['qty'] -= quantity
  return session['cart'][index]