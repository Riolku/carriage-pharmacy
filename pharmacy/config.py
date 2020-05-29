import os

from .utils.files import load_json

def configure_app(application):
  keys = load_json(os.environ['PHARMACY_KEYS_FILE'])
  
  application.secret_key = keys['SECRET_KEY']
  
  app_config = dict(
    SQLALCHEMY_DATABASE_URI = keys['DATABASE_URI'],
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    
    COOKIES_SECURE = True,
    COOKIES_HTTPONLY = True,
    
    PREFERRED_URL_SCHEME = "https",
    
    TRAP_BAD_REQUEST_ERRORS = True,
    
    SERVER_NAME = "pharmacy.kgugeler.ca"
  )
  
  for k, v in app_config.items():
    application.config[k] = v
    
  return application