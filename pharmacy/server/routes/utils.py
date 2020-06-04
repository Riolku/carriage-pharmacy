from pharmacy import app

from pharmacy.auth.manage_user import user
from pharmacy.utils.time import get_time

# Globals in templates
@app.context_processor
def context_processor():
  return dict(
    user = user,
    get_time = get_time
  )