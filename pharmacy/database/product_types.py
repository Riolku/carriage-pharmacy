from pharmacy import db

from .aliases import *
from .helper import Helper

class ProductTypes(Helper, dbmodel):
  __tablename__ = "product_types"
  
  id = dbcol(dbint, primary_key = True)
  name = dbcol(dbstr(64), nullable = False) # The name of the product type (service, prescription, non-prescreption)
  prompt = dbcol(dbstr(256), nullable = False) # Additional info shown to the user
  