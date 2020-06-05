from flask import session

def assert_cart(func):
  def inner(*args, **kwargs):
    session.setdefault('cart', [])

    return func(*args, **kwargs)
    
  return inner

@assert_cart
def add_to_cart(pid, note):
  session['cart'].append(dict(
    id = pid,
    notes = note
  ))
  
@assert_cart
def remove_from_cart(index):
  if index >= len(session['cart']): return None
  
  return session['cart'].pop(index)