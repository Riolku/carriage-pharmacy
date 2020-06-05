from pharmacy import db

from .aliases import *
from .helper import Helper

class OrderTypes(Helper, dbmodel):
  __tablename__ = "order_types"
  
  id = dbcol(dbint, primary_key = True)
  name = dbcol(dbstr(64), nullable = False) # The name displayed to the user
  address = dbcol(dbbool, nullable = False) # If the order type should show the address (aka dropoff order type)
  prompt = dbcol(dbstr(256), nullable = False) # Additional info shown to the user
  