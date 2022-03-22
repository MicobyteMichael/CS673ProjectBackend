from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class Goals(db.Model):
		userid = db.Column(db.Integer, primary_key = True )
		name   = db.Column(db.String,  primary_key = True )
		type   = db.Column(db.String,  nullable    = False)
		comp   = db.Column(db.String,  nullable    = False)
		thresh = db.Column(db.Float,   nullable    = False)
		param  = db.Column(db.String                      )
		active = db.Column(db.Boolean, nullable    = False)
	
	class GoalAchievements(db.Model):
		userid   = db.Column(db.Integer, primary_key = True )
		year     = db.Column(db.Integer, primary_key = True )
		day      = db.Column(db.Integer, primary_key = True )
		name     = db.Column(db.String,  primary_key = True )
		achieved = db.Column(db.Boolean, nullable    = False)
	
	class GoalTracking(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("name", type = str, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("type",   type = str,   required = True)
			self.parser2.add_argument("comp",   type = str,   required = True)
			self.parser2.add_argument("thresh", type = float, required = True)
			self.parser2.add_argument("param",  type = str)
			self.parser2.add_argument("active", type = bool)
			
			self.parser3 = RequestParser()
			self.parser3.add_argument("active", type = bool, required = True)
		
		def get(self):
			if "userid" in session:
				goals = (Goals.query.filter_by(userid = session["userid"].all()) or []
				goals_data = [ { "name": goal.name, "type": goal.type, "comp": goal.comp, "thresh": goal.thresh, "param": goal.param, "active": goal.active } for goal in goals ]
				return { "goals": goals_data }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args()
			
			if "userid" in session:
				existing_goal = Goals.query.filter_by(userid = session["userid"], name = args["name"]).first()
				if existing_goal is not None:
					return { "error": "A goal with that name is already added" }
				
				db.session.add(Goals(userid = session["userid"], name = args["name"], type = args["type"], comp = args["comp"], thresh = args["thresh"], param = args["param"], active = args["active"]))
				db.session.commit()
				
				return { "added": True }
			else:
				return { "error": "Not signed in" }
		
		def patch(self):
			args = self.parser.parse_args() | self.parser3.parse_args()
			
			if "userid" in session:
				goal = Goals.query.filter_by(userid = session["userid"], name = args["name"]).first()
				if goal is None:
					return { "error": "No goal exists by that name" }
				
				goal.active = args["active"]
				db.session.commit()
				
				return { "updated": True }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(GoalTracking, "/goals")