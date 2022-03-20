from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from .authentication import hash

def start(flaskapp, db, api, UserAccount):
	class UserInfo(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("username", type = str)
			self.parser.add_argument("password", type = str)
			self.parser.add_argument("email", type = str)
			self.parser.add_argument("phone", type = str)
		
		def get(self):
			user = None
			info = {}
			
			if "user" in session:
				user = UserAccount.query.filter_by(username = session["user"]).first()
				info = { "username": user.username, "email": user.email, "phone": user.phone }
			
			return { "loggedIn": user is not None } | info
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			changed = False
			
			if "user" in session:
				user = UserAccount.query.filter_by(username = session["user"]).first()
				
				for key, val in args.items():
					if key == "password":
						key = "passhash"
						val = hash(val, user.salt.encode("utf-8"))
					
					user.__setattr__(key, val)
					changed = True
			
			if changed:
				db.session.commit()
			
			return { "changed": changed }
	
	api.add_resource(UserInfo, "/userinfo")