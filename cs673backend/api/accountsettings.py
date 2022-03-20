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
			print(args)
			if "user" in session:
				user = UserAccount.query.filter_by(username = session["user"]).first()
				
				for key, val in args.items():
					if val is not None:
						if key == "password":
							key = "passhash"
							val = hash(val, user.salt.encode("utf-8"))
						else:
							otheruser = UserAccount.query.filter_by(**{key : val}).first()
							if otheruser is not None:
								db.sesion.rollback()
								return { "changed": False, "reason": "duplicate " + key }
						
						if key == "username":
							session["user"] = val
						
						user.__setattr__(key, val)
						changed = True
			
			if changed:
				db.session.commit()
			
			print(changed)
			return { "changed": changed }
	
	api.add_resource(UserInfo, "/userinfo")