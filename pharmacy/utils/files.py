from flask import json

def load_json(filename):
  return json.load(open(filename))