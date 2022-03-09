from secrets import token_urlsafe
from os import environ

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .api import start_api

def get_environment_var(name):
	return environ[name] if name in environ else None

def startup():
	flaskapp = Flask(__name__)
	
	key = get_environment_var("SESSION_SECRET_KEY")
	if key is None:
		print("Warning: Generating RANDOM session key, this WILL NOT WORK in production!")
		key = token_urlsafe(16)
	flaskapp.secret_key = key
	
	flaskapp.config["SESSION_TYPE"] = "sqlalchemy"
	flaskapp.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"
	flaskapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	flaskapp.config["SQLALCHEMY_DATABASE_URI"] = get_environment_var("DATABASE_URL").replace("postgres", "postgresql+psycopg2")
	
	db = SQLAlchemy(flaskapp)
	api = Api(flaskapp)
	Session(flaskapp)
	
	start_api(flaskapp, db, api)
	db.create_all()
	
	return flaskapp