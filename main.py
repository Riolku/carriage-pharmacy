from pharmacy import app

from pharmacy.database import *
from pharmacy.server.routes import *

from sys import argv

if __name__ == "__main__":  
  port = 4010
  
  if app.config['ALT_PORT']:
    port = 4020
  
  app.run(host = "0.0.0.0", port = port, debug = "debug" in argv)