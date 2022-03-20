from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from bcrypt import gensalt, hashpw
from hashlib import sha256
from hmac import new as hash_mac
from os import environ

PEPPER = environ["PEPPER"].encode("utf-8")

def hash(password, salt):
	return hashpw(hash_mac(PEPPER, password.encode("utf-8"), sha256).hexdigest().encode("utf-8"), salt).decode("utf-8")

def start(flaskapp, db, api, UserAccount):
	class Login(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("username", type = str, required = True)
			self.parser.add_argument("password", type = str, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			user = UserAccount.query.filter_by(username = args["username"]).first()
			success = False
			
			if user is not None:
				pass_hash = hash(args["password"], user.salt.encode("utf-8"))
				if pass_hash == user.passhash:
					session["user"] = user.username
					session["userid"] = user.id
					success = True
			
			return { "authenticated": success }
	
	class Register(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("username", type = str, required = True)
			self.parser.add_argument("password", type = str, required = True)
			self.parser.add_argument("email", type = str, required = True)
			self.parser.add_argument("phone", type = str, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			new_args = { k:v for k, v in args.items() if k != "password" }
			
			for k, v in new_args.items():
				user = UserAccount.query.filter_by(**{k : v}).first()
				if user is not None:
					return { "created": False, "reason": "duplicate " + k }
			
			salt = gensalt()
			new_args["salt"] = salt.decode("utf-8")
			new_args["passhash"] = hash(args["password"], salt)
			user = UserAccount(**new_args)
			
			db.session.add(user)
			db.session.commit()
			
			session["user"] = user.username
			session["userid"] = user.id
			
			return { "created": True }
	
	class ResetPassword(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("username", type = str, required = True)
			self.parser.add_argument("newPass", type = str, required = True)
			self.parser.add_argument("email", type = str, required = True)
			self.parser.add_argument("phone", type = str, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			new_args = { k:v for k, v in args.items() if k != "newPass" }
			user = UserAccount.query.filter_by(**new_args).first()
			
			if user is not None:
				user.passhash = hash(args["newPass"], user.salt.encode("utf-8"))
				db.session.commit()
				
				session["user"] = user.username
				session["userid"] = user.id
			
			return { "reset": user is not None }
	
	api.add_resource(Login,         "/login")
	api.add_resource(Register,      "/register")
	api.add_resource(ResetPassword, "/resetpass")