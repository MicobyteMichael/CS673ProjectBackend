from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class UserAccount(db.Model):
		id		= db.Column(db.Integer, primary_key = True)
		username= db.Column(db.String(80), unique = True, nullable = False)
		password= db.Column(db.String(80), nullable = False)
		email	= db.Column(db.String(80), unique = True, nullable = False)
		phone	= db.Column(db.String(20), unique = True, nullable = False)
	
	class Login(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("username", type = str, required = True)
			self.parser.add_argument("password", type = str, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			user = UserAccount.query.filter_by(**args).first()
			
			if user is not None:
				session["user"] = user.username
			
			return { "authenticated": user is not None }
	
	class Register(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("username", type = str, required = True)
			self.parser.add_argument("password", type = str, required = True)
			self.parser.add_argument("email", type = str, required = True)
			self.parser.add_argument("phone", type = str, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			user = UserAccount(**args)
			
			db.session.add(user)
			db.session.commit()
			session["user"] = user.username
			
			return { "created": True }
	
	api.add_resource(Login, "/login")
	api.add_resource(Register, "/register")