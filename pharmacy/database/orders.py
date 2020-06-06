from pharmacy import db

from .aliases import *
from .helper import Helper
from .users import Users
from .order_types import OrderTypes
from .products import Products
from .utils import db_commit

class Orders(Helper, dbmodel):
  __tablename__ = "orders"
  
  id = dbcol(dbint, primary_key = True)
  uid = dbcol(dbint, dbforkey(Users.id), nullable = False)
  otid = dbcol(dbint, dbforkey(OrderTypes.id), nullable = False)
  notes = dbcol(dbstr(1024), nullable = False)
  time = dbcol(dbint, nullable = False, unique = True)
  payment = dbcol(dbstr, nullable = False)
  
  @property
  def products(self):
    return Products.query.join(OrderProducts).filter(OrderProducts.oid == self.id).all()
    
  @property
  def user(self):
    return Users.query.filter_by(id = self.uid).first()
    
  @property
  def order_type(self):
    return OrderTypes.query.filter_by(id = self.otid).first()

  def create(otid, time, products, notes, payment, uid = None): # Get uid from user.id
    from pharmacy.auth.manage_user import user
    if uid is None: uid = user.uid
      
    if time % 1800 != 0: return False
    if Orders.query.filter_by(time = time).count() > 0: return False
    
    order = Orders.add(uid = uid, otid = otid, notes = notes, time = time, payment = payment)
    
    for p in product_ids:
      OrderProducts.add(oid = order.id, pid = p['id'], notes = p['notes'], _commit = False)
      
    db_commit()
    
    return True
  
class OrderProducts(Helper, dbmodel):
  __tablename__ = "order_products"
  
  id = dbcol(dbint, primary_key = True)
  oid = dbcol(dbint, dbforkey(Orders.id), nullable = False)
  pid = dbcol(dbint, dbforkey(Products.id), nullable = False)
  notes = dbcol(dbstr(1024), nullable = False) # Notes for this product, submitted by the user