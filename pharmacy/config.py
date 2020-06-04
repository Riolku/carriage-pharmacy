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
    
    SERVER_NAME = "pharmacy.kgugeler.ca",
    
    MAIL_SERVER = keys["MAIL_SERVER"],
    MAIL_USE_TLS = True,
    MAIL_PORT = 587,
    MAIL_USERNAME = keys['MAIL_USERNAME'],
    MAIL_PASSWORD = keys['MAIL_PASSWORD'],
    DEFAULT_MAIL_SENDER = tuple(keys['MAIL_SENDER'])
  )
  
  application.config.update(app_config)
    
  return application