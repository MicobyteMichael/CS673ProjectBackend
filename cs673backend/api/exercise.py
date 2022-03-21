from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class ExcerciseSessions(db.Model):
		userid    = db.Column(db.Integer, primary_key = True)
		year      = db.Column(db.Integer, primary_key = True)
		day       = db.Column(db.Integer, primary_key = True)
		name      = db.Column(db.String,  primary_key = True)
		type      = db.Column(db.String,  nullable = False)
		start     = db.Column(db.Integer, nullable = False)
		end       = db.Column(db.Integer)
		heartrate = db.Column(db.Integer)
		calories  = db.Column(db.Integer)
	
	class Exercise(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int, required = True)
			self.parser.add_argument("day",  type = int, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("name", type = str, required = True)
			
			self.parser3 = RequestParser()
			self.parser3.add_argument("start", type = int, required = True)
			self.parser3.add_argument("type",  type = str, required = True)
			
			self.parser4 = RequestParser()
			self.parser4.add_argument("end",       type = int, required = True)
			self.parser4.add_argument("heartrate", type = int, required = True)
			self.parser4.add_argument("calories",  type = int, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				sessions = (ExcerciseSessions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).all()) or []
				sessions_data = [ { "name": session.name, "type": session.type, "start": session.start, "end": session.end, "heartrate": session.heartrate, "calories": session.calories } for session in sessions ]
				
				return { "sessions": sessions_data }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args() | self.parser3.parse_args()
			
			if "userid" in session:
				existing_session = ExcerciseSessions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"], name = args["name"]).first()
				if existing_session is not None:
					return { "error": "An exercise session with that name is already added" }
				
				db.session.add(ExcerciseSessions(userid = session["userid"], year = args["year"], day = args["day"], name = args["name"], type = args["type"], start = args["start"], end = None, heartrate = None, calories = None))
				db.session.commit()
				
				return { "added": True }
			else:
				return { "error": "Not signed in" }
		
		def patch(self):
			args = self.parser.parse_args() | self.parser2.parse_args() | self.parser4.parse_args()
			
			if "userid" in session:
				existing_session = ExcerciseSessions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"], name = args["name"]).first()
				if existing_session is None:
					return { "error": "An exercise session with that name does not exist" }
				
				existing_session.end       = args["end"      ]
				existing_session.heartrate = args["heartrate"]
				existing_session.calories  = args["calories" ]
				db.session.commit()
				
				return { "updated": True }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(Exercise, "/exercise")