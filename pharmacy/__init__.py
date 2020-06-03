from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from .config import configure_app

app = Flask("pharmacy")

app = configure_app(app)

db = SQLAlchemy(app)
