from pharmacy import app

from pharmacy.database import *
from pharmacy.server.routes import *

from sys import argv

if __name__ == "__main__":
  port = 4010
  
  for i in range(len(argv)):
    if argv[i].startswith("--port="):
      port = int(argv[i][len("--port="):])
  
  app.run(host = "0.0.0.0", port = port, debug = "debug" in argv)