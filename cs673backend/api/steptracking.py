from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class Steps(db.Model):
		userid = db.Column(db.Integer, primary_key = True)
		year   = db.Column(db.Integer, primary_key = True)
		day    = db.Column(db.Integer, primary_key = True)
		steps  = db.Column(db.Integer, nullable = False)
	
	class StepTracking(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int, required = True)
			self.parser.add_argument("day",  type = int, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("steps", type = int, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				step = Steps.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				steps = 0
				
				if step is not None:
					steps = step.steps
				
				return { "steps": steps }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args()
			
			if "userid" in session:
				steps = Steps.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				if steps is None:
					steps = Steps(userid = session["userid"], year = args["year"], day = args["day"], glasses = 0)
					db.session.add(steps)
				
				steps.steps = args["steps"]
				db.session.commit()
				
				return { "updated": True }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(StepTracking, "/steps")