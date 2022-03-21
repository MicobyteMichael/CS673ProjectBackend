from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

def start(flaskapp, db, api):
	class BodyCompositions(db.Model):
		userid  = db.Column(db.Integer, primary_key = True)
		year    = db.Column(db.Integer, primary_key = True)
		day     = db.Column(db.Integer, primary_key = True)
		weight  = db.Column(db.Integer, nullable = False)
		bodyfat = db.Column(db.Integer, nullable = False)
		muscle  = db.Column(db.Integer, nullable = False)
	
	class BodyCompTracking(Resource):
		def __init__(self):
			self.parser = RequestParser()
			self.parser.add_argument("year", type = int, required = True)
			self.parser.add_argument("day",  type = int, required = True)
			
			self.parser2 = RequestParser()
			self.parser2.add_argument("weight",  type = int, required = True)
			self.parser2.add_argument("bodyfat", type = int, required = True)
			self.parser2.add_argument("muscle",  type = int, required = True)
		
		def post(self):
			args = self.parser.parse_args(strict = True)
			
			if "userid" in session:
				comp = BodyCompositions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				
				if comp is None:
					return { "error": "Not recorded yet" }
				else:
					return { "weight": comp.weight, "fatpercentage": comp.bodyfat, "muscle": comp.muscle }
			else:
				return { "error": "Not signed in" }
		
		def put(self):
			args = self.parser.parse_args() | self.parser2.parse_args()
			
			if "userid" in session:
				comp = BodyCompositions.query.filter_by(userid = session["userid"], year = args["year"], day = args["day"]).first()
				if comp is None:
					comp = BodyCompositions(userid = session["userid"], year = args["year"], day = args["day"])
					db.session.add(comp)
				
				comp.weight = args["weight"]
				comp.bodyfat = args["bodyfat"]
				comp.muscle = args["muscle"]
				
				db.session.commit()
				
				return { "submitted": True }
			else:
				return { "error": "Not signed in" }
	
	api.add_resource(BodyCompTracking, "/bodycomp")