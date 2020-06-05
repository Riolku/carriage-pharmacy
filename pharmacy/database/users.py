from pharmacy import db

import argon2

from .aliases import *
from .helper import Helper

from os import urandom

class Users(dbmodel, Helper):
  id = dbcol(dbint, primary_key = True)
  
  name = dbcol(dbstr(256), unique = False, nullable = False)
  email = dbcol(dbstr(256), unique = True, nullable = False)
  
  salt = dbcol(dbbinary, nullable = False)
  pass_hash = dbcol(dbbinary, nullable = False)
  
  # Create a new user with the specified name, email and password
  def create(name, email, password):
    s = urandom(16)
    
    ph = argon2.argon2_hash(password, s)
    
    Users.add(name = name, email = email, salt = s, pass_hash = ph)
    
  # Hash the password with the user's salt
  def hash(self, pword):
    return argon2.argon2_hash(pword, self.salt)
    
  # Check that the password provided is the same as the stored one
  def check_pass(self, newpass):
    return hash(pword) == pass_hash
  
  # Try to login a user and return them, otherwise Falsy
  def login(email, password):
    u = Users.query.filter_by(email = email).first()
    
    if u is None: return None
    
    if u.pass_hash != u.check_pass(password):
      return False
    
    return u
  
  # Update a user object
  def update(self, email = None, name = None, password = None):
    if email is not None:
      self.email = email
      
    if name is not None:
      self.name = name
      
    if password is not None:
      self.pass_hash = self.hash(password)
  
  __tablename__ = "users"