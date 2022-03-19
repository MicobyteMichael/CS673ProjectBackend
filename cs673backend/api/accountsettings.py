from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api, UserAccount):
	class UserInfo(Resource):
		def get(self):
			user = None
			info = {}
			
			if "user" in session:
				user = UserAccount.query.filter_by(username = session["user"]).first()
				info = { "username": user.username, "email": user.email, "phone": user.phone }
			
			return { "loggedIn": user is not None } | info
	
	api.add_resource(UserInfo, "/userinfo")