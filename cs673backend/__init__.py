from secrets import token_urlsafe
from flask import Flask

from .dbconn import connect
from .api import start_api

def startup():
	flaskapp = Flask(__name__)
	flaskapp.secret_key = token_urlsafe(16)
	
	return flaskapp