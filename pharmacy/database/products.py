from pharmacy import db

from .aliases import *
from .helper import Helper
from .product_types import ProductTypes

class Products(Helper, dbmodel):
  __tablename__ = "products"
  
  id = dbcol(dbint, primary_key = True)
  ptid = dbcol(dbint, dbforkey(ProductTypes.id), nullable = False)
  name = dbcol(dbstr(64), nullable = False) # The name displayed to the user
  desc = dbcol(dbstr(1024), nullable = False) # Product description