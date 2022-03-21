from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class SleepSessions(db.Model):
		userid  = db.Column(db.Integer, primary_key = True)
		year    = db.Column(db.Integer, primary_key = True)
		day     = db.Column(db.Integer, primary_key = True)
		name    = db.Column(db.String,  primary_key = True)
		start   = db.Column(db.Integer, nullable = False)
		end     = db.Column(db.Integer)
	
	class Sleep(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int, required = True)
			self.parser.add_argument("day",  type = int, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("name", type = str, required = True)
			
			self.parser3 = RequestParser()
			self.parser3.add_argument("start", type = int, required = True)
			
			self.parser4 = RequestParser()
			self.parser4.add_argument("end", type = int, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				sleeps = (SleepSessions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).all()) or []
				sleeps_data = [ { "name": sleep.name, "start": sleep.start, "end": sleep.end } for sleep in sleeps ]
				
				return { "sleeps": sleeps_data }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args() | self.parser3.parse_args()
			
			if "userid" in session:
				existing_sleep = SleepSessions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"], name = args["name"]).first()
				if existing_sleep is not None:
					return { "error": "A sleep session with that name is already added" }
				
				db.session.add(SleepSessions(userid = session["userid"], year = args["year"], day = args["day"], name = args["name"], start = args["start"], end = None))
				db.session.commit()
				
				return { "added": True }
			else:
				return { "error": "Not signed in" }
		
		def patch(self):
			args = self.parser.parse_args() | self.parser2.parse_args() | self.parser4.parse_args()
			
			if "userid" in session:
				existing_sleep = SleepSessions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"], name = args["name"]).first()
				if existing_sleep is None:
					return { "error": "A sleep session with that name does not exist" }
				
				existing_sleep.end = args["end"]
				db.session.commit()
				
				return { "updated": True }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(Sleep, "/sleeptracking")